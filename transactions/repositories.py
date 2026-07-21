from .models import Transaction, Transfer


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
        return (
            Transaction.objects.select_for_update()
            .filter(
                id=transaction_id,
                created_by=user,
                status="pending",
                transaction_type="deposit",
            )
            .first()
        )

    def complete_transaction(self, transaction):
        transaction.status = "completed"
        transaction.save(update_fields=["status"])
        return transaction

    def wallet_transactions(self, user, wallet_id):
        return Transaction.objects.filter(
            wallet_id=wallet_id,
            wallet__user=user,
        ).order_by("-created_at")

    def single_transaction(self, user, wallet_id, transaction_id):
        return Transaction.objects.filter(
            id=transaction_id, wallet_id=wallet_id, wallet__user=user
        ).first()

    def transfer_transaction(self, user, sender_wallet, amount, reference, description):
        return Transaction.objects.create(
            created_by=user,
            wallet=sender_wallet,
            transaction_type="transfer",
            amount=amount,
            reference=reference,
            description=description,
        )

    def create_transfer(self, transaction, receiver_wallet):
        return Transfer.objects.create(
            transaction=transaction,
            receiver_wallet=receiver_wallet,
        )
