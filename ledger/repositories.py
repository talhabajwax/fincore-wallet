from .models import LedgerAccount

class LedgerRepository:
    
    def create_ledger(self, wallet):
        return LedgerAccount.objects.create(wallet=wallet)
    