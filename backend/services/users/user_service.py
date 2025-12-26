from models.user import User
from repositories.user_repository import UserRepository
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

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
    
    def login_user(self, data: dict):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return {"message": "Email and Password are required", "status": 400}
        
        user = self.user_repository.find_by_email(email)
        if not user:
            return {"message": "Invalid email or password", "status": 401}
        
        if user.is_locked:
            return {"message": "Account is locked due to too many invalid login attempts", "status": 403}
        
        if not check_password_hash(user.password, password):
            user.login_attempts += 1
            if user.login_attempts >= Config.MAX_LOGIN_ATTEMPTS:
                user.is_locked = True
            self.user_repository.update(user)
            return {"message": "Invalid email or password", "status": 401}
        
        user.login_attempts = 0
        user.last_login_at = datetime.utcnow()
        self.user_repository.update(user)
        
        session_expiry = datetime.utcnow() + timedelta(seconds=Config.SESSION_TIMEOUT)
        return {"message": "Login successful", "session_expiry": session_expiry.isoformat(), "status": 200}