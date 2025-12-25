from typing import Optional
from backend.models.session import Session
from backend.repositories.session_repository import SessionRepository
from datetime import datetime, timedelta
import secrets

class SessionService:
    def __init__(self, session_repository: SessionRepository):
        self.session_repository = session_repository

    def create_session(self, user_id: int) -> Session:
        token = secrets.token_hex(16)
        expiry = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry for example
        session = Session(user_id=user_id, token=token, expiry=expiry)
        self.session_repository.add_session(session)
        return session

    def validate_session(self, token: str) -> bool:
        session = self.session_repository.get_session(token)
        if session:
            if session['expiry'] > datetime.utcnow():
                return True
            self.session_repository.remove_session(token)
        return False

    def invalidate_session(self, token: str) -> None:
        self.session_repository.remove_session(token)