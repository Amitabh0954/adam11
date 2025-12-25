from flask import Blueprint, request, jsonify
from backend.services.users.profile_service import ProfileService
from backend.repositories.user_repository import UserRepository

profile_bp = Blueprint('profile', __name__)
profile_service = ProfileService(UserRepository())

@profile_bp.route('/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id')
    if user_id is not None:
        user_id = int(user_id)
    user = profile_service.get_profile(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@profile_bp.route('/profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    try:
        user = profile_service.update_profile(
            user_id=data['user_id'],
            email=data['email'],
            password=data['password']
        )
        return jsonify(user), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400