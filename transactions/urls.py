from django.urls import path
from .views import DepositView

urlpatterns = [
    path(
    "wallets/<int:wallet_id>/deposit/",DepositView.as_view(),name="deposit"
)
]