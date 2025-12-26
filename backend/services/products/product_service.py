from repositories.product_repository import ProductRepository
from models.product import Product

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
    
    def add_product(self, data: dict):
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        category_id = data.get('category_id')
        attributes = data.get('attributes', {})
        if not name or price is None or not description or category_id is None:
            return {"message": "Name, Price, Description, and Category are required", "status": 400}
        
        if price <= 0:
            return {"message": "Price must be a positive number", "status": 400}
        
        existing_product = self.product_repository.find_by_name(name)
        if existing_product:
            return {"message": "Product with this name already exists", "status": 400}
        
        product = Product(name=name, price=price, description=description, category_id=category_id, attributes=attributes, updated_by=data.get('updated_by'))
        self.product_repository.save(product)
        
        return {"message": "Product added successfully", "status": 201}
    
    def update_product(self, product_id: int, data: dict,