"""
UserController — FastAPI router for user-related endpoints.
Contains NO business logic — only receives requests and delegates to UserService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from BusinessLogic.user_service import UserService
from Domain.ViewModels.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
)

router = APIRouter(prefix="/api/users", tags=["Users"])


# ─── GET /api/users ──────────────────────────────────────────────────

@router.get("/", response_model=list[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get a paginated list of all users."""
    service = UserService(db)
    return service.get_all_users(skip=skip, limit=limit)


# ─── GET /api/users/{user_id} ────────────────────────────────────────

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get a single user by ID."""
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    return user


# ─── POST /api/users/register ────────────────────────────────────────

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user. Password will be hashed by the service."""
    service = UserService(db)
    # Check if email already taken
    existing = service.get_user_by_email(data.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{data.email}' already exists.",
        )
    return service.create_user(data)


# ─── PUT /api/users/{user_id} ────────────────────────────────────────

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    """Update user profile (partial update)."""
    service = UserService(db)
    user = service.update_user(user_id, data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    return user


# ─── DELETE /api/users/{user_id} ─────────────────────────────────────

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    service = UserService(db)
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
