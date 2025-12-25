import unittest
from flask import Flask
from backend.controllers.user_controller import user_bp

class UserControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(user_bp, url_prefix='/users')
        self.client = self.app.test_client()

    def test_register_user_successfully(self):
        response = self.client.post('/users/register', json={
            'email': 'test@example.com',
            'password': 'Password1'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['email'], 'test@example.com')

    def test_register_user_invalid_email(self):
        response = self.client.post('/users/register', json={
            'email': 'invalid-email',
            'password': 'Password1'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email format', response.json['error'])

    def test_register_user_invalid_password(self):
        response = self.client.post('/users/register', json={
            'email': 'test@example.com',
            'password': 'short'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password must meet security criteria', response.json['error'])

    def test_register_user_duplicate_email(self):
        self.client.post('/users/register', json={
            'email': 'test@example.com',
            'password': 'Password1'
        })
        response = self.client.post('/users/register', json={
            'email': 'test@example.com',
            'password': 'Password2'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email must be unique', response.json['error'])