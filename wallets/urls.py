from django.urls import path
from .views import CreateWalletView,AllWalletsView

urlpatterns = [
        path("create/", CreateWalletView.as_view(), name="create-wallet"),
        path("wallets/", AllWalletsView.as_view(), name="All-Wallets"),

]
