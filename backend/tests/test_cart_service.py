import unittest
from backend.repositories.shopping_cart_repository import ShoppingCartRepository
from backend.services.carts.cart_service import CartService
from backend.models.user import User
from backend.models.product import Product
from backend.models.shopping_cart import ShoppingCartItem

class CartServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.cart_repository = ShoppingCartRepository()
        self.cart_service = CartService(self.cart_repository)
        self.user = User(id=1, username='testuser', email='test@example.com')
        self.product = Product(id=1, name='Product1', price=100.0, description='Description1')

    def test_add_product_to_cart(self):
        cart_item = ShoppingCartItem(product=self.product, quantity=1)
        self.cart_service.add_product_to_cart(self.user, cart_item)
        cart = self.cart_service.view_cart(self.user)
        self.assertEqual(len(cart['items']), 1)

    def test_view_cart(self):
        cart_item = ShoppingCartItem(product=self.product, quantity=1)
        self.cart_service.add_product_to_cart(self.user, cart_item)
        cart = self.cart_service.view_cart(self.user)
        self.assertEqual(cart['user']['username'], 'testuser')

    def test_checkout(self):
        cart_item = ShoppingCartItem(product=self.product, quantity=1)
        self.cart_service.add_product_to_cart(self.user, cart_item)
        self.cart_service.checkout(self.user)
        cart = self.cart_service.view_cart(self.user)
        self.assertEqual(len(cart['items']), 0)

    def test_remove_product_from_cart(self):
        cart_item = ShoppingCartItem(product=self.product, quantity=1)
        self.cart_service.add_product_to_cart(self.user, cart_item)
        self.cart_service.remove_product_from_cart(self.user, self.product['id'], confirm=True)
        cart = self.cart_service.view_cart(self.user)
        self.assertEqual(len(cart['items']), 0)
        self.assertEqual(cart['total_price'], 0.0)

    def test_remove_product_without_confirmation(self):
        cart_item = ShoppingCartItem(product=self.product, quantity=1)
        self.cart_service.add_product_to_cart(self.user, cart_item)
        with self.assertRaises(ValueError):
            self.cart_service.remove_product_from_cart(self.user, self.product['id'], confirm=False)

    def test_update_quantity(self):
        cart_item = ShoppingCartItem(product=self.product, quantity=1)
        self.cart_service.add_product_to_cart(self.user, cart_item)
        self.cart_service.update_quantity(self.user, self.product['id'], quantity=5)
        cart = self.cart_service.view_cart(self.user)
        self.assertEqual(cart['items'][0]['quantity'], 5)
        self.assertEqual(cart['total_price'], 500.0)

    def test_update_quantity_invalid(self):
        cart_item = ShoppingCartItem(product=self.product, quantity=1)
        self.cart_service.add_product_to_cart(self.user, cart_item)
        with self.assertRaises(ValueError):
            self.cart_service.update_quantity(self.user, self.product['id'], quantity=-1)