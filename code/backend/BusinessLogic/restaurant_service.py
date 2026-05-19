"""
RestaurantService — бізнес-логіка для роботи з ресторанами.
Делегує операції з БД у RestaurantRepository.
Викликається з Controllers через Dependency Injection.
"""

from typing import Optional

from sqlalchemy.orm import Session

from Domain.Models.restaurant import Restaurant
from Domain.ViewModels.restaurant_schema import RestaurantCreate, RestaurantUpdate
from Repositories.restaurant_repository import RestaurantRepository


class RestaurantService:
    """Service layer for restaurant-related business logic."""

    def __init__(self, db: Session) -> None:
        self.repo = RestaurantRepository(db)

    def get_all_restaurants(self, skip: int = 0, limit: int = 100) -> list[Restaurant]:
        """Get a paginated list of all restaurants."""
        return self.repo.get_all(skip=skip, limit=limit)

    def get_active_restaurants(self, skip: int = 0, limit: int = 100) -> list[Restaurant]:
        """Get a paginated list of active restaurants only."""
        return self.repo.get_active(skip=skip, limit=limit)

    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Get a single restaurant by ID."""
        return self.repo.get_by_id(restaurant_id)

    def create_restaurant(self, data: RestaurantCreate) -> Restaurant:
        """Create a new restaurant."""
        restaurant = Restaurant(
            name=data.name,
            address=data.address,
            rating=data.rating,
            is_active=data.is_active,
        )
        return self.repo.create(restaurant)

    def update_restaurant(self, restaurant_id: int, data: RestaurantUpdate) -> Optional[Restaurant]:
        """Update a restaurant. Only updates fields that are provided (not None)."""
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return self.repo.get_by_id(restaurant_id)
        return self.repo.update(restaurant_id, update_data)

    def delete_restaurant(self, restaurant_id: int) -> bool:
        """
        Delete a restaurant by ID.
        Cascade will also delete all related dishes (configured in ORM model).
        """
        return self.repo.delete(restaurant_id)
