"""
OrderService — бізнес-логіка для роботи із замовленнями.
Містить КРИТИЧНІ бізнес-правила:
  1. total_price розраховується ТІЛЬКИ на сервері (ніколи не довіряємо клієнту).
  2. Перевірка, чи ресторан is_active перед створенням замовлення.
  3. Валідація переходів між статусами замовлення.
Викликається з Controllers через Dependency Injection.
"""

from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from Domain.Models.order import Order
from Domain.Models.order_item import OrderItem
from Domain.ViewModels.order_schema import OrderCreate, OrderStatusUpdate
from Repositories.order_repository import OrderRepository
from Repositories.dish_repository import DishRepository
from Repositories.restaurant_repository import RestaurantRepository


# Valid status transitions: current_status -> [allowed_next_statuses]
VALID_STATUS_TRANSITIONS: dict[str, list[str]] = {
    "pending":    ["confirmed", "cancelled"],
    "confirmed":  ["preparing", "cancelled"],
    "preparing":  ["delivering"],
    "delivering": ["delivered"],
    "delivered":  [],       # final state
    "cancelled":  [],       # final state
}


class OrderService:
    """Service layer for order-related business logic."""

    def __init__(self, db: Session) -> None:
        self.order_repo = OrderRepository(db)
        self.dish_repo = DishRepository(db)
        self.restaurant_repo = RestaurantRepository(db)

    def get_all_orders(self, skip: int = 0, limit: int = 100) -> list[Order]:
        """Get a paginated list of all orders."""
        return self.order_repo.get_all(skip=skip, limit=limit)

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Get a single order by ID (with items)."""
        return self.order_repo.get_by_id(order_id)

    def get_orders_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Order]:
        """Get all orders for a specific user."""
        return self.order_repo.get_by_user_id(user_id, skip=skip, limit=limit)

    def create_order(self, user_id: int, data: OrderCreate) -> Order:
        """
        Create a new order with items.

        CRITICAL BUSINESS RULES:
        1. Verify restaurant exists and is_active.
        2. Verify all dishes exist and belong to the specified restaurant.
        3. Calculate total_price SERVER-SIDE from actual dish prices * quantities.
           The client NEVER sends total_price — we compute it ourselves.
        4. Store price_at_order to freeze the price at the moment of ordering.
        """
        # 1. Check restaurant exists and is active
        restaurant = self.restaurant_repo.get_by_id(data.restaurant_id)
        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restaurant with id {data.restaurant_id} not found.",
            )
        if not restaurant.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Restaurant '{restaurant.name}' is currently not accepting orders.",
            )

        # 2. Validate items and calculate total_price
        if not data.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order must contain at least one item.",
            )

        order_items: list[OrderItem] = []
        total_price: float = 0.0

        for item_data in data.items:
            dish = self.dish_repo.get_by_id(item_data.dish_id)
            if dish is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Dish with id {item_data.dish_id} not found.",
                )
            if dish.restaurant_id != data.restaurant_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Dish '{dish.name}' (id={dish.id}) does not belong to restaurant id={data.restaurant_id}.",
                )

            # 3. Freeze the current price and calculate subtotal
            price_at_order = dish.price
            subtotal = price_at_order * item_data.quantity
            total_price += subtotal

            order_items.append(
                OrderItem(
                    dish_id=item_data.dish_id,
                    quantity=item_data.quantity,
                    price_at_order=price_at_order,
                )
            )

        # 4. Create the order with server-calculated total
        order = Order(
            user_id=user_id,
            restaurant_id=data.restaurant_id,
            total_price=round(total_price, 2),
            status="pending",
            items=order_items,
        )
        return self.order_repo.create(order)

    def update_order_status(self, order_id: int, data: OrderStatusUpdate) -> Order:
        """
        Update order status with transition validation.
        Only allows transitions defined in VALID_STATUS_TRANSITIONS.
        """
        order = self.order_repo.get_by_id(order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found.",
            )

        new_status = data.status.lower()
        current_status = order.status

        # Validate the transition
        allowed = VALID_STATUS_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from '{current_status}' to '{new_status}'. "
                       f"Allowed transitions: {allowed}.",
            )

        return self.order_repo.update_status(order_id, new_status)

    def cancel_order(self, order_id: int) -> Order:
        """
        Cancel an order. Only allowed from 'pending' or 'confirmed' status.
        """
        order = self.order_repo.get_by_id(order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found.",
            )

        if order.status not in ("pending", "confirmed"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel order with status '{order.status}'. "
                       f"Cancellation is only allowed for 'pending' or 'confirmed' orders.",
            )

        return self.order_repo.update_status(order_id, "cancelled")
