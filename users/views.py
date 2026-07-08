from django.shortcuts import render
from .serializers import UserRegistrationSerializer
from .models import User
from .services import UserService
from rest_framework.views import APIView
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