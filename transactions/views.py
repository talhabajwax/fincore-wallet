from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import DepositSerializer
from .services import transactionService

class DepositView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,wallet_id):
        serializer = DepositSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user
        description = serializer.validated_data.get("description", "")
        amount =serializer.validated_data["amount"]
        service = transactionService()
        try:
         transaction = service.deposit(user,wallet_id,amount,description)
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
    {
        "message": "Deposit request created.",
        "transaction_id": transaction.id,
        "reference": transaction.reference,
        "status": transaction.status,
    },
    status=status.HTTP_201_CREATED
)