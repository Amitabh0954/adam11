from models.user import User

class UserRepository:
    def __init__(self):
        self.users = []
    
    def find_by_email(self, email: str) -> User:
        return next((user for user in self.users if user.email == email), None)
    
    def find_by_reset_token(self, token: str) -> User:
        return next((user for user in self.users if user.reset_token == token), None)
    
    def save(self, user: User) -> None:
        self.users.append(user)
    
    def update(self, user: User) -> None:
        index = next((i for i, u in enumerate(self.users) if u.email == user.email), None)
        if index is not None:
            self.users[index] = user