"""
UserService — бізнес-логіка для роботи з користувачами.
Забезпечує хешування паролів та делегує операції з БД у UserRepository.
Викликається з Controllers через Dependency Injection.
"""

from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from Domain.Models.user import User
from Domain.ViewModels.user_schema import UserCreate, UserUpdate
from Repositories.user_repository import UserRepository


# Password hashing context (bcrypt algorithm)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service layer for user-related business logic."""

    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get a paginated list of all users."""
        return self.repo.get_all(skip=skip, limit=limit)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a single user by ID."""
        return self.repo.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a single user by email (used for auth)."""
        return self.repo.get_by_email(email)

    def create_user(self, data: UserCreate) -> User:
        """
        Create a new user.
        CRITICAL: Password is hashed via bcrypt BEFORE saving to DB.
        Plain-text passwords are NEVER stored.
        """
        hashed_password = pwd_context.hash(data.password)

        user = User(
            full_name=data.full_name,
            email=data.email,
            password_hash=hashed_password,
            phone=data.phone,
            role=data.role,
        )
        return self.repo.create(user)

    def update_user(self, user_id: int, data: UserUpdate) -> Optional[User]:
        """Update user profile. Only updates fields that are provided (not None)."""
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return self.repo.get_by_id(user_id)
        return self.repo.update(user_id, update_data)

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID."""
        return self.repo.delete(user_id)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against a bcrypt hash."""
        return pwd_context.verify(plain_password, hashed_password)
