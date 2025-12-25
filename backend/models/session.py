from typing import TypedDict
from datetime import datetime

class Session(TypedDict):
    user_id: int
    token: str
    expiry: datetime