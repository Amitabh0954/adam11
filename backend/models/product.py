class Product:
    def __init__(self, name: str, price: float, description: str):
        self.id = id(self)  # Placeholder for a unique ID, to be replaced by actual DB auto-increment ID
        self.name = name
        self.price = price
        self.description = description