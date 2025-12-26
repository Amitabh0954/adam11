from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from models.cart_item import CartItem

class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()
        self.product_repository = ProductRepository()
    
    def add_product_to_cart(self, data: dict):
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        if user_id is None or product_id is None or quantity is None: