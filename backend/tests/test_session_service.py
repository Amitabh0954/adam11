import unittest
from backend.repositories.session_repository import SessionRepository
from backend.services.session_service import SessionService
from datetime import datetime, timedelta

class SessionServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.session_repository = SessionRepository()
        self.session_service = SessionService(self.session_repository)

    def test_create_session(self):
        session = self.session_service.create_session(user_id=1)
        self.assertIn('token', session)
        self.assertEqual(session['user_id'], 1)

    def test_validate_session(self):
        session = self.session_service.create_session(user_id=1)
        is_valid = self.session_service.validate_session(session['token'])
        self.assertTrue(is_valid)

    def test_validate_expired_session(self):
        session = self.session_service.create_session(user_id=1)
        session['expiry'] = datetime.utcnow() - timedelta(hours=1)  # Force expiry
        self.session_repository.add_session(session)
        is_valid = self.session_service.validate_session(session['token'])
        self.assertFalse(is_valid)

    def test_invalidate_session(self):
        session = self.session_service.create_session(user_id=1)
        self.session_service.invalidate_session(session['token'])
        is_valid = self.session_service.validate_session(session['token'])
        self.assertFalse(is_valid)