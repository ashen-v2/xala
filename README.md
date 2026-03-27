# Xala v1

Full-stack food business management app with a FastAPI backend and a Vue 3 frontend.

## What This Project Does

- Authenticates users with JWT tokens.
- Lets each user manage a menu (up to 20 items).
- Supports cart-based sale recording and order creation.
- Provides revenue and item analytics (monthly, weekly, daily).
- Adds AI-generated business insights using Gemini.

## Repository Structure

- `backend/`: FastAPI API, SQLModel models, Alembic migrations, auth, analytics, AI routes.
- `frontend/`: Vue 3 + Vite single-page app (sales, menu management, analytics, profile).

## Tech Stack

### Backend

- Python 3
- FastAPI
- SQLModel / SQLAlchemy
- Alembic
- PyJWT
- Pydantic + pydantic-settings
- Google GenAI (Gemini)
- Mailtrap SDK

### Frontend

- Vue 3 (Composition API)
- Vite
- Pinia
- Vue Router
- Axios
- TanStack Vue Query
- ApexCharts
- Tailwind CSS
- Vee Validate + Yup

## High-Level Architecture

- Frontend calls backend REST endpoints under `/v1`.
- Backend validates JWT bearer tokens for protected endpoints.
- Backend stores business data in SQL database using SQLModel ORM.
- Alembic handles schema migrations.
- Analytics endpoints aggregate order/order_item data.
- AI endpoint uses Gemini with tool-calling functions that read analytics data.

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- A SQL database reachable by the backend connection string
- Gemini API key
- Mailtrap API key

## Environment Variables

Create `backend/.env` with:

```env
database_url=postgresql+psycopg://user:password@host:5432/dbname
secret_key=change-me
algorithm=HS256
access_token_expire_minutes=60
gemini_api_key=your-gemini-key
mail_api_key=your-mailtrap-key
frontend_url=http://localhost:5173
```

Create `frontend/.env.local` with:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Backend Setup

Run these commands from `xala/backend`:

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Apply migrations:

```bash
alembic upgrade head
```

Start API server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```text
GET http://localhost:8000/v1/health
```

## Frontend Setup

Run these commands from `xala/frontend`:

```bash
npm install
npm run dev
```

Vite default local URL is usually:

```text
http://localhost:5173
```

## API Summary

All API routes are mounted under `/v1`.

### Users (`/v1/users`)

- `POST /`: register user
- `POST /login`: login with `application/x-www-form-urlencoded`
- `GET /me`: current user profile (auth required)
- `PATCH /me`: update current user (auth required)
- `POST /forgot-password/{email}`: request password reset
- `POST /reset-password`: reset password with reset token

### Menu (`/v1/menu`)

- `GET /`: list current user's menu items
- `GET /{item_id}`: get one menu item
- `POST /`: create menu item
- `PATCH /{item_id}`: update menu item
- `DELETE /{item_id}`: delete menu item

Notes:
- Menu table is auto-created per user when needed.
- Max menu item count is enforced at 20 per user.

### Cart (`/v1/cart`)

- `POST /`: add item to cart
- `GET /`: list cart items
- `PATCH /{cart_item_id}`: update quantity
- `DELETE /{cart_item_id}`: remove item

### Orders (`/v1/orders`)

- `POST /`: create order from cart and clear cart
- `GET /`: list orders
- `GET /{order_id}`: order details
- `GET /{order_id}/items`: order items with product names
- `DELETE /{order_id}`: delete order

### Analytics (`/v1/analytics`)

- `GET /monthly-sales/{year}`
- `GET /weekly-sales/{year}/{month}`
- `GET /daily-sales/{year}/{month}/{week}`
- `GET /top-selling-items?limit=5`
- `GET /monthly-item-sales/{year}`

### AI (`/v1/ai`)

- `POST /analytics`: generate insights from analytics data

Request body:

```json
{
  "data": "How are my sales doing this month?"
}
```

Response body:

```json
{
  "insights": "..."
}
```

## Frontend Features

- Auth screens: register, login, forgot password, reset password.
- Track sales screen: add menu items to cart and create orders.
- Menu management screen: create/update/delete menu items.
- Analytics dashboard: revenue charts, top items, monthly item volume, AI insights panel.
- Profile screen: view and update user profile.

## Frontend Routing

Public routes:

- `/register`
- `/login`
- `/forgot-password`
- `/reset-password`

Protected routes:

- `/track-sales`
- `/analytics`
- `/menu-management`
- `/profile`

Route guard behavior:

- Unauthenticated users are redirected to `/login` for protected routes.
- Authenticated users visiting public auth pages are redirected to `/track-sales`.

## Authentication Flow

- Login returns `{ access_token, token_type }`.
- Frontend stores token in `localStorage` and sends it as `Authorization: Bearer <token>`.
- Backend decodes JWT to resolve `user_id` for protected operations.

## Migrations

Common Alembic commands from `xala/backend`:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
alembic downgrade -1
```

## Development Notes

- Backend CORS currently allows all origins/methods/headers (development-friendly, tighten for production).
- Access tokens currently do not include expiry claims in access token creation logic.
- Backend dependency file may appear UTF-16 encoded in some editors/tools.
- Frontend commands must be run from `xala/frontend`.

## Troubleshooting

- `401 Invalid token`: login again and ensure bearer token is set in requests.
- `422` on `/v1/users/login`: send form data, not JSON.
- AI endpoint failures (`502`): verify `gemini_api_key` and network access.
- Password reset link issues: verify `frontend_url` in backend env.
- Database startup errors: verify `database_url` and run `alembic upgrade head`.

## Useful Paths

- `backend/main.py`: API entrypoint and router registration.
- `backend/config/config.py`: required backend environment variables.
- `backend/routes/`: route modules by domain.
- `backend/alembic/versions/`: migration history.
- `frontend/src/router/index.js`: route definitions and auth guard.
- `frontend/src/api/axios.js`: base URL and auth header injection.
- `frontend/src/composables/`: domain data logic.
- `frontend/docs/menu-management-ui.md`: menu UI design reference.

