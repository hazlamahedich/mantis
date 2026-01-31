# Story 0.1: Project Skeleton & Docker Environment

Status: ready-for-dev

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

- [ ] Task 1: Clone Starter Template (AC: #1)
  - [ ] Clone Vinta's nextjs-fastapi-template from GitHub
  - [ ] Verify initial structure matches expected monorepo layout
  - [ ] Remove example/demo code not needed for Mantis

- [ ] Task 2: Configure Docker Compose Stack (AC: #1)
  - [ ] Add PostgreSQL 17 service to docker-compose.yml
  - [ ] Add Redis 8.x service to docker-compose.yml
  - [ ] Configure persistent volumes for Postgres data
  - [ ] Set up environment variables for database connections
  - [ ] Configure network for inter-service communication

- [ ] Task 3: Backend Health Endpoint (AC: #1)
  - [ ] Create `/health` endpoint in FastAPI returning 200
  - [ ] Add dependency checks for Postgres and Redis connectivity
  - [ ] Return JSON with service status: `{"status": "healthy", "postgres": "ok", "redis": "ok"}`

- [ ] Task 4: Frontend Verification (AC: #1)
  - [ ] Verify Next.js dev server starts on port 3000
  - [ ] Add minimal landing page confirming app bootstrap
  - [ ] Configure hot reload for development

- [ ] Task 5: Documentation (AC: #1)
  - [ ] Update README.md with setup instructions
  - [ ] Document environment variables required
  - [ ] Add troubleshooting section for common Docker issues

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

_To be filled by dev agent_

### Debug Log References

_To be filled during implementation_

### Completion Notes List

_To be filled after implementation_

### File List

_To be filled with files created/modified_
