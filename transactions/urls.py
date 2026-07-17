from django.urls import path
from .views import DepositView,ConfirmDepositView

urlpatterns = [
    path(
    "wallets/<int:wallet_id>/deposit/",DepositView.as_view(),name="deposit"
    
),
    path(
    "<int:transaction_id>/confirm/",
    ConfirmDepositView.as_view(),
    name="confirm-deposit",
)
]