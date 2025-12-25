from typing import Optional
from backend.models.product import Product
from backend.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def add_product(self, name: str, price: float, description: str) -> Product:
        product = Product(
            id=len(self.product_repository.products) + 1,
            name=name,
            price=price,
            description=description
        )
        self.product_repository.add_product(product)
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.product_repository.get_product_by_id(product_id)

    def get_product_by_name(self, name: str) -> Optional[Product]:
        return self.product_repository.get_product_by_name(name)

    def update_product(self, product_id: int, name: Optional[str], price: Optional[float], description: Optional[str]) -> Product:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        if name:
            if self.product_repository.get_product_by_name(name):
                raise ValueError("Product name must be unique")
            product['name'] = name
        if price:
            if price <= 0:
                raise ValueError("Product price must be a positive number")
            product['price'] = price
        if description is not None:
            if description == '':
                raise ValueError("Product description cannot be empty")
            product['description'] = description

        self.product_repository.add_product(product)
        return product