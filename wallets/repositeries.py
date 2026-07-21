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
 
    def receiver_wallet(self, receiver_username, currency):
     return Wallet.objects.filter(
        user__username=receiver_username,
        currency=currency,
    ).first()
     
    def decrease_balance(self, sender_wallet, amount):
         locked_wallet = (
            Wallet.objects
            .select_for_update()
            .get(id=sender_wallet.id)
        )
         locked_wallet.balance = locked_wallet.balance - amount
         locked_wallet.save(update_fields=["balance"])

         return locked_wallet
     
    def lock_transfer_wallets(self, sender_wallet_id, receiver_wallet_id):
     wallets = (
        Wallet.objects
        .select_for_update()
        .filter(id__in=[sender_wallet_id, receiver_wallet_id])
        .order_by("id")
    )

     wallets_by_id = {
        wallet.id: wallet
        for wallet in wallets
    }

     sender_wallet = wallets_by_id.get(sender_wallet_id)
     receiver_wallet = wallets_by_id.get(receiver_wallet_id)

     return sender_wallet, receiver_wallet         