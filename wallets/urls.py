from django.urls import path
from .views import CreateWalletView

urlpatterns = [
        path("create/", CreateWalletView.as_view(), name="create-wallet"),

]
