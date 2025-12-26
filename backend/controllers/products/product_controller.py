from flask import Blueprint, request, jsonify
from services.products.product_service import ProductService

product_controller = Blueprint('product_controller', __name__)
product_service = ProductService()

@product_controller.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    response = product_service.add_product(data)
    return jsonify(response), response['status']

@product_controller.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    data = request.get_json()
    response = product_service.update_product(product_id, data)
    return jsonify(response), response['status']

@product_controller.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    response = product_service.delete_product(product_id)
    return jsonify(response), response['status']

@product_controller.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '')
    category = request.args.get('category')
    attributes = request.args.getlist('attributes')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    response = product_service.search_products(query, category, attributes, page, per_page)
    return jsonify(response), response['status']