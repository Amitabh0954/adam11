from flask import Blueprint, request, jsonify
from backend.services.products.product_service import ProductService
from backend.repositories.product_repository import ProductRepository

product_bp = Blueprint('product', __name__)
product_service = ProductService(ProductRepository())

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
def get_product(product_id: int):
    product = product_service.get_product(product_id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Product not found"}), 404

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    data = request.get_json()
    is_admin = data.get('is_admin', False)
    try:
        product = product_service.update_product(
            product_id=product_id,
            name=data.get('name'),
            price=data.get('price'),
            description=data.get('description'),
            is_admin=is_admin
        )
        return jsonify(product), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    data = request.get_json()
    is_admin = data.get('is_admin', False)
    if not data.get('confirm', False):
        return jsonify({"error": "Deletion confirmation required"}), 400
    try:
        product_service.delete_product(product_id=product_id, is_admin=is_admin)
        return jsonify({"message": "Product deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400