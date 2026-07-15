from .repositories import TransactionRepository
from wallets.repositeries import WalletRepository
import uuid


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