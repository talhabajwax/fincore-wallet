from .serializers import UserRegistrationSerializer
from .services import UserService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user_service = UserService()
            user = user_service.create_user(user_data)
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)