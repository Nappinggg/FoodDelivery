"""
Restaurant schemas — Pydantic ViewModels for restaurant-related endpoints.
Used for request validation (Create/Update) and response serialization (Response).
"""

from pydantic import BaseModel, ConfigDict


# ─── Base (shared fields) ────────────────────────────────────────────

class RestaurantBase(BaseModel):
    """Base schema with common restaurant fields."""
    name: str
    address: str
    rating: float = 0.0
    is_active: bool = True


# ─── Create (input for POST /restaurants) ─────────────────────────────

class RestaurantCreate(RestaurantBase):
    """Schema for creating a new restaurant."""
    pass


# ─── Update (input for PUT /restaurants/{id}) ─────────────────────────

class RestaurantUpdate(BaseModel):
    """Schema for partial restaurant updates. All fields optional."""
    name: str | None = None
    address: str | None = None
    rating: float | None = None
    is_active: bool | None = None


# ─── Response (output from API) ──────────────────────────────────────

class RestaurantResponse(RestaurantBase):
    """Schema for returning restaurant data."""
    id: int

    model_config = ConfigDict(from_attributes=True)
