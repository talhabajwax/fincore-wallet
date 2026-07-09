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
        print("IDENTIFIER:", identifier)
        print("PASSWORD:", password)
        print("USER:", user)
        if user and user.check_password(password):
            print("DB PASSWORD:", user.password)
            print("CHECK:", user.check_password(password))
            return user
         
         
        return None