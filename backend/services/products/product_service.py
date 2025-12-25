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