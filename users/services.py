from .repositories import UserRepository

class UserService:
    def create_user(self, user_data):
        user_repository = UserRepository()
        return user_repository.create_user(user_data)
    
    def login_user(self, login_data):
        identifier = login_data["identifier"]
        password = login_data["password"]
        user_repository = UserRepository()
        user = user_repository.login_user(identifier)
        if user and user.check_password(password):
            return user
         
         
        return None
    
    def get_user_profile(self, user):
        user_repository = UserRepository()
        return user_repository.get_user_profile(user)
    
    def update_user_profile(self, user, updated_data):
        user_repository = UserRepository()
        return user_repository.update_user_profile(user, updated_data)