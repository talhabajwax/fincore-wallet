from .repositories import transactionRepository
from wallets.repositeries import WalletRepository
import uuid

class transactionService():
    def deposit(self, user,wallet_id,amount,description):
        walletRepo = WalletRepository()
        valid_wallet=walletRepo.a_wallet(user,wallet_id)
        if valid_wallet is None:
          raise ValueError("Wallet not found.")
        if valid_wallet.status != "active":
          raise ValueError("Wallet is not active.")
        if amount <= 0:
          raise ValueError("Amount must be greater than zero.")
        transaction_type = "deposit"
        reference = f"TXN-{uuid.uuid4()}"
        transaction_repo= transactionRepository()
        transaction = transaction_repo.deposit(user,transaction_type,reference,amount,description)
        return transaction