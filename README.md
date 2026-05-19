# 📌 Концепт Проєкту: "Сайт доставки їжі" (Food Delivery Platform)

**Ціль проєкту:** Розробити вебдодаток для замовлення їжі, де користувачі можуть переглядати меню ресторанів, додавати страви у кошик та оформлювати замовлення, а система відслідковуватиме зміну статусів замовлення.

## Стек технологій

| Компонент | Технологія |
|-----------|-----------|
| **Backend** | Python 3, FastAPI, SQLAlchemy (ORM), SQLite (файлова СУБД) |
| **Frontend** | Next.js (React, App Router), TypeScript, Tailwind CSS |
| **Аутентифікація** | JWT (access + refresh tokens), `passlib[bcrypt]` для хешування паролів |
| **Архітектура** | Багаторівнева: Controllers → BusinessLogic/Services → Repositories → Database |


## 🚀 Інструкція із запуску (Локально)

Щоб запустити проєкт, вам знадобиться 2 відкритих вікна терміналу (одне для сервера, інше для клієнта).

### Крок 1. Запуск Backend (Серверна частина)
У першому терміналі перейдіть до папки бекенду:
bash
cd code/backend
Створіть віртуальне середовище:

Bash
python -m venv venv
Активуйте віртуальне середовище:

Для Windows: .\venv\Scripts\activate (або cmd, а потім venv\Scripts\activate)

Для MacOS/Linux: source venv/bin/activate

Встановіть залежності:

Bash
pip install -r requirements.txt
Заповніть базу даних тестовими ресторанами (обов'язково для першого запуску):

Bash
python seed.py
Запустіть сервер:

Bash
uvicorn main:app --reload
✅ API запрацює за адресою: http://localhost:8000
✅ Документація Swagger (панель керування БД): http://localhost:8000/docs

Крок 2. Запуск Frontend (Клієнтська частина)
У другому терміналі перейдіть до папки фронтенду:

Bash
cd code/frontend
Встановіть Node-залежності:

Bash
npm install
Запустіть клієнтський застосунок:

Bash
npm run dev
✅ Сайт відкриється у браузері за адресою: http://localhost:3000

✨ Основний функціонал
Авторизація та реєстрація користувачів (з безпечним хешуванням паролів).

Перегляд списку доступних ресторанів та їх меню.

Додавання страв у кошик із підрахунком загальної суми.

Імітація процесу оформлення замовлення (Checkout) з вибором оплати.

Збереження історії замовлень у профілі користувача.


Ці два файли повністю знімають будь-які питання. Проєкт виглядає завершеним, професійно запакованим і готовим до презентації. Готовий додавати їх у папки?




---

## ⚙️ План розробки Backend (Лабораторні 1–6)

Викладач вимагає сувору структуру папок та чіткий розподіл обов'язків між шарами коду.

### 1. База даних (Лабораторна 1)

**Вимога викладача:** Мінімум 3 зв'язані таблиці, мінімум по 5 колонок у кожній. Наповнити даними. Реалізувати 4 базові CRUD операції (Create, Read, Update, Delete).

**План реалізації:** Створюємо **5 таблиць** за допомогою SQLAlchemy. Дані зберігаються у локальному файлі `food_delivery.db`. Для візуального перегляду бази — програма DB Browser for SQLite.

#### Таблиця `Users`

| Колонка | Тип | Примітки |
|---------|-----|----------|
| `id` | Integer, PK | Auto-increment |
| `full_name` | String | |
| `email` | String, Unique | |
| `password_hash` | String | Хешування через `passlib[bcrypt]`, plain text НІКОЛИ не зберігається |
| `phone` | String | |
| `role` | String | `"customer"` або `"admin"` |

#### Таблиця `Restaurants`

| Колонка | Тип | Примітки |
|---------|-----|----------|
| `id` | Integer, PK | Auto-increment |
| `name` | String | |
| `address` | String | |
| `rating` | Float | 0.0–5.0 |
| `is_active` | Boolean | Чи приймає ресторан замовлення зараз |

#### Таблиця `Dishes`

| Колонка | Тип | Примітки |
|---------|-----|----------|
| `id` | Integer, PK | Auto-increment |
| `restaurant_id` | Integer, FK → `Restaurants.id` | `cascade="all, delete-orphan"` — при видаленні ресторану видаляються його страви |
| `name` | String | |
| `description` | String | |
| `price` | Float | |
| `category` | String | Наприклад: "Піца", "Суші", "Напої" |

#### Таблиця `Orders`

| Колонка | Тип | Примітки |
|---------|-----|----------|
| `id` | Integer, PK | Auto-increment |
| `user_id` | Integer, FK → `Users.id` | |
| `restaurant_id` | Integer, FK → `Restaurants.id` | |
| `total_price` | Float | Розраховується ТІЛЬКИ на сервері (в `OrderService`), не довіряємо клієнту |
| `status` | String (Enum) | Визначені переходи — див. нижче |
| `created_at` | DateTime | UTC |

#### Таблиця `OrderItems` *(нова — зв'язок замовлення ↔ страви)*

| Колонка | Тип | Примітки |
|---------|-----|----------|
| `id` | Integer, PK | Auto-increment |
| `order_id` | Integer, FK → `Orders.id` | `cascade="all, delete-orphan"` |
| `dish_id` | Integer, FK → `Dishes.id` | |
| `quantity` | Integer | ≥ 1 |
| `price_at_order` | Float | Фіксує ціну страви на момент замовлення (ціна може змінитися пізніше) |

#### Статуси замовлення (Enum)

```
pending → confirmed → preparing → delivering → delivered
                                              ↘ cancelled
```

Переходи між статусами валідуються у `OrderService`. Неможливо перескочити або повернутися назад.

#### ER-діаграма

```
Users ──1:N──> Orders ──1:N──> OrderItems <──N:1── Dishes
                  ↑
Restaurants ──1:N─┘
Restaurants ──1:N──> Dishes
```

---

### 2. Структура проєкту та Моделі (Лабораторна 2)

**Вимога викладача:** Створити папки на сервері: Controllers, Repositories, BusinessLogic, Domain. У Domain створити ViewModels та перенести таблиці з БД у вигляді класів (Models).

**План реалізації:**

"""
backend/
├── main.py                         # Точка входу FastAPI, CORS, підключення роутерів
├── database.py                     # SQLAlchemy engine + SessionLocal + Base
├── Domain/
│   ├── Models/                     # SQLAlchemy ORM-моделі (діалект SQLite)
│   │   ├── user.py
│   │   ├── restaurant.py
│   │   ├── dish.py
│   │   ├── order.py
│   │   └── order_item.py
│   └── ViewModels/                 # Pydantic-схеми для валідації вхідних/вихідних даних
│       ├── user_vm.py
│       ├── restaurant_vm.py
│       ├── dish_vm.py
│       ├── order_vm.py
│       └── order_item_vm.py
├── Repositories/                   # Шар роботи з БД (SQLAlchemy queries)
│   ├── user_repository.py
│   ├── restaurant_repository.py
│   ├── dish_repository.py
│   ├── order_repository.py
│   └── order_item_repository.py
├── BusinessLogic/                  # Шар сервісів (бізнес-правила, DI)
│   ├── auth_service.py
│   ├── user_service.py
│   ├── restaurant_service.py
│   ├── dish_service.py
│   └── order_service.py
└── Controllers/                    # FastAPI роутери (ендпоінти)
    ├── auth_controller.py
    ├── user_controller.py
    ├── restaurant_controller.py
    ├── dish_controller.py
    └── order_controller.py

"""
---

### 3. Контролери та Запити (Лабораторна 3)

**Вимога викладача:** 5–8 контролерів, мінімум 15 запитів. Описати лише методи, параметри та типи даних на виході (без логіки). Використовувати ViewModels.

**План реалізації (5 контролерів, 17 ендпоінтів):**

| # | Controller | Method | Endpoint | Опис |
|---|-----------|--------|----------|------|
| 1 | Auth | POST | `/api/auth/login` | Авторизація, повертає JWT |
| 2 | Auth | POST | `/api/auth/register` | Реєстрація нового користувача |
| 3 | Auth | POST | `/api/auth/refresh` | Оновлення access token |
| 4 | User | GET | `/api/users/profile` | Отримати профіль поточного юзера |
| 5 | User | PUT | `/api/users/profile` | Оновити профіль |
| 6 | Restaurant | GET | `/api/restaurants` | Список ресторанів (з пагінацією: `skip`, `limit`) |
| 7 | Restaurant | GET | `/api/restaurants/{id}` | Деталі одного ресторану |
| 8 | Restaurant | POST | `/api/restaurants` | Створити ресторан (admin) |
| 9 | Dish | GET | `/api/restaurants/{id}/dishes` | Меню ресторану |
| 10 | Dish | POST | `/api/dishes` | Додати страву (admin) |
| 11 | Dish | PUT | `/api/dishes/{id}` | Оновити страву |
| 12 | Dish | DELETE | `/api/dishes/{id}` | Видалити страву |
| 13 | Order | POST | `/api/orders` | Створити замовлення (з items) |
| 14 | Order | GET | `/api/orders` | Замовлення поточного юзера (з пагінацією) |
| 15 | Order | GET | `/api/orders/{id}` | Деталі замовлення |
| 16 | Order | PUT | `/api/orders/{id}/status` | Змінити статус (admin) |
| 17 | Order | DELETE | `/api/orders/{id}` | Скасувати замовлення |

---

### 4. Бізнес-логіка (Лабораторна 4)

**Вимога викладача:** Створити класи Service. Вони не зберігають стан, а виконують логіку. Обов'язкове використання Dependency Injection.

**План реалізації:**

- **AuthService:** JWT генерація/валідація, хешування пароля через `passlib[bcrypt]`, перевірка credentials.
- **UserService:** Отримання/оновлення профілю.
- **RestaurantService:** CRUD, фільтрація, перевірка `is_active`.
- **DishService:** CRUD, прив'язка до ресторану.
- **OrderService:**
  - Перевірка, чи ресторан `is_active` перед створенням замовлення.
  - **Серверний розрахунок `total_price`** — сума `(price_at_order × quantity)` для кожного `OrderItem`. Ніколи не довіряємо клієнту.
  - Валідація переходів між статусами (Enum state machine).
  - Скасування замовлення (тільки зі статусу `pending` або `confirmed`).

**Dependency Injection** через `Depends()`:
```python
# Контролер отримує сервіс:
@router.post("/orders")
def create_order(data: OrderCreate, service: OrderService = Depends()):
    return service.create_order(data)

# Сервіс отримує репозиторій:
class OrderService:
    def __init__(self, repo: OrderRepository = Depends()):
        self.repo = repo
```

---

### 5. Репозиторії (Лабораторна 5)

**Вимога викладача:** Реалізувати прямі запити до бази даних у папці Repositories, які викликатимуться з BusinessLogic.

**План реалізації:**

Кожен Repository містить методи CRUD:
- `get_by_id(id)`, `get_all(skip, limit)` — з **пагінацією** для списків
- `create(entity)`, `update(id, data)`, `delete(id)`
- Спеціалізовані: `OrderRepository.get_by_user_id()`, `DishRepository.get_by_restaurant_id()`

Усі запити — через SQLAlchemy ORM, що транслюються в SQL для SQLite.

---

### 6. Збірка Сервера (Лабораторна 6)

**Вимога викладача:** Зібрати все докупи. Повноцінний сервер, де запит йде: Контролер → Сервіс → Репозиторій → База даних і повертається назад клієнту.

**План реалізації:**

- **`main.py`:**
  - Рядок підключення: `sqlite:///./food_delivery.db`
  - **CORS Middleware** — дозвіл запитів з `http://localhost:3000` (Next.js)
  - Підключення всіх 5 роутерів (контролерів)
  - **Глобальний Exception Handler** — уніфіковані JSON-відповіді для помилок (400, 401, 403, 404, 500)
- Тестування API через **Swagger UI** (автоматично на `/docs`)
- Для здачі — архів із папкою проєкту + готовий файл `food_delivery.db`

---

## 💻 План розробки Frontend (Лабораторні 7–8)

### 7. Ініціалізація та Структура (Лабораторна 7)

**Вимога:** Побудувати базовий UI та підключити маршрутизацію.

**План реалізації:**

- Next.js (App Router) + TypeScript + Tailwind CSS
- **Сторінки:**
  - `/` — Головна (каталог ресторанів із пагінацією)
  - `/restaurant/[id]` — Сторінка ресторану (меню зі стравами)
  - `/cart` — Кошик
  - `/profile` — Профіль користувача
  - `/auth` — Авторизація / Реєстрація
  - `/orders` — Історія замовлень та відслідковування статусу
- **Глобальний стан кошика** через Zustand або React Context
  - Зберігає: `restaurant_id`, масив `{dish_id, name, price, quantity}`
  - Обмеження: замовлення тільки з одного ресторану одночасно

---

### 8. Інтеграція з Backend та Бізнес-процеси (Лабораторна 8)

**Вимога:** Підключити бекенд, відправити реальні запити (17 ендпоінтів).

**План реалізації:**

- **API-клієнт** (axios або fetch) з базовим URL `http://localhost:8000/api`
- **Авторизація:**
  - Login → отримання access + refresh JWT
  - Збереження в `localStorage` або cookies
  - Автоматичний refresh при 401
  - Захищені сторінки перенаправляють на `/auth`
- **Флоу замовлення:**
  1. Юзер переглядає меню ресторану
  2. Додає страви в кошик (глобальний стан)
  3. Переходить у кошик → бачить підсумок
  4. Натискає "Замовити" → `POST /api/orders` з масивом `items`
  5. Сервер розраховує `total_price`, створює замовлення
  6. Юзер бачить статус замовлення на сторінці `/orders`

---

## 📋 Порядок реалізації

```
Phase 1 — Backend Foundation (Labs 1–2)
  ├── database.py (engine, session, Base)
  ├── Domain/Models/ (5 таблиць, включаючи OrderItems)
  ├── Domain/ViewModels/ (Pydantic schemas)
  └── Seed data script

Phase 2 — Backend API Layer (Labs 3–5)
  ├── Repositories/ (CRUD + пагінація)
  ├── BusinessLogic/ (Services з DI, Enum статусів)
  └── Controllers/ (Routers, тільки виклик сервісів)

Phase 3 — Backend Assembly (Lab 6)
  ├── main.py (CORS, global error handler, router includes)
  ├── Swagger testing
  └── food_delivery.db з seed data

Phase 4 — Frontend (Labs 7–8)
  ├── Next.js init + pages + routing
  ├── API client + JWT auth flow
  └── Cart state + order flow + status tracking
```
