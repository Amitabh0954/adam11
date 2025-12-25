from typing import Optional
from backend.models.password_reset import PasswordReset

class PasswordResetRepository:
    def __init__(self):
        self.password_resets = {}

    def add_password_reset(self, password_reset: PasswordReset) -> None:
        self.password_resets[password_reset['token']] = password_reset

    def get_password_reset(self, token: str) -> Optional[PasswordReset]:
        return self.password_resets.get(token)

    def remove_password_reset(self, token: str) -> None:
        if token in self.password_resets:
            del self.password_resets[token]