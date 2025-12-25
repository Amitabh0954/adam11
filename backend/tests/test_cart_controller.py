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
        self.assertEqual(response.json['cart']['user_id'], 1)

    def test_add_item_to_cart(self):
        response = self.client.post('/api/cart/items', json={
            'user_id': 1,
            'product_id': 1,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['cart']['items']), 1)
        self.assertEqual(response.json['cart']['items'][0]['product_id'], 1)

    def test_remove_item_from_cart(self):
        self.client.post('/api/cart/items', json={'user_id': 1, 'product_id': 1, 'quantity': 2})
        response = self.client.delete('/api/cart/items/1', query_string={'user_id': 1, 'confirm': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['cart']['items']), 0)

    def test_remove_item_from_cart_without_confirmation(self):
        self.client.post('/api/cart/items', json={'user_id': 1, 'product_id': 1, 'quantity': 2})
        response = self.client.delete('/api/cart/items/1', query_string={'user_id': 1, 'confirm': False})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Confirmation required to remove item', response.json['error'])

    def test_clear_cart(self):
        self.client.post('/api/cart/items', json={'user_id': 1, 'product_id': 1, 'quantity': 2})
        response = self.client.post('/api/cart/clear', json={'user_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Cart cleared', response.json['message'])