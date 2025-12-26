from flask import Blueprint, request, jsonify
from services.carts.cart_service import CartService

cart_controller = Blueprint('cart_controller', __name__)
cart_service = CartService()

@cart_controller.route('/carts', methods=['POST'])
def add_product_to_cart():
    data = request.get_json()
    response = cart_service.add_product_to_cart(data)
    return jsonify(response), response['status']

@cart_controller.route('/carts/<int:item_id>', methods=['DELETE'])
def remove_product_from_cart(item_id: int):
    response = cart_service.remove_product_from_cart(item_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts', methods=['GET'])
def get_cart_items():
    response = cart_service.get_cart_items()
    return jsonify(response), response['status']