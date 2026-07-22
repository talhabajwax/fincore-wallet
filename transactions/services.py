import hashlib
import uuid

from django.db import transaction

from ledger.repositories import LedgerEntryRepository, LedgerRepository
from wallets.repositeries import WalletRepository

from .repositories import IdempotencyRepository, TransactionRepository


class TransactionService:
    def deposit(self, user, wallet_id, amount, description):
        wallet_repo = WalletRepository()
        valid_wallet = wallet_repo.a_wallet(user, wallet_id)

        if valid_wallet is None:
            raise ValueError("Wallet not found.")

        if valid_wallet.status != "active":
            raise ValueError("Wallet is not active.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        transaction_type = "deposit"
        reference = f"TXN-{uuid.uuid4()}"

        transaction_repo = TransactionRepository()

        transaction = transaction_repo.deposit(
            user,
            valid_wallet,
            transaction_type,
            reference,
            amount,
            description,
        )

        return transaction

    @transaction.atomic
    def transfer(
        self,
        user,
        sender_wallet_id,
        receiver_username,
        amount,
        description,
        idempotency_key,
    ):
        wallet_repo = WalletRepository()
        transaction_repo = TransactionRepository()
        ledger_repo = LedgerRepository()
        ledger_entry_repo = LedgerEntryRepository()
        idempotency_repo = IdempotencyRepository()
        idempotency_service = IdempotencyService()

        if not idempotency_key:
            raise ValueError("Idempotency key is required.")

        request_fingerprint = idempotency_service.generate_transfer_fingerprint(
            sender_wallet_id,
            receiver_username,
            amount,
            description,
        )

        idempotency_record = idempotency_repo.find_record(
            user,
            "transfer",
            idempotency_key,
        )

        if idempotency_record is not None:
            if idempotency_record.request_fingerprint != request_fingerprint:
                raise ValueError(
                    "Idempotency key was already used " "with different request data."
                )

            if idempotency_record.status == "completed":
                return idempotency_record.transaction

            if idempotency_record.status == "processing":
                raise ValueError("Request is already being processed.")

            if idempotency_record.status == "failed":
                raise ValueError(
                    "Idempotency key was already used " "for a failed request."
                )

        else:
            idempotency_record = idempotency_repo.create_record(
                user,
                "transfer",
                idempotency_key,
                request_fingerprint,
            )

        sender_wallet = wallet_repo.a_wallet(
            user,
            sender_wallet_id,
        )

        if sender_wallet is None:
            raise ValueError("Sender wallet not found.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        receiver_wallet = wallet_repo.receiver_wallet(
            receiver_username,
            sender_wallet.currency,
        )

        if receiver_wallet is None:
            raise ValueError("Receiver wallet not found.")

        if sender_wallet.id == receiver_wallet.id:
            raise ValueError("Cannot transfer to the same wallet.")

        sender_wallet, receiver_wallet = wallet_repo.lock_transfer_wallets(
            sender_wallet.id,
            receiver_wallet.id,
        )

        if sender_wallet is None or receiver_wallet is None:
            raise ValueError("Unable to lock transfer wallets.")

        if sender_wallet.status != "active":
            raise ValueError("Sender wallet is not active.")

        if receiver_wallet.status != "active":
            raise ValueError("Receiver wallet is not active.")

        if sender_wallet.currency != receiver_wallet.currency:
            raise ValueError("Wallet currencies do not match.")

        if sender_wallet.balance < amount:
            raise ValueError("Insufficient balance.")

        reference = f"TXN-{uuid.uuid4()}"

        transaction_record = transaction_repo.transfer_transaction(
            user,
            sender_wallet,
            amount,
            reference,
            description,
        )

        transaction_repo.create_transfer(
            transaction_record,
            receiver_wallet,
        )

        sender_ledger = ledger_repo.find_ledger_account(
            sender_wallet,
        )

        if sender_ledger is None:
            raise ValueError("Sender wallet ledger account not found.")

        receiver_ledger = ledger_repo.find_ledger_account(
            receiver_wallet,
        )

        if receiver_ledger is None:
            raise ValueError("Receiver wallet ledger account not found.")

        ledger_entry_repo.create_ledger_entry(
            transaction_record,
            sender_ledger,
            "debit",
            amount,
        )

        ledger_entry_repo.create_ledger_entry(
            transaction_record,
            receiver_ledger,
            "credit",
            amount,
        )

        wallet_repo.decrease_balance(
            sender_wallet,
            amount,
        )

        wallet_repo.increase_balance(
            receiver_wallet,
            amount,
        )

        completed_transaction = transaction_repo.complete_transaction(
            transaction_record,
        )

        idempotency_repo.complete_record(
            idempotency_record,
            completed_transaction,
        )

        return completed_transaction


class IdempotencyService:

    def generate_transfer_fingerprint(
        self, sender_wallet_id, receiver_username, amount, description
    ):
        request_data = (
            f"{sender_wallet_id}|"
            f"{receiver_username.strip().lower()}|"
            f"{amount:.2f}|"
            f"{description.strip()}"
        )
        return hashlib.sha256(request_data.encode()).hexdigest()
