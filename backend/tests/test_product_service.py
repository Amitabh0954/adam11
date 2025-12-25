import unittest
from backend.repositories.product_repository import ProductRepository
from backend.services.products.product_service import ProductService

class ProductServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.product_repository = ProductRepository()
        self.product_service = ProductService(self.product_repository)

    def test_add_product_success(self):
        product = self.product_service.add_product(name='Product1', price=100.0, description='Description1')
        self.assertEqual(product['name'], 'Product1')
        self.assertEqual(product['price'], 100.0)

    def test_add_product_duplicate_name(self):
        self.product_service.add_product(name='Product1', price=100.0, description='Description1')
        with self.assertRaises(ValueError):
            self.product_service.add_product(name='Product1', price=100.0, description='Description2')

    def test_add_product_invalid_price(self):
        with self.assertRaises(ValueError):
            self.product_service.add_product(name='Product1', price=-10.0, description='Description1')

    def test_add_product_empty_description(self):
        with self.assertRaises(ValueError):
            self.product_service.add_product(name='Product1', price=100.0, description='')

    def test_get_product(self):
        product = self.product_service.add_product(name='Product1', price=100.0, description='Description1')
        fetched_product = self.product_service.get_product(product['id'])
        self.assertEqual(fetched_product['name'], 'Product1')

    def test_get_product_not_found(self):
        product = self.product_service.get_product(999)
        self.assertIsNone(product)

    def test_update_product_success(self):
        product = self.product_service.add_product(name='Product1', price=100.0, description='Description1')
        updated_product = self.product_service.update_product(product_id=product['id'], name='UpdatedName', price=200.0, description='UpdatedDescription')
        self.assertEqual(updated_product['name'], 'UpdatedName')
        self.assertEqual(updated_product['price'], 200.0)
        self.assertEqual(updated_product['description'], 'UpdatedDescription')

    def test_update_product_duplicate_name(self):
        self.product_service.add_product(name='Product1', price=100.0, description='Description1')
        product = self.product_service.add_product(name='Product2', price=200.0, description='Description2')
        with self.assertRaises(ValueError):
            self.product_service.update_product(product_id=product['id'], name='Product1', price=300.0, description='UpdatedDescription')

    def test_update_product_invalid_price(self):
        product = self.product_service.add_product(name='Product1', price=100.0, description='Description1')
        with self.assertRaises(ValueError):
            self.product_service.update_product(product_id=product['id'], price=-200.0)

    def test_update_product_empty_description(self):
        product = self.product_service.add_product(name='Product1', price=100.0, description='Description1')
        with self.assertRaises(ValueError):
            self.product_service.update_product(product_id=product['id'], description='')