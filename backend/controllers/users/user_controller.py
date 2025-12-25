from flask import Blueprint, request, jsonify
from backend.services.users.user_service import UserService
from backend.repositories.user_repository import UserRepository

user_bp = Blueprint('user', __name__)
user_service = UserService(UserRepository())

@user_bp.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        user = user_service.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404