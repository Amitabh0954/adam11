from typing import Optional
from backend.models.session import Session

class SessionRepository:
    def __init__(self):
        self.sessions = {}

    def add_session(self, session: Session) -> None:
        self.sessions[session['token']] = session

    def get_session(self, token: str) -> Optional[Session]:
        return self.sessions.get(token)

    def remove_session(self, token: str) -> None:
        if token in self.sessions:
            del self.sessions[token]