import unittest
from flask import Flask
from backend.controllers.users.profile_controller import profile_bp
from backend.repositories.user_repository import UserRepository
user_repository = UserRepository()
user_repository.add_user({
    'id': 1,
    'email': 'test@example.com',
    'password': 'Password1'
})

class ProfileControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(profile_bp, url_prefix='/users')
        self.client = self.app.test_client()

    def test_get_profile(self):
        response = self.client.get('/users/profile?user_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'test@example.com')

    def test_get_profile_nonexistent_user(self):
        response = self.client.get('/users/profile?user_id=999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.json['error'])

    def test_update_profile_success(self):
        response = self.client.post('/users/profile', json={
            'user_id': 1,
            'email': 'new@example.com',
            'password': 'NewPassword1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'new@example.com')

    def test_update_profile_invalid_email(self):
        response = self.client.post('/users/profile', json={
            'user_id': 1,
            'email': 'invalid-email',
            'password': 'NewPassword1'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email format', response.json['error'])

    def test_update_profile_invalid_password(self):
        response = self.client.post('/users/profile', json={
            'user_id': 1,
            'email': 'new@example.com',
            'password': 'short'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password must meet security criteria', response.json['error'])

    def test_update_nonexistent_user(self):
        response = self.client.post('/users/profile', json={
            'user_id': 999,
            'email': 'new@example.com',
            'password': 'NewPassword1'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('User not found', response.json['error'])