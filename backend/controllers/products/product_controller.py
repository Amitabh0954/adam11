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