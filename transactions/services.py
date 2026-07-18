import uuid

from django.db import transaction

from ledger.repositories import LedgerEntryRepository, LedgerRepository
from wallets.repositeries import WalletRepository

from .repositories import TransactionRepository


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
    def proceed_transaction(self, transaction_id, user):
        repo = TransactionRepository()
        proceed = repo.proceed_transaction(transaction_id, user)
        if proceed is None:
            raise ValueError("Pending deposit transaction not found.")
        wallet = proceed.wallet
        ledgerRepo = LedgerRepository()
        ledger = ledgerRepo.find_ledger_account(wallet)
        if ledger is None:
            raise ValueError("Wallet ledger account not found.")
        account_type = "external_funding"
        wallet_for_ledger = None
        currency = wallet.currency
        ledgerAccountRepo = ledgerRepo.ledger_for_external_account(
            account_type, wallet_for_ledger, currency
        )
        entryRepo = LedgerEntryRepository()
        amount = proceed.amount
        entry1type = "debit"
        Entry1 = entryRepo.create_ledger_entry(
            proceed, ledgerAccountRepo, entry1type, amount
        )
        entry2type = "credit"
        Entry2 = entryRepo.create_ledger_entry(proceed, ledger, entry2type, amount)
        walletrepo = WalletRepository()
        balance = walletrepo.increase_balance(wallet, amount)
        updateStatus = repo.complete_transaction(proceed)
        return updateStatus

    def wallet_transactions(self, user, wallet_id):
        wallet_repo = WalletRepository()
        valid_wallet = wallet_repo.a_wallet(user, wallet_id)

        if valid_wallet is None:
            raise ValueError("Wallet not found.")
        repo = TransactionRepository()
        transactions = repo.wallet_transactions(user, wallet_id)
        return transactions
    
    def single_transaction(self,user,wallet_id,transaction_id):
        repo = TransactionRepository()
        transaction = repo.single_transaction(user,wallet_id,transaction_id)
        if transaction is None:
         raise ValueError("Transaction not found.")
        return transaction
