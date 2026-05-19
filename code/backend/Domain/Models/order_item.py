"""
OrderItem — модель таблиці позицій замовлення (зв'язок замовлення ↔ страви).
Колонки: id, order_id (FK), dish_id (FK), quantity, price_at_order.
Зв'язки: належить замовленню (order) та страві (dish).
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_at_order = Column(Float, nullable=False)  # Ціна страви на момент замовлення

    # Зв'язок: OrderItem -> Order (багато до одного)
    order = relationship("Order", back_populates="items")

    # Зв'язок: OrderItem -> Dish (багато до одного)
    dish = relationship("Dish", back_populates="order_items")

    @property
    def dish_name(self) -> str | None:
        return self.dish.name if self.dish else f"Dish #{self.dish_id}"
