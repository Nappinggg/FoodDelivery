"""
Controllers/__init__.py — Central import for all FastAPI routers.
Used by main.py to include all routes via app.include_router().
"""

from Controllers.user_controller import router as user_router
from Controllers.restaurant_controller import router as restaurant_router
from Controllers.dish_controller import router as dish_router
from Controllers.order_controller import router as order_router

__all__ = [
    "user_router",
    "restaurant_router",
    "dish_router",
    "order_router",
]
