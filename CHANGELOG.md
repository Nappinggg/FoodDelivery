# CHANGELOG — Food Delivery Platform

All notable progress on this project will be documented in this file.

---

## [2026-05-17] Phase 1 — Backend Foundation (Labs 1-2)

### Database Setup
- [x] Created `database.py` — SQLAlchemy engine (`sqlite:///./food_delivery.db`), `SessionLocal`, `Base`, `get_db()` dependency
- [x] Created `Domain/__init__.py` — package marker
- [x] Created `Domain/Models/__init__.py` — central import of all 5 models

### ORM Models (Domain/Models/)
- [x] `user.py` — Users table (id, full_name, email, password_hash, phone, role)
- [x] `restaurant.py` — Restaurants table (id, name, address, rating, is_active) + cascade delete on dishes
- [x] `dish.py` — Dishes table (id, restaurant_id FK, name, description, price, category)
- [x] `order.py` — Orders table (id, user_id FK, restaurant_id FK, total_price, status, created_at) + cascade delete on items
- [x] `order_item.py` — OrderItems table (id, order_id FK, dish_id FK, quantity, price_at_order)

### Database File
- [x] Created `create_db.py` — script to run `Base.metadata.create_all()`
- [x] Generated `food_delivery.db` (49 KB) with all 5 tables verified

---

## [2026-05-17] Phase 2 — Repositories Layer (Lab 5)

### Repositories (Repositories/)
- [x] `user_repository.py` — UserRepository: `get_all`, `get_by_id`, `get_by_email`, `create`, `update`, `delete`
- [x] `restaurant_repository.py` — RestaurantRepository: `get_all`, `get_active`, `get_by_id`, `create`, `update`, `delete`
- [x] `dish_repository.py` — DishRepository: `get_all`, `get_by_id`, `get_by_restaurant_id`, `create`, `update`, `delete`
- [x] `order_repository.py` — OrderRepository: `get_all`, `get_by_id`, `get_by_user_id`, `create`, `update`, `update_status`, `delete` + OrderItems: `add_item`, `get_items_by_order_id`, `delete_item`
- [x] `__init__.py` — central import of all 4 repositories
- [x] All imports verified via terminal test

---

## [2026-05-17] Phase 2 (continued) — ViewModels (Lab 3)

### Pydantic Schemas (Domain/ViewModels/)
- [x] `user_schema.py` — UserBase, UserCreate, UserUpdate, UserResponse, UserLogin (with EmailStr validation)
- [x] `restaurant_schema.py` — RestaurantBase, RestaurantCreate, RestaurantUpdate, RestaurantResponse
- [x] `dish_schema.py` — DishBase, DishCreate, DishUpdate, DishResponse
- [x] `order_schema.py` — OrderItemBase, OrderItemCreate, OrderItemResponse, OrderCreate, OrderStatusUpdate, OrderResponse
- [x] `__init__.py` — central import of all 19 schema classes
- [x] All schemas use `model_config = ConfigDict(from_attributes=True)` for SQLAlchemy compatibility
- [x] Installed `pydantic[email]` for EmailStr support
- [x] All 19 schema imports verified via terminal test

---

## [2026-05-17] Phase 2 (continued) — BusinessLogic / Services (Lab 4)

### Service Classes (BusinessLogic/)
- [x] `user_service.py` — UserService: create (bcrypt hash), get_all, get_by_id, get_by_email, update, delete, verify_password
- [x] `restaurant_service.py` — RestaurantService: create, get_all, get_active, get_by_id, update, delete (cascade)
- [x] `dish_service.py` — DishService: create, get_all, get_by_id, get_by_restaurant, update, delete
- [x] `order_service.py` — OrderService: create (server-side total_price), get_all, get_by_id, get_by_user, update_status (state machine), cancel
- [x] `__init__.py` — central import of all 4 services
- [x] All 4 service imports verified via terminal test

### Critical Business Rules Enforced
- [x] Password hashing: `passlib[bcrypt]` in UserService.create_user — plain text NEVER stored
- [x] Server-side total_price: OrderService fetches dish prices from DB, multiplies by quantity
- [x] Restaurant is_active check before order creation
- [x] Dish-restaurant ownership validation (dish must belong to specified restaurant)
- [x] Status transition state machine: pending->confirmed->preparing->delivering->delivered/cancelled
- [x] Cancellation only from 'pending' or 'confirmed'

---

## [2026-05-17] Phase 3 — Controllers & Server Assembly (Labs 3, 6)

### Controllers (Controllers/)
- [x] `user_controller.py` — 5 endpoints: GET list, GET by id, POST register, PUT update, DELETE
- [x] `restaurant_controller.py` — 5 endpoints: GET list, GET by id, POST create, PUT update, DELETE
- [x] `dish_controller.py` — 6 endpoints: GET list, GET by restaurant, GET by id, POST create, PUT update, DELETE
- [x] `order_controller.py` — 6 endpoints: GET list, GET by user, GET by id, POST create, PUT status, DELETE cancel
- [x] `__init__.py` — central import of all 4 routers
- [x] All controllers follow architecture rules: NO business logic, only delegation to Services

### Server Assembly (main.py)
- [x] `main.py` — FastAPI app with title "Food Delivery API", version 1.0.0
- [x] CORS Middleware — allow_origins=["*"] for development
- [x] All 4 routers included via app.include_router()
- [x] Auto table creation on startup: Base.metadata.create_all()
- [x] Health check endpoint at root (/)

### Verification
- [x] 22 API endpoints + 5 system endpoints (docs, redoc, openapi.json) = 27 total routes
- [x] Server starts successfully: `uvicorn main:app --reload`
- [x] Root endpoint returns: {"message": "Food Delivery API is running!"}
- [x] GET /api/restaurants/ returns: [] (empty, no seed data yet)
- [x] Swagger UI available at /docs

---

## [2026-05-17] Phase 4 — Frontend (Labs 7-8)

### Project Setup (Lab 7)
- [x] Next.js 15 initialized with TypeScript, App Router, Tailwind CSS v4
- [x] Dark theme design system: brand orange, card backgrounds, glassmorphism navbar
- [x] Custom `globals.css` with CSS variables and custom scrollbar

### Core Infrastructure
- [x] `lib/types.ts` — TypeScript interfaces matching backend schemas (Restaurant, Dish, Order, CartItem)
- [x] `lib/api.ts` — API client with typed fetch wrapper, base URL `http://127.0.0.1:8000/api`
- [x] `lib/cart-context.tsx` — React Context for global cart state (single-restaurant constraint)
- [x] `components/navbar.tsx` — Sticky navbar with cart badge counter

### Pages (Lab 7-8)
- [x] `/` (Home) — Hero section + restaurant grid with emoji banners, ratings, open/closed badges
- [x] `/restaurant/[id]` — Restaurant detail: menu grouped by category, add-to-cart with animation
- [x] `/cart` — Full checkout flow: quantity controls, line totals, place order, success confirmation

### Integration with Backend (Lab 8)
- [x] GET /api/restaurants/ — home page loads restaurant list
- [x] GET /api/restaurants/{id} — restaurant detail page
- [x] GET /api/dishes/restaurant/{id} — menu items
- [x] POST /api/orders/ — checkout creates order with server-side total_price
- [x] GET /api/orders/user/{id} — order history (ready for orders page)

### Verification
- [x] `npm run build` — compiles with 0 TypeScript errors
- [x] Routes: `/` (static), `/cart` (static), `/restaurant/[id]` (dynamic)

---

## [2026-05-17] Frontend Redesign — Light Theme

### Design Changes
- [x] Removed all dark theme / dark: classes
- [x] Background: `bg-orange-50` (warm, almost-white)
- [x] Cards: `bg-white`, `shadow-sm`, `rounded-3xl`, no borders
- [x] Buttons: `rounded-full`, orange-500 accent
- [x] Text: `text-stone-800` (soft dark gray), `text-stone-500` secondary
- [x] Hover: `-translate-y-1` lift + `hover:shadow-md` with `transition-all duration-300`
- [x] More whitespace: `p-6`/`p-8` padding, larger gaps between sections
- [x] Navbar: `bg-white/70 backdrop-blur-xl shadow-sm` glassmorphism
- [x] `npm run build` — 0 errors

---

## [2026-05-17] Unsplash Photo Integration

### Restaurant Cards (app/page.tsx)
- [x] 8 curated Unsplash photos: cozy cafe, restaurant interiors, bakery, pizza oven, coffee, plated food
- [x] `h-48` photo banner with `object-cover`, hover zoom (`group-hover:scale-105`)
- [x] Subtle `bg-gradient-to-t from-black/20` overlay for depth

### Dish Cards (app/restaurant/[id]/page.tsx)
- [x] 10 curated Unsplash food photos: pizza, breakfast, salad, pancakes, burger, latte, pasta, BBQ, cake
- [x] `h-40` photo at top of card with `object-cover`, hover zoom
- [x] Card restructured: photo top → content bottom with `overflow-hidden rounded-3xl`
- [x] `npm run build` — 0 errors

---

## [2026-05-17] Missing Pages & Auth System

### Auth Infrastructure
- [x] `lib/auth-context.tsx` — AuthProvider with localStorage session persistence
- [x] `lib/api.ts` — added `registerUser()`, `getUserById()`, dynamic `userId` for orders
- [x] `lib/types.ts` — added `User` interface
- [x] `app/layout.tsx` — wrapped with `AuthProvider`

### New Pages
- [x] `/auth` — Login/Register form with smooth pill toggle, rounded-2xl inputs, focus rings
- [x] `/profile` — User card with avatar initial, email/phone/ID rows, My Orders link, logout
- [x] `/orders` — Order history with receipt-style cards, color-coded status badges, item list, date, total

### Pagination (Home Page)
- [x] 6 restaurants per page (`PER_PAGE = 6`)
- [x] Rounded-full page number buttons, active = orange-500 pill
- [x] Prev/Next arrows with disabled state

### Navbar Updates
- [x] 📦 Orders link (visible when logged in)
- [x] 👤 Profile link (visible when logged in)
- [x] Avatar initial circle (logged in) or "Sign In" button (logged out)
- [x] Cart page now passes `user.id` for user-aware orders

### Verification
- [x] 7 routes: `/`, `/auth`, `/cart`, `/orders`, `/profile`, `/restaurant/[id]`, `/_not-found`
- [x] `npm run build` — 0 TypeScript errors

---

## [2026-05-18] Checkout Flow (Оплата та Доставка)

### Cart Page Redesign
- [x] 3-step flow: Кошик → Checkout → Успіх
- [x] Форма доставки: вулиця, квартира, коментар для кур'єра (rounded-2xl інпути)
- [x] Перемикач оплати: Готівкою 💵 / Карткою 💳 (card-style radio buttons з ring-2)
- [x] Імітація еквайрингу: 2с спінер при оплаті карткою
- [x] Безпека: адреса/оплата — тільки в React state, API отримує лише `{ restaurant_id, items }`
- [x] Успіх: "Ваше замовлення готується!" + кнопка "Перейти до моїх замовлень"
- [x] Повна українізація UI

---

## All Phases Complete! 🎉

Backend (Labs 1-6): FastAPI + SQLAlchemy + SQLite — fully operational
Frontend (Labs 7-8): Next.js + TypeScript + Tailwind CSS — fully integrated
