from models.product import Product

class ProductRepository:
    def __init__(self):
        self.products = []
    
    def find_by_name(self, name: str) -> Product:
        return next((product for product in self.products if product.name == name), None)
    
    def find_by_id(self, product_id: int) -> Product:
        return next((product for product in self.products if product.id == product_id), None)
    
    def save(self, product: Product) -> None:
        self.products.append(product)
    
    def update(self, product: Product) -> None:
        index = next((i for i, p in enumerate(self.products) if p.id == product.id), None)
        if index is not None:
            self.products[index] = product
    
    def delete(self, product: Product) -> None:
        self.products.remove(product)
    
    def search(self, query: str) -> list[Product]:
        query = query.lower()
        return [product for product in self.products if query in product.name.lower() or query in product.description.lower()]