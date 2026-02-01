# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mantis Bot is a multi-tenant, AI-powered chatbot platform for managing automated conversations across Facebook and Instagram. The project is a monorepo with a FastAPI backend, Next.js frontend, and Keycloak authentication service.

## Common Commands

### Docker Development (Recommended)

```bash
# Start all services (backend, frontend, db, redis, mailhog)
docker compose up -d

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Run tests in Docker
make docker-test-backend   # Backend pytest
make docker-test-frontend  # Frontend Jest

# Database migrations
make docker-migrate-db                    # Run migrations
make docker-db-schema migration_name="..."  # Create new migration

# Access container shells
make docker-backend-shell   # Backend shell
make docker-frontend-shell  # Frontend shell
```

### Local Development

**Backend (FastAPI):**
```bash
cd fastapi_backend

# Install dependencies (uses uv package manager)
uv sync --group dev

# Run migrations
uv run alembic upgrade head

# Start dev server with hot reload (auto-runs mypy + OpenAPI gen)
./start.sh

# Manual commands
uv run fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload
uv run pytest                 # Run tests
uv run ruff check .           # Lint
uv run ruff format .          # Format
uv run mypy app               # Type check
```

**Frontend (Next.js):**
```bash
cd nextjs-frontend

# Install dependencies (uses pnpm)
pnpm install

# Start dev server with hot reload (auto-generates API client on schema changes)
./start.sh

# Manual commands
pnpm run dev              # Next.js dev server
pnpm run test             # Jest unit tests
pnpm run lint             # ESLint
pnpm run lint:fix         # ESLint auto-fix
pnpm run tsc              # TypeScript check
pnpm run generate-client  # Generate OpenAPI client from backend schema
pnpm run test:e2e         # Playwright E2E tests
```

**Makefile shortcuts:**
```bash
make start-backend    # Start backend locally
make start-frontend   # Start frontend locally
make test-backend     # Run backend tests locally
make test-frontend    # Run frontend tests locally
```

### Single Test Execution

```bash
# Backend - Run specific test file
cd fastapi_backend
uv run pytest tests/test_specific_file.py -v

# Backend - Run specific test function
uv run pytest tests/test_file.py::test_function_name -v

# Frontend - Run specific test file
cd nextjs-frontend
pnpm test path/to/test.test.ts
```

## Architecture

### Monorepo Structure

```
mantis/
├── fastapi_backend/          # Python 3.12 / FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── config.py         # Pydantic settings (env vars)
│   │   ├── database.py       # SQLAlchemy async session
│   │   ├── users.py          # FastAPI-Users auth setup
│   │   ├── schemas.py        # Pydantic models (request/response)
│   │   ├── models.py         # SQLAlchemy ORM models
│   │   ├── routes/           # API route modules
│   │   ├── core/             # Middleware, metrics, logging
│   │   └── email_templates/  # Email templates
│   ├── alembic/              # Database migrations
│   ├── tests/                # pytest tests
│   ├── commands/             # CLI commands (OpenAPI generation)
│   ├── watcher.py            # Dev hot reload (mypy + OpenAPI gen)
│   └── start.sh              # Dev server startup script
├── nextjs-frontend/          # Next.js 15 / React 19 frontend
│   ├── src/
│   │   └── app/              # Next.js App Router
│   ├── client/               # Auto-generated OpenAPI client
│   ├── openapitools.json     # OpenAPI TS generator config
│   ├── watcher.js            # Dev hot reload (client generation)
│   └── start.sh              # Dev server startup script
├── local-shared-data/        # Shared volume for OpenAPI schema
├── postgres/                 # Database initialization scripts
├── e2e/                      # Playwright E2E tests
└── docker-compose.yml        # Full stack orchestration
```

### Backend Architecture (FastAPI)

**Framework:** FastAPI 0.115 with async/await, SQLAlchemy 2.x async ORM

**Key Patterns:**
- **Dependency Injection:** FastAPI's dependency system for database sessions and auth
- **Async-First:** All database operations use `async/await` with asyncpg
- **Modular Routes:** Each domain has its own router in `app/routes/`
- **Pydantic Settings:** Configuration via `app/config.py` with environment variable validation
- **FastAPI-Users:** User management with JWT authentication (see `app/users.py`)

**Authentication Flow:**
1. FastAPI-Users provides JWT auth routes (`/auth/jwt/login`, `/auth/jwt/refresh`)
2. JWT tokens validate via `fastapi_users.authenticator` dependency
3. Protected routes use `current_user` or `current_active_user` dependencies
4. Keycloak integration available but not mandatory (settings: `KEYCLOAK_*`)

**Hot Reload System:**
- `watcher.py` monitors `app/main.py`, `app/schemas.py`, and `app/routes/**/*.py`
- On change: runs mypy type checks → generates OpenAPI schema → restarts FastAPI
- OpenAPI schema written to `local-shared-data/openapi.json`

### Frontend Architecture (Next.js)

**Framework:** Next.js 15 with App Router, React 19, TypeScript 5

**Key Patterns:**
- **App Router:** File-based routing in `src/app/`
- **Type-Safe API:** Auto-generated client from OpenAPI schema (`@hey-api/client-fetch`)
- **shadcn/ui:** Radix UI components with Tailwind styling
- **React Hook Form + Zod:** Form validation with type safety

**Hot Reload System:**
- `watcher.js` monitors `local-shared-data/openapi.json`
- On change: runs `pnpm run generate-client` → regenerates TypeScript API client
- Frontend always stays in sync with backend schema

### Data Layer

**Database:** PostgreSQL 17 with asyncpg driver
**ORM:** SQLAlchemy 2.x with async sessions
**Migrations:** Alembic (versions in `fastapi_backend/alembic/versions/`)

**Key Models:**
- `User` (FastAPI-Users): Email, hashed_password, is_active, is_superuser, is_verified
- `Item` (Example): User-scoped CRUD model with ownership validation

**Cache/Queue:** Redis 8.x for session storage and rate limiting

### API Design

**OpenAPI-First:** All routes documented automatically via FastAPI

**Route Organization:**
- `/auth/jwt/*` - JWT token management
- `/auth/*` - Registration, password reset, email verification
- `/users/*` - User CRUD operations
- `/items/*` - Example resource with pagination
- `/health` - Health check endpoint (postgres + redis status)

**Pagination:** `fastapi-pagination` adds `?page=1&size=50` to list endpoints

**CORS:** Configured via `CORS_ORIGINS` setting (comma-separated or list)

## Important Notes

### Environment Variables

Backend uses `pydantic-settings` with validation. Required vars:
- `DATABASE_URL` - PostgreSQL connection string (asyncpg required)
- `ACCESS_SECRET_KEY` - JWT signing key
- `RESET_PASSWORD_SECRET_KEY` - Password reset tokens
- `VERIFICATION_SECRET_KEY` - Email verification tokens

Optional vars (have defaults):
- `REDIS_URL` - Default: `redis://localhost:6379/0`
- `CORS_ORIGINS` - Default: `http://localhost:3000,http://localhost:8000`
- `KEYCLOAK_*` - Keycloak SSO (optional integration)

Frontend reads `.env.local` for:
- `OPENAPI_OUTPUT_FILE` - Path to backend OpenAPI schema
- `NEXT_PUBLIC_API_URL` - Backend API base URL

### Package Managers

- **Backend:** `uv` (ultra-fast Python package manager, faster than pip)
- **Frontend:** `pnpm` (specified in package.json: 10.7.1)

### Code Quality Standards

**Backend ( enforced in CI ):**
- Ruff linting and formatting
- MyPy type checking
- pytest with ≥80% coverage threshold
- Coverage reports uploaded to Codecov (flag: `backend`)

**Frontend ( enforced in CI ):**
- ESLint with Next.js config
- Prettier formatting
- TypeScript strict mode
- Jest with ≥80% coverage threshold
- Coverage reports uploaded to Codecov (flag: `frontend`)

### Multi-Tenancy Design

**Data Isolation:**
- All resources have `user_id` foreign key
- Routes validate ownership before CRUD operations
- Example: `Item` model scoped to `current_user.id`

**Role-Based Access:**
- `is_superuser` - Admin access to all resources
- `is_active` - Account status check
- `is_verified` - Email verification status

### Testing Strategies

**Backend Tests:**
- `pytest-asyncio` for async test functions
- `pytest-mock` for mocking dependencies
- `factory-boy` for test data generation
- `freezegun` for time-dependent tests

**Frontend Tests:**
- Jest with React Testing Library
- Playwright for E2E (optional in CI)

### Database Migrations

**Creating migrations:**
```bash
# Via Docker
make docker-db-schema migration_name="add user preferences"

# Via local
cd fastapi_backend
uv run alembic revision --autogenerate -m "description"
```

**Running migrations:**
```bash
# Via Docker
make docker-migrate-db

# Via local
cd fastapi_backend
uv run alembic upgrade head
```

### Hot Reload Details

The hot reload system ensures backend-frontend synchronization:

1. **Backend watcher** (`fastapi_backend/watcher.py`):
   - Triggers on changes to `main.py`, `schemas.py`, `routes/*.py`
   - Runs mypy type checks
   - Regenerates OpenAPI schema to `local-shared-data/openapi.json`

2. **Frontend watcher** (`nextjs-frontend/watcher.js`):
   - Triggers on `local-shared-data/openapi.json` changes
   - Runs `pnpm run generate-client`
   - Regenerates TypeScript client in `client/` directory

This enables end-to-end type safety: backend Pydantic models → OpenAPI schema → frontend TypeScript types.
