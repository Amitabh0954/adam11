from models.product import Product

class ProductRepository:
    def __init__(self):
        self.products = []
    
    def find_by_name(self, name: str) -> Product:
        return next((product for product in self.products if product.name == name), None)
    
    def save(self, product: Product) -> None:
        self.products.append(product)