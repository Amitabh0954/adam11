import unittest
from backend.repositories.category_repository import CategoryRepository
from backend.services.products.category_service import CategoryService

class CategoryServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.category_repository = CategoryRepository()
        self.category_service = CategoryService(self.category_repository)

    def test_add_category_success(self):
        category = self.category_service.add_category(name='Electronics')
        self.assertEqual(category['name'], 'Electronics')

    def test_add_category_duplicate_name(self):
        self.category_service.add_category(name='Electronics')
        with self.assertRaises(ValueError):
            self.category_service.add_category(name='Electronics')

    def test_add_category_with_parent(self):
        parent = self.category_service.add_category(name='Electronics')
        category = self.category_service.add_category(name='Laptops', parent_id=parent['id'])
        self.assertEqual(category['parent_id'], parent['id'])

    def test_get_category(self):
        category = self.category_service.add_category(name='Electronics')
        fetched_category = self.category_service.get_category(category['id'])
        self.assertEqual(fetched_category['name'], 'Electronics')

    def test_get_category_not_found(self):
        category = self.category_service.get_category(999)
        self.assertIsNone(category)

    def test_update_category(self):
        category = self.category_service.add_category(name='Electronics')
        updated_category = self.category_service.update_category(category_id=category['id'], name='Gadgets')
        self.assertEqual(updated_category['name'], 'Gadgets')

    def test_update_category_invalid_parent(self):
        category = self.category_service.add_category(name='Electronics')
        with self.assertRaises(ValueError):
            self.category_service.update_category(category_id=category['id'], parent_id=999)

    def test_delete_category(self):
        category = self.category_service.add_category(name='Electronics')
        self.category_service.delete_category(category_id=category['id'])
        fetched_category = self.category_service.get_category(category['id'])
        self.assertIsNone(fetched_category)

    def test_list_categories(self):
        self.category_service.add_category(name='Electronics')
        self.category_service.add_category(name='Laptops')
        categories = self.category_service.list_categories()
        self.assertEqual(len(categories), 2)