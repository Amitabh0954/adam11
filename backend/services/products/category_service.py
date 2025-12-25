from typing import Optional, List
from backend.models.category import Category
from backend.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def add_category(self, name: str, parent_id: Optional[int] = None) -> Category:
        category = Category(
            id=len(self.category_repository.categories) + 1,
            name=name,
            parent_id=parent_id
        )
        self.category_repository.add_category(category)
        return category

    def get_category(self, category_id: int) -> Optional<Category]:
        return self.category_repository.get_category_by_id(category_id)

    def get_all_categories(self) -> List<Category]:
        return self.category_repository.get_all_categories()

    def remove_category(self, category_id: int) -> None:
        if not self.category_repository.get_category_by_id(category_id):
            raise ValueError("Category not found")
        self.category_repository.remove_category(category_id)