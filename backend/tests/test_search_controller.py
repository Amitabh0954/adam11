import unittest
from flask import Flask
from backend.controllers.products.search_controller import search_bp

class SearchControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(search_bp, url_prefix='/catalog')
        self.client = self.app.test_client()

    def test_search_products_success(self):
        # Add products directly to the repository for test setup
        self.client.post('/catalog/products', json={
            'name': 'Product1',
            'price': 100.0,
            'description': 'Description1'
        })
        self.client.post('/catalog/products', json={
            'name': 'Product2',
            'price': 200.0,
            'description': 'Description2'
        })

        response = self.client.get('/catalog/search/products?query=Product')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 2)

    def test_search_products_no_query(self):
        response = self.client.get('/catalog/search/products')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Search query required', response.json['error'])

    def test_search_products_pagination(self):
        for i in range(1, 21):
            self.client.post('/catalog/products', json={
                'name': f'Product{i}',
                'price': 100.0 * i,
                'description': f'Description{i}'
            })

        response = self.client.get('/catalog/search/products?query=Product&page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 10)
        self.assertEqual(response.json['page'], 2)