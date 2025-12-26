from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository

class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()
        self.product_repository = ProductRepository()
    
    def add_product_to_cart(self, data: dict, user_id: int):
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id or quantity is None:
            return {"message": "Product ID and quantity are required", "status": 400}
        
        existing_product = self.product_repository.find_by_id(product_id)
        if not existing_product:
            return {"message": "Product not found", "status": 404}
        
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        self.cart_repository.save(cart_item)
        
        return {"message": "Product added to cart", "status": 201}
    
    def remove_product_from_cart(self, item_id: int, confirm: bool, user_id: int):
        if not confirm:
            return {"message": "Deletion requires confirmation. Set confirm to true.", "status": 400}
        
        cart_item = self.cart_repository.find_by_id(item_id)
        if not cart_item or cart_item.user_id != user_id:
            return {"message": "Cart item not found", "status": 404}
        
        self.cart_repository.delete(cart_item)
        return {"message": "Product removed from cart", "status": 200}
    
    def get_cart_items(self, user_id: int):
        cart_items = self.cart_repository.find_by_user_id(user_id)
        products = [self.product_repository.find_by_id(item.product_id) for item in cart_items]
        total_price = sum(item.quantity * product.price for item, product in zip(cart_items, products))
        
        return {"cart_items": cart_items, "total_price": total_price, "status": 200}
    
    def update_cart_item_quantity(self, item_id: int, data: dict, user_id: int):
        quantity = data.get('quantity')
        if quantity is None or quantity <= 0:
            return {"message": "Quantity must be a positive number", "status": 400}
        
        cart_item = self.cart_repository.find_by_id(item_id)
        if not cart_item or cart_item.user_id != user_id:
            return {"message": "Cart item not found", "status": 404}
        
        cart_item.quantity = quantity
        self.cart_repository.update(cart_item)
        return {"message": "Cart item quantity updated", "status": 200}