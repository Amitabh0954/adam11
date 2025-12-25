import unittest
from backend.repositories.user_repository import UserRepository
from backend.repositories.session_repository import SessionRepository
from backend.services.users.auth_service import AuthService

class AuthServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()
        self.session_repository = SessionRepository()
        self.auth_service = AuthService(self.user_repository, self.session_repository)

        self.user_repository.add_user({
            'id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123'
        })

    def test_login_success(self):
        token = self.auth_service.login(email='test@example.com', password='Password123')
        self.assertIsNotNone(token)

    def test_login_invalid_credentials(self):
        with self.assertRaises(ValueError):
            self.auth_service.login(email='test@example.com', password='WrongPassword')

    def test_login_too_many_attempts(self):
        for _ in range(6):
            with self.assertRaises(ValueError):
                self.auth_service.login(email='test@example.com', password='WrongPassword')

    def test_logout(self):
        token = self.auth_service.login(email='test@example.com', password='Password123')
        self.auth_service.logout(token)
        session = self.session_repository.get_session(token)
        self.assertIsNone(session)

    def test_get_user_from_token(self):
        token = self.auth_service.login(email='test@example.com', password='Password123')
        user = self.auth_service.get_user_from_token(token)
        self.assertEqual(user['email'], 'test@example.com')