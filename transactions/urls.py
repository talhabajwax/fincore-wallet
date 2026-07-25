from django.urls import path

from .views import (
    ConfirmDepositView,
    DepositView,
    TransferView,
    WalletTransactionsView,
    WalletTransactionView,
    WithdrawalApproveView,
    WithdrawalView,
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
    path(
        "wallets/<int:wallet_id>/withdraw/",
        WithdrawalView.as_view(),
        name="withdrawal-request",
    ),
    path(
        "withdrawals/<int:withdrawal_id>/approve/",
        WithdrawalApproveView.as_view(),
        name="withdrawal-approve",
    ),
]
