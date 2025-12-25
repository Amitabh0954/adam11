import unittest
from flask import Flask
from backend.controllers.password_reset_controller import password_reset_bp
from backend.repositories.user_repository import UserRepository
user_repository = UserRepository()
user_repository.add_user({
    'id': 1,
    'email': 'test@example.com',
    'password': 'Password1'
})

class PasswordResetControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(password_reset_bp, url_prefix='/auth')
        self.client = self.app.test_client()

    def test_request_password_reset_success(self):
        response = self.client.post('/auth/password_reset/request', json={
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password reset link sent to your email', response.json['message'])

    def test_request_password_reset_user_not_found(self):
        response = self.client.post('/auth/password_reset/request', json={
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('User not found', response.json['error'])

    def test_reset_password_success(self):
        response = self.client.post('/auth/password_reset/request', json={
            'email': 'test@example.com'
        })
        token = response.json['message']
        response = self.client.post('/auth/password_reset/reset', json={
            'token': token,
            'new_password': 'NewPassword1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password has been reset successfully', response.json['message'])

    def test_reset_password_invalid_token(self):
        response = self.client.post('/auth/password_reset/reset', json={
            'token': 'invalidtoken',
            'new_password': 'NewPassword1'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid or expired password reset token', response.json['error'])