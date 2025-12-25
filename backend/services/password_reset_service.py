from typing import Optional
from backend.models.password_reset import PasswordReset
from backend.repositories.password_reset_repository import PasswordResetRepository
from backend.repositories.user_repository import UserRepository
from datetime import datetime, timedelta
import secrets

class PasswordResetService:
    def __init__(self, password_reset_repository: PasswordResetRepository, user_repository: UserRepository):
        self.password_reset_repository = password_reset_repository
        self.user_repository = user_repository

    def create_password_reset(self, email: str) -> PasswordReset:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")

        token = secrets.token_hex(16)
        expiry = datetime.utcnow() + timedelta(hours=24)  # 24 hours expiry
        password_reset = PasswordReset(user_id=user['id'], token=token, expiry=expiry)
        self.password_reset_repository.add_password_reset(password_reset)
        return password_reset

    def validate_password_reset(self, token: str) -> bool:
        password_reset = self.password_reset_repository.get_password_reset(token)
        if password_reset:
            if password_reset['expiry'] > datetime.utcnow():
                return True
            self.password_reset_repository.remove_password_reset(token)
        return False

    def use_password_reset(self, token: str, new_password: str) -> None:
        password_reset = self.password_reset_repository.get_password_reset(token)
        if not password_reset or password_reset['expiry'] <= datetime.utcnow():
            raise ValueError("Invalid or expired password reset token")

        user = self.user_repository.get_user_by_id(password_reset['user_id'])
        if not user:
            raise ValueError("User not found")

        user['password'] = new_password  # Assume password is hashed in real-world scenario
        self.user_repository.add_user(user)  # Save changes
        self.password_reset_repository.remove_password_reset(token)