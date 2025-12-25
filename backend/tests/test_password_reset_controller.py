import unittest
from flask import Flask
from backend.controllers.users.password_reset_controller import password_reset_bp

class PasswordResetControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(password_reset_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_initiate_password_reset(self):
        response = self.client.post('/api/password-reset', json={
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password reset email sent', response.json['message'])

    def test_initiate_password_reset_nonexistent_email(self):
        response = self.client.post('/api/password-reset', json={
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email or password', response.json['error'])

    def test_reset_password(self):
        self.client.post('/api/password-reset', json={
            'email': 'test@example.com'
        })
        response = self.client.post('/api/password-reset/token', json={
            'new_password': 'NewPassword123'
        })  # Make sure to capture the actual token from the reset repository
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password has been reset', response.json['message'])

    def test_reset_password_invalid_token(self):
        response = self.client.post('/api/password-reset/invalidtoken', json={
            'new_password': 'NewPassword123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid or expired token', response.json['error'])

    def test_reset_password_insecure_password(self):
        self.client.post('/api/password-reset', json={
            'email': 'test@example.com'
        })
        response = self.client.post('/api/password-reset/token', json={
            'new_password': 'short'
        })  # Make sure to capture the actual token from the reset repository
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password does not meet security criteria', response.json['error'])