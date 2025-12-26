from models.product import Product

class ProductRepository:
    def __init__(self):
        self.products = []
    
    def find_by_name(self, name: str) -> Product:
        return next((product for product in self.products if product.name == name), None)
    
    def find_by_id(self, product_id: int) -> Product:
        return next((product for product in self.products if product.id == product_id and not product.is_deleted), None)
    
    def save(self, product: Product) -> None:
        self.products.append(product)
    
    def update(self, product: Product) -> None:
        index = next((i for i, p in enumerate(self.products) if p.id == product.id), None)
        if index is not None:
            self.products[index] = product
    
    def delete(self, product: Product) -> None:
        product.is_deleted = True  # Soft delete the product
        update(product)
    
    def search(self, query: str, category: str = None, attributes: list = []) -> list[Product]:
        results = [product for product in self.products if query.lower() in product.name.lower() and not product.is_deleted]
        if category:
            results = [product for product in results if product.category_id == category]
        if attributes:
            results = [product for product in results if any(attr in product.attributes for attr in attributes)]
        return results