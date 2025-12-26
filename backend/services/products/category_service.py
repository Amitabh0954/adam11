from repositories.category_repository import CategoryRepository
from models.category import Category

class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()
    
    def add_category(self, data: dict):
        name = data.get('name')
        parent_id = data.get('parent_id')
        if not name:
            return {"message": "Name is required", "status": 400}
        
        existing_category = self.category_repository.find_by_name(name)
        if existing_category:
            return {"message":