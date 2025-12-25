from flask import Blueprint, request, jsonify
from backend.services.products.search_service import SearchService
from backend.repositories.product_repository import ProductRepository

search_bp = Blueprint('search', __name__)
search_service = SearchService(ProductRepository())

@search_bp.route('/search/products', methods=['GET'])
def search_products():
    query = request.args.get('query')
    page = request.args.get('page', default=1, type=int)
    if not query:
        return jsonify({"error": "Search query required"}), 400

    results = search_service.search_products(query=query, page=page)
    return jsonify(results), 200