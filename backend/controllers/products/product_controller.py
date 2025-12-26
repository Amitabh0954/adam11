from flask import Blueprint, request, jsonify
from services.products.product_service import ProductService

product_controller = Blueprint('product_controller', __name__)
product_service = ProductService()

@product_controller.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    response = product_service.add_product(data)
    return jsonify(response), response['status']