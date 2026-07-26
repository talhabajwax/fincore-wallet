from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ledger.models import LedgerAccount, LedgerEntry
from transactions.models import Transaction, Withdrawal
from wallets.models import Wallet


class WithdrawalFlowTests(APITestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="withdrawal_user",
            email="withdrawal_user@example.com",
            phone_number="03000000001",
            password="TestPass123!",
        )
        self.staff = User.objects.create_user(
            username="withdrawal_admin",
            email="withdrawal_admin@example.com",
            phone_number="03000000002",
            password="TestPass123!",
            is_staff=True,
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            email="other_user@example.com",
            phone_number="03000000003",
            password="TestPass123!",
        )

        self.wallet = Wallet.objects.create(
            user=self.user,
            currency="PKR",
            balance=Decimal("1000.00"),
            status="active",
        )
        self.wallet_account = LedgerAccount.objects.create(
            wallet=self.wallet,
            account_type="wallet",
            currency="PKR",
        )

    def create_withdrawal(self, amount=Decimal("200.00")):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("withdrawal-request", args=[self.wallet.id]),
            {
                "amount": str(amount),
                "description": "Automated withdrawal test",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        transaction = Transaction.objects.get(id=response.data["transaction_id"])
        withdrawal = transaction.withdrawal_details

        return response, transaction, withdrawal

    def assert_transaction_is_balanced(self, transaction):
        debit_total = LedgerEntry.objects.filter(
            transaction=transaction,
            entry_type="debit",
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        credit_total = LedgerEntry.objects.filter(
            transaction=transaction,
            entry_type="credit",
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        self.assertEqual(debit_total, credit_total)

    def test_withdrawal_request_reserves_funds(self):
        amount = Decimal("200.00")
        response, transaction, withdrawal = self.create_withdrawal(amount)

        self.wallet.refresh_from_db()

        self.assertEqual(response.data["withdrawal_id"], withdrawal.id)
        self.assertEqual(response.data["transaction_id"], transaction.id)
        self.assertEqual(response.data["withdrawal_status"], "pending_review")
        self.assertEqual(response.data["transaction_status"], "pending")

        self.assertEqual(self.wallet.balance, Decimal("800.00"))
        self.assertEqual(transaction.status, "pending")
        self.assertEqual(withdrawal.status, "pending_review")
        self.assertIsNone(withdrawal.reviewer)
        self.assertIsNone(withdrawal.reviewed_at)

        entries = LedgerEntry.objects.filter(transaction=transaction)
        self.assertEqual(entries.count(), 2)

        self.assertTrue(
            entries.filter(
                ledger_account=self.wallet_account,
                entry_type="debit",
                amount=amount,
            ).exists()
        )
        self.assertTrue(
            entries.filter(
                ledger_account__account_type="withdrawal_pending",
                ledger_account__currency="PKR",
                entry_type="credit",
                amount=amount,
            ).exists()
        )

        self.assert_transaction_is_balanced(transaction)

    def test_staff_can_approve_withdrawal(self):
        amount = Decimal("200.00")
        _, transaction, withdrawal = self.create_withdrawal(amount)

        self.client.force_authenticate(user=self.staff)
        response = self.client.post(
            reverse("withdrawal-approve", args=[withdrawal.id]),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        withdrawal.refresh_from_db()
        transaction.refresh_from_db()
        self.wallet.refresh_from_db()

        self.assertEqual(withdrawal.status, "approved")
        self.assertEqual(withdrawal.reviewer, self.staff)
        self.assertIsNotNone(withdrawal.reviewed_at)
        self.assertEqual(transaction.status, "completed")
        self.assertEqual(self.wallet.balance, Decimal("800.00"))

        entries = LedgerEntry.objects.filter(transaction=transaction)
        self.assertEqual(entries.count(), 4)

        self.assertTrue(
            entries.filter(
                ledger_account__account_type="withdrawal_pending",
                ledger_account__currency="PKR",
                entry_type="debit",
                amount=amount,
            ).exists()
        )
        self.assertTrue(
            entries.filter(
                ledger_account__account_type="external_funding",
                ledger_account__currency="PKR",
                entry_type="credit",
                amount=amount,
            ).exists()
        )

        self.assert_transaction_is_balanced(transaction)

        duplicate_approval = self.client.post(
            reverse("withdrawal-approve", args=[withdrawal.id]),
            {},
            format="json",
        )
        reject_after_approval = self.client.post(
            reverse("withdrawal-reject", args=[withdrawal.id]),
            {},
            format="json",
        )

        self.assertEqual(duplicate_approval.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reject_after_approval.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            LedgerEntry.objects.filter(transaction=transaction).count(),
            4,
        )

    def test_staff_can_reject_and_release_reserved_funds(self):
        amount = Decimal("200.00")
        _, transaction, withdrawal = self.create_withdrawal(amount)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("800.00"))

        self.client.force_authenticate(user=self.staff)
        response = self.client.post(
            reverse("withdrawal-reject", args=[withdrawal.id]),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        withdrawal.refresh_from_db()
        transaction.refresh_from_db()
        self.wallet.refresh_from_db()

        self.assertEqual(withdrawal.status, "rejected")
        self.assertEqual(withdrawal.reviewer, self.staff)
        self.assertIsNotNone(withdrawal.reviewed_at)
        self.assertEqual(transaction.status, "failed")
        self.assertEqual(self.wallet.balance, Decimal("1000.00"))

        entries = LedgerEntry.objects.filter(transaction=transaction)
        self.assertEqual(entries.count(), 4)

        self.assertTrue(
            entries.filter(
                ledger_account__account_type="withdrawal_pending",
                ledger_account__currency="PKR",
                entry_type="debit",
                amount=amount,
            ).exists()
        )
        self.assertTrue(
            entries.filter(
                ledger_account=self.wallet_account,
                entry_type="credit",
                amount=amount,
            ).exists()
        )

        self.assert_transaction_is_balanced(transaction)

        duplicate_rejection = self.client.post(
            reverse("withdrawal-reject", args=[withdrawal.id]),
            {},
            format="json",
        )
        approve_after_rejection = self.client.post(
            reverse("withdrawal-approve", args=[withdrawal.id]),
            {},
            format="json",
        )

        self.assertEqual(duplicate_rejection.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            approve_after_rejection.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            LedgerEntry.objects.filter(transaction=transaction).count(),
            4,
        )

    def test_non_staff_user_cannot_review_withdrawal(self):
        _, transaction, withdrawal = self.create_withdrawal(Decimal("50.00"))

        self.client.force_authenticate(user=self.user)

        approve_response = self.client.post(
            reverse("withdrawal-approve", args=[withdrawal.id]),
            {},
            format="json",
        )
        reject_response = self.client.post(
            reverse("withdrawal-reject", args=[withdrawal.id]),
            {},
            format="json",
        )

        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reject_response.status_code, status.HTTP_403_FORBIDDEN)

        withdrawal.refresh_from_db()
        transaction.refresh_from_db()
        self.wallet.refresh_from_db()

        self.assertEqual(withdrawal.status, "pending_review")
        self.assertEqual(transaction.status, "pending")
        self.assertEqual(self.wallet.balance, Decimal("950.00"))
        self.assertEqual(
            LedgerEntry.objects.filter(transaction=transaction).count(),
            2,
        )

    def test_insufficient_balance_is_rejected_without_money_movement(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("withdrawal-request", args=[self.wallet.id]),
            {
                "amount": "1200.00",
                "description": "Too much",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Insufficient balance.")

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("1000.00"))
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(Withdrawal.objects.count(), 0)
        self.assertEqual(LedgerEntry.objects.count(), 0)

    def test_frozen_wallet_cannot_request_withdrawal(self):
        self.wallet.status = "frozen"
        self.wallet.save(update_fields=["status"])

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("withdrawal-request", args=[self.wallet.id]),
            {"amount": "100.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Wallet is not active.")
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(Withdrawal.objects.count(), 0)
        self.assertEqual(LedgerEntry.objects.count(), 0)

    def test_user_cannot_withdraw_from_another_users_wallet(self):
        other_wallet = Wallet.objects.create(
            user=self.other_user,
            currency="PKR",
            balance=Decimal("500.00"),
            status="active",
        )
        LedgerAccount.objects.create(
            wallet=other_wallet,
            account_type="wallet",
            currency="PKR",
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("withdrawal-request", args=[other_wallet.id]),
            {"amount": "100.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Wallet not found.")

        other_wallet.refresh_from_db()
        self.assertEqual(other_wallet.balance, Decimal("500.00"))
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(Withdrawal.objects.count(), 0)
        self.assertEqual(LedgerEntry.objects.count(), 0)

    def test_missing_wallet_ledger_rolls_back_entire_request(self):
        wallet_without_ledger = Wallet.objects.create(
            user=self.user,
            currency="USD",
            balance=Decimal("500.00"),
            status="active",
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("withdrawal-request", args=[wallet_without_ledger.id]),
            {"amount": "100.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Wallet ledger account not found.")

        wallet_without_ledger.refresh_from_db()
        self.assertEqual(wallet_without_ledger.balance, Decimal("500.00"))
        self.assertFalse(
            Transaction.objects.filter(wallet=wallet_without_ledger).exists()
        )
        self.assertEqual(Withdrawal.objects.count(), 0)
        self.assertEqual(LedgerEntry.objects.count(), 0)
