# logic/order.py
from logic.storage import next_order_number, now_iso, save_order


class OrderItem:
    def __init__(self, product):
        self.product = product
        self.qty = 1

    @property
    def sum(self):
        return self.product.price * self.qty


class Order:
    def __init__(self, cashier_name):
        self.order_id = next_order_number()
        self.cashier = cashier_name
        self.items = []          # список OrderItem
        self.discount = 0        # скидка в рублях
        self.packaging = 180     # подарочная упаковка
        self.payment_method = "card"

    def add_product(self, product):
        for item in self.items:
            if item.product.id == product.id:
                item.qty += 1
                return
        self.items.append(OrderItem(product))

    def remove_item(self, product_id):
        self.items = [i for i in self.items if i.product.id != product_id]

    def change_qty(self, product_id, delta):
        for item in self.items:
            if item.product.id == product_id:
                item.qty += delta
                if item.qty <= 0:
                    self.remove_item(product_id)
                return

    @property
    def subtotal(self):
        return sum(i.sum for i in self.items)

    @property
    def total(self):
        return max(0, self.subtotal + self.packaging - self.discount)

    def apply_discount(self, code):
        """Простая логика скидки по коду"""
        codes = {
            "SWEET10": 0.10,
            "SWEET20": 0.20,
            "BIRTHDAY": 0.15,
        }
        if code.upper() in codes:
            self.discount = int(self.subtotal * codes[code.upper()])
            return True, f"Скидка {int(codes[code.upper()] * 100)}% применена"
        return False, "Код не найден"

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "cashier": self.cashier,
            "created_at": now_iso(),
            "items": [
                {
                    "product_id": i.product.id,
                    "name": i.product.name,
                    "qty": i.qty,
                    "price": i.product.price,
                    "sum": i.sum,
                }
                for i in self.items
            ],
            "subtotal": self.subtotal,
            "packaging": self.packaging,
            "discount": self.discount,
            "total": self.total,
            "payment_method": self.payment_method,
        }

    def save(self):
        save_order(self.to_dict())