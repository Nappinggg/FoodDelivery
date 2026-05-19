"""
Repositories/__init__.py — Імпорт усіх репозиторіїв.
Дозволяє зручний імпорт: from Repositories import UserRepository, OrderRepository, ...
"""

from Repositories.user_repository import UserRepository
from Repositories.restaurant_repository import RestaurantRepository
from Repositories.dish_repository import DishRepository
from Repositories.order_repository import OrderRepository

__all__ = [
    "UserRepository",
    "RestaurantRepository",
    "DishRepository",
    "OrderRepository",
]
