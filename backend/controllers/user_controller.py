from flask import Blueprint, request, jsonify
from backend.services.user_service import UserService
from backend.repositories.user_repository import UserRepository
from backend.services.session_service import SessionService
from backend.repositories.session_repository import SessionRepository

user_bp = Blueprint('user', __name__)
user_service = UserService(UserRepository())
session_service = SessionService(SessionRepository())

@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    try:
        user = user_service.authenticate_user(
            email=data['email'],
            password=data['password']
        )
        session = session_service.create_session(user['id'])
        return jsonify({"token": session['token']}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400