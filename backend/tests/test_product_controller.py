import unittest
from flask import Flask
from backend.controllers.products.product_controller import product_bp

class ProductControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(product_bp, url_prefix='/catalog')
        self.client = self.app.test_client()

    def test_add_product_success(self):
        response = self.client.post('/catalog/products', json={
            'name': 'Product1',
            'price': 100.0,
            'description': 'Description1'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Product1')

    def test_add_product_duplicate_name(self):
        self.client.post('/catalog/products', json={
            'name': 'Product1',
            'price': 100.0,
            'description': 'Description1'
        })
        response = self.client.post('/catalog/products', json={
            'name': 'Product1',
            'price': 100.0,
            'description': 'Description2'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Product name must be unique', response.json['error'])

    def test_add_product_invalid_price(self):
        response = self.client.post('/catalog/products', json={
            'name': 'Product1',
            'price': -100.0,
            'description': 'Description1'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Product price must be a positive number', response.json['error'])

    def test_add_product_empty_description(self):
        response = self.client.post('/catalog/products', json={
            'name': 'Product1',
            'price': 100.0,
            'description': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Product description cannot be empty', response.json['error'])

    def test_get_product(self):
        self.client.post('/catalog/products', json={
            'name': 'Product1',
            'price': 100.0,
            'description': 'Description1'
        })
        response = self.client.get('/catalog/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Product1')

    def test_get_product_not_found(self):
        response = self.client.get('/catalog/products/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Product not found', response.json['error'])