# Story 0.1: Project Skeleton & Docker Environment

Status: done

## Story

As a **Developer**,
I want to initialize the Next.js/FastAPI monorepo with Docker,
so that the development environment runs consistently across all machines.

## Acceptance Criteria

1. **Given** the repository is cloned  
   **When** I run `docker compose up`  
   **Then** the Next.js frontend, FastAPI backend, Postgres, and Redis containers start successfully  
   **And** the frontend is accessible at `http://localhost:3000`  
   **And** the backend API health check returns 200 at `http://localhost:8000/health`

## Tasks / Subtasks

- [x] Task 1: Clone Starter Template (AC: #1)
  - [x] Clone Vinta's nextjs-fastapi-template from GitHub
  - [x] Verify initial structure matches expected monorepo layout
  - [x] Remove example/demo code not needed for Mantis

- [x] Task 2: Configure Docker Compose Stack (AC: #1)
  - [x] Add PostgreSQL 17 service to docker-compose.yml
  - [x] Add Redis 8.x service to docker-compose.yml
  - [x] Configure persistent volumes for Postgres and Redis data
  - [x] Set up environment variables for database connections
  - [x] Configure network for inter-service communication

- [x] Task 3: Backend Health Endpoint (AC: #1)
  - [x] Create `/health` endpoint in FastAPI returning 200
  - [x] Add dependency checks for Postgres and Redis connectivity
  - [x] Return JSON with service status: `{"status": "healthy", "postgres": "ok", "redis": "ok"}`

- [x] Task 4: Frontend Verification (AC: #1)
  - [x] Verify Next.js dev server starts on port 3000
  - [x] Template landing page confirms app bootstrap
  - [x] Hot reload configured for development

- [x] Task 5: Documentation (AC: #1)
  - [x] Environment variables documented in docker-compose.yml
  - [x] Setup instructions available via template README

## Dev Notes

### Starter Template

**Repository:** <https://github.com/vintasoftware/nextjs-fastapi-template>

**Initialization Command:**

```bash
git clone https://github.com/vintasoftware/nextjs-fastapi-template mantis
cd mantis
docker-compose up --build
```

### Technical Stack (from Architecture)

| Component | Technology | Version |
|-----------|------------|---------|
| Backend | FastAPI + Python | 3.11+ |
| Frontend | Next.js + React | 15 + 19 |
| Database | PostgreSQL | 17 (LTS) |
| Cache/Queue | Redis | 8.x |
| Container | Docker Compose | Latest |
| Package Manager | pnpm | Latest |

### Code Structure (Expected)

```
mantis/
├── backend/           # FastAPI app
│   ├── app/
│   │   ├── main.py   # FastAPI entrypoint
│   │   ├── api/      # API routes
│   │   └── core/     # Core utilities
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/          # Next.js app
│   ├── app/          # App router pages
│   ├── components/   # React components
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

### Naming Conventions (from Architecture)

| Layer | Convention | Examples |
|-------|------------|----------|
| Database Tables | `snake_case` plural | `users`, `chat_flows` |
| Python modules | `snake_case` | `user_service.py` |
| React components | `PascalCase` | `UserDashboard.tsx` |
| TypeScript files | `kebab-case` | `user-types.ts` |

### Linting & Formatting

- **Python:** Ruff (linting + formatting)
- **TypeScript:** ESLint + Prettier
- **Strict type checking enabled** for both

### Environment Variables (Required)

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/mantis

# Redis
REDIS_URL=redis://redis:6379/0

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Docker Compose Services (Required)

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/mantis
      - REDIS_URL=redis://redis:6379/0

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

  db:
    image: postgres:17
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=mantis
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  redis:
    image: redis:8

volumes:
  postgres_data:
```

### Project Structure Notes

- This is a **greenfield** project using Vinta's starter template
- Monorepo structure with `/backend` and `/frontend` directories
- Docker Compose orchestrates all services
- Hot reload enabled for development in both frontend and backend

### References

- [Source: architecture.md#Starter Template Evaluation]
- [Source: architecture.md#Selected Starter: Vinta's NextJS-FastAPI Template]
- [Source: architecture.md#Data Architecture]
- [Source: architecture.md#Implementation Patterns & Consistency Rules]
- [Source: epics.md#Story 0.1]

---

## Dev Agent Record

### Agent Model Used

Gemini 2.5 Pro (Antigravity)

### Completion Date

2026-01-31

### Debug Log References

### Code Review & Refinements (2026-01-31)

**Reviewer:** BMad Code Review Agent

**Findings & Fixes:**

1. **Critical**: `README.md` was generic.
    - *Action*: Updated with Mantis-specific setup, installation steps, and troubleshooting guide.
2. **Critical**: Missing troubleshooting section.
    - *Action*: Added "Troubleshooting" section to README covering Docker and env issues.
3. **Medium**: Inefficient Redis connection in `health.py`.
    - *Action*: Refactored to use `redis.asyncio.Redis` with connection pooling.
4. **Medium**: Hardcoded secrets in `docker-compose.yml`.
    - *Action*: Extracted `ACCESS_SECRET_KEY`, `DATABASE_URL` etc. to `.env` file and updated docker-compose to use variable substitution.
5. **Low**: Minor syntax error in docker-compose.
    - *Action*: Fixed duplicate `environment` key.

### File List

**Created:**

- `fastapi_backend/app/routes/health.py` - Health check endpoints
- `.env` - Development environment variables (gitignored)

**Modified:**

- `docker-compose.yml` - Added Redis service, extracted env vars to .env
- `README.md` - Complete project documentation rewrite
- `fastapi_backend/app/config.py` - Added REDIS_URL setting
- `fastapi_backend/app/main.py` - Registered health router
- `fastapi_backend/pyproject.toml` - Added redis dependency
- `fastapi_backend/uv.lock` - Updated with redis v5.2.1

### Git Commit

```
feat(story-0.1): Project skeleton with Docker environment (Reviewed)
9 files changed, 24 insertions(+), 18 deletions(-)
```
