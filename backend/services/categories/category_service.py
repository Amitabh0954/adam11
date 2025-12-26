from repositories.category_repository import CategoryRepository
from models.category import Category

class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()
    
    def add_category(self, data: dict):
        name = data.get('name')
        parent_id = data.get('parent_id', None)
        if not name:
            return {"message": "Name is required", "status": 400}
        
        existing_category = self.category_repository.find_by_name(name)
        if existing_category:
            return {"message": "Category with this name already exists", "status": 400}
        
        category = Category(name=name, parent_id=parent_id)
        self.category_repository.save(category)
        
        return {"message": "Category added successfully", "status": 201}
    
    def update_category(self, category_id: int, data: dict):
        category = self.category_repository.find_by_id(category_id)
        if not category:
            return {"message": "Category not found", "status": 404}
        
        if 'name' in data:
            existing_category = self.category_repository.find_by_name(data['name'])
            if existing_category and existing_category.id != category_id:
                return {"message": "Category with this name already exists", "status": 400}
            category.name = data['name']
        
        if 'parent_id' in data:
            category.parent_id = data['parent_id']

        self.category_repository.update(category)
        return {"message": "Category updated successfully", "status": 200}
    
    def delete_category(self, category_id: int):
        category = self.category_repository.find_by_id(category_id)
        if not category:
            return {"message": "Category not found", "status": 404}
        
        self.category_repository.delete(category)
        return {"message": "Category deleted successfully", "status": 200}