from typing import Dict
from src.api.models import (
    UserInDB, Restaurant, Menu, MenuItem, Order, Payment, Delivery, Review, Notification
)

# --- Basic in-memory "DB" ---
users: Dict[int, UserInDB] = {}
restaurants: Dict[int, Restaurant] = {}
menus: Dict[int, Menu] = {}
menu_items: Dict[int, MenuItem] = {}
orders: Dict[int, Order] = {}
payments: Dict[int, Payment] = {}
deliveries: Dict[int, Delivery] = {}
reviews: Dict[int, Review] = {}
notifications: Dict[int, Notification] = {}

# --- Auto-increment IDs ---
counters = {
    "user": 1,
    "restaurant": 1,
    "menu": 1,
    "menu_item": 1,
    "order": 1,
    "payment": 1,
    "delivery": 1,
    "review": 1,
    "notification": 1,
}

def get_next_id(key: str) -> int:
    counters[key] += 1
    return counters[key] - 1
