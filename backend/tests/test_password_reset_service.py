import unittest
from backend.repositories.password_reset_repository import PasswordResetRepository
from backend.repositories.user_repository import UserRepository
from backend.services.password_reset_service import PasswordResetService

class PasswordResetServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.password_reset_repository = PasswordResetRepository()
        self.user_repository = UserRepository()
        self.user_repository.add_user({
            'id': 1,
            'email': 'test@example.com',
            'password': 'Password1'
        })
        self.password_reset_service = PasswordResetService(self.password_reset_repository, self.user_repository)

    def test_create_password_reset_success(self):
        password_reset = self.password_reset_service.create_password_reset(email='test@example.com')
        self.assertIn('token', password_reset)
        self.assertEqual(password_reset['user_id'], 1)

    def test_create_password_reset_user_not_found(self):
        with self.assertRaises(ValueError):
            self.password_reset_service.create_password_reset(email='nonexistent@example.com')

    def test_validate_password_reset(self):
        password_reset = self.password_reset_service.create_password_reset(email='test@example.com')
        is_valid = self.password_reset_service.validate_password_reset(password_reset['token'])
        self.assertTrue(is_valid)

    def test_use_password_reset_success(self):
        password_reset = self.password_reset_service.create_password_reset(email='test@example.com')
        self.password_reset_service.use_password_reset(token=password_reset['token'], new_password='NewPassword1')
        user = self.user_repository.get_user_by_id(1)
        self.assertEqual(user['password'], 'NewPassword1')

    def test_use_password_reset_invalid_token(self):
        with self.assertRaises(ValueError):
            self.password_reset_service.use_password_reset(token='invalidtoken', new_password='NewPassword1')