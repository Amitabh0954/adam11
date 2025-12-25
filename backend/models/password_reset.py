from typing import TypedDict
from datetime import datetime

class PasswordReset(TypedDict):
    user_id: int
    token: str
    expiry: datetime