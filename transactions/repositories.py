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