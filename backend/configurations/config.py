import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_LOGIN_ATTEMPTS = int(os.environ.get('MAX_LOGIN_ATTEMPTS', 5))
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', 1800))  # 30 minutes
    RESET_TOKEN_EXPIRY = int(os.environ.get('RESET_TOKEN_EXPIRY', 86400))  # 24 hours