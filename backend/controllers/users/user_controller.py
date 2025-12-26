from flask import Blueprint, request, jsonify
from services.users.user_service import UserService

user_controller = Blueprint('user_controller', __name__)
user_service = UserService()

@user_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = user_service.register_user(data)
    return jsonify(response), response['status']

@user_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = user_service.login_user(data)
    return jsonify(response), response['status']

@user_controller.route('/password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    response = user_service.request_password_reset(data)
    return jsonify(response), response['status']

@user_controller.route('/password-reset/<token>', methods=['POST'])
def reset_password(token: str):
    data = request.get_json()
    response = user_service.reset_password(data, token)
    return jsonify(response), response['status']