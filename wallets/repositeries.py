from .models import Wallet

class WalletRepository:
    def create_wallet(self, user, currency="PKR"):
        return Wallet.objects.create(user=user, currency=currency)
    
    
    def wallet_exists(self, user,currency="PKR"):
        return Wallet.objects.filter(user=user, currency=currency).exists()
    
    def all_wallets(self,user):
       return Wallet.objects.filter(user=user)
   
    def a_wallet(self,user,wallet_id):
        return Wallet.objects.filter(user=user,id=wallet_id).first()
    
    
    def increase_balance(self, user_wallet, amount):
     locked_wallet = (
        Wallet.objects
        .select_for_update()
        .get(id=user_wallet.id)
    )

     locked_wallet.balance = locked_wallet.balance + amount
     locked_wallet.save(update_fields=["balance"])

     return locked_wallet