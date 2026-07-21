from rest_framework import serializers
from .models import Transaction,Transfer
from decimal import Decimal

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields=[
            "amount","description"
        ]
    
class WalletTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Transaction
        fields = [
            "id",
            "transaction_type",
            "amount",
            "status",
            "reference",
            "description",
            "created_at",
        ]
        
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Transaction
        fields = [
            "id",
            "transaction_type",
            "amount",
            "status",
            "reference",
            "description",
            "created_at",
        ]
        
        
class TransferSerializer(serializers.Serializer):
    receiver_username = serializers.CharField(max_length=150)

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )