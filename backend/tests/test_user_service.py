import unittest
from backend.repositories.user_repository import UserRepository
from backend.services.users.user_service import UserService

class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()
        self.user_service = UserService(self.user_repository)

    def test_register_user_success(self):
        user = self.user_service.register_user(username='testuser', email='test@example.com', password='Password123')
        self.assertEqual(user['username'], 'testuser')
        self.assertEqual(user['email'], 'test@example.com')

    def test_register_user_duplicate_email(self):
        self.user_service.register_user(username='testuser', email='test@example.com', password='Password123')
        with self.assertRaises(ValueError):
            self.user_service.register_user(username='testuser2', email='test@example.com', password='Password1234')

    def test_register_user_insecure_password(self):
        with self.assertRaises(ValueError):
            self.user_service.register_user(username='testuser', email='test@example.com', password='short')

    def test_get_user(self):
        user = self.user_service.register_user(username='testuser', email='test@example.com', password='Password123')
        fetched_user = self.user_service.get_user(user['id'])
        self.assertEqual(fetched_user['username'], 'testuser')

    def test_get_user_not_found(self):
        user = self.user_service.get_user(999)
        self.assertIsNone(user)

    def test_get_user_by_email(self):
        user = self.user_service.register_user(username='testuser', email='test@example.com', password='Password123')
        fetched_user = self.user_service.get_user_by_email('test@example.com')
        self.assertEqual(fetched_user['username'], 'testuser')

    def test_get_user_by_email_not_found(self):
        user = self.user_service.get_user_by_email('nonexistent@example.com')
        self.assertIsNone(user)