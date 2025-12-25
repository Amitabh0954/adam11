from typing import Optional
from backend.models.shopping_cart import ShoppingCart, CartItem
from backend.repositories.shopping_cart_repository import ShoppingCartRepository

class CartService:
    def __init__(self, cart_repository: ShoppingCartRepository):
        self.cart_repository = cart_repository

    def get_or_create_cart(self, user_id: int) -> ShoppingCart:
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            cart = self.cart_repository.create_cart(user_id)
        return cart

    def add_item_to_cart(self, user_id: int, product_id: int, quantity: int) -> ShoppingCart:
        cart = self.get_or_create_cart(user_id)
        for item in cart['items']:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                break
        else:
            cart['items'].append(CartItem(product_id=product_id, quantity=quantity))
        self.cart_repository.update_cart(cart)
        return cart

    def remove_item_from_cart(self, user_id: int, product_id: int) -> ShoppingCart:
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")

        cart['items'] = [item for item in cart['items'] if item['product_id'] != product_id]
        self.cart_repository.update_cart(cart)
        return cart

    def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> ShoppingCart:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")

        item_found = False
        for item in cart['items']:
            if item['product_id'] == product_id:
                item['quantity'] = quantity
                item_found = True
                break

        if not item_found:
            raise ValueError("Product not found in cart")

        self.cart_repository.update_cart(cart)
        return cart

    def clear_cart(self, user_id: int) -> None:
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if cart:
            cart['items'] = []
            self.cart_repository.update_cart(cart)

    def delete_cart(self, user_id: int) -> None:
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if cart:
            self.cart_repository.delete_cart(cart['id'])

    def get_cart_total_price(self, cart: ShoppingCart) -> float:
        # Implementation details left abstracted
        return sum(item['quantity'] * self.product_repository.get_product_by_id(item['product_id'])['price'] for item in cart['items'])

    def save_cart_state(self, user_id: int) -> None:
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")
        # Persist cart state (implementation abstracted)

    def load_cart_state(self, user_id: int) -> ShoppingCart:
        # Load cart state (implementation abstracted)
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            cart = self.cart_repository.create_cart(user_id)
        return cart