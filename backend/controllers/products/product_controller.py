from flask import Blueprint, request, jsonify
from backend.services.products.product_service import ProductService
from backend.services.products.category_service import CategoryService
from backend.repositories.product_repository import ProductRepository
from backend.repositories.category_repository import CategoryRepository

product_bp = Blueprint('product', __name__)
product_service = ProductService(ProductRepository())
category_service = CategoryService(CategoryRepository())

@product_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    try:
        product = product_service.add_product(
            name=data['name'],
            price=data['price'],
            description=data['description']
        )
        return jsonify(product), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = product_service.get_product(product_id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Product not found"}), 404

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    try:
        product = product_service.update_product(
            product_id=product_id,
            name=data.get('name'),
            price=data.get('price'),
            description=data.get('description')
        )
        return jsonify(product), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    data = request.get_json()
    try:
        confirm = data.get('confirm')
        if not confirm:
            return jsonify({"error": "Delete confirmation required"}), 400
        product_service.delete_product(product_id=product_id)
        return jsonify({"message": "Product deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/categories', methods=['POST'])
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

@product_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = category_service.get_category(category_id)
    if category:
        return jsonify(category), 200
    else:
        return jsonify({"error": "Category not found"}), 404

@product_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category_service.remove_category(category_id)
        return jsonify({"message": "Category deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400