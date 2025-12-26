from repositories.cart_repository import CartRepository
from models.cart_item import CartItem

class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()
    
    def add_product_to_cart(self, data: dict):
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        if user_id is None or product_id is None or quantity is None:
            return {"message": "User ID, Product ID, and Quantity are required", "status": 400}
        
        cart_item = CartItem(user_id=user