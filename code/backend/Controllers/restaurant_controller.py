"""
RestaurantController — FastAPI router for restaurant-related endpoints.
Contains NO business logic — only receives requests and delegates to RestaurantService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from BusinessLogic.restaurant_service import RestaurantService
from Domain.ViewModels.restaurant_schema import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
)

router = APIRouter(prefix="/api/restaurants", tags=["Restaurants"])


# ─── GET /api/restaurants ────────────────────────────────────────────

@router.get("/", response_model=list[RestaurantResponse])
def get_all_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get a paginated list of all restaurants."""
    service = RestaurantService(db)
    return service.get_all_restaurants(skip=skip, limit=limit)


# ─── GET /api/restaurants/{restaurant_id} ─────────────────────────────

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    """Get a single restaurant by ID."""
    service = RestaurantService(db)
    restaurant = service.get_restaurant_by_id(restaurant_id)
    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with id {restaurant_id} not found.",
        )
    return restaurant


# ─── POST /api/restaurants ───────────────────────────────────────────

@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db)):
    """Create a new restaurant (admin)."""
    service = RestaurantService(db)
    return service.create_restaurant(data)


# ─── PUT /api/restaurants/{restaurant_id} ─────────────────────────────

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    db: Session = Depends(get_db),
):
    """Update a restaurant (partial update)."""
    service = RestaurantService(db)
    restaurant = service.update_restaurant(restaurant_id, data)
    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with id {restaurant_id} not found.",
        )
    return restaurant


# ─── DELETE /api/restaurants/{restaurant_id} ──────────────────────────

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """Delete a restaurant by ID (cascades to dishes)."""
    service = RestaurantService(db)
    deleted = service.delete_restaurant(restaurant_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with id {restaurant_id} not found.",
        )
