from models.user import User
from repositories.user_repository import UserRepository
from configurations.config import Config
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import uuid

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
    
    def register_user(self, data: dict):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return {"message": "Email and Password are required", "status": 400}
        
        if not self.is_password_secure(password):
            return {"message": "Password does not meet security criteria", "status": 400}

        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            return {"message": "Email already registered", "status": 400}
        
        user = User(email=email, password=password)
        self.user_repository.save(user)
        
        # Send verification email (omitted for brevity)
        
        return {"message": "User registered successfully. Please verify your email.", "status": 201}
    
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
    
    def request_password_reset(self, data: dict):
        email = data.get('email')
        if not email:
            return {"message": "Email is required", "status": 400}
        
        user = self.user_repository.find_by_email(email)
        if not user:
            return {"message": "Invalid email", "status": 400}
        
        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        user.reset_token_expiry = datetime.utcnow() + timedelta(seconds=Config.RESET_TOKEN_EXPIRY)
        self.user_repository.update(user)
        
        # Send password reset email with token (omitted for brevity)
        
        return {"message": "Password reset link has been sent to your email", "status": 200}
    
    def reset_password(self, data: dict, token: str):
        password = data.get('password')
        if not password:
            return {"message": "Password is required", "status": 400}
        
        if not self.is_password_secure(password):
            return {"message": "Password does not meet security criteria", "status": 400}

        user = self.user_repository.find_by_reset_token(token)
        if not user or user.reset_token_expiry < datetime.utcnow():
            return {"message": "Invalid or expired reset token", "status": 400}
        
        user.password = generate_password_hash(password)
        user.reset_token = None
        user.reset_token_expiry = None
        self.user_repository.update(user)
        
        return {"message": "Password has been reset successfully", "status": 200}

    def update_profile(self, data: dict):
        email = data.get('email')
        user = self.user_repository.find_by_email(email)
        if not user:
            return {"message": "User not found", "status": 404}
        
        update_fields = False
        if 'new_email' in data:
            user.email = data['new_email']
            update_fields = True
        if 'password' in data:
            if not self.is_password_secure(data['password']):
                return {"message": "Password does not meet security criteria", "status": 400}
            user.password = generate_password_hash(data['password'])
            update_fields = True

        if update_fields:
            self.user_repository.update(user)
            return {"message": "Profile updated successfully", "status": 200}

        return {"message": "No updates made to profile", "status": 200}

    @staticmethod
    def is_password_secure(password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char is lower() for char in password):
            return False
        if not any char is upper() for char in password):
            return False
        if not any char in "!@#$%^&*()_+-=[]{}|;:'\",.<>?/":
            return False
        return True