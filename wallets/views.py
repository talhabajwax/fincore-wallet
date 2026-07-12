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
        
    def get (self ,request):
        