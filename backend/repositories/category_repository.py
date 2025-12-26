from models.category import Category

class CategoryRepository:
    def __init__(self):
        self.categories = []
    
    def find_by_name(self, name: str) -> Category:
        return next((category for category in self.categories if category.name == name), None)
    
    def find_by_id(self, category_id: int) -> Category:
        return next((category for category in self.categories if category.id == category_id), None)
    
    def save(self, category: Category) -> None:
        self.categories.append(category)
    
    def update(self, category: Category) -> None:
        index = next((i for i, c in enumerate(self.categories) if c.id == category.id), None)
        if index is not None:
            self.categories[index] = category
    
    def delete(self, category: Category) -> None:
        self.categories.remove(category)