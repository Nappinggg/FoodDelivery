"""
Dish schemas — Pydantic ViewModels for dish-related endpoints.
Used for request validation (Create/Update) and response serialization (Response).
"""

from pydantic import BaseModel, ConfigDict


# ─── Base (shared fields) ────────────────────────────────────────────

class DishBase(BaseModel):
    """Base schema with common dish fields."""
    name: str
    description: str | None = None
    price: float
    category: str


# ─── Create (input for POST /dishes) ─────────────────────────────────

class DishCreate(DishBase):
    """Schema for creating a new dish. Requires restaurant_id."""
    restaurant_id: int


# ─── Update (input for PUT /dishes/{id}) ──────────────────────────────

class DishUpdate(BaseModel):
    """Schema for partial dish updates. All fields optional."""
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None


# ─── Response (output from API) ──────────────────────────────────────

class DishResponse(DishBase):
    """Schema for returning dish data."""
    id: int
    restaurant_id: int

    model_config = ConfigDict(from_attributes=True)
