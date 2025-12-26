from datetime import datetime
from werkzeug.security import generate_password_hash

class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = generate_password_hash(password)
        self.login_attempts = 0
        self.is_locked = False
        self.last_login_at = None
        self.reset_token = None
        self.reset_token_expiry = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()