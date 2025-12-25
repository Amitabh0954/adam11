from typing import Optional
from backend.models.shopping_cart import ShoppingCart, ShoppingCartItem
from backend.models.user import User

class ShoppingCartRepository:
    def __init__(self):
        self.carts = {}

    def add_item(self, user: User, item: ShoppingCartItem) -> None:
        if user['id'] not in self.carts:
            self.carts[user['id']] = {'user': user, 'items': [], 'total_price': 0.0}
        self.carts[user['id']]['items'].append(item)
        self._recalculate_total_price(user['id'])

    def get_cart(self, user: User) -> Optional[ShoppingCart]:
        return self.carts.get(user['id'])

    def clear_cart(self, user: User) -> None:
        if user['id'] in self.carts:
            self.carts[user['id']]['items'] = []
            self.carts[user['id']]['total_price'] = 0.0

    def remove_item(self, user: User, product_id: int, confirm: bool) -> None:
        if not confirm:
            raise ValueError("Remove confirmation required")
        if user['id'] in self.carts:
            items = self.carts[user['id']]['items']
            for item in items:
                if item['product']['id'] == product_id:
                    items.remove(item)
                    break
            self._recalculate_total_price(user['id'])

    def update_quantity(self, user: User, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        if user['id'] in self.carts:
            items = self.carts[user['id']]['items']
            for item in items:
                if item['product']['id'] == product_id:
                    item['quantity'] = quantity
                    break
            self._recalculate_total_price(user['id'])

    def _recalculate_total_price(self, user_id: int) -> None:
        total_price = 0.0
        for item in self.carts[user_id]['items']:
            total_price += item['product']['price'] * item['quantity']
        self.carts[user_id]['total_price'] = total_price

    def save_cart(self, user: User) -> None:
        # Assume `save_cart_to_db` is a function that saves the cart to the database
        cart = self.get_cart(user)
        if cart:
            save_cart_to_db(cart)

    def load_cart(self, user: User) -> None:
        # Assume `load_cart_from_db` is a function that loads the cart from the database
        cart = load_cart_from_db(user['id'])
        if cart:
            self.carts[user['id']] = cart