class Category:
    def __init__(self, name: str, parent_id: int = None):
        self.id = id(self)  # Placeholder for a unique ID, to be replaced by actual DB auto-increment ID
        self.name = name
        self.parent_id = parent_id