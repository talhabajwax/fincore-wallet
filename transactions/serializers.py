from rest_framework import serializers
from .models import Transaction

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