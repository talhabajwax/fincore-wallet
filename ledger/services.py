from .repositories import LedgerRepository

class LedgerService:
    def create_ledger(self,wallet):
          account_type = "wallet"
          ledger_repo = LedgerRepository()
          CreateLedger = ledger_repo.create_ledger(account_type,wallet)
          return CreateLedger
      
    def ledger_for_external_account(self):
        account_type = "external_funding"
        wallet = None
        ledger_repo = LedgerRepository()
        external_account = ledger_repo.ledger_for_external_account(account_type,wallet)
        return external_account