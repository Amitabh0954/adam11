from typing import Optional, List
from backend.models.shopping_cart import ShoppingCart, ShoppingCartItem
from backend.models.user import User

class ShoppingCartRepository:
    def __init__(self):
        self.carts = {}

    def add_item(self, user: User, item: ShoppingCartItem) -> None:
        if user['id'] not in self.carts:
            self.carts[user['id']] = {'user': user, 'items': []}
        self.carts[user['id']]['items'].append(item)

    def get_cart(self, user: User) -> Optional[ShoppingCart]:
        return self.carts.get(user['id'])

    def clear_cart(self, user: User) -> None:
        if user['id'] in self.carts:
            self.carts[user['id']]['items'] = []