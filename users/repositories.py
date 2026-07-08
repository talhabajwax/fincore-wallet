from .models import User


class UserRepository:
    def create_user(self, user_data):
        return User.objects.create_user(**user_data)