class Cart:
    def __init__(self, user_id: int):
        self.id = id(self)  # Placeholder for a unique ID, to be replaced by actual DB auto-increment ID
        self.user_id = user_id
        self.items = []