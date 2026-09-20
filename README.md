# Xala

Xala is a food-business management application for recording sales, managing a menu, and understanding business performance. It combines a Vue 3 single-page frontend with a FastAPI backend, PostgreSQL, Alembic migrations, and Gemini-powered sales insights.

## Features

- Account registration with email verification.
- JWT login and protected application routes.
- Menu item creation, editing, and deletion, with a maximum of 20 items per user.
- Cart-based sale recording and order creation.
- Revenue analytics by month, week, and day.
- Item sales analytics and top-selling item reports.
- Recent order history with order and line-item details.
- Profile name and store-name updates.
- Password reset by email.
- Gemini-generated sales insights for verified users.


# Get Up and Running with one command

The quickest way to try Xala is with Docker. You do not need to install Python, Node.js, or PostgreSQL first.

1. If not installed Install Docker Desktop or Docker Engine with Docker Compose v2.
2. Clone this repository, or download and extract it.
3. Open a terminal in the project directory.
4. Run below docker compose command to start the application:

```bash
docker compose up --build
```

Open [http://localhost](http://localhost) in your browser. The basic Docker configuration includes local development defaults, so the application and database can start without creating environment files first.

When registering, you may see an email-sending error because email integrations are disabled until you provide a real Mailtrap API key. **Ignore that message and continue to the login page. Your account is created before the verification email is sent, so you can log in and explore the core menu, sales, Analytics and order features.**

Stop the application with `Ctrl+C`, or run `docker compose down` from another terminal. Your database data remains in the `dbvolume` volume unless you remove it with `docker compose down -v`.

## Current Limitations

- **Email verification, password recovery, and AI analytics require API keys.** These features do not work with the default Docker values. Create Google GenAI and Mailtrap API keys, then inject them when starting Compose:

  ```bash
  GEMINI_API_KEY="your-google-genai-key" \\
  MAIL_API_KEY="your-mailtrap-key" \\
  docker compose up --build
  ```

  You can also provide a stronger `SECRET_KEY` in the same command. The keys are passed to the backend container by the Compose configuration, and Docker email links use `http://localhost` by default.
- **Unverified users can create up to five food items.** Verify the account to use the normal maximum of 20 menu items.
- Email verification tokens currently do not expire.
- Configured access-token expiration is not currently encoded into access tokens.
- Docker startup order does not guarantee that PostgreSQL is ready before migrations run. If the backend exits during the first startup, wait for the database and start it again.

## Architecture

```text
Vue 3 + Vite frontend
          |
          | /api/v1/... in the Docker deployment
          v
Nginx reverse proxy  --->  FastAPI /v1/... API
                                  |
                                  v
                         PostgreSQL via SQLModel
```

The frontend uses Axios for API requests, Pinia for authentication state, TanStack Vue Query for server state, and ApexCharts for analytics visualizations. The backend registers all domain routes under the `/v1` prefix.

## Repository Layout

```text
backend/
  main.py                 FastAPI application entrypoint
  config/                 Environment-backed settings
  routes/                 User, menu, cart, order, analytics, and AI routes
  models/                 SQLModel database and response models
  db/                     Database engine and session helpers
  oauth2/                 JWT and password-reset token helpers
  integrations/           Mailtrap email integration
  alembic/                Database migration environment and revisions
frontend/
  src/views/              Application screens
  src/components/         Shared and domain components
  src/composables/        Menu, analytics, sales, and user data logic
  src/router/             Frontend routes and auth guard
  src/api/                Axios client configuration
nginx/
  nginx.conf              Static frontend serving and API proxy
docker-compose.yml        Local multi-container deployment
```

## Requirements

For local development:

- Python 3.10 or newer
- Node.js 18 or newer and npm 9 or newer
- PostgreSQL 18, or a compatible PostgreSQL server
- Gemini API access for AI insights
- Mailtrap API access for verification and password-reset emails

For the containerized setup, install Docker Engine and Docker Compose v2.

## Configuration

### Backend

Create `backend/.env` with the settings required by `backend/config/config.py`:

```env
DATABASE_USER=postgres
DATABASE_PASSWORD=change-me
DATABASE_HOST=localhost
DATABASE_NAME=xala
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEMINI_API_KEY=your-gemini-api-key
MAIL_API_KEY=your-mailtrap-api-key
FRONTEND_URL=http://localhost:5173
```

The backend constructs a PostgreSQL connection using `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, and `DATABASE_NAME`. Do not commit real credentials or API keys.

### Frontend

For Vite development, create `frontend/.env.local`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

The checked-in production frontend configuration uses `/api/`. In the Docker deployment, the browser requests `/api/v1/...`; Nginx strips `/api` and forwards the request to the backend as `/v1/...`. Changing this value requires rebuilding the frontend image.

## Docker Compose

Compose starts three services:

| Service | Purpose | Host address |
| --- | --- | --- |
| `db` | PostgreSQL 18 database | Internal to Compose |
| `backend` | FastAPI API | `http://localhost:8000` |
| `srvr` | Built Vue app served by Nginx | `http://localhost` |

PostgreSQL data is stored in the named `dbvolume` volume. The backend container runs `alembic upgrade heads` before starting FastAPI. The Compose file publishes port 8000 for direct API access and port 80 for the frontend.

The Compose configuration includes safe local defaults for the database, JWT settings, frontend URL, Gemini key, and Mailtrap key. The Gemini and Mailtrap defaults are placeholders and do not enable those integrations. For real integrations, export `GEMINI_API_KEY` and `MAIL_API_KEY` before starting Compose, as shown in [Current Limitations](#current-limitations).

Start the stack from the repository root:

```bash
docker compose up --build
```

Open the application at [http://localhost](http://localhost). Check the API with [http://localhost:8000/v1/health](http://localhost:8000/v1/health).

Useful commands:

```bash
# Start in the background
docker compose up --build -d

# View service status
docker compose ps

# Follow all logs
docker compose logs -f

# Stop containers and keep the database volume
docker compose down

# Stop containers and delete the database volume
docker compose down -v
```

`depends_on` controls startup order but does not wait for PostgreSQL to become ready. If the first startup races the database, inspect the logs and restart the backend after PostgreSQL is ready.

## Local Development

### 1. Start PostgreSQL

Create a PostgreSQL database named `xala`, then set `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, and `DATABASE_NAME` in `backend/.env`.

### 2. Install and start the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade heads
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

On Windows PowerShell, activate the virtual environment with `venv\Scripts\Activate.ps1`.

The API is available at `http://localhost:8000`. The health check is:

```text
GET http://localhost:8000/v1/health
```

### 3. Install and start the frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite normally serves the frontend at `http://localhost:5173`. With `VITE_API_BASE_URL=http://localhost:8000`, it calls the backend directly. The local Vite configuration does not define an `/api` proxy.

## Frontend Routes

Public routes:

- `/login`
- `/register`
- `/forgot-password`
- `/reset-password`
- `/verify-email`

Protected routes:

- `/track-sales`
- `/menu-management`
- `/analytics`
- `/profile`

The root route redirects to `/track-sales`, and `/dashboard` is an alias for the same screen. Unauthenticated users are sent to `/login`. The frontend guard checks for a stored token; token validity and email verification are enforced by the backend.

## Authentication and Account Flows

- Registration creates a user and sends a verification email through Mailtrap.
- Login uses OAuth2 form data at `POST /v1/users/login`, not a JSON request body.
- The login response contains a bearer access token. The frontend stores it in `localStorage` and adds it to API requests.
- Cart operations and AI analytics require a verified email address.
- Password-reset tokens expire after 10 minutes.
- Email-verification tokens currently do not include an expiration claim.
- `ACCESS_TOKEN_EXPIRE_MINUTES` is configured, but the current access-token creation code does not add an `exp` claim. Treat this as a known implementation limitation.

## API Reference

All domain endpoints are prefixed with `/v1`.

### System

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/v1/health` | Health check |
| `GET` | `/` | Root response |

### Users

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/v1/users/` | Register a user |
| `POST` | `/v1/users/login` | Log in with OAuth2 form data |
| `GET` | `/v1/users/me` | Get the current user |
| `PATCH` | `/v1/users/me` | Update name or store name |
| `POST` | `/v1/users/forgot-password/{email}` | Send a password-reset email |
| `POST` | `/v1/users/reset-password` | Set a new password with a reset token |
| `POST` | `/v1/users/verify-email` | Verify an email with a verification token |

### Menu, Cart, and Orders

| Method | Path | Description |
| --- | --- | --- |
| `GET` / `POST` | `/v1/menu/` | List or create menu items |
| `GET` / `PATCH` / `DELETE` | `/v1/menu/{item_id}` | Read, update, or delete a menu item |
| `GET` / `POST` | `/v1/cart/` | List the cart or add an item |
| `PATCH` / `DELETE` | `/v1/cart/{cart_item_id}` | Change quantity or remove a cart item |
| `GET` / `POST` | `/v1/orders/` | List orders or create an order from the cart |
| `GET` / `DELETE` | `/v1/orders/{order_id}` | Read or delete an order |
| `GET` | `/v1/orders/{order_id}/items` | List order line items |

Creating an order clears the current cart. Menu, cart, and order data are scoped to the authenticated user.

### Analytics

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/v1/analytics/monthly-sales/{year}` | Revenue grouped by month |
| `GET` | `/v1/analytics/weekly-sales/{year}/{month}` | Revenue grouped by week |
| `GET` | `/v1/analytics/daily-sales/{year}/{month}/{week}` | Revenue grouped by day |
| `GET` | `/v1/analytics/top-selling-items?limit=5` | Top-selling items |
| `GET` | `/v1/analytics/monthly-item-sales/{year}` | Item quantities by month |
| `GET` | `/v1/analytics/weekly-item-sales/{year}/{month}` | Item quantities by week |
| `GET` | `/v1/analytics/daily-item-sales/{year}/{month}/{week}` | Item quantities by day |

### AI Insights

`POST /v1/ai/analytics` requires a bearer token and a verified user. The request body is:

```json
{
  "data": "How are my sales doing this month?"
}
```

Successful responses have this shape:

```json
{
  "insights": "..."
}
```

The endpoint uses Gemini tools to retrieve sales and top-item data. Responses are framed for a small street-food business and use LKR currency. Each user can make three AI requests during an approximately 24-hour period. Empty prompts are rejected, and Gemini failures return HTTP 502.

## Database Migrations

Alembic migrations are in `backend/alembic/versions/`. The repository currently has multiple migration heads, so use `heads` rather than `head`:

```bash
cd backend
alembic upgrade heads
```

Other useful commands:

```bash
alembic current
alembic history
alembic revision --autogenerate -m "describe the change"
alembic downgrade -1
```

Review autogenerated migrations before applying them. Alembic imports the SQLModel metadata from `backend/models/` when generating revisions.

## Troubleshooting

### Database connection errors

Confirm that PostgreSQL is running and that `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, and `DATABASE_NAME` match the database. In Compose, the database host is `db`, not `localhost`.

### Migration errors on startup

Use `alembic upgrade heads`. With Compose, PostgreSQL may still be initializing when the backend migration command runs; check `docker compose logs db backend` and restart the backend if necessary.

### Frontend requests return 404

For Vite development, set `VITE_API_BASE_URL=http://localhost:8000`. For the Docker frontend, use `/api/` so Nginx can forward `/api/v1/...` to the backend's `/v1/...` routes.

### Verification or password reset emails do not arrive

Check `MAIL_API_KEY`, the Mailtrap account, and `FRONTEND_URL`. The backend sends verification and reset links through Mailtrap.

### AI insights fail

Check `GEMINI_API_KEY`, network access, user verification status, and the per-user request limit. The API returns 502 for upstream Gemini failures and 429 when the request limit is exceeded.

## Development Notes

- CORS middleware is currently commented out in `backend/main.py`; the backend does not currently allow arbitrary cross-origin requests.
- The supported Compose command overrides the standalone backend Dockerfile command and starts `main.py`.
- The Docker frontend bakes its API base URL at build time.
- Do not commit `.env` files, database passwords, JWT secrets, Gemini keys, or Mailtrap keys.
- The project is licensed under the MIT License. See [LICENSE](LICENSE).

## License

Xala is available under the MIT License. See [LICENSE](LICENSE) for the full text.