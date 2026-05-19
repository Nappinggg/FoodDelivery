"""
database.py — Налаштування підключення до бази даних SQLite через SQLAlchemy.
Створює engine, SessionLocal (фабрику сесій) та Base (базовий клас для моделей).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Рядок підключення до файлової бази SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./food_delivery.db"

# Створення engine з параметром check_same_thread=False (потрібно для SQLite + FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Фабрика сесій — кожен запит отримує свою сесію через Depends(get_db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас, від якого наслідуються всі ORM-моделі
Base = declarative_base()


def get_db():
    """
    Генератор сесії бази даних.
    Використовується як залежність (Dependency) у FastAPI через Depends(get_db).
    Гарантує закриття сесії після завершення запиту.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
