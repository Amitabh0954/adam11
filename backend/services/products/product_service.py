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
    
    def update_product(self, product_id: int, data: dict, authorization: str):
        if authorization != "admin":
            return {"message": "Unauthorized. Only admin can update products.", "status": 403}

        product = self.product_repository.find_by_id(product_id)
        if not product:
            return {"message": "Product not found", "status": 404}
        
        if 'name' in data:
            existing_product = self.product_repository.find_by_name(data['name'])
            if existing_product and existing_product.id != product_id:
                return {"message": "Product with this name already exists", "status": 400}
            product.name = data['name']
        
        if 'price' in data:
            try:
                price = float(data['price'])
                if price <= 0:
                    return {"message": "Price must be a positive number", "status": 400}
            except ValueError:
                return {"message": "Price must be a numeric value", "status": 400}
            product.price = price
        
        if 'description' in data:
            if not data['description']:
                return {"message": "Description cannot be empty", "status": 400}
            product.description = data['description']

        if 'category_id' in data:
            product.category_id = data['category_id']

        if 'attributes' in data:
            product.attributes = data['attributes']

        product.updated_by = authorization
        self.product_repository.update(product)
        return {"message": "Product updated successfully", "status": 200}
    
    def delete_product(self, product_id: int, confirm: bool, authorization: str):
        if authorization != "admin":
            return {"message": "Unauthorized. Only admin can delete products.", "status": 403}

        if not confirm:
            return {"message": "Deletion requires confirmation. Set confirm to true.", "status": 400}

        product = self.product_repository.find_by_id(product_id)
        if not product:
            return {"message": "Product not found", "status": 404}
        
        self.product_repository.delete(product)
        return {"message