from flask import Blueprint, request, jsonify
from backend.services.carts.cart_service import CartService
from backend.repositories.shopping_cart_repository import ShoppingCartRepository

cart_bp = Blueprint('cart', __name__)
cart_service = CartService(ShoppingCartRepository())

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400
    
    cart = cart_service.get_or_create_cart(user_id)
    return jsonify(cart), 200

@cart_bp.route('/cart/items', methods=['POST'])
def add_item_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if user_id is None or product_id is None:
        return jsonify({"error": "User ID and Product ID are required"}), 400
    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 400

    cart = cart_service.add_item_to_cart(user_id, product_id, quantity)
    return jsonify(cart), 200

@cart_bp.route('/cart/items/<int:product_id>', methods=['DELETE'])
def remove_item_from_cart(product_id: int):
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400

    cart = cart_service.remove_item_from_cart(user_id, product_id)
    return jsonify(cart), 200

@cart_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    user_id = request.get_json().get('user_id')
    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400

    cart_service.clear_cart(user_id)
    return jsonify({"message": "Cart cleared"}), 200