from django.urls import path

from .views import AllWalletsView, CreateWalletView

urlpatterns = [
    path("create/", CreateWalletView.as_view(), name="create-wallet"),
    path("", AllWalletsView.as_view(), name="All-Wallets"),
]
