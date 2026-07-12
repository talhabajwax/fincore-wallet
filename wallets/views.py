from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import WalletSerializer
from .services import WalletService


class CreateWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WalletSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        currency = serializer.validated_data["currency"]
        wallet_service = WalletService()

        try:
            wallet = wallet_service.create_wallet(user, currency)
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Wallet created successfully."},
            status=status.HTTP_201_CREATED
        )
        
class AllWalletsView(APIView):
    permission_classes = [IsAuthenticated]        
        
    def get (self ,request):
        wallets_service = WalletService()
        user=request.user
        wallets=wallets_service.all_wallets(user)
        serializer = WalletSerializer(wallets, many=True)

        return Response(
        serializer.data,
        status=status.HTTP_200_OK)
        