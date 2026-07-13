from .repositories import LedgerRepository

class LedgerService:
    def create_ledger(self,wallet):
        ledger_repo = LedgerRepository()
        CreateLedger = ledger_repo.create_ledger(wallet)
        return CreateLedger