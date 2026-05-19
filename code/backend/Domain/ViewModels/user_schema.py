"""
User schemas — Pydantic ViewModels for user-related endpoints.
Used for request validation (Create/Update) and response serialization (Response).
"""

from pydantic import BaseModel, ConfigDict, EmailStr


# ─── Base (shared fields) ────────────────────────────────────────────

class UserBase(BaseModel):
    """Base schema with common user fields."""
    full_name: str
    email: EmailStr
    phone: str
    role: str = "customer"


# ─── Create (input for POST /register) ───────────────────────────────

class UserCreate(UserBase):
    """Schema for creating a new user. Requires plain-text password."""
    password: str


# ─── Update (input for PUT /profile) ─────────────────────────────────

class UserUpdate(BaseModel):
    """Schema for partial user updates. All fields optional."""
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


# ─── Response (output from API) ──────────────────────────────────────

class UserResponse(UserBase):
    """Schema for returning user data. Excludes password_hash."""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ─── Login (input for POST /login) ───────────────────────────────────

class UserLogin(BaseModel):
    """Schema for login credentials."""
    email: EmailStr
    password: str
