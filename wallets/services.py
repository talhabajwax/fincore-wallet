from .repositeries import WalletRepository

class WalletService:
    
    def create_wallet(self, user, currency="PKR"):
        wallet_repo = WalletRepository()
        if wallet_repo.wallet_exists(user, currency):
            raise ValueError("Wallet already exists for this user and currency.")
        return wallet_repo.create_wallet(user, currency)
    
    def all_wallets(self, user):
        all_wallets_repo= WalletRepository()
        return all_wallets_repo.all_wallets(user)