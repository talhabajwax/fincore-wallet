from .repositories import LedgerRepository,LedgerEntryRepository

class LedgerService:
    def create_ledger(self,wallet):
          account_type = "wallet"
          ledger_repo = LedgerRepository()
          CreateLedger = ledger_repo.create_ledger(account_type,wallet)
          return CreateLedger
      
    def ledger_for_external_account(self,currency):
        account_type = "external_funding"
        wallet = None
        ledger_repo = LedgerRepository()
        external_account = ledger_repo.ledger_for_external_account(account_type,wallet,currency)
        return external_account
    
    def ledger_entries(self,transaction):
        repo = LedgerEntryRepository()
        entries = repo.ledger_entries(transaction)
        return entries