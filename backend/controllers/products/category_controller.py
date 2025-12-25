from flask import Blueprint, request, jsonify
from backend.services.products.category_service import CategoryService
from backend.repositories.category_repository import CategoryRepository

category_bp = Blueprint('category', __name__)
category_service = CategoryService(CategoryRepository())

@category_bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    try:
        category = category_service.add_category(
            name=data['name'],
            parent_id=data.get('parent_id')
        )
        return jsonify(category), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id: int):
    category = category_service.get_category(category_id)
    if category:
        return jsonify(category), 200
    else:
        return jsonify({"error": "Category not found"}), 404

@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id: int):
    data = request.get_json()
    try:
        category = category_service.update_category(
            category_id=category_id,
            name=data.get('name'),
            parent_id=data.get('parent_id')
        )
        return jsonify(category), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id: int):
    try:
        category_service.delete_category(category_id)
        return jsonify({"message": "Category deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@category_bp.route('/categories', methods=['GET'])
def list_categories():
    categories = category_service.list_categories()
    return jsonify(categories), 200