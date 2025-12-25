from typing import Optional
from backend.models.user import User
from backend.models.shopping_cart import ShoppingCart, ShoppingCartItem
from backend.repositories.shopping_cart_repository import ShoppingCartRepository

class CartService:
    def __init__(self, cart_repository: ShoppingCartRepository):
        self.cart_repository = cart_repository

    def add_product_to_cart(self, user: User, product: ShoppingCartItem) -> None:
        self.cart_repository.add_item(user, product)

    def view_cart(self, user: User) -> Optional[ShoppingCart]:
        return self.cart_repository.get_cart(user)

    def checkout(self, user: User) -> None:
        self.cart_repository.clear_cart(user)