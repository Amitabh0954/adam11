from typing import Optional
import secrets
from datetime import datetime
from backend.models.user import User
from backend.models.password_reset import PasswordReset
from backend.repositories.user_repository import UserRepository
from backend.repositories.password_reset_repository import PasswordResetRepository
from backend.configurations.email_config import send_password_reset_email

class PasswordResetService:
    def __init__(self, user_repository: UserRepository, reset_repository: PasswordResetRepository):
        self.user_repository = user_repository
        self.reset_repository = reset_repository

    def initiate_password_reset(self, email: str) -> None:
        user = self.user_repository.get_user_by_email(email)
        if user:
            token = secrets.token_hex(16)
            self.reset_repository.create_reset_request(user['id'], token)
            send_password_reset_email(email, token)

    def reset_password(self, token: str, new_password: str) -> None:
        reset_request = self.reset_repository.get_reset_request(token)
        if reset_request:
            user = self.user_repository.get_user_by_id(reset_request['user_id'])
            if user:
                if self._is_secure_password(new_password):
                    user['password'] = new_password
                    self.reset_repository.invalidate_reset_request(token)
                else:
                    raise ValueError("Password does not meet security criteria")
            else:
                raise ValueError("User not found")
        else:
            raise ValueError("Invalid or expired token")

    def _is_secure_password(self, password: str) -> bool:
        return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)