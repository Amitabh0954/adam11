from models.cart import Cart

class CartRepository:
    def __init__(self):
        self.carts = []
    
    def find_or_create_by_user_id(self, user_id: int) -> Cart:
        cart = next((cart for cart in self.carts if cart.user_id == user_id), None)
        if not cart:
            cart = Cart(user_id=user_id)
            self.carts.append(cart)
        return cart
    
    def find_by_id(self, cart_id: int) -> Cart:
        return next((cart for cart in self.carts if cart.id == cart_id), None)
    
    def save(self, cart: Cart) -> None:
        self.carts.append(cart)
    
    def update(self, cart: Cart) -> None:
        index = next((i for i, c in enumerate(self.carts) if c.id == cart.id), None)
        if index is not None:
            self.carts[index] = cart