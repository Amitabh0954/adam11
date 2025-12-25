import unittest
from backend.repositories.user_repository import UserRepository
from backend.services.users.profile_service import ProfileService

class ProfileServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()
        self.profile_service = ProfileService(self.user_repository)
        self.user_repository.add_user({
            'id': 1,
            'email': 'test@example.com',
            'password': 'Password1'
        })

    def test_get_profile(self):
        user = self.profile_service.get_profile(user_id=1)
        self.assertEqual(user['email'], 'test@example.com')

    def test_update_profile_success(self):
        user = self.profile_service.update_profile(user_id=1, email='new@example.com', password='NewPassword1')
        self.assertEqual(user['email'], 'new@example.com')
        self.assertEqual(user['password'], 'NewPassword1')

    def test_update_profile_invalid_email(self):
        with self.assertRaises(ValueError):
            self.profile_service.update_profile(user_id=1, email='invalid-email', password='NewPassword1')

    def test_update_profile_invalid_password(self):
        with self.assertRaises(ValueError):
            self.profile_service.update_profile(user_id=1, email='new@example.com', password='short')

    def test_update_nonexistent_user(self):
        with self.assertRaises(ValueError):
            self.profile_service.update_profile(user_id=999, email='new@example.com', password='NewPassword1')