import unittest
from flask import Flask
from backend.controllers.users.profile_controller import profile_bp

class ProfileControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(profile_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_get_profile(self):
        response = self.client.get('/api/profile/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'testuser')

    def test_get_profile_not_found(self):
        response = self.client.get('/api/profile/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.json['error'])

    def test_update_profile_success(self):
        response = self.client.put('/api/profile/1', json={
            'username': 'newusername'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'newusername')

    def test_update_profile_email_taken(self):
        self.client.put('/api/profile/2', json={
            'email': 'taken@example.com'
        })
        response = self.client.put('/api/profile/1', json={
            'email': 'taken@example.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email must be unique', response.json['error'])