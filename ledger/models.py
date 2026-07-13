from django.db import models

class LedgerAccount(models.Model):
        wallet = models.OneToOneField(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="ledger_account",)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        