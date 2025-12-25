from typing import Optional, List
from backend.models.category import Category
from backend.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def add_category(self, name: str, parent_id: Optional[int] = None) -> Category:
        if parent_id and not self.category_repository.get_category_by_id(parent_id):
            raise ValueError("Parent category not found")

        category = Category(
            id=len(self.category_repository.categories) + 1,
            name=name,
            parent_id=parent_id
        )
        self.category_repository.add_category(category)
        return category

    def get_category(self, category_id: int) -> Optional<Category]:
        return self.category_repository.get_category_by_id(category_id)

    def update_category(self, category_id: int, name: Optional[str] = None, parent_id: Optional[int] = None) -> Category:
        category = self.category_repository.get_category_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        if name:
            if self.category_repository.get_category_by_name(name) and name != category['name']:
                raise ValueError("Category name must be unique")
            category['name'] = name

        if parent_id is not None:
            if parent_id != category['parent_id'] and not self.category_repository.get_category_by_id(parent_id):
                raise ValueError("Parent category not found")
            category['parent_id'] = parent_id

        self.category_repository.update_category(category)
        return category

    def delete_category(self, category_id: int) -> None:
        self.category_repository.delete_category(category_id)

    def list_categories(self) -> List[Category]:
        return self.category_repository.list_categories()