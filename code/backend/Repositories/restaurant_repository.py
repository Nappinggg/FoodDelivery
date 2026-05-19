"""
RestaurantRepository — шар доступу до даних для таблиці Restaurants.
Усі прямі запити до БД (через SQLAlchemy Session) інкапсульовані тут.
Викликається ТІЛЬКИ з шару BusinessLogic (Services).
"""

from typing import Optional

from sqlalchemy.orm import Session

from Domain.Models.restaurant import Restaurant


class RestaurantRepository:
    """Repository for CRUD operations on the Restaurants table."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Restaurant]:
        """Get a paginated list of all restaurants."""
        return self.db.query(Restaurant).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 100) -> list[Restaurant]:
        """Get a paginated list of active restaurants only."""
        return (
            self.db.query(Restaurant)
            .filter(Restaurant.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Get a single restaurant by ID. Returns None if not found."""
        return self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    def create(self, restaurant: Restaurant) -> Restaurant:
        """Insert a new restaurant into the database and return it with generated ID."""
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def update(self, restaurant_id: int, update_data: dict) -> Optional[Restaurant]:
        """
        Update an existing restaurant by ID.
        Accepts a dict of {column_name: new_value} for partial updates.
        Returns the updated restaurant or None if not found.
        """
        restaurant = self.get_by_id(restaurant_id)
        if restaurant is None:
            return None
        for key, value in update_data.items():
            if hasattr(restaurant, key):
                setattr(restaurant, key, value)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def delete(self, restaurant_id: int) -> bool:
        """
        Delete a restaurant by ID.
        Cascade will also delete all related dishes (configured in the model).
        Returns True if deleted, False if not found.
        """
        restaurant = self.get_by_id(restaurant_id)
        if restaurant is None:
            return False
        self.db.delete(restaurant)
        self.db.commit()
        return True
