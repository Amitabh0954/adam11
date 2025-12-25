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
        self.carts[user['id']]['total_price'] += item['product']['price'] * item['quantity']

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
                    self.carts[user['id']]['total_price'] -= item['product']['price'] * item['quantity']
                    items.remove(item)
                    break