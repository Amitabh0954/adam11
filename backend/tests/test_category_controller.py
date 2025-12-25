import unittest
from flask import Flask
from backend.controllers.products.category_controller import category_bp

class CategoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(category_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def test_add_category(self):
        response = self.client.post('/api/categories', json={'name': 'Electronics'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Electronics')

    def test_add_category_duplicate_name(self):
        self.client.post('/api/categories', json={'name': 'Electronics'})
        response = self.client.post('/api/categories', json={'name': 'Electronics'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Category name must be unique', response.json['error'])

    def test_add_category_with_parent(self):
        parent_response = self.client.post('/api/categories', json={'name': 'Electronics'})
        response = self.client.post('/api/categories', json={'name': 'Laptops', 'parent_id': parent_response.json['id']})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['parent_id'], parent_response.json['id'])

    def test_get_category(self):
        response = self.client.post('/api/categories', json={'name': 'Electronics'})
        category_id = response.json['id']
        response = self.client.get(f'/api/categories/{category_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Electronics')

    def test_get_category_not_found(self):
        response = self.client.get('/api/categories/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Category not found', response.json['error'])

    def test_update_category(self):
        response = self.client.post('/api/categories', json={'name': 'Electronics'})
        category_id = response.json['id']
        response = self.client.put(f'/api/categories/{category_id}', json={'name': 'Gadgets'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Gadgets')

    def test_update_category_invalid_parent(self):
        response = self.client.post('/api/categories', json={'name': 'Electronics'})
        category_id = response.json['id']
        response = self.client.put(f'/api/categories/{category_id}', json={'parent_id': 999})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Parent category not found', response.json['error'])

    def test_delete_category(self):
        response = self.client.post('/api/categories', json={'name': 'Electronics'})
        category_id = response.json['id']
        response = self.client.delete(f'/api/categories/{category_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Category deleted', response.json['message'])

    def test_list_categories(self):
        self.client.post('/api/categories', json={'name': 'Electronics'})
        self.client.post('/api/categories', json={'name': 'Laptops'})
        response = self.client.get('/api/categories')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)