from .models import LedgerAccount,LedgerEntry

class LedgerRepository:
    
    def create_ledger(self, account_type,wallet):
        return LedgerAccount.objects.create(wallet=wallet,account_type=account_type,currency=wallet.currency)
    
    def ledger_for_external_account(self , account_type,wallet,currency):
        external_account,created= LedgerAccount.objects.get_or_create(account_type=account_type,wallet=wallet,currency=currency)
        return external_account
    def find_ledger_account(self , wallet):
        return LedgerAccount.objects.filter(wallet=wallet).first()
    
    
class LedgerEntryRepository:
    def create_ledger_entry(self,transaction,ledger_account,entry_type,amount):
        return LedgerEntry.objects.create(transaction=transaction,ledger_account=ledger_account,entry_type=entry_type,amount=amount)