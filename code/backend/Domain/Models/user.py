"""
User — модель таблиці користувачів.
Колонки: id, full_name, email, password_hash, phone, role.
Зв'язки: один користувач має багато замовлень (orders).
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(String, nullable=False, default="customer")  # "customer" або "admin"

    # Зв'язок: User -> Orders (один до багатьох)
    orders = relationship("Order", back_populates="user")
