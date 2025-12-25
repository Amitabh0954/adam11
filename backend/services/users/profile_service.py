from typing import Optional
from backend.models.user import User
from backend.repositories.user_repository import UserRepository
import re

class ProfileService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_profile(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_user_by_id(user_id)

    def update_profile(self, user_id: int, email: str, password: str) -> User:
        if not self.is_valid_email(email):
            raise ValueError("Invalid email format")

        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user['email'] = email
        if password:
            if not self.is_valid_password(password):
                raise ValueError("Password must meet security criteria")
            user['password'] = password  # Assume password is hashed

        self.user_repository.add_user(user)  # Save changes
        return user

    def is_valid_email(self, email: str) -> bool:
        email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        return re.match(email_regex, email) is not None

    def is_valid_password(self, password: str) -> bool:
        # Example criteria: At least 8 characters, 1 uppercase, 1 lowercase, 1 number
        return (len(password) >= 8 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password))