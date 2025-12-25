import unittest
from backend.repositories.shopping_cart_repository import ShoppingCartRepository
from backend.repositories.product_repository import ProductRepository
from backend.services.carts.cart_service import CartService

class CartServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.cart_repository = ShoppingCartRepository()
        self.product_repository = ProductRepository()
        self.product_repository.add_product({'id': 1, 'name': 'Test Product', 'price': 100.0, 'description': 'Test Description'})
        self.cart_service = CartService(self.cart_repository)
        self.cart_service.product_repository = self.product_repository
        self.user_id = 1

    def test_get_or_create_cart(self):
        cart = self.cart_service.get_or_create_cart(self.user_id)
        self.assertIsNotNone(cart)
        self.assertEqual(cart['user_id'], self.user_id)

    def test_add_item_to_cart(self):
        cart = self.cart_service.add_item_to_cart(self.user_id, product_id=1, quantity=2)
        self.assertEqual(len(cart['items']), 1)
        self.assertEqual(cart['items'][0]['product_id'], 1)
        self.assertEqual(cart['items'][0]['quantity'], 2)

    def test_remove_item_from_cart(self):
        self.cart_service.add_item_to_cart(self.user_id, product_id=1, quantity=2)
        cart = self.cart_service.remove_item_from_cart(self.user_id, product_id=1)
        self.assertEqual(len(cart['items']), 0)

    def test_clear_cart(self):
        self.cart_service.add_item_to_cart(self.user_id, product_id=1, quantity=2)
        self.cart_service.clear_cart(self.user_id)
        cart = self.cart_service.get_or_create_cart(self.user_id)
        self.assertEqual(len(cart['items']), 0)

    def test_delete_cart(self):
        cart = self.cart_service.get_or_create_cart(self.user_id)
        self.cart_service.delete_cart(self.user_id)
        cart = self.cart_service.get_or_create_cart(self.user_id)
        self.assertEqual(len(cart['items']), 0)

    def test_get_cart_total_price(self):
        self.cart_service.add_item_to_cart(self.user_id, product_id=1, quantity=2)
        cart = self.cart_service.get_or_create_cart(self.user_id)
        total_price = self.cart_service.get_cart_total_price(cart)
        self.assertEqual(total_price, 200.0)