from .models import IdempotencyRecord, Transaction, Transfer


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


class IdempotencyRepository:
    def find_record(self, user, operation_type, key):
        return IdempotencyRecord.objects.filter(
            user=user,
            operation_type=operation_type,
            key=key,
        ).first()

    def create_record(self, user, operation_type, key, request_fingerprint):
        return IdempotencyRecord.objects.create(
            user=user,
            operation_type=operation_type,
            key=key,
            request_fingerprint=request_fingerprint,
        )

    def complete_record(self, record, transaction):
        record.transaction = transaction
        record.status = "completed"
        record.save(update_fields=["transaction", "status", "updated_at"])
        return record

    def fail_record(self, record):
        record.status = "failed"
        record.save(update_fields=["status", "updated_at"])
        return record
    
    def create_withdrawal_transaction(self,user,wallet,amount,reference,description):
            return Transaction.objects.create(
                created_by=user,
                wallet=wallet,
                amount=amount,
                reference=reference,
                description=description,
                transaction_type="withdrawal",
                status="pending",
            )
            
    