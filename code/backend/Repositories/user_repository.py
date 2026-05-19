"""
UserRepository — шар доступу до даних для таблиці Users.
Усі прямі запити до БД (через SQLAlchemy Session) інкапсульовані тут.
Викликається ТІЛЬКИ з шару BusinessLogic (Services).
"""

from typing import Optional

from sqlalchemy.orm import Session

from Domain.Models.user import User


class UserRepository:
    """Repository for CRUD operations on the Users table."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get a paginated list of all users."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a single user by ID. Returns None if not found."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a single user by email. Used for auth. Returns None if not found."""
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        """Insert a new user into the database and return it with generated ID."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, update_data: dict) -> Optional[User]:
        """
        Update an existing user by ID.
        Accepts a dict of {column_name: new_value} for partial updates.
        Returns the updated user or None if not found.
        """
        user = self.get_by_id(user_id)
        if user is None:
            return None
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """Delete a user by ID. Returns True if deleted, False if not found."""
        user = self.get_by_id(user_id)
        if user is None:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
