from typing import Optional
from backend.models.user import User
from backend.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username: str, email: str, password: str) -> User:
        user = User(
            id=len(self.user_repository.users) + 1,
            username=username,
            email=email,
            password=password
        )
        self.user_repository.add_user(user)
        return user

    def get_user(self, user_id: int) -> Optional<User]:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional<User]:
        return self.user_repository.get_user_by_email(email)