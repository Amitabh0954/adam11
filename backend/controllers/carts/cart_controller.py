from flask import Blueprint, request, jsonify
from services.carts.cart_service import CartService

cart_controller = Blueprint('cart_controller', __name__)
cart_service = CartService()

@cart_controller.route('/carts', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    response = cart_service.add_to_cart(data)
    return jsonify(response), response['status']

@cart_controller.route('/carts/<int:cart_id>', methods=['GET'])
def get_cart(cart_id: int):
    response = cart_service.get_cart(cart_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts/<int:cart_id>', methods=['DELETE'])
def clear_cart(cart_id: int):
    response = cart_service.clear_cart(cart_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts/<int:cart_id>/items/<int:product_id>', methods=['DELETE'])
def remove_from_cart(cart_id: int, product_id: int):
    response = cart_service.remove_from_cart(cart_id, product_id)
    return jsonify(response), response['status']