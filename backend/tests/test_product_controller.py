import unittest
from flask import Flask
from backend.controllers.products.product_controller import product_bp

class ProductControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(product_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_add_product(self):
        response = self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Test Product')

    def test_add_product_duplicate_name(self):
        self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        response = self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 200.0,
            'description': 'Another Description'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Product name must be unique', response.json['error'])

    def test_add_product_invalid_price(self):
        response = self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': -50,
            'description': 'Test Description'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Product price must be a positive number', response.json['error'])

    def test_get_product(self):
        self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        response = self.client.get('/api/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Product')

    def test_get_product_not_found(self):
        response = self.client.get('/api/products/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Product not found', response.json['error'])

    def test_update_product(self):
        self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        response = self.client.put('/api/products/1', json={
            'name': 'Updated Product',
            'price': 150.0,
            'description': 'Updated Description',
            'is_admin': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Product')

    def test_update_product_non_admin(self):
        self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        response = self.client.put('/api/products/1', json={
            'name': 'Updated Product',
            'is_admin': False
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Only admin can update product details', response.json['error'])

    def test_update_product_invalid_price(self):
        self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        response = self.client.put('/api/products/1', json={
            'price': 'invalid',
            'is_admin': True
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Price must be a numeric value', response.json['error'])

    def test_delete_product(self):
        self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        response = self.client.delete('/api/products/1', json={
            'is_admin': True,
            'confirm': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Product deleted', response.json['message'])

    def test_delete_product_non_admin(self):
        self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        response = self.client.delete('/api/products/1', json={
            'is_admin': False,
            'confirm': True
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Only admin can delete products', response.json['error'])

    def test_delete_product_no_confirmation(self):
        self.client.post('/api/products', json={
            'name': 'Test Product',
            'price': 100.0,
            'description': 'Test Description'
        })
        response = self.client.delete('/api/products/1', json={
            'is_admin': True,
            'confirm': False
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Deletion confirmation required', response.json['error'])