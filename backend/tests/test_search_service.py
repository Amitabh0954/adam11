import unittest
from backend.repositories.product_repository import ProductRepository
from backend.services.products.search_service import SearchService

class SearchServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.product_repository = ProductRepository()
        self.search_service = SearchService(self.product_repository)
        self.product_repository.add_product({
            'id': 1,
            'name': 'Product1',
            'price': 100.0,
            'description': 'Description1'
        })
        self.product_repository.add_product({
            'id': 2,
            'name': 'Product2',
            'price': 200.0,
            'description': 'Description2'
        })

    def test_search_products_name(self):
        results = self.search_service.search_products(query='Product1', page=1)
        self.assertEqual(len(results['results']), 1)
        self.assertEqual(results['results'][0]['name'], 'Product1')

    def test_search_products_description(self):
        results = self.search_service.search_products(query='Description2', page=1)
        self.assertEqual(len(results['results']), 1)
        self.assertEqual(results['results'][0]['description'], 'Description2')

    def test_search_products_no_results(self):
        results = self.search_service.search_products(query='Nonexistent', page=1)
        self.assertEqual(len(results['results']), 0)

    def test_search_products_pagination(self):
        for i in range(3, 23):
            self.product_repository.add_product({
                'id': i,
                'name': f'Product{i}',
                'price': 100.0 * i,
                'description': f'Description{i}'
            })
        results = self.search_service.search_products(query='Product', page=2)
        self.assertEqual(len(results['results']), 10)
        self.assertEqual(results['page'], 2)