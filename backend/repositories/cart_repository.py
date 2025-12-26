from models.cart import Cart

class CartRepository:
    def __init__(self):
        self.carts = []
    
    def find_or_create_by_user_id(self, user_id: int) ->