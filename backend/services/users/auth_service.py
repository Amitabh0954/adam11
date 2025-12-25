from typing import Optional
import secrets
from datetime import datetime, timedelta
from backend.models.user import User
from backend.models.session import Session
from backend.repositories.user_repository import UserRepository
from backend.repositories.session_repository import SessionRepository

class AuthService:
    def __init__(self, user_repository: UserRepository, session_repository: SessionRepository):
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.failed_attempts = {}
        self.MAX_FAILED_ATTEMPTS = 5

    def login(self, email: str, password: str) -> str:
        user = self.user_repository.get_user_by_email(email)
        if user and user['password'] == password:
            token = secrets.token_hex(16)
            session = self.session_repository.create_session(user['id'], token, duration_minutes=30)
            self.failed_attempts[email] = 0  # reset failed attempts on successful login
            return session['token']
        else:
            self.failed_attempts[email] = self.failed_attempts.get(email, 0) + 1
            if self.failed_attempts[email] > self.MAX_FAILED_ATTEMPTS:
                raise ValueError("Too many failed login attempts")
            raise ValueError("Invalid email or password")

    def logout(self, token: str) -> None:
        self.session_repository.invalidate_session(token)

    def get_user_from_token(self, token: str) -> Optional[User]:
        session = self.session_repository.get_session(token)
        if session:
            return self.user_repository.get_user_by_id(session['user_id'])
        return None