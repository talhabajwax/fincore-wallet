from django.db import models


# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("transfer", "Transfer"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("reversed", "Reversed"),
    ]

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    reference = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Transfer(models.Model):
    transaction = models.OneToOneField(
        "transactions.Transaction",
        on_delete=models.PROTECT,
        related_name="transfer_details",
    )

    receiver_wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.PROTECT,
        related_name="received_transfers",
    )
    
class IdempotencyRecord(models.Model):
    user = models.ForeignKey(
    "users.User",
    on_delete=models.PROTECT,
    related_name="idempotency_records",)
    key = models.CharField(max_length=255)
    OPERATION_TYPES = [
    ("transfer", "Transfer"),
    ("deposit", "Deposit"),
    ("withdrawal", "Withdrawal"),
    ("reversal", "Reversal"),]
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPES)
    request_fingerprint = models.CharField(max_length=64)
    STATUS_CHOICES = [
    ("processing", "Processing"),
    ("completed", "Completed"),
    ("failed", "Failed"),]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="processing")
    transaction = models.ForeignKey(
    "transactions.Transaction",
    on_delete=models.PROTECT,
    related_name="idempotency_records",
    null=True,
    blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
