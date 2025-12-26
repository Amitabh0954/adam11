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
    confirm = request.args.get('confirm', False, type=bool)
    response = cart_service.remove_product_from_cart(item_id, confirm)
    return jsonify(response), response['status']

@cart_controller.route('/carts', methods=['GET'])
def get_cart_items():
    user_id = request.args.get('user_id')
    response = cart_service.get_cart_items(user_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts/<int:item_id>', methods=['PUT'])
def update_cart_item_quantity(item_id: int):
    data = request.get_json()
    response = cart_service.update_cart_item_quantity(item_id, data)
    return jsonify(response), response['status']