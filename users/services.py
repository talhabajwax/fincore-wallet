from .repositories import UserRepository

class UserService:
    def create_user(self, user_data):
        user_repository = UserRepository()
        return user_repository.create_user(user_data)