from django.db import models

class ledgerAccount(models.Model):
        wallet = models.OneToOneField(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="ledger_account",)
        