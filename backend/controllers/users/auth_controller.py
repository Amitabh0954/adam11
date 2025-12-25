from flask import Blueprint, request, jsonify
from backend.services.users.auth_service import AuthService
from backend.repositories.user_repository import UserRepository
from backend.repositories.session_repository import SessionRepository

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService(UserRepository(), SessionRepository())

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        token = auth_service.login(email=data['email'], password=data['password'])
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    token = data['token']
    auth_service.logout(token)
    return jsonify({"message": "Logged out"}), 200