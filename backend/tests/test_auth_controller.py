import unittest
from flask import Flask
from backend.controllers.users.auth_controller import auth_bp

class AuthControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(auth_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_login(self):
        response = self.client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email or password', response.json['error'])

    def test_login_too_many_attempts(self):
        for _ in range(6):
            self.client.post('/api/login', json={
                'email': 'test@example.com',
                'password': 'WrongPassword'
            })
        response = self.client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Too many failed login attempts", response.json['error'])

    def test_logout(self):
        response = self.client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'Password123'
        })
        token = response.json['token']
        response = self.client.post('/api/logout', json={
            'token': token
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged out', response.json['message'])