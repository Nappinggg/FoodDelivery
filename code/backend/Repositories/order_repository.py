"""
OrderRepository — шар доступу до даних для таблиць Orders та OrderItems.
Логіка OrderItems об'єднана тут, оскільки items завжди існують у контексті замовлення.
Усі прямі запити до БД (через SQLAlchemy Session) інкапсульовані тут.
Викликається ТІЛЬКИ з шару BusinessLogic (Services).
"""

from typing import Optional

from sqlalchemy.orm import Session, joinedload

from Domain.Models.order import Order
from Domain.Models.order_item import OrderItem


class OrderRepository:
    """Repository for CRUD operations on the Orders and OrderItems tables."""

    def __init__(self, db: Session) -> None:
        self.db = db

    # ─── Orders ───────────────────────────────────────────────────────

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
        """Get a paginated list of all orders (with items eager-loaded)."""
        return (
            self.db.query(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.dish))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Get a single order by ID with items eager-loaded. Returns None if not found."""
        return (
            self.db.query(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.dish))
            .filter(Order.id == order_id)
            .first()
        )

    def get_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Order]:
        """Get all orders for a specific user (paginated, items eager-loaded)."""
        return (
            self.db.query(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.dish))
            .filter(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, order: Order) -> Order:
        """
        Insert a new order (with its items) into the database.
        OrderItems should be attached to order.items before calling this method.
        Returns the order with generated ID.
        """
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_status(self, order_id: int, new_status: str) -> Optional[Order]:
        """
        Update the status of an existing order.
        Returns the updated order or None if not found.
        """
        order = self.get_by_id(order_id)
        if order is None:
            return None
        order.status = new_status
        self.db.commit()
        self.db.refresh(order)
        return order

    def update(self, order_id: int, update_data: dict) -> Optional[Order]:
        """
        General-purpose update for an order by ID.
        Accepts a dict of {column_name: new_value} for partial updates.
        Returns the updated order or None if not found.
        """
        order = self.get_by_id(order_id)
        if order is None:
            return None
        for key, value in update_data.items():
            if hasattr(order, key):
                setattr(order, key, value)
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete(self, order_id: int) -> bool:
        """
        Delete an order by ID.
        Cascade will also delete all related OrderItems (configured in the model).
        Returns True if deleted, False if not found.
        """
        order = self.get_by_id(order_id)
        if order is None:
            return False
        self.db.delete(order)
        self.db.commit()
        return True

    # ─── OrderItems (допоміжні методи) ────────────────────────────────

    def add_item(self, item: OrderItem) -> OrderItem:
        """Add a single item to an existing order."""
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_items_by_order_id(self, order_id: int) -> list[OrderItem]:
        """Get all items for a specific order."""
        return (
            self.db.query(OrderItem)
            .filter(OrderItem.order_id == order_id)
            .all()
        )

    def delete_item(self, item_id: int) -> bool:
        """Delete a single order item by its ID."""
        item = self.db.query(OrderItem).filter(OrderItem.id == item_id).first()
        if item is None:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
