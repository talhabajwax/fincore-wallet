from django.urls import path

from .views import (
    ConfirmDepositView,
    DepositView,
    TransferView,
    WalletTransactionsView,
    WalletTransactionView,
)

urlpatterns = [
    path(
        "wallets/<int:wallet_id>/deposit/",
        DepositView.as_view(),
        name="deposit",
    ),
    path(
        "<int:transaction_id>/confirm/",
        ConfirmDepositView.as_view(),
        name="confirm-deposit",
    ),
    path(
        "wallets/<int:wallet_id>/transactions/",
        WalletTransactionsView.as_view(),
        name="wallet-transactions",
    ),
    path(
        "wallets/<int:wallet_id>/transactions/<int:transaction_id>/",
        WalletTransactionView.as_view(),
        name="wallet-transaction-detail",
    ),
    path(
        "wallets/<int:wallet_id>/transfer/",
        TransferView.as_view(),
        name="wallet-transfer",
    ),
]