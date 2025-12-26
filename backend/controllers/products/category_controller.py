from flask import Blueprint, request, jsonify
from services.products.category_service import CategoryService

category_controller = Blueprint('category_controller', __name__)
category_service = CategoryService()

@category_controller.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    response = category_service.add_category(data)
    return jsonify(response), response['status']

@category_controller.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id: int):
    data = request.get_json()
    response = category_service.update_category(category_id, data)
    return jsonify(response), response['status']

@category_controller.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id: int):
    response = category_service.delete_category(category_id)
    return jsonify(response), response['status']

@category_controller.route('/categories', methods=['GET'])
def get_all_categories():
    response = category_service.get_all_categories()
    return jsonify(response), response['status']