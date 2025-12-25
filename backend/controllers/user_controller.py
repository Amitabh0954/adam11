from flask import Blueprint, request, jsonify
from backend.services.user_service import UserService
from backend.repositories.user_repository import UserRepository

user_bp = Blueprint('user', __name__)
user_service = UserService(UserRepository())

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        user = user_service.register_user(
            email=data['email'],
            password=data['password']
        )
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400