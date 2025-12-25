from typing import Optional
from datetime import datetime, timedelta
from backend.models.password_reset import PasswordReset

class PasswordResetRepository:
    def __init__(self):
        self.reset_requests = {}

    def create_reset_request(self, user_id: int, token: str) -> PasswordReset:
        expires_at = (datetime.utcnow() + timedelta(hours=24)).isoformat()
        reset_request = PasswordReset(user_id=user_id, token=token, expires_at=expires_at)
        self.reset_requests[token] = reset_request
        return reset_request

    def get_reset_request(self, token: str) -> Optional[PasswordReset]:
        reset_request = self.reset_requests.get(token)
        if reset_request and datetime.fromisoformat(reset_request['expires_at']) > datetime.utcnow():
            return reset_request
        return None

    def invalidate_reset_request(self, token: str) -> None:
        if token in self.reset_requests:
            del self.reset_requests[token]