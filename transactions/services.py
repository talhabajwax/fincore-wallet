import uuid

from django.db import transaction

from ledger.repositories import LedgerEntryRepository, LedgerRepository
from wallets.repositeries import WalletRepository

from .repositories import TransactionRepository
from .models import Transaction, Transfer


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
    ):
        wallet_repo = WalletRepository()
        transaction_repo = TransactionRepository()
        ledger_repo = LedgerRepository()
        ledger_entry_repo = LedgerEntryRepository()

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

        transaction = transaction_repo.transfer_transaction(
            user,
            sender_wallet,
            amount,
            reference,
            description,
        )

        transaction_repo.create_transfer(
            transaction,
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
            transaction,
            sender_ledger,
            "debit",
            amount,
        )

        ledger_entry_repo.create_ledger_entry(
            transaction,
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
            transaction,
        )

        return completed_transaction
