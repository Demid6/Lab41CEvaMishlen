# logic/storage.py
# Загрузка и сохранение данных в JSON

import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _path(filename):
    return os.path.join(DATA_DIR, filename)


def load_products():
    """Загружает список товаров из products.json"""
    with open(_path("products.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def load_users():
    """Загружает список пользователей из users.json"""
    with open(_path("users.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def load_orders():
    """Загружает список заказов из orders.json (если файла нет — пустой список)"""
    if not os.path.exists(_path("orders.json")):
        return []
    with open(_path("orders.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def save_order(order_dict):
    """Сохраняет заказ в orders.json (добавляет в конец)"""
    orders = load_orders()
    orders.append(order_dict)
    with open(_path("orders.json"), "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


def next_order_number():
    """Генерирует следующий номер заказа"""
    orders = load_orders()
    if not orders:
        return "00001"
    last = orders[-1]["order_id"]
    return f"{int(last) + 1:05d}"


def now_iso():
    """Текущее время в формате ISO"""
    return datetime.now().isoformat(timespec="seconds")