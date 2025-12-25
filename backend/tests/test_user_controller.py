import unittest
from flask import Flask
from backend.controllers.users.user_controller import user_bp

class UserControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(user_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_register_user(self):
        response = self.client.post('/api/users/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['username'], 'testuser')

    def test_register_user_duplicate_email(self):
        self.client.post('/api/users/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123'
        })
        response = self.client.post('/api/users/register', json={
            'username': 'anotheruser',
            'email': 'test@example.com',
            'password': 'AnotherPassword123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email must be unique', response.json['error'])

    def test_register_user_insecure_password(self):
        response = self.client.post('/api/users/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password does not meet security criteria', response.json['error'])

    def test_get_user(self):
        self.client.post('/api/users/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123'
        })
        response = self.client.get('/api/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'testuser')

    def test_get_user_not_found(self):
        response = self.client.get('/api/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.json['error'])