from django.test import TestCase
from django.contrib.auth import get_user_model
from wallets.models import Wallet
from ledger.models import LedgerAccount
from transactions.models import Transaction
from transactions.services import TransactionService
from ledger.models import  LedgerEntry


class TestDepositFlow(TestCase):
      def setUp(self):
          User = get_user_model()
          self.user = User.objects.create_user(username="talha",email="talhabajwa.x1@gmail.com", password="123456",)     
          self.wallet = Wallet.objects.create(user=self.user,currency="PKR",)
          self.wallet_ledger = LedgerAccount.objects.create(wallet=self.wallet,account_type="wallet")
          self.transaction = Transaction.objects.create(created_by =self.user,wallet =self.wallet,amount = 100,transaction_type ="deposit",status = "pending",reference ="dsfdsfd")
                
                
      def test_successful_deposit(self):
          transaction_test = TransactionService()
          completed_transaction = transaction_test.proceed_transaction(self.transaction.id,self.user)
          self.assertEqual(completed_transaction.status, "completed")
          self.wallet.refresh_from_db()
          self.assertEqual(self.wallet.balance, 100)
          entries = LedgerEntry.objects.filter(transaction=self.transaction)
          self.assertEqual(entries.count(), 2)
          external_entry = entries.filter(
    ledger_account__account_type="external_funding",
    entry_type="debit",
    amount=100,
).first()

          self.assertIsNotNone(external_entry)