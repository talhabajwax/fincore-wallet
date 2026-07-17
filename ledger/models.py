from django.db import models

class LedgerAccount(models.Model):
        ACCOUNT_TYPES = [("external_funding","External Funding"),("wallet","UserWallet")]
        wallet = models.OneToOneField(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="ledger_account",null=True,blank=True)
        currency = models.CharField(max_length=3)
        account_type= models.CharField(max_length=20,choices=ACCOUNT_TYPES,)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
class LedgerEntry(models.Model):
        ENTRY_TYPES = [("credit","Credit"),("debit","Debit")]
        transaction = models.ForeignKey("transactions.Transaction",on_delete=models.PROTECT,related_name="transactions_entries",)
        ledger_account = models.ForeignKey("ledger.LedgerAccount",on_delete=models.PROTECT,related_name="ledger_entries",)
        entry_type = models.CharField(max_length=20,choices=ENTRY_TYPES,)
        amount = models.DecimalField(max_digits=12,decimal_places=2,)
        created_at = models.DateTimeField(auto_now_add=True,)