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
    
    @transaction.atomic
    def freeze_wallet(self, wallet_id):
        freeze_wallet_repo = WalletRepository()
        active_wallet = freeze_wallet_repo.lock_for_freeze(wallet_id)
        if active_wallet is None:
            raise ValueError("Wallet not found.")
        if active_wallet.status == "frozen":
            raise ValueError("Wallet is already frozen.")
        if active_wallet.status == "expired":
            raise ValueError("Wallet is expired.")
        return freeze_wallet_repo.freeze_wallet(active_wallet)
    
    @transaction.atomic
    def unfreeze_wallet(self, wallet_id):
        unfreeze_wallet_repo = WalletRepository()
        freezed_wallet = unfreeze_wallet_repo.lock_for_freeze(wallet_id)
        if freezed_wallet is None:
            raise ValueError("Wallet not found.")
        if freezed_wallet.status == "active":
            raise ValueError("Wallet is already active.")
        if freezed_wallet.status == "expired":
            raise ValueError("Wallet is expired.")
        return unfreeze_wallet_repo.unfreeze_wallet(freezed_wallet)