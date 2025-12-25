from typing import TypedDict

class User(TypedDict):
    id: int
    username: str
    email: str
    password: str