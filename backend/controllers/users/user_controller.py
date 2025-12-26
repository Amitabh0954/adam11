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