import unittest
from backend.repositories.product_repository import ProductRepository
from backend.services.products.product_service import ProductService

class ProductServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.product_repository = ProductRepository()
        self.product_service = ProductService(self.product_repository)

    def test_add_product_success(self):
        product = self.product_service.add_product(name='Test Product', price=100.0, description='Test Description')
        self.assertEqual(product['name'], 'Test Product')
        self.assertEqual(product['price'], 100.0)
        self.assertEqual(product['description'], 'Test Description')

    def test_add_product_duplicate_name(self):
        self.product_service.add_product(name='Test Product', price=100.0, description='Test Description')
        with self.assertRaises(ValueError):
            self.product_service.add_product(name='Test Product', price=200.0, description='Another Description')

    def test_add_product_invalid_price(self):
        with self.assertRaises(ValueError):
            self.product_service.add_product(name='Test Product', price=-10, description='Test Description')

    def test_get_product(self):
        product = self.product_service.add_product(name='Test Product', price=100.0, description='Test Description')
        fetched_product = self.product_service.get_product(product['id'])
        self.assertEqual(fetched_product['name'], 'Test Product')

    def test_get_product_not_found(self):
        product = self.product_service.get_product(999)
        self.assertIsNone(product)

    def test_update_product(self):
        product = self.product_service.add_product(name='Test Product', price=100.0, description='Test Description')
        updated_product = self.product_service.update_product(
            product_id=product['id'],
            name='Updated Product',
            price=150.0,
            description='Updated Description',
            is_admin=True
        )
        self.assertEqual(updated_product['name'], 'Updated Product')
        self.assertEqual(updated_product['price'], 150.0)
        self.assertEqual(updated_product['description'], 'Updated Description')

    def test_update_product_non_admin(self):
        product = self.product_service.add_product(name='Test Product', price=100.0, description='Test Description')
        with self.assertRaises(ValueError):
            self.product_service.update_product(
                product_id=product['id'],
                name='Updated Product',
                is_admin=False
            )

    def test_update_product_invalid_price(self):
        product = self.product_service.add_product(name='Test Product', price=100.0, description='Test Description')
        with self.assertRaises(ValueError):
            self.product_service.update_product(
                product_id=product['id'],
                price='invalid',
                is_admin=True
            )

    def test_delete_product(self):
        product = self.product_service.add_product(name='Test Product', price=100.0, description='Test Description')
        self.product_service.delete_product(product_id=product['id'], is_admin=True)
        fetched_product = self.product_service.get_product(product['id'])
        self.assertIsNone(fetched_product)

    def test_delete_product_non_admin(self):
        product = self.product_service.add_product(name='Test Product', price=100.0, description='Test Description')
        with self.assertRaises(ValueError):
            self.product_service.delete_product(product_id=product['id'], is_admin=False)