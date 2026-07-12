from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "user",
            "status",
            "currency",
            "balance",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "balance", "created_at", "updated_at"]
