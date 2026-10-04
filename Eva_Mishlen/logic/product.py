# logic/product.py

class Product:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.sub = data.get("sub", "")
        self.price = data["price"]
        self.emoji = data.get("emoji", "🍰")
        self.category = data.get("category", "Прочее")

    def __repr__(self):
        return f"<Product {self.name} — {self.price} ₽>"