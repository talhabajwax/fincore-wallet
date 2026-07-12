from .models import Wallet

class WalletRepository:
    def create_wallet(self, user, currency="PKR"):
        return Wallet.objects.create(user=user, currency=currency)
    
    
    def wallet_exists(self, user,currency="PKR"):
        return Wallet.objects.filter(user=user, currency=currency).exists()
    
    def all_wallets(self,user):
       return Wallet.objects.filter(user=user)