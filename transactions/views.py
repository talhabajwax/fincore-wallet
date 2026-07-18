from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import DepositSerializer,WalletTransactionsSerializer,WalletTransactionSerializer
from .services import TransactionService
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
        service = TransactionService()
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
            
            
class ConfirmDepositView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, transaction_id):
     user = request.user
     service = TransactionService()
     try:
      proceed = service.proceed_transaction(transaction_id,user)
     except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )
     return Response(
         {
             "message":"Deposit completed successfully."
         }
     )
     
class WalletTransactionsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,wallet_id):
        user=request.user
        service = TransactionService()
        try:
              transactions = service.wallet_transactions(user,wallet_id)
        except ValueError as error:
                    return Response(
                        {"error": str(error)},
                        status=status.HTTP_404_NOT_FOUND
                    )
        serializer = WalletTransactionsSerializer(transactions,many=True)
        return Response(
            {
                "wallet_id": wallet_id,
                "transactions": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
        

class WalletTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,wallet_id,transaction_id):
        user=request.user
        service = TransactionService()
        try:
              transaction = service.single_transaction(user,wallet_id,transaction_id)
        except ValueError as error:
                    return Response(
                        {"error": str(error)},
                        status=status.HTTP_404_NOT_FOUND
                    )
        serializer = WalletTransactionSerializer(transaction)
        return Response(
            {
                "transactionID": transaction_id,
                "transaction": serializer.data,
            },
            status=status.HTTP_200_OK,
        )              