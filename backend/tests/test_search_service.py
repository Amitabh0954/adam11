import unittest
from backend.repositories.product_repository import ProductRepository
from backend.services.products.search_service import SearchService

class SearchServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.product_repository = ProductRepository()
        self.search_service = SearchService(self.product_repository)

        self.product_repository.add_product({'id': 1, 'name': 'Test Product 1', 'price': 100.0, 'description': 'Description 1'})
        self.product_repository.add_product({'id': 2, 'name': 'Another Product', 'price': 150.0, 'description': 'Description 2'})
        self.product_repository.add_product({'id': 3, 'name': 'Test Product 3', 'price': 200.0, 'description': 'Description 3', 'category': 'Electronics'})
        
    def test_search_products_by_name(self):
        results = self.search_service.search_products('Test')
        self.assertEqual(len(results), 2)

    def test_search_products_by_description(self):
        results = self.search_service.search_products('Description 2')
        self.assertEqual(len(results), 1)

    def test_search_products_by_category(self):
        results = self.search_service.search_products('Electronics')
        self.assertEqual(len(results), 1)

    def test_search_products_pagination(self):
        results = self.search_service.search_products('Product', page=1, page_size=2)
        self.assertEqual(len(results), 2)
        results = self.search_service.search_products('Product', page=2, page_size=2)
        self.assertEqual(len(results), 1)