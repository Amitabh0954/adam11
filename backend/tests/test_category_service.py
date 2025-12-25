import unittest
from backend.repositories.category_repository import CategoryRepository
from backend.services.products.category_service import CategoryService

class CategoryServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.category_repository = CategoryRepository()
        self.category_service = CategoryService(self.category_repository)

    def test_add_category_success(self):
        category = self.category_service.add_category(name='Category1')
        self.assertEqual(category['name'], 'Category1')

    def test_add_category_duplicate_name(self):
        self.category_service.add_category(name='Category1')
        with self.assertRaises(ValueError):
            self.category_service.add_category(name='Category1')

    def test_get_category(self):
        category = self.category_service.add_category(name='Category1')
        fetched_category = self.category_service.get_category(category['id'])
        self.assertEqual(fetched_category['name'], 'Category1')

    def test_get_category_not_found(self):
        category = self.category_service.get_category(999)
        self.assertIsNone(category)

    def test_remove_category_success(self):
        category = self.category_service.add_category(name='Category1')
        self.category_service.remove_category(category['id'])
        self.assertIsNone(self.category_service.get_category(category['id']))

    def test_remove_category_not_found(self):
        with self.assertRaises(ValueError):
            self.category_service.remove_category(999)