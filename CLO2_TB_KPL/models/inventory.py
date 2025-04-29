class InventoryItem:
    def __init__(self, name: str, status: str = "Tersedia"):
        self.name = name
        self.status = status  # Tersedia, Digunakan, Rusak
