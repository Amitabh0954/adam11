import unittest
from flask import Flask
from backend.controllers.carts.cart_controller import cart_bp

class CartControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(cart_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_get_cart(self):
        response = self.client.get('/api/cart', query_string={'user_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user_id'], 1)

    def test_add_item_to_cart(self):
        response = self.client.post('/api/cart/items', json={
            'user_id': 1,
            'product_id': 1,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['items']), 1)
        self.assertEqual(response.json['items'][0]['product_id'], 1)

    def test_remove_item_from_cart(self):
        self.client.post('/api/cart/items', json={'user_id': 1, 'product_id': 1, 'quantity': 2})
        response = self.client.delete('/api/cart/items/1', query_string={'user_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['items']), 0)

    def test_clear_cart(self):
        self.client.post('/api/cart/items', json={'user_id': 1, 'product_id': 1, 'quantity': 2})
        response = self.client.post('/api/cart/clear', json={'user_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Cart cleared', response.json['message'])