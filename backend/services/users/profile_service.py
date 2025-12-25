from typing import Optional
from backend.models.user import User
from backend.repositories.user_repository import UserRepository

class ProfileService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def update_profile(self, user_id: int, username: Optional[str] = None, email: Optional[str] = None) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        if username:
            user['username'] = username

        if email:
            if self.user_repository.get_user_by_email(email):
                raise ValueError("Email must be unique")
            user['email'] = email

        self.user_repository.update_user(user)
        return user

    def get_profile(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_user_by_id(user_id)