from repositories.cart_repository import CartRepository
from models.cart import Cart
from models.cart_item import CartItem

class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()
    
    def add_to_cart(self, data: dict):
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        if not user_id or not product_id:
            return {"message": "User ID and Product ID are required", "status": 400}
        
        if quantity <= 0:
            return {"message": "Quantity must be a positive integer", "status": 400}

        cart = self.cart_repository.find_or_create_by_user_id(user_id)
        if not cart:
            cart = Cart(user_id=user_id)
            self.cart_repository.save(cart)
        
        cart_item = CartItem(product_id=product_id, quantity=quantity)
        cart.items.append(cart_item)
        self.cart_repository.update(cart)
        
        return {"message": "Product added to cart successfully", "status": 201}
    
    def get_cart(self, cart_id: int):
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            return {"message": "Cart not found", "status": 404}
        
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in cart.items],
            "status": 200
        }
    
    def clear_cart(self, cart_id: int):
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            return {"message": "Cart not found", "status": 404}
        
        cart.items = []
        self.cart_repository.update(cart)
        return {"message": "Cart cleared successfully", "status": 200}
    
    def remove_from_cart(self, cart_id: int, product_id: int):
        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            return {"message": "Cart not found", "status": 404}
        
        cart.items = [item for item in cart.items if item.product_id != product_id]
        self.cart_repository.update(cart)
        return {"message": "Product removed from cart successfully", "status": 200}

    def update_cart_quantity(self, cart_id: int, product_id: int, quantity: int):
        if quantity <= 0:
            return {"message": "Quantity must be a positive integer", "status": 400}

        cart = self.cart_repository.find_by_id(cart_id)
        if not cart:
            return {"message": "Cart not found", "status": 404}

        for item in cart.items:
            if item.product_id == product_id:
                item.quantity = quantity
                break
        else:
            return {"message": "Product not found in cart", "status": 404}

        self.cart_repository.update(cart)
        return {"message": "Product quantity updated successfully", "status": 200}