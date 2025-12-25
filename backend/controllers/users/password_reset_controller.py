from flask import Blueprint, request, jsonify
from backend.services.users.password_reset_service import PasswordResetService
from backend.repositories.user_repository import UserRepository
from backend.repositories.password_reset_repository import PasswordResetRepository

password_reset_bp = Blueprint('password_reset', __name__)
password_reset_service = PasswordResetService(UserRepository(), PasswordResetRepository())

@password_reset_bp.route('/password-reset', methods=['POST'])
def initiate_password_reset():
    data = request.get_json()
    try:
        password_reset_service.initiate_password_reset(email=data['email'])
        return jsonify({"message": "Password reset email sent"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@password_reset_bp.route('/password-reset/<token>', methods=['POST'])
def reset_password(token: str):
    data = request.get_json()
    try:
        password_reset_service.reset_password(token=token, new_password=data['new_password'])
        return jsonify({"message": "Password has been reset"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400