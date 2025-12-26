from repositories.product_repository import ProductRepository
from models.product import Product

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
    
    def add_product(self, data: dict):
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        if not name or price is None or not description:
            return {"message": "Name, Price, and Description are required", "status": 400}
        
        if price <= 0:
            return {"message": "Price must be a positive number", "status": 400}
        
        existing_product = self.product_repository.find_by_name(name)
        if existing_product:
            return {"message": "Product with this name already exists", "status": 400}
        
        product = Product(name=name, price=price, description=description)
        self.product_repository.save(product)
        
        return {"message": "Product added successfully", "status": 201}