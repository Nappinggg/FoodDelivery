"""
DishService — бізнес-логіка для роботи зі стравами.
Делегує операції з БД у DishRepository.
Викликається з Controllers через Dependency Injection.
"""

from typing import Optional

from sqlalchemy.orm import Session

from Domain.Models.dish import Dish
from Domain.ViewModels.dish_schema import DishCreate, DishUpdate
from Repositories.dish_repository import DishRepository


class DishService:
    """Service layer for dish-related business logic."""

    def __init__(self, db: Session) -> None:
        self.repo = DishRepository(db)

    def get_all_dishes(self, skip: int = 0, limit: int = 100) -> list[Dish]:
        """Get a paginated list of all dishes."""
        return self.repo.get_all(skip=skip, limit=limit)

    def get_dish_by_id(self, dish_id: int) -> Optional[Dish]:
        """Get a single dish by ID."""
        return self.repo.get_by_id(dish_id)

    def get_dishes_by_restaurant(
        self, restaurant_id: int, skip: int = 0, limit: int = 100
    ) -> list[Dish]:
        """Get all dishes for a specific restaurant (menu)."""
        return self.repo.get_by_restaurant_id(restaurant_id, skip=skip, limit=limit)

    def create_dish(self, data: DishCreate) -> Dish:
        """Create a new dish linked to a restaurant."""
        dish = Dish(
            restaurant_id=data.restaurant_id,
            name=data.name,
            description=data.description,
            price=data.price,
            category=data.category,
        )
        return self.repo.create(dish)

    def update_dish(self, dish_id: int, data: DishUpdate) -> Optional[Dish]:
        """Update a dish. Only updates fields that are provided (not None)."""
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return self.repo.get_by_id(dish_id)
        return self.repo.update(dish_id, update_data)

    def delete_dish(self, dish_id: int) -> bool:
        """Delete a dish by ID."""
        return self.repo.delete(dish_id)
