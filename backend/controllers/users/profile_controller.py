from flask import Blueprint, request, jsonify
from backend.services.users.profile_service import ProfileService
from backend.repositories.user_repository import UserRepository

profile_bp = Blueprint('profile', __name__)
profile_service = ProfileService(UserRepository())

@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        user = profile_service.get_profile(user_id)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@profile_bp.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    try:
        user = profile_service.update_profile(
            user_id=user_id,
            username=data.get('username'),
            email=data.get('email')
        )
        return jsonify(user), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400