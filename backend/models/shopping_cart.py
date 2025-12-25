from typing import TypedDict, List

class CartItem(TypedDict):
    product_id: int
    quantity: int

class ShoppingCart(TypedDict):
    id: int
    user_id: int
    items: List[CartItem]