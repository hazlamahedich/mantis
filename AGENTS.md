# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Mantis Bot is a multi-tenant, AI-powered chatbot platform for managing automated conversations across Facebook and Instagram. Built with a FastAPI backend and Next.js 15 frontend, deployed via Docker Compose.

**Tech Stack:**
- Backend: FastAPI (Python 3.12), PostgreSQL 17 (asyncpg), Redis 8.x
- Frontend: Next.js 15, React 19, TypeScript
- Infrastructure: Docker Compose, Alembic (migrations)
- Authentication: fastapi-users with JWT

## Development Commands

### Starting the Environment

```bash
# Start all services (recommended for development)
docker compose up -d

# Access containers
make docker-backend-shell   # Backend container shell
make docker-frontend-shell  # Frontend container shell
```

### Backend Development

```bash
# Run backend locally (requires Python 3.12, uses uv)
cd fastapi_backend && ./start.sh

# Run tests
cd fastapi_backend && uv run pytest
# Or via Docker
make docker-test-backend

# Database migrations
make docker-migrate-db                                    # Apply migrations
make docker-db-schema migration_name="description here"   # Generate new migration

# Type checking
cd fastapi_backend && uv run mypy app/
```

### Frontend Development

```bash
# Run frontend locally (requires pnpm)
cd nextjs-frontend && ./start.sh

# Run tests
cd nextjs-frontend && pnpm run test

# Linting and formatting
cd nextjs-frontend && pnpm run lint
cd nextjs-frontend && pnpm run lint:fix
cd nextjs-frontend && pnpm run prettier

# Type checking
cd nextjs-frontend && pnpm run tsc

# Generate API client from OpenAPI spec
cd nextjs-frontend && pnpm run generate-client
```

### Testing Individual Components

```bash
# Backend: Run specific test file
cd fastapi_backend && uv run pytest tests/test_database.py

# Backend: Run specific test function
cd fastapi_backend && uv run pytest tests/routes/test_items.py::test_create_item

# Frontend: Run specific test file
cd nextjs-frontend && pnpm run test -- __tests__/specific-test.test.tsx
```

## Architecture

### Backend Structure

**Core Application (`fastapi_backend/app/`):**
- `main.py` - FastAPI application entry point, registers all routers
- `config.py` - Pydantic settings for environment variables
- `database.py` - Async SQLAlchemy session management
- `models.py` - SQLAlchemy ORM models (User, Item)
- `schemas.py` - Pydantic schemas for API validation
- `users.py` - fastapi-users authentication setup with custom UserManager
- `routes/` - API endpoint routers organized by resource

**Authentication Flow:**
- Uses fastapi-users library with JWT bearer tokens
- UserManager in `users.py` handles password validation, registration, password reset
- Auth endpoints: `/auth/jwt/login`, `/auth/register`, `/auth/forgot-password`, `/auth/reset-password`
- Protected routes use `current_active_user` dependency

**Database Management:**
- Alembic migrations in `alembic_migrations/versions/`
- Async SQLAlchemy with asyncpg driver
- Models use UUID primary keys
- Test database configured separately (see `conftest.py`)

**Testing:**
- `tests/conftest.py` - Shared fixtures including `test_client`, `db_session`, `authenticated_user`
- Tests use a separate test database (TEST_DATABASE_URL)
- Each test function gets fresh DB schema via fixture

### Frontend Structure

**App Router (`nextjs-frontend/app/`):**
- Uses Next.js 15 App Router architecture
- `layout.tsx` - Root layout with metadata
- `page.tsx` - Landing/home page
- `dashboard/` - Protected dashboard area with items CRUD
- `login/`, `register/`, `password-recovery/` - Auth pages

**API Client:**
- Auto-generated from backend OpenAPI spec via `@hey-api/openapi-ts`
- Located in `app/openapi-client/`
- Backend exports OpenAPI JSON to `shared-data/` volume, frontend watches and regenerates
- Client config in `lib/clientConfig.ts`

**State Management:**
- No global state library; uses React hooks and form libraries
- react-hook-form with zod validation for forms

**Styling:**
- Tailwind CSS with custom configuration
- Radix UI components in `components/`
- shadcn/ui style component structure

### Key Architectural Patterns

**Multi-tenancy:**
- User model from fastapi-users provides user isolation
- Items have `user_id` foreign key for user-scoped data
- All queries should filter by current user

**Shared Data Volume:**
- Backend writes OpenAPI spec to `local-shared-data/openapi.json`
- Frontend watches this file and regenerates TypeScript client
- Both containers mount this volume in docker-compose

**Hot Reload:**
- Backend: `start.sh` runs FastAPI in dev mode + watcher.py for OpenAPI changes
- Frontend: `start.sh` runs Next.js dev + watcher.js for OpenAPI changes
- Both services automatically restart on relevant file changes

**Password Validation:**
- Minimum 8 characters
- At least one uppercase letter
- At least one special character
- Cannot contain email address

## Environment Configuration

Environment variables are managed in `docker-compose.yml` for development. For local development, create a `.env` file in the root with:

```
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/mydatabase
TEST_DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5433/testdatabase
REDIS_URL=redis://localhost:6379/0
ACCESS_SECRET_KEY=<generate-secure-key>
RESET_PASSWORD_SECRET_KEY=<generate-secure-key>
VERIFICATION_SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=["http://localhost:3000"]
MAIL_SERVER=mailhog
MAIL_PORT=1025
MAIL_STARTTLS=False
MAIL_SSL_TLS=False
USE_CREDENTIALS=False
```

## Common Workflows

### Adding a New API Endpoint

1. Create/update router in `fastapi_backend/app/routes/`
2. Include router in `fastapi_backend/app/main.py`
3. Backend auto-generates OpenAPI spec to shared volume
4. Frontend watcher detects change and regenerates TypeScript client
5. Use generated client in frontend via `app/openapi-client/`

### Adding a Database Model

1. Add model to `fastapi_backend/app/models.py`
2. Create migration: `make docker-db-schema migration_name="add_new_model"`
3. Review generated migration in `alembic_migrations/versions/`
4. Apply migration: `make docker-migrate-db`
5. Add corresponding Pydantic schemas to `schemas.py`

### Testing Strategy

**Backend:**
- Unit tests for business logic
- Integration tests use real test database
- `authenticated_user` fixture provides pre-authenticated test user
- Tests clean up after themselves via fixture teardown

**Frontend:**
- Jest + Testing Library for component tests
- Tests located in `__tests__/` directory
- Test utilities in `jest.config.ts`

## Troubleshooting

### Backend Container Issues
- Stale venv: `docker volume rm mantis_fastapi-venv && docker compose up -d --build`
- Check logs: `docker compose logs backend`

### Frontend Container Issues
- Stale node_modules: `docker volume rm mantis_nextjs-node-modules && docker compose up -d --build`
- Check logs: `docker compose logs frontend`

### Database Connection Issues
- Ensure db container is healthy: `docker compose ps`
- For external connections: `localhost:5432` (main), `localhost:5433` (test)

### MailHog (Email Testing)
- Web UI: http://localhost:8025
- SMTP: localhost:1025
- All emails sent by backend appear here in development
