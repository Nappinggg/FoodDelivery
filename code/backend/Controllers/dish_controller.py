"""
DishController — FastAPI router for dish-related endpoints.
Contains NO business logic — only receives requests and delegates to DishService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from BusinessLogic.dish_service import DishService
from Domain.ViewModels.dish_schema import (
    DishCreate,
    DishUpdate,
    DishResponse,
)

router = APIRouter(prefix="/api/dishes", tags=["Dishes"])


# ─── GET /api/dishes ─────────────────────────────────────────────────

@router.get("/", response_model=list[DishResponse])
def get_all_dishes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get a paginated list of all dishes across all restaurants."""
    service = DishService(db)
    return service.get_all_dishes(skip=skip, limit=limit)


# ─── GET /api/dishes/restaurant/{restaurant_id} ──────────────────────

@router.get("/restaurant/{restaurant_id}", response_model=list[DishResponse])
def get_dishes_by_restaurant(
    restaurant_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all dishes (menu) for a specific restaurant."""
    service = DishService(db)
    return service.get_dishes_by_restaurant(restaurant_id, skip=skip, limit=limit)


# ─── GET /api/dishes/{dish_id} ───────────────────────────────────────

@router.get("/{dish_id}", response_model=DishResponse)
def get_dish_by_id(dish_id: int, db: Session = Depends(get_db)):
    """Get a single dish by ID."""
    service = DishService(db)
    dish = service.get_dish_by_id(dish_id)
    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish with id {dish_id} not found.",
        )
    return dish


# ─── POST /api/dishes ────────────────────────────────────────────────

@router.post("/", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
def create_dish(data: DishCreate, db: Session = Depends(get_db)):
    """Create a new dish (admin). Requires restaurant_id in body."""
    service = DishService(db)
    return service.create_dish(data)


# ─── PUT /api/dishes/{dish_id} ───────────────────────────────────────

@router.put("/{dish_id}", response_model=DishResponse)
def update_dish(dish_id: int, data: DishUpdate, db: Session = Depends(get_db)):
    """Update a dish (partial update)."""
    service = DishService(db)
    dish = service.update_dish(dish_id, data)
    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish with id {dish_id} not found.",
        )
    return dish


# ─── DELETE /api/dishes/{dish_id} ────────────────────────────────────

@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    """Delete a dish by ID."""
    service = DishService(db)
    deleted = service.delete_dish(dish_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish with id {dish_id} not found.",
        )
