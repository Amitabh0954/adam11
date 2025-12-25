import unittest
from flask import Flask
from backend.controllers.carts.cart_controller import cart_bp

class CartControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(cart_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_add_to_cart(self):
        response = self.client.post('/api/cart', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product': {'id': 1, 'name': 'Product1', 'price': 100.0, 'description': 'Description1'},
            'quantity': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Product added to cart', response.json['message'])

    def test_view_cart(self):
        self.client.post('/api/cart', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product': {'id': 1, 'name': 'Product1', 'price': 100.0, 'description': 'Description1'},
            'quantity': 1
        })
        response = self.client.get('/api/cart', query_string={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.json)

    def test_checkout(self):
        self.client.post('/api/cart', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product': {'id': 1, 'name': 'Product1', 'price': 100.0, 'description': 'Description1'},
            'quantity': 1
        })
        response = self.client.post('/api/cart/checkout', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Checkout successful', response.json['message'])

    def test_remove_from_cart(self):
        self.client.post('/api/cart', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product': {'id': 1, 'name': 'Product1', 'price': 100.0, 'description': 'Description1'},
            'quantity': 1
        })
        response = self.client.post('/api/cart/remove', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product_id': 1,
            'confirm': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Product removed from cart', response.json['message'])

    def test_remove_from_cart_without_confirmation(self):
        self.client.post('/api/cart', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product': {'id': 1, 'name': 'Product1', 'price': 100.0, 'description': 'Description1'},
            'quantity': 1
        })
        response = self.client.post('/api/cart/remove', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product_id': 1,
            'confirm': False
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Remove confirmation required', response.json['error'])

    def test_update_quantity(self):
        self.client.post('/api/cart', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product': {'id': 1, 'name': 'Product1', 'price': 100.0, 'description': 'Description1'},
            'quantity': 1
        })
        response = self.client.post('/api/cart/quantity', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product_id': 1,
            'quantity': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Quantity updated', response.json['message'])

    def test_update_quantity_invalid(self):
        self.client.post('/api/cart', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product': {'id': 1, 'name': 'Product1', 'price': 100.0, 'description': 'Description1'},
            'quantity': 1
        })
        response = self.client.post('/api/cart/quantity', json={
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'product_id': 1,
            'quantity': -1
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Quantity must be a positive integer', response.json['error'])