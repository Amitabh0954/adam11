from typing import Optional, List
from backend.models.product import Product

class ProductRepository:
    def __init__(self):
        self.products = {}
        self.name_index = set()

    def add_product(self, product: Product) -> None:
        if product['name'] in self.name_index:
            raise ValueError("Product name must be unique")
        if product['price'] <= 0:
            raise ValueError("Product price must be a positive number")
        if not product['description']:
            raise ValueError("Product description cannot be empty")

        self.products[product['id']] = product
        self.name_index.add(product['name'])

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.products.get(product_id)

    def get_product_by_name(self, name: str) -> Optional[Product]:
        for product in self.products.values():
            if product['name'] == name:
                return product
        return None

    def get_all_products(self) -> List[Product]:
        return list(self.products.values())

    def remove_product(self, product_id: int) -> None:
        product = self.products.pop(product_id, None)
        if product:
            self.name_index.remove(product['name'])