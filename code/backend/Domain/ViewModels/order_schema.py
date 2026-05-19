"""
Order & OrderItem schemas — Pydantic ViewModels for order-related endpoints.
Used for request validation (Create) and response serialization (Response).
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ═══════════════════════════════════════════════════════════════════════
# OrderItem schemas
# ═══════════════════════════════════════════════════════════════════════

class OrderItemBase(BaseModel):
    """Base schema for an order item."""
    dish_id: int
    quantity: int = 1


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item (sent inside OrderCreate)."""
    pass


class OrderItemResponse(OrderItemBase):
    """Schema for returning an order item."""
    id: int
    order_id: int
    price_at_order: float
    dish_name: str | None = None  # Added to show name on frontend

    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════════════════
# Order schemas
# ═══════════════════════════════════════════════════════════════════════

class OrderCreate(BaseModel):
    """
    Schema for creating a new order.
    Client sends restaurant_id + list of items (dish_id, quantity).
    total_price is calculated SERVER-SIDE in OrderService — never trust the client.
    """
    restaurant_id: int
    items: list[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status (admin endpoint)."""
    status: str


class OrderResponse(BaseModel):
    """Schema for returning full order data with items."""
    id: int
    user_id: int
    restaurant_id: int
    total_price: float
    status: str
    created_at: datetime
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
