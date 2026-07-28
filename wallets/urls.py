from django.urls import path

from .views import (
    AllWalletsView,
    AWalletView,
    CreateWalletView,
    FreezeWalletView,
    UnfreezeWalletView,
)

urlpatterns = [
    path("create/", CreateWalletView.as_view(), name="create-wallet"),
    path("", AllWalletsView.as_view(), name="All-Wallets"),
    path("<int:wallet_id>/", AWalletView.as_view(), name="a-wallet"),
    path(
        "<int:wallet_id>/freeze/",
        FreezeWalletView.as_view(),
        name="freeze-wallet",
    ),
    path(
        "<int:wallet_id>/unfreeze/",
        UnfreezeWalletView.as_view(),
        name="unfreeze-wallet",
    ),
]
