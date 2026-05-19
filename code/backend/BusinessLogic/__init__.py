"""
BusinessLogic/__init__.py — Central import for all service classes.
Allows clean imports: from BusinessLogic import UserService, OrderService, ...
"""

from BusinessLogic.user_service import UserService
from BusinessLogic.restaurant_service import RestaurantService
from BusinessLogic.dish_service import DishService
from BusinessLogic.order_service import OrderService

__all__ = [
    "UserService",
    "RestaurantService",
    "DishService",
    "OrderService",
]
