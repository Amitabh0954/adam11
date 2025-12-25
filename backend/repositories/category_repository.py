from typing import Optional, List
from backend.models.category import Category

class CategoryRepository:
    def __init__(self):
        self.categories = {}
        self.name_index = set()

    def add_category(self, category: Category) -> None:
        if category['name'] in self.name_index:
            raise ValueError("Category name must be unique")
        self.categories[category['id']] = category
        self.name_index.add(category['name'])

    def get_category_by_id(self, category_id: int) -> Optional<Category]:
        return self.categories.get(category_id)

    def get_category_by_name(self, name: str) -> Optional<Category]:
        for category in self.categories.values():
            if category['name'] == name:
                return category
        return None

    def update_category(self, category: Category) -> None:
        if category['id'] not in self.categories:
            raise ValueError("Category not found")
        self.categories[category['id']] = category

    def delete_category(self, category_id: int) -> None:
        if category_id in self.categories:
            category = self.categories.pop(category_id)
            self.name_index.discard(category['name'])

    def list_categories(self) -> List[Category]:
        return list(self.categories.values())