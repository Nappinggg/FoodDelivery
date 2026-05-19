"""
create_db.py — Script to create all tables in the SQLite database.
Run: py create_db.py
"""

import sys
import os

# Add current directory to sys.path for correct imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base, engine

# Import all models so SQLAlchemy registers them
from Domain.Models import User, Restaurant, Dish, Order, OrderItem

print("Creating tables in database...")
print(f"Database: {engine.url}")
print(f"Tables to create: {list(Base.metadata.tables.keys())}")
print()

# Create all tables
Base.metadata.create_all(bind=engine)

print("All tables created successfully!")
print()
for table_name, table in Base.metadata.tables.items():
    columns = [col.name for col in table.columns]
    print(f"  {table_name}: {columns}")
