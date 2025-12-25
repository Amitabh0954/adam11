from typing import Optional
from datetime import datetime, timedelta
from backend.models.session import Session

class SessionRepository:
    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id: int, token: str, duration_minutes: int) -> Session:
        expires_at = (datetime.utcnow() + timedelta(minutes=duration_minutes)).isoformat()
        session = Session(user_id=user_id, token=token, expires_at=expires_at)
        self.sessions[token] = session
        return session

    def get_session(self, token: str) -> Optional[Session]:
        session = self.sessions.get(token)
        if session and datetime.fromisoformat(session['expires_at']) > datetime.utcnow():
            return session
        return None

    def invalidate_session(self, token: str) -> None:
        if token in self.sessions:
            del self.sessions[token]