"""
Domain/Models/__init__.py — Імпорт усіх ORM-моделей.
Цей файл гарантує, що SQLAlchemy "бачить" усі моделі при виклику Base.metadata.create_all(),
що необхідно для автоматичного створення таблиць у базі даних.
"""

from Domain.Models.user import User
from Domain.Models.restaurant import Restaurant
from Domain.Models.dish import Dish
from Domain.Models.order import Order
from Domain.Models.order_item import OrderItem

__all__ = ["User", "Restaurant", "Dish", "Order", "OrderItem"]
