# Suggested Commands

## General
- `make help`: Show help for makefile commands

## Backend (FastAPI)
- `cd fastapi_backend`
- `poetry install`: Install dependencies
- `poetry run uvicorn app.main:app --reload`: Run backend locally

## Frontend (Next.js)
- `cd nextjs-frontend`
- `pnpm install`: Install dependencies
- `pnpm dev`: Run frontend locally
- `pnpm run generate-client`: Generate API client

## Infrastructure
- `docker-compose up -d`: Start all services
- `docker-compose logs -f`: View logs
- `docker-compose down`: Stop all services

## Code Quality
- `pre-commit run --all-files`: Run pre-commit hooks (linting, formatting)
