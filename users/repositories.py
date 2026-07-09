from .models import User


class UserRepository:
    def create_user(self, user_data):
        return User.objects.create_user(**user_data)
    
    def login_user(self, identifier):
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                return None
            
        return user

   