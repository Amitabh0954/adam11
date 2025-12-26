from models.cart_item import CartItem

class CartRepository:
    def __init__(self):
        self.cart_items = []
    
    def find_by_user_id(self, user_id: int) -> list[CartItem]:
        return [item for item in self.cart_items if item.user_id == user_id]
    
    def find_by_id(self, item_id: int) -> CartItem:
        return next((item for item in self.cart_items if item.id == item_id), None)
    
    def save(self, cart_item: CartItem) -> None:
        self.cart_items.append(cart_item)
    
    def update(self, cart_item: CartItem) -> None:
        index = next((i, item for i, item in enumerate(self.cart_items) if item.id == cart_item.id), None)
        if index is not None:
            self.cart_items[index] = cart_item
    
    def delete(self, cart_item: CartItem) -> None:
        self.cart_items.remove(cart_item)