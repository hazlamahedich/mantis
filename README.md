# Mantis Bot 🦗

[![CI](https://github.com/YOUR_USERNAME/mantis/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/mantis/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/mantis/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/mantis)

A multi-tenant, AI-powered chatbot platform for managing automated conversations across Facebook and Instagram.

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (v2+)
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url> mantis
   cd mantis
   ```

2. **Start the environment**

   ```bash
   docker compose up -d
   ```

   This will spin up:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:8000](http://localhost:8000)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **MailHog**: [http://localhost:8025](http://localhost:8025)
   - **PostgreSQL**: Port 5432
   - **Redis**: Port 6379

3. **Verify Installation**
   Check the health endpoint:

   ```bash
   curl http://localhost:8000/health
   # Expected: {"status": "healthy", "postgres": "ok", "redis": "ok"}
   ```

## 🛠 Technology Stack

- **Backend**: FastAPI (Python 3.12)
- **Frontend**: Next.js 15 (React 19, TypeScript)
- **Database**: PostgreSQL 17 + asyncpg
- **Cache/Queue**: Redis 8.x
- **Infrastructure**: Docker Compose

## 🔧 Configuration

Environment variables are currently managed in `docker-compose.yml` for development.

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Postgres connection string | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379/0` |
| `ACCESS_SECRET_KEY` | JWT signing key | `dev-access-secret...` |

**Security Note:** For production, use a `.env` file and never commit secrets to version control.

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for continuous integration with quality gates.

### Quality Gates

- **Backend**: Ruff linting, formatting checks, and pytest with 80% coverage threshold
- **Frontend**: ESLint, Prettier, TypeScript checks, and Jest with 80% coverage threshold
- **E2E**: Playwright tests (optional, doesn't block pipeline)

### Branch Protection

For production deployments, configure branch protection rules on GitHub:

1. Go to **Settings → Branches**
2. Add rule for `main` branch:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select required checks: `Lint Backend`, `Lint Frontend`, `Test Backend`, `Test Frontend`

### Coverage Reports

Coverage reports are automatically uploaded to Codecov. To enable:

1. Go to [Codecov](https://codecov.io/) and sign in with GitHub
2. Add `CODECOV_TOKEN` to repository secrets (Settings → Secrets and variables → Actions)

## ❓ Troubleshooting

### Docker Containers Failed to Start

1. **Check logs**: `docker compose logs backend`
2. **Rebuild containers**: `docker compose up -d --build`
3. **Port conflicts**: Ensure ports 3000, 8000, 5432, 6379 are free.

### "No module named redis" Error

This occurs if the venv volume is stale. Force a rebuild:

```bash
docker compose down
docker volume rm mantis_fastapi-venv
docker compose up -d --build
```

### Database Connection Refused

Ensure the `db` container is healthy. If using an external DB tool, connect to `localhost:5432`.

---
*Based on Vinta's Next.js FastAPI Template*
