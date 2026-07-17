from .models import Transaction



class TransactionRepository:
    def deposit(
        self,
        created_by,
        wallet,
        transaction_type,
        reference,
        amount,
        description,
    ):
        return Transaction.objects.create(
            created_by=created_by,
            wallet=wallet,
            transaction_type=transaction_type,
            reference=reference,
            amount=amount,
            description=description,
        )
        
    def proceed_transaction(self, transaction_id, user):
        return Transaction.objects.filter(id=transaction_id,created_by=user,status="pending",transaction_type="deposit", ).first()
    
    def complete_transaction(self, transaction):
      transaction.status = "completed"
      transaction.save(update_fields=["status"])
      return transaction