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
        
        product = Product(name=name, price=price, description=description, category_id=category_id, attributes=attributes)
        self.product_repository.save(product)
        
        return {"message": "Product added successfully", "status": 201}
    
    def update_product(self, product_id: int, data: dict):
        product = self.product_repository.find_by_id(product_id)
        if not product:
            return {"message": "Product not found", "status": 404}
        
        if 'name' in data:
            existing_product = self.product_repository.find_by_name(data['name'])
            if existing_product and existing_product.id != product_id:
                return {"message": "Product with this name already exists", "status": 400}
            product.name = data['name']
        
        if 'price' in data:
            price = data['price']
            if price <= 0:
                return {"message": "Price must be a positive number", "status": 400}
            product.price = price
        
        if 'description' in data:
            product.description = data['description']

        if 'category_id' in data:
            product.category_id = data['category_id']

        if 'attributes' in data:
            product.attributes = data['attributes']

        self.product_repository.update(product)
        return {"message": "Product updated successfully", "status": 200}
    
    def delete_product(self, product_id: int):
        product = self.product_repository.find_by_id(product_id)
        if not product:
            return {"message": "Product not found", "status": 404}
        
        self.product_repository.delete(product)
        return {"message": "Product deleted successfully", "status": 200}
    
    def search_products(self, query: str, category: str = None, attributes: list = [], page: int = 1, per_page: int = 10):
        products = self.product_repository.search(query, category, attributes)
        total = len(products)
        start = (page - 1) * per_page
        end = start + per_page
        results = products[start:end]
        return {
            "results": [{"id": p.id, "name": p.name, "price": p.price, "description": p.description, "category_id": p.category_id, "attributes": p.attributes} for p in results],
            "page": page,
            "per_page": per_page,
            "total": total,
            "status": 200
        }