import unittest
from flask import Flask
from backend.controllers.products.search_controller import search_bp

class SearchControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(search_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_search_products(self):
        response = self.client.get('/api/search', query_string={'query': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    def test_search_products_no_query(self):
        response = self.client.get('/api/search')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Query parameter is required', response.json['error'])

    def test_search_products_pagination(self):
        response = self.client.get('/api/search', query_string={'query': 'Product', 'page': 1, 'page_size': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        response = self.client.get('/api/search', query_string={'query': 'Product', 'page': 2, 'page_size': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)