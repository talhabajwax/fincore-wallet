from django.urls import path

from .views import AllWalletsView, CreateWalletView,AWalletView

urlpatterns = [
    path("create/", CreateWalletView.as_view(), name="create-wallet"),
    path("", AllWalletsView.as_view(), name="All-Wallets"),
    path("<int:wallet_id>/", AWalletView.as_view(), name="a-wallet"),
]
