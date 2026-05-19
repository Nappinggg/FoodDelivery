"""
Dish — модель таблиці страв.
Колонки: id, restaurant_id (FK), name, description, price, category.
Зв'язки: належить ресторану (restaurant), може входити в OrderItems.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)  # Наприклад: "Піца", "Суші", "Напої"

    # Зв'язок: Dish -> Restaurant (багато до одного)
    restaurant = relationship("Restaurant", back_populates="dishes")

    # Зв'язок: Dish -> OrderItems (одна страва може бути в багатьох замовленнях)
    order_items = relationship("OrderItem", back_populates="dish")
