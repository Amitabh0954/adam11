from flask import Blueprint, request, jsonify
from backend.services.password_reset_service import PasswordResetService
from backend.repositories.password_reset_repository import PasswordResetRepository
from backend.repositories.user_repository import UserRepository

password_reset_bp = Blueprint('password_reset', __name__)
password_reset_service = PasswordResetService(PasswordResetRepository(), UserRepository())

@password_reset_bp.route('/password_reset/request', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    try:
        password_reset = password_reset_service.create_password_reset(email=data['email'])
        # Assume sending email to user with password_reset['token']
        return jsonify({"message": "Password reset link sent to your email"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@password_reset_bp.route('/password_reset/reset', methods=['POST'])
def reset_password():
    data = request.get_json()
    try:
        password_reset_service.use_password_reset(
            token=data['token'],
            new_password=data['new_password']
        )
        return jsonify({"message": "Password has been reset successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400