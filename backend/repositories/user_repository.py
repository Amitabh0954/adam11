from models.user import User

class UserRepository:
    def __init__(self):
        self.users = []
    
    def find_by_email(self, email: str) -> User:
        return next((user for user in self.users if user.email == email), None)
    
    def save(self, user: User) -> None:
        self.users.append(user)