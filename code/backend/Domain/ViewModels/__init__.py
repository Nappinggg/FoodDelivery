"""
Domain/ViewModels/__init__.py — Central import for all Pydantic schemas.
Allows clean imports: from Domain.ViewModels import UserCreate, OrderResponse, ...
"""

from Domain.ViewModels.user_schema import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
)
from Domain.ViewModels.restaurant_schema import (
    RestaurantBase,
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
)
from Domain.ViewModels.dish_schema import (
    DishBase,
    DishCreate,
    DishUpdate,
    DishResponse,
)
from Domain.ViewModels.order_schema import (
    OrderItemBase,
    OrderItemCreate,
    OrderItemResponse,
    OrderCreate,
    OrderStatusUpdate,
    OrderResponse,
)

__all__ = [
    "UserBase", "UserCreate", "UserUpdate", "UserResponse", "UserLogin",
    "RestaurantBase", "RestaurantCreate", "RestaurantUpdate", "RestaurantResponse",
    "DishBase", "DishCreate", "DishUpdate", "DishResponse",
    "OrderItemBase", "OrderItemCreate", "OrderItemResponse",
    "OrderCreate", "OrderStatusUpdate", "OrderResponse",
]
