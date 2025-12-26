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

        self.product_repository.update(product)
        return {"message": "Product updated successfully", "status": 200}
    
    def delete_product(self, product_id: int):
        product = self.product_repository.find_by_id(product_id)
        if not product:
            return {"message": "Product not found", "status": 404}
        
        self.product_repository.delete(product)
        return {"message": "Product deleted successfully", "status": 200}
    
    def search_products(self, query: str, page: int, per_page: int):
        products = self.product_repository.search(query)
        total = len(products)
        start = (page - 1) * per_page
        end = start + per_page
        results = products[start:end]
        return {
            "results": [{"id": p.id, "name": p.name, "price": p.price, "description": p.description} for p in results],
            "page": page,
            "per_page": per_page,
            "total": total,
            "status": 200
        }