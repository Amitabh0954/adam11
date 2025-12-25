from typing import List, Dict
from backend.repositories.product_repository import ProductRepository
from backend.models.product import Product

class SearchService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def search_products(self, query: str, page: int) -> Dict[str, List[Product]]:
        all_products = self.product_repository.get_all_products()
        filtered_products = [product for product in all_products if self.matches_query(product, query)]
        
        # Pagination
        per_page = 10
        total_results = len(filtered_products)
        start = (page - 1) * per_page
        end = start + per_page

        return {
            "results": filtered_products[start:end],
            "total_results": total_results,
            "page": page,
            "per_page": per_page,
            "highlighted_term": query
        }

    def matches_query(self, product: Product, query: str) -> bool:
        return (query.lower() in product['name'].lower() or
                query.lower() in product['description'].lower())