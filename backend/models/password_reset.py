from typing import TypedDict

class PasswordReset(TypedDict):
    user_id: int
    token: str
    expires_at: str  # ISO format datetime string