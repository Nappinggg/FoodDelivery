"""
main.py — Entry point for the Food Delivery API.
Initializes the FastAPI application, configures CORS, and includes all routers.
Run: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# Import all models to ensure tables are registered with Base.metadata
import Domain.Models  # noqa: F401

# Import all routers
from Controllers import user_router, restaurant_router, dish_router, order_router


# ─── Create tables (if they don't exist yet) ─────────────────────────
Base.metadata.create_all(bind=engine)


# ─── Initialize FastAPI app ──────────────────────────────────────────
app = FastAPI(
    title="Food Delivery API",
    description="API for ordering food from restaurants. "
                "Built with FastAPI + SQLAlchemy + SQLite.",
    version="1.0.0",
)


# ─── CORS Middleware ─────────────────────────────────────────────────
# Allow all origins during development (Next.js runs on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # In production: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Include Routers ─────────────────────────────────────────────────
app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(dish_router)
app.include_router(order_router)


# ─── Root endpoint ───────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    """Health check / welcome endpoint."""
    return {
        "message": "Food Delivery API is running!",
        "docs": "/docs",
        "version": "1.0.0",
    }
