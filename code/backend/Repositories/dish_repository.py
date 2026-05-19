"""
DishRepository — шар доступу до даних для таблиці Dishes.
Усі прямі запити до БД (через SQLAlchemy Session) інкапсульовані тут.
Викликається ТІЛЬКИ з шару BusinessLogic (Services).
"""

from typing import Optional

from sqlalchemy.orm import Session

from Domain.Models.dish import Dish


class DishRepository:
    """Repository for CRUD operations on the Dishes table."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Dish]:
        """Get a paginated list of all dishes across all restaurants."""
        return self.db.query(Dish).offset(skip).limit(limit).all()

    def get_by_id(self, dish_id: int) -> Optional[Dish]:
        """Get a single dish by ID. Returns None if not found."""
        return self.db.query(Dish).filter(Dish.id == dish_id).first()

    def get_by_restaurant_id(
        self, restaurant_id: int, skip: int = 0, limit: int = 100
    ) -> list[Dish]:
        """Get all dishes for a specific restaurant (paginated)."""
        return (
            self.db.query(Dish)
            .filter(Dish.restaurant_id == restaurant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, dish: Dish) -> Dish:
        """Insert a new dish into the database and return it with generated ID."""
        self.db.add(dish)
        self.db.commit()
        self.db.refresh(dish)
        return dish

    def update(self, dish_id: int, update_data: dict) -> Optional[Dish]:
        """
        Update an existing dish by ID.
        Accepts a dict of {column_name: new_value} for partial updates.
        Returns the updated dish or None if not found.
        """
        dish = self.get_by_id(dish_id)
        if dish is None:
            return None
        for key, value in update_data.items():
            if hasattr(dish, key):
                setattr(dish, key, value)
        self.db.commit()
        self.db.refresh(dish)
        return dish

    def delete(self, dish_id: int) -> bool:
        """Delete a dish by ID. Returns True if deleted, False if not found."""
        dish = self.get_by_id(dish_id)
        if dish is None:
            return False
        self.db.delete(dish)
        self.db.commit()
        return True
