import unittest
from backend.repositories.user_repository import UserRepository
from backend.services.user_service import UserService

class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()
        self.user_service = UserService(self.user_repository)

    def test_register_user_successfully(self):
        user = self.user_service.register_user(email='test@example.com', password='Password1')
        self.assertEqual(user['email'], 'test@example.com')
        self.assertTrue(self.user_service.is_valid_password('Password1'))

    def test_register_user_invalid_email(self):
        with self.assertRaises(ValueError):
            self.user_service.register_user(email='invalid-email', password='Password1')

    def test_register_user_invalid_password(self):
        with self.assertRaises(ValueError):
            self.user_service.register_user(email='test@example.com', password='short')

    def test_register_user_duplicate_email(self):
        self.user_service.register_user(email='test@example.com', password='Password1')
        with self.assertRaises(ValueError):
            self.user_service.register_user(email='test@example.com', password='Password2')

    def test_authenticate_user_successful(self):
        self.user_service.register_user(email='test@example.com', password='Password1')
        user = self.user_service.authenticate_user(email='test@example.com', password='Password1')
        self.assertEqual(user['email'], 'test@example.com')

    def test_authenticate_user_invalid_email(self):
        with self.assertRaises(ValueError):
            self.user_service.authenticate_user(email='nonexistent@example.com', password='Password1')

    def test_authenticate_user_invalid_password(self):
        self.user_service.register_user(email='test@example.com', password='Password1')
        with self.assertRaises(ValueError):
            self.user_service.authenticate_user(email='test@example.com', password='WrongPassword')