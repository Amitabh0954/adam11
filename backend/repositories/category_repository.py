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

    def get_all_categories(self) -> List[Category]:
        return list(self.categories.values())

    def remove_category(self, category_id: int) -> None:
        category = self.categories.pop(category_id, None)
        if category:
            self.name_index.remove(category['name'])