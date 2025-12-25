import unittest
from backend.repositories.user_repository import UserRepository
from backend.services.users.profile_service import ProfileService

class ProfileServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()
        self.profile_service = ProfileService(self.user_repository)

        self.user_repository.add_user({
            'id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123'
        })

    def test_update_profile_success(self):
        user = self.profile_service.update_profile(user_id=1, username='newusername')
        self.assertEqual(user['username'], 'newusername')

    def test_update_profile_email_taken(self):
        self.user_repository.add_user({
            'id': 2,
            'username': 'anotheruser',
            'email': 'taken@example.com',
            'password': 'Password123'
        })
        with self.assertRaises(ValueError):
            self.profile_service.update_profile(user_id=1, email='taken@example.com')

    def test_get_profile(self):
        user = self.profile_service.get_profile(user_id=1)
        self.assertEqual(user['username'], 'testuser')

    def test_get_profile_not_found(self):
        user = self.profile_service.get_profile(user_id=999)
        self.assertIsNone(user)