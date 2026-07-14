from .repositeries import WalletRepository
from ledger.services import LedgerService
from django.db import transaction

class WalletService:
    
    @transaction.atomic
    def create_wallet(self, user, currency="PKR"):
        wallet_repo = WalletRepository()
        
        if wallet_repo.wallet_exists(user, currency):
            raise ValueError("Wallet already exists for this user and currency.")
        wallet = wallet_repo.create_wallet(user, currency)
        ledger_service = LedgerService()
        ledger_service.create_ledger(wallet)
        return wallet
    
    def all_wallets(self, user):
        all_wallets_repo= WalletRepository()
        return all_wallets_repo.all_wallets(user)
    
    def a_wallet(self,user,wallet_id):
        a_wallet_repo=WalletRepository()
        return a_wallet_repo.a_wallet(user,wallet_id)