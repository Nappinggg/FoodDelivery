"""
Order — модель таблиці замовлень.
Колонки: id, user_id (FK), restaurant_id (FK), total_price, status, created_at.
Зв'язки: належить користувачу (user) та ресторану (restaurant), містить items (order_items).
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    total_price = Column(Float, nullable=False, default=0.0)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Зв'язок: Order -> User (багато до одного)
    user = relationship("User", back_populates="orders")

    # Зв'язок: Order -> Restaurant (багато до одного)
    restaurant = relationship("Restaurant", back_populates="orders")

    # Зв'язок: Order -> OrderItems (один до багатьох, cascade delete)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
