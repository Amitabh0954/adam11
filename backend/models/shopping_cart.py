from typing import TypedDict, List
from backend.models.product import Product
from backend.models.user import User

class ShoppingCartItem(TypedDict):
    product: Product
    quantity: int

class ShoppingCart(TypedDict):
    user: User
    items: List[ShoppingCartItem]