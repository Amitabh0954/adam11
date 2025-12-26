class CartItem:
    def __init__(self, user_id: int, product_id: int, quantity: int):
        self.id = id(self)  # Placeholder for a unique ID, to be replaced by actual DB auto-increment ID
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity