"""
Restaurant — модель таблиці ресторанів.
Колонки: id, name, address, rating, is_active.
Зв'язки: один ресторан має багато страв (dishes) та замовлень (orders).
"""

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    rating = Column(Float, nullable=False, default=0.0)  # 0.0–5.0
    is_active = Column(Boolean, nullable=False, default=True)

    # Зв'язок: Restaurant -> Dishes (один до багатьох, cascade delete)
    dishes = relationship("Dish", back_populates="restaurant", cascade="all, delete-orphan")

    # Зв'язок: Restaurant -> Orders (один до багатьох)
    orders = relationship("Order", back_populates="restaurant")
