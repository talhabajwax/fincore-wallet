from django import path
from .views import CreateWalletView

urlpatterns = [
        path("=CreateWallet/", CreateWalletView.as_view(), name="user-profile-update")

]
