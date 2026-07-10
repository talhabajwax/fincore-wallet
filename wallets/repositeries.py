from .models import Wallet

class WalletRepository:
    def create_wallet(self, user, currency="PKR"):
        wallet = Wallet.objects.create(user=user, currency=currency)
        return wallet
    def wallet_exists(self, user,currency="PKR"):
        return Wallet.objects.filter(user=user, currency=currency).exists()
    
   