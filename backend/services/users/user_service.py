from models.user import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
    
    def register_user(self, data: dict):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return {"message": "Email and Password are required", "status": 400}
        
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            return {"message": "Email already registered", "status": 400}
        
        user = User(email=email, password=password)
        self.user_repository.save(user)
        
        return {"message": "User registered successfully", "status": 201}