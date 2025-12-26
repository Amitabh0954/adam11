from flask import Blueprint, request, jsonify
from services.products.product_service import ProductService
from services.products.category_service import CategoryService

product_controller = Blueprint('product_controller', __name__)
product_service = ProductService()
category_service = CategoryService()

@product_controller.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    response = product_service.add_product(data)
    return jsonify(response), response['status']

@product_controller.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    data = request.get_json()
    response = product_service.update_product(product_id, data, request.headers.get('Authorization'))
    return jsonify(response), response['status']

@product_controller.route('/products/<int:product_id>', methods['DELETE'])
def delete_product(product_id: int):
    confirm = request.args.get('confirm', False, type=bool)
    response = product_service.delete_product(product_id, confirm, request.headers.get('Authorization'))
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

@product_controller.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    response = category_service.add_category(data)
    return jsonify(response), response['status']

@product_controller.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id: int):
    data = request.get_json()
    response = category_service.update_category(category_id, data)
    return jsonify(response), response['status']

@product_controller.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id: int):
    response = category_service.delete_category(category_id)
    return jsonify(response), response['status']