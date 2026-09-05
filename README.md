# Food Delivery Platform

Full-stack web application for ordering food from restaurants: browse menus, build a cart, place an order and track its status through delivery.

University course project — backend and frontend written from scratch.

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, FastAPI, SQLAlchemy (ORM), SQLite |
| **Frontend** | Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS |
| **Architecture** | Layered: Controllers → Services → Repositories → Database |

## Architecture

The backend is split into four layers, each with a single responsibility. A request travels through all of them and back:

Client → Controller → Service → Repository → Database


- **Controllers** — FastAPI routers. Parse and validate input, then delegate. No business logic.
- **Services** — business rules, stateless.
- **Repositories** — all database access, via SQLAlchemy ORM.
- **Domain** — SQLAlchemy models and Pydantic schemas.

### Order logic

The most interesting part of the project is `BusinessLogic/order_service.py`.

**Totals are calculated server-side.** The client sends only dish IDs and quantities — never a price. The service looks up the current price of each dish and computes the total itself.

**Prices are frozen at order time.** Each `OrderItem` stores `price_at_order`, so a later menu change never rewrites past orders.

**Dishes are checked against the restaurant.** An order for restaurant A cannot contain a dish belonging to restaurant B.

**Order status is a state machine.** Transitions are validated in the service layer — a status cannot skip ahead or move backwards:

pending → confirmed → preparing → delivering → delivered
↓ ↓
cancelled cancelled


`delivered` and `cancelled` are final states.

## Database

Five related tables:

Users ──1:N──> Orders ──1:N──> OrderItems <──N:1── Dishes
↑ ↑
Restaurants ──1:N┘─────────────1:N──────────────────┘


Passwords are hashed with bcrypt (`passlib`) and never stored in plain text. Deleting a restaurant cascades to its dishes.

## API

22 endpoints across 4 routers. Interactive documentation is generated at `/docs` (Swagger UI).

| Router | Prefix | Endpoints |
|---|---|---|
| Users | `/api/users` | list, get, register, update, delete |
| Restaurants | `/api/restaurants` | list, get, create, update, delete |
| Dishes | `/api/dishes` | list, by restaurant, get, create, update, delete |
| Orders | `/api/orders` | list, by user, get, create, update status, cancel |

## Known limitations

This is coursework, and some parts are deliberately simplified:

- **No authentication.** There is no login endpoint and no token handling. The frontend keeps a user ID in `localStorage` and the API trusts it — anyone can act as any user. Password hashing is implemented, but never verified on login.
- **No authorization.** Admin-style endpoints (create restaurant, change order status, delete user) are open to everyone.
- **CORS is wide open** for local development.

Adding JWT auth with a proper `get_current_user` dependency is the next planned step.

## Running Locally

You'll need two terminal windows.

**Backend**

```bash
cd code/backend
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python seed.py                  # populates the database with sample data
uvicorn main:app --reload
```

API runs on `http://localhost:8000`, Swagger UI on `http://localhost:8000/docs`.

**Frontend**

```bash
cd code/frontend
npm install
npm run dev
```

App opens at `http://localhost:3000`.
