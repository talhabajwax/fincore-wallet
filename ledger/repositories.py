from .models import LedgerAccount

class LedgerRepository:
    
    def create_ledger(self, account_type,wallet):
        return LedgerAccount.objects.create(wallet=wallet,account_type=account_type)
    
    def ledger_for_external_account(self , account_type,wallet):
        external_account,created= LedgerAccount.objects.get_or_create(account_type=account_type,wallet=wallet)
        return external_account