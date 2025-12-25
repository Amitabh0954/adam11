from flask import Blueprint, request, jsonify
from backend.services.carts.cart_service import CartService
from backend.repositories.shopping_cart_repository import ShoppingCartRepository
from backend.models.user import User

cart_bp = Blueprint('cart', __name__)
cart_service = CartService(ShoppingCartRepository())

@cart_bp.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    try:
        user = User(id=data['user_id'], username=data['username'], email=data['email'])
        product = {'product': data['product'], 'quantity': data['quantity']}
        cart_service.add_product_to_cart(user, product)
        return jsonify({"message": "Product added to cart"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@cart_bp.route('/cart', methods=['GET'])
def view_cart():
    user_id = request.args.get('user_id', type=int)
    username = request.args.get('username')
    email = request.args.get('email')
    
    user = User(id=user_id, username=username, email=email)
    cart = cart_service.view_cart(user)
    if cart:
        return jsonify(cart), 200
    else:
        return jsonify({"error": "Cart not found"}), 404

@cart_bp.route('/cart/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    try:
        user = User(id=data['user_id'], username=data['username'], email=data['email'])
        cart_service.checkout(user)
        return jsonify({"message": "Checkout successful"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400