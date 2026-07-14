from .models import Transaction

class transactionRepository:
    def create_transaction(self ,created_by,transaction_type,reference,amount,description):
        return Transaction.objects.create(created_by = created_by,transaction_type=transaction_type,reference=reference,amount=amount,description=description)