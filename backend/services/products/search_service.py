from typing import List
from backend.models.product import Product
from backend.repositories.product_repository import ProductRepository

class SearchService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def search_products(self, query: str, page: int = 1, page_size: int = 10) -> List[Product]:
        products = list(self.product_repository.products.values())
        filtered_products = [product for product in products if self._matches_query(product, query)]
        start = (page - 1) * page_size
        end = start + page_size
        return filtered_products[start:end]

    def _matches_query(self, product: Product, query: str) -> bool:
        return query.lower() in product['name'].lower() or query.lower() in product.get('category', '').lower() or query.lower() in product.get('attributes', '')