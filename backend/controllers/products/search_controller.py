from flask import Blueprint, request, jsonify
from backend.services.products.search_service import SearchService
from backend.repositories.product_repository import ProductRepository

search_bp = Blueprint('search', __name__)
search_service = SearchService(ProductRepository())

@search_bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    try:
        products = search_service.search_products(query=query, page=page, page_size=page_size)
        return jsonify(products), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400