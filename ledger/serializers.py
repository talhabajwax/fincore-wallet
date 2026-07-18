from rest_framework import serializers

from .models import LedgerEntry


class LedgerEntrySerializer(serializers.ModelSerializer):

    account_type = serializers.CharField(
        source="ledger_account.account_type",
        read_only=True,
    )

    currency = serializers.CharField(
        source="ledger_account.currency",
        read_only=True,
    )

    class Meta:
        model = LedgerEntry
        fields = [
            "entry_type",
            "amount",
            "account_type",
            "currency",
            "created_at",
        ]
