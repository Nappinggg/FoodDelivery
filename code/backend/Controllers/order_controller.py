"""
OrderController — FastAPI router for order-related endpoints.
Contains NO business logic — only receives requests and delegates to OrderService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from BusinessLogic.order_service import OrderService
from Domain.ViewModels.order_schema import (
    OrderCreate,
    OrderStatusUpdate,
    OrderResponse,
)

router = APIRouter(prefix="/api/orders", tags=["Orders"])


# ─── GET /api/orders ─────────────────────────────────────────────────

@router.get("/", response_model=list[OrderResponse])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get a paginated list of all orders (admin)."""
    service = OrderService(db)
    return service.get_all_orders(skip=skip, limit=limit)


# ─── GET /api/orders/user/{user_id} ──────────────────────────────────

@router.get("/user/{user_id}", response_model=list[OrderResponse])
def get_orders_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all orders for a specific user."""
    service = OrderService(db)
    return service.get_orders_by_user(user_id, skip=skip, limit=limit)


# ─── GET /api/orders/{order_id} ──────────────────────────────────────

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    """Get a single order by ID (with items)."""
    service = OrderService(db)
    order = service.get_order_by_id(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found.",
        )
    return order


# ─── POST /api/orders ────────────────────────────────────────────────

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreate,
    user_id: int = 1,  # TODO: Replace with actual auth (JWT) in Lab 8
    db: Session = Depends(get_db),
):
    """
    Create a new order.
    Client sends restaurant_id + list of items (dish_id, quantity).
    total_price is calculated SERVER-SIDE by OrderService.
    """
    service = OrderService(db)
    return service.create_order(user_id=user_id, data=data)


# ─── PUT /api/orders/{order_id}/status ────────────────────────────────

@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    """Update order status (admin). Validates status transitions."""
    service = OrderService(db)
    return service.update_order_status(order_id, data)


# ─── DELETE /api/orders/{order_id} ───────────────────────────────────

@router.delete("/{order_id}", response_model=OrderResponse)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """Cancel an order. Only allowed from 'pending' or 'confirmed' status."""
    service = OrderService(db)
    return service.cancel_order(order_id)
