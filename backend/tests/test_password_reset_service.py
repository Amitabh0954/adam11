import unittest
from backend.repositories.user_repository import UserRepository
from backend.repositories.password_reset_repository import PasswordResetRepository
from backend.services.users.password_reset_service import PasswordResetService

class PasswordResetServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()
        self.reset_repository = PasswordResetRepository()
        self.reset_service = PasswordResetService(self.user_repository, self.reset_repository)

        self.user_repository.add_user({
            'id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123'
        })

    def test_initiate_password_reset(self):
        self.reset_service.initiate_password_reset(email='test@example.com')
        reset_requests = list(self.reset_repository.reset_requests.values())
        self.assertEqual(len(reset_requests), 1)
        self.assertEqual(reset_requests[0]['user_id'], 1)

    def test_initiate_password_reset_nonexistent_email(self):
        with self.assertRaises(ValueError):
            self.reset_service.initiate_password_reset(email='nonexistent@example.com')

    def test_reset_password_success(self):
        self.reset_service.initiate_password_reset(email='test@example.com')
        reset_requests = list(self.reset_repository.reset_requests.values())
        reset_request = reset_requests[0]
        self.reset_service.reset_password(token=reset_request['token'], new_password='NewPassword123')
        user = self.user_repository.get_user_by_id(1)
        self.assertEqual(user['password'], 'NewPassword123')

    def test_reset_password_invalid_token(self):
        with self.assertRaises(ValueError):
            self.reset_service.reset_password(token='invalidtoken', new_password='NewPassword123')

    def test_reset_password_insecure_password(self):
        self.reset_service.initiate_password_reset(email='test@example.com')
        reset_requests = list(self.reset_repository.reset_requests.values())
        reset_request = reset_requests[0]
        with self.assertRaises(ValueError):
            self.reset_service.reset_password(token=reset_request['token'], new_password='short')