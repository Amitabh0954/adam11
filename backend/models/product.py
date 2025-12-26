class Product:
    def __init__(self, name: str, price: float, description: str, category_id: int, attributes: dict, updated_by: str):
        self.id = id(self)  # Placeholder for a unique ID, to be replaced by actual DB auto-increment ID
        self.name = name
        self.price = price
        self.description = description
        self.category_id = category_id
        self.is_deleted = False  # To mark if the product is deleted
        self.attributes = attributes  # Additional attributes for the product
        self.updated_by = updated_by  # Track who modified the product