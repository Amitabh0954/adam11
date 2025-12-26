from flask import Blueprint, request, jsonify
from services.carts.cart_service import CartService

cart_controller = Blueprint('cart_controller', __name__)
cart_service = CartService()

@cart_controller.route('/carts', methods=['POST'])
def add_product_to_cart():
    data = request.get_json()
    user_id = request.headers.get('User-ID')
    response = cart_service.add_product_to_cart(data, user_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts/<int:item_id>', methods=['DELETE'])
def remove_product_from_cart(item_id: int):
    confirm = request.args.get('confirm', False, type=bool)
    user_id = request.headers.get('User-ID')
    response = cart_service.remove_product_from_cart(item_id, confirm, user_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts', methods=['GET'])
def get_cart_items():
    user_id = request.headers.get('User-ID')
    response = cart_service.get_cart_items(user_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts/save', methods=['POST'])
def save_cart():
    user_id = request.headers.get('User-ID')
    response = cart_service.save_cart(user_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts/retrieve', methods=['GET'])
def retrieve_cart():
    user_id = request.headers.get('User-ID')
    response = cart_service.retrieve_cart(user_id)
    return jsonify(response), response['status']

@cart_controller.route('/carts/<int:item_id>', methods=['PUT'])
def update_cart_item_quantity(item_id: int):
    data = request.get_json()
    user_id = request.headers.get('User-ID')
    response = cart_service.update_cart_item_quantity(item_id, data, user_id)
    return jsonify(response), response['status']