from typing import TypedDict

class Session(TypedDict):
    user_id: int
    token: str
    expires_at: str  # ISO format datetime string