from typing import Optional
from backend.models.product import Product

class ProductRepository:
    def __init__(self):
        self.products = {}
        self.name_index = set()

    def add_product(self, product: Product) -> None:
        if product['name'] in self.name_index:
            raise ValueError("Product name must be unique")
        if not product['description']:
            raise ValueError("Product description cannot be empty")
        if product['price'] <= 0:
            raise ValueError("Product price must be a positive number")
        self.products[product['id']] = product
        self.name_index.add(product['name'])

    def get_product_by_id(self, product_id: int) -> Optional<Product]:
        return self.products.get(product_id)

    def get_product_by_name(self, name: str) -> Optional<Product]:
        for product in self.products.values():
            if product['name'] == name:
                return product
        return None

    def update_product(self, product: Product) -> None:
        if product['id'] not in self.products:
            raise ValueError("Product not found")
        self.products[product['id']] = product

    def delete_product(self, product_id: int) -> None:
        if product_id in self.products:
            product = self.products.pop(product_id)
            self.name_index.discard(product['name'])