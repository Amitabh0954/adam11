from typing import Optional
from backend.models.shopping_cart import ShoppingCart

class ShoppingCartRepository:
    def __init__(self):
        self.carts = {}
        self.user_carts = {}

    def create_cart(self, user_id: int) -> ShoppingCart:
        cart = ShoppingCart(id=len(self.carts) + 1, user_id=user_id, items=[])
        self.carts[cart['id']] = cart
        self.user_carts[user_id] = cart
        return cart

    def get_cart_by_id(self, cart_id: int) -> Optional<ShoppingCart]:
        return self.carts.get(cart_id)

    def get_cart_by_user_id(self, user_id: int) -> Optional<ShoppingCart]:
        return self.user_carts.get(user_id)

    def update_cart(self, cart: ShoppingCart) -> None:
        self.carts[cart['id']] = cart
        self.user_carts[cart['user_id']] = cart

    def delete_cart(self, cart_id: int) -> None:
        cart = self.carts.pop(cart_id, None)
        if cart:
            self.user_carts.pop(cart['user_id'], None)