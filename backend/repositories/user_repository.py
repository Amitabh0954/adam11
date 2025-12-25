from typing import Optional
from backend.models.user import User

class UserRepository:
    def __init__(self):
        self.users = {}
        self.email_index = set()

    def add_user(self, user: User) -> None:
        if user['email'] in self.email_index:
            raise ValueError("Email must be unique")
        self.users[user['id']] = user
        self.email_index.add(user['email'])

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user['email'] == email:
                return user
        return None