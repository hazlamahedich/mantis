---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - /Users/sherwingorechomante/mantis/Mantis_Bot_PRD.md
  - /Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/brainstorming/brainstorming-session-2026-01-31.md
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-01-31'
project_name: 'mantis'
user_name: 'team mantis'
date: '2026-01-31'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery._

---

## Project Context Analysis

### Requirements Overview

**Functional Requirements (13 major areas):**

| Category | Key Requirements |
|----------|------------------|
| Authentication | RBAC, OAuth2/JWT, Keycloak integration |
| Bot Management | CRUD bots, platform connectors, test/live environments |
| Connectors | Messenger + Telegram (MVP), plugin architecture (Phase 2) |
| Flow System | Goal-driven flows with entry/exit conditions, rules, actions |
| Rules Engine | Keyword match, button clicks, tags, variables, fallback |
| Actions | Text, buttons, variables, tags, webhooks, flow jumps |
| Skills System | Reusable mini-flows, versioning, marketplace |
| State Management | Current goal, active flow, variables, tags, history |
| Simulator | Chat UI, rule tracing, goal progress, replay |
| Explainability | Why-sent, rule triggered, alternatives skipped |
| Broadcasting | Tag-based sends, throttling, opt-out |
| Flexible LLM | Ollama (self-hosted) + cloud providers (MVP) |
| E-commerce Pack | Reference skill implementation |

**Non-Functional Requirements:**

| NFR | Requirement |
|-----|-------------|
| Performance | Message processing < 300ms |
| Security | Webhook validation, replay protection, tenant isolation, PII masking |
| Scalability | Horizontal scaling |
| Reliability | Graceful degradation, retry queues |
| Data Ownership | Self-hosted by default |

### Scale & Complexity

- **Project complexity:** Medium-High
- **Primary domain:** Full-stack web platform
- **Real-time features:** Yes (chat, simulator)
- **Multi-tenancy:** Yes (RBAC, tenant isolation)
- **Integration complexity:** Medium (Messenger, Telegram, LLM providers)

### Technical Constraints & Dependencies

- Keycloak for auth (external dependency)
- PostgreSQL for persistence
- Redis for caching/queuing
- Multiple LLM providers (Ollama, OpenAI, Anthropic)

### Cross-Cutting Concerns

1. **Authentication/Authorization** — Spans all endpoints
2. **Multi-tenancy** — Data isolation across all components
3. **LLM Abstraction** — Must support multiple providers
4. **Event/Webhook Handling** — Security + rate limiting
5. **Explainability Logging** — All decisions must be traceable

---

## Party Mode Insights (Agent Perspectives)

### 🏗️ Winston (Architect)

- **Concern:** Multi-tenancy isolation strategy
- **Recommendation:** Decide DB-level vs app-level isolation early
- **Note:** Flexible LLM in MVP forces good abstraction layer design

### 💻 Amelia (Dev)

- **Concern:** Skills System is essentially a mini package manager
- **Key Decisions Needed:**
  1. Skill schema format (JSON? YAML?)
  2. Version resolution strategy
  3. Conflict detection algorithm

### 🎨 Sally (UX Designer)

- **Concern:** "Partner, Not Tool" positioning requires adaptive UI
- **Recommendations:**
  - Onboarding that learns user's business
  - Proactive suggestions ("I noticed you haven't set up X...")
  - Personality consistency across all touchpoints

### 🧪 Murat (Test Architect)

- **Concern:** Explainability must be designed test-first
- **Recommendation:** Consider **event sourcing pattern** for conversation state
- **Rationale:** Time-Travel Debugger requires replayable, verifiable decisions

---

## Starter Template Evaluation

### Primary Technology Domain

**Full-stack web platform** with:

- Backend: FastAPI (Python)
- Frontend: Next.js 15 (React/TypeScript)
- Database: PostgreSQL
- Cache/Queue: Redis
- Auth: Keycloak
- Container: Docker

### Technical Preferences Captured

| Preference | Decision |
|------------|----------|
| Frontend | Next.js (full SSR framework) |
| Repository | Monorepo |
| Containerization | Docker from day 1 |
| Team Experience | New to all technologies |

### Starter Options Considered

1. **Vinta's nextjs-fastapi-template** — Monorepo, Docker, type-safe API client ✅
2. **tiangolo's Full Stack FastAPI** — Production-ready, but separate repos
3. **Custom from scratch** — Maximum control, steep learning curve

### Selected Starter: Vinta's NextJS-FastAPI Template

**Rationale:**

- Monorepo structure matches requirements
- Docker Compose included out of the box
- Auto-generates TypeScript types from FastAPI OpenAPI spec
- Well-documented for beginners
- Active maintenance (updated December 2024)

**Initialization Command:**

```bash
git clone https://github.com/vintasoftware/nextjs-fastapi-template mantis
cd mantis
docker-compose up --build
```

### Architectural Decisions Provided by Starter

**Language & Runtime:**

- Python 3.11+ with FastAPI
- TypeScript 5+ with Next.js 15
- Strict type checking enabled

**Build Tooling:**

- Ruff for Python linting
- ESLint + Prettier for TypeScript
- pnpm for Node package management

**Code Organization:**

- `/backend` — FastAPI app
- `/frontend` — Next.js app
- Docker Compose orchestration

### Party Mode Recommendations for Starter

| Agent | Recommendation | Priority |
|-------|----------------|----------|
| Winston | Add PostgreSQL + Alembic migrations BEFORE business logic | 🔴 High |
| Amelia | Document hot reload workflows for DX | 🟡 Medium |
| Murat | Add E2E test container + separate test DB | 🔴 High |
| Barry | Consider backend-first approach (add frontend in week 2-3) | 🟡 Medium |

### Implementation Order (Recommended)

1. **Week 1**: Clone template, add PostgreSQL + Redis + Alembic
2. **Week 2**: Add Keycloak integration, basic auth flows
3. **Week 3**: Add Next.js frontend, connect to API
4. **Week 4**: Add test infrastructure (Playwright, test DB)

**Note:** Project initialization using this template should be the first implementation story.

---

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**

- Multi-tenancy isolation strategy → Row-Level Security
- LLM provider abstraction → LiteLLM
- Flow builder library → React Flow

**Important Decisions (Shape Architecture):**

- ORM choice → SQLAlchemy 2
- State management → Zustand
- Background jobs → ARQ

**Deferred Decisions (Post-MVP):**

- Kubernetes orchestration
- Advanced monitoring (Prometheus, OpenTelemetry)
- GraphQL API layer

---

### Data Architecture

| Decision | Choice | Version | Rationale |
|----------|--------|---------|-----------|
| Database | PostgreSQL | 17 (LTS) | Stable, supported until Nov 2029 |
| ORM | SQLAlchemy 2 | 2.x | Industry standard, async support, huge community |
| Migrations | Alembic | Latest | Bundled with SQLAlchemy, handles schema changes |
| Caching | Redis | 8.x | Also used for sessions and job queue |

---

### Authentication & Security

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth Provider | Keycloak 26.x | PRD requirement, OIDC/OAuth2 support |
| Multi-Tenancy | Row-Level Security (RLS) | PostgreSQL-native, good security/simplicity balance |
| Token Strategy | JWT + Redis sessions | Allows token revocation, leverages existing Redis |
| RBAC | Keycloak roles | Centralized role management |

**Implementation Notes:**

- Every table includes `tenant_id` column
- PostgreSQL RLS policies filter by tenant automatically
- Refresh tokens stored in Redis with TTL

---

### API & Communication Patterns

| Decision | Choice | Rationale |
|----------|--------|-----------|
| API Style | REST + WebSocket hybrid | REST for CRUD, WebSocket for real-time |
| API Docs | OpenAPI (auto-generated) | FastAPI generates this automatically |
| LLM Abstraction | LiteLLM | Unified interface for 100+ LLM providers |
| Webhook Security | HMAC signatures | Prevents replay attacks |

**Real-Time Features:**

- Chat simulator → WebSocket
- Flow preview → WebSocket
- Bot management → REST

---

### Frontend Architecture

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | Next.js 15 | App Router, React 19, SSR support |
| State Management | Zustand | Simple, tiny, beginner-friendly |
| Flow Builder | React Flow | Industry standard, 25k+ stars |
| UI Components | Shadcn/ui | Modern, copy-paste, Tailwind-based |
| Styling | Tailwind CSS v4 | Utility-first, great DX |

---

### Infrastructure & Deployment

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Orchestration | Docker Compose | Simple for MVP, K8s deferred |
| Background Jobs | ARQ | Async-native, Redis-based, simpler than Celery |
| Logging | Structured JSON | Parseable, works with any log aggregator |
| Monitoring | Defer to post-MVP | Prometheus + OpenTelemetry later |

---

### Decision Impact Analysis

**Implementation Sequence:**

1. PostgreSQL + Redis + Alembic (foundation)
2. Keycloak + RLS (security layer)
3. FastAPI endpoints + LiteLLM (core API)
4. React Flow + Zustand (flow builder UI)
5. WebSocket integration (real-time)
6. ARQ background jobs (broadcasts, retries)

**Cross-Component Dependencies:**

- Redis → Sessions, Cache, Job Queue, WebSocket pub/sub
- PostgreSQL RLS → Requires tenant context in all queries
- LiteLLM → Managed via "Context Stuffing" pipeline (Extract -> Truncate -> Inject)
- React Flow → State managed by Zustand, persisted via API
- Skills System → Skills are imported as packages (Logic + Config) into Templates

---

### Party Mode Recommendations (Step 4)

**From Winston (Architect):**

- Plan **state persistence strategy** for flow builder (autosave intervals)
- Consider conflict resolution for multi-user editing in Phase 2

**From Amelia (Dev):**

- Budget time for React Flow **custom node learning curve**
- Set up `components/ui` folder early for Shadcn/ui
- Implement robust **error handling for LiteLLM** provider failures

**From Murat (Test Architect):**

- Add `test` service to docker-compose from start
- Include **separate test database**
- Plan visual testing (Playwright screenshots) for React Flow

**From Sally (UX Designer):**

- Build **undo/redo into Zustand** from day 1 (middleware available)
- Add **keyboard shortcuts** for flow builder
- Design empty states for new users

**From Barry (Quick Flow Dev):**

- Focus Week 1 on Docker Compose + PostgreSQL + FastAPI basics
- Add ARQ, LiteLLM, WebSocket **incrementally when needed**
- Don't touch React Flow until CRUD is working

---

## Implementation Patterns & Consistency Rules

> These patterns ensure ALL AI agents and developers write compatible, consistent code.

### Naming Patterns

| Layer | Convention | Examples |
|-------|------------|----------|
| **Database Tables** | `snake_case` plural | `users`, `chat_flows`, `bot_rules` |
| **Database Columns** | `snake_case` | `user_id`, `created_at`, `tenant_id` |
| **Foreign Keys** | `{table_singular}_id` | `bot_id`, `flow_id`, `skill_id` |
| **Python Code** | `snake_case` | `get_user_data()`, `bot_service` |
| **JSON/API Fields** | `camelCase` | `{ "botId": "123", "chatFlow": {...} }` |
| **TypeScript** | `camelCase` | `userId`, `getBotData()` |
| **React Components** | `PascalCase` | `BotCard`, `FlowEditor`, `SkillPanel` |
| **Files (Python)** | `snake_case.py` | `bot_service.py`, `flow_models.py` |
| **Files (React)** | `PascalCase.tsx` | `BotCard.tsx`, `FlowEditor.tsx` |

### Structure Patterns

**Project Organization:** Feature-based (domain modules)

```
backend/
  app/
    bots/           # Bot management domain
      api.py
      models.py
      service.py
    flows/          # Flow builder domain
      api.py
      models.py
      service.py
    core/           # Shared infrastructure
      auth.py
      database.py
  tests/
    bots/
    flows/

frontend/
  src/
    features/
      bots/
        components/
        hooks/
        store.ts
      flows/
        components/
        hooks/
        store.ts
    components/ui/  # Shadcn/ui components
  __tests__/
```

**Test Location:** Separate `/tests` folders (not co-located)

### API Format Patterns

**Success Response Format:**

```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 100
  }
}
```

**Error Response Format:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "details": [
      { "field": "email", "issue": "Invalid format" }
    ]
  }
}
```

**Standard Error Codes:**

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input |
| `UNAUTHORIZED` | 401 | Not authenticated |
| `FORBIDDEN` | 403 | Not authorized |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Duplicate/conflict |
| `INTERNAL_ERROR` | 500 | Server error |

**Date/Time Format:** ISO 8601 strings (`"2026-01-31T09:00:00Z"`)

### State Management Patterns

**Zustand Store Organization:** One store per feature

```typescript
// features/bots/store.ts
interface BotsState {
  bots: Bot[];
  isLoading: boolean;
  error: string | null;
  fetchBots: () => Promise<void>;
  createBot: (data: CreateBotInput) => Promise<Bot>;
}
```

**Loading State Pattern:**

```typescript
{
  isLoading: boolean;
  error: string | null;
  data: T | null;
}
```

**UI Pattern:** Skeleton loaders (not spinners)

### Error Handling Patterns

**Backend Exceptions:**

```python
# Custom exception classes
class BotNotFoundError(Exception):
    code = "BOT_NOT_FOUND"

class ValidationError(Exception):
    code = "VALIDATION_ERROR"
```

**Frontend Error Handling:**

- Error boundaries for component crashes
- Toast notifications for API errors
- Form-level validation messages

### AI Agent Enforcement Rules

**All AI Agents MUST:**

1. Use the naming conventions specified above (snake_case Python, camelCase TypeScript)
2. Place files in feature-based folders, not by type
3. Use the standard response wrapper for ALL API endpoints
4. Include `tenant_id` in ALL database models
5. Use ISO 8601 for ALL date/time fields
6. Create one Zustand store per feature domain
7. Use custom exception classes with error codes

**Anti-Patterns to Avoid:**

| ❌ Don't | ✅ Do |
|----------|-------|
| `class Users` | `class User` (singular for models) |
| `get_user()` returning unwrapped | `get_user()` returning `{data: ...}` |
| Global `useAppStore()` | Feature-specific `useBotsStore()` |
| `new Date().toISOString()` in DB | Store as `timestamp with time zone` |
| `raise Exception("not found")` | `raise BotNotFoundError()` |

---

### Party Mode Recommendations (Step 5)

**From Winston (Architect):**

- Use `model_dump(by_alias=True)` for Pydantic → JSON (camelCase output)
- Configure Pydantic models with `alias_generator=to_camel`

**From Amelia (Dev):**

- Environment variables: Use `MANTIS_*` prefix for all custom vars
- Add Zustand **devtools middleware** in development mode
- Create FastAPI dependency for automatic response wrapping

**From Murat (Test Architect):**

- Test naming: `test_<action>_<scenario>` → `test_create_bot_success`
- Use `freezegun` for date/time testing
- Test that error codes match HTTP status codes

**From Sally (UX Designer):**

- Skeleton loaders: Match actual component dimensions
- List skeletons: Show 3-5 placeholder items
- React Flow canvas: Use blur overlay + spinner during load

**From Barry (Quick Flow Dev):**

- Migration naming: `YYYYMMDD_HHMMSS_description.py`
- Create a **naming cheat sheet** for quick reference
- Add ESLint/Ruff rules to enforce patterns automatically

---

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
mantis/
├── docker-compose.yml          # Orchestration
├── docker-compose.dev.yml      # Dev overrides
├── .env.example                # Environment template
├── .gitignore
├── README.md
│
├── backend/                    # FastAPI Application
│   ├── Dockerfile
│   ├── pyproject.toml          # Python dependencies (Ruff, Alembic)
│   ├── alembic.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI entry point
│   │   ├── core/               # Shared infrastructure
│   │   │   ├── config.py       # MANTIS_* env vars
│   │   │   ├── database.py     # PostgreSQL + RLS
│   │   │   ├── auth.py         # Keycloak integration
│   │   │   ├── redis.py        # Redis client
│   │   │   ├── exceptions.py   # Custom exception classes
│   │   │   └── response.py     # {data, meta} wrapper
│   │   ├── bots/               # Bot Management domain
│   │   │   ├── api.py
│   │   │   ├── models.py
│   │   │   ├── service.py
│   │   │   └── schemas.py      # Pydantic with alias_generator
│   │   ├── flows/              # Flow Builder domain
│   │   │   ├── api.py
│   │   │   ├── models.py
│   │   │   ├── service.py
│   │   │   └── schemas.py
│   │   ├── skills/             # Skills System domain
│   │   │   ├── api.py
│   │   │   ├── models.py
│   │   │   └── service.py
│   │   ├── connectors/         # Platform Connectors domain
│   │   │   ├── api.py
│   │   │   ├── base.py         # Abstract connector
│   │   │   ├── manychat.py
│   │   │   ├── twilio.py
│   │   │   └── webhooks.py     # HMAC validation
│   │   ├── llm/                # LLM Abstraction domain
│   │   │   ├── api.py
│   │   │   ├── service.py      # LiteLLM wrapper
│   │   │   └── providers.py
│   │   └── jobs/               # ARQ Background Jobs
│   │       ├── worker.py
│   │       └── tasks.py
│   ├── migrations/             # Alembic migrations
│   │   └── versions/           # YYYYMMDD_HHMMSS_description.py
│   └── tests/
│       ├── conftest.py         # Fixtures, test DB
│       ├── bots/
│       ├── flows/
│       └── connectors/
│
├── frontend/                   # Next.js Application
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── src/
│   │   ├── app/                # App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── (auth)/         # Auth routes
│   │   │   │   ├── login/
│   │   │   │   └── callback/
│   │   │   ├── dashboard/
│   │   │   ├── bots/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [botId]/
│   │   │   └── flows/
│   │   │       ├── page.tsx
│   │   │       └── [flowId]/
│   │   │           └── editor/page.tsx  # React Flow editor
│   │   ├── features/           # Feature stores + hooks
│   │   │   ├── bots/
│   │   │   │   ├── store.ts    # Zustand store
│   │   │   │   ├── hooks.ts
│   │   │   │   └── api.ts
│   │   │   ├── flows/
│   │   │   │   ├── store.ts
│   │   │   │   ├── hooks.ts
│   │   │   │   └── nodes/      # React Flow custom nodes
│   │   │   └── auth/
│   │   │       └── store.ts
│   │   ├── components/
│   │   │   ├── ui/             # Shadcn/ui components
│   │   │   ├── layout/
│   │   │   └── skeletons/      # Skeleton loaders
│   │   ├── lib/
│   │   │   ├── api.ts          # API client
│   │   │   ├── keycloak.ts
│   │   │   └── utils.ts
│   │   └── types/
│   │       └── generated.ts    # Auto-generated from OpenAPI
│   └── __tests__/
│       ├── components/
│       └── features/
│
└── e2e/                        # Playwright E2E tests
    ├── playwright.config.ts
    └── tests/
```

### Architectural Boundaries

**API Boundaries:**

| Boundary | Description |
|----------|-------------|
| `/api/v1/` | All REST endpoints versioned |
| `/ws/` | WebSocket connections for real-time |
| Internal services | Never exposed directly, only via API |

**Data Boundaries:**

| Boundary | Enforcement |
|----------|-------------|
| Tenant isolation | PostgreSQL RLS on every table |
| Auth | Keycloak JWT validated on every request |
| Secrets | Only in environment variables |

**Component Boundaries:**

| Frontend | Backend |
|----------|---------|
| `features/bots/` | `app/bots/` |
| `features/flows/` | `app/flows/` |
| `features/auth/` | `app/core/auth.py` |

### Requirements to Structure Mapping

| PRD Feature | Backend | Frontend |
|-------------|---------|----------|
| Bot Management (FR-02) | `app/bots/` | `features/bots/`, `app/bots/` |
| Flow Builder (FR-04) | `app/flows/` | `features/flows/`, `app/flows/[flowId]/editor/` |
| Skills System (FR-05) | `app/skills/` | `features/skills/` |
| Connectors (FR-03) | `app/connectors/` | `features/connectors/` |
| LLM Integration (FR-06) | `app/llm/` | (via API) |
| Auth (FR-01) | `app/core/auth.py` | `features/auth/`, `app/(auth)/` |

### Integration Points

**Internal Communication:**

- Frontend → Backend: REST API + WebSocket
- Backend services: Direct function calls within domain
- Background jobs: ARQ task queue via Redis

**External Integrations:**

- Keycloak: OIDC authentication
- LLM Providers: Via LiteLLM abstraction
- Platform APIs: ManyChat, Twilio, etc.

**Data Flow:**

1. Request → FastAPI → Service → Repository → PostgreSQL
2. Response → Pydantic schema (camelCase) → JSON → Frontend
3. WebSocket → Redis pub/sub → All connected clients

---

### Party Mode Recommendations (Step 6)

**From Winston (Architect):**

- Add `backend/app/core/middleware.py` for tenant context injection
- Add `backend/app/core/deps.py` for FastAPI dependency injection
- Consider `backend/app/shared/` for cross-domain utilities

**From Amelia (Dev):**

- Add `frontend/src/hooks/` for shared hooks (useAuth, useApi)
- Add `frontend/src/contexts/` for React contexts
- Add `frontend/.env.local` for local environment variables

**From Murat (Test Architect):**

- Add `backend/tests/fixtures/` for test fixtures
- Add `backend/tests/factories/` for test factories
- Add `frontend/__tests__/__mocks__/` for mock data
- Add `e2e/fixtures/` for Playwright test data

**From Sally (UX Designer):**

- Add `frontend/src/components/forms/` for reusable form components
- Add `frontend/src/components/feedback/` for toasts, modals, alerts
- Add `frontend/public/` for static assets (icons, images)

**From Barry (Quick Flow Dev):**

- Add `Makefile` or `justfile` for common commands
- Add `.vscode/` with recommended extensions and settings
- Add `docs/` folder for developer documentation

---

## Nice-to-Have Gaps (Future Enhancements)

These are not blocking implementation but should be addressed as the project matures:

### Database Seeding Strategy

- Seed scripts for development/demo data
- Location: `backend/scripts/seed.py`
- Commands: `make seed`, `make seed-demo`

### CI/CD Pipeline Details

- GitHub Actions workflow for testing and deployment
- Location: `.github/workflows/ci.yml`
- Stages: lint → test → build → deploy

### Monitoring & Alerting

- Prometheus metrics endpoint
- Grafana dashboards (Phase 2)
- Error tracking with Sentry integration

---

### Party Mode Recommendations (Step 7 - Validation)

**From Winston (Architect):**

- Create ADR (Architecture Decision Record) template
- Location: `docs/adr/0001-template.md`
- Track WHY decisions were made for future reference

**From Amelia (Dev):**

- Create `DEVELOPMENT.md` onboarding guide
- Priority order: Docker+Keycloak → FastAPI auth → Next.js login → first domain

**From Murat (Test Architect):**

- Unit test coverage target: **80%**
- E2E critical path: Login → Create Bot → Create Flow
- API performance baseline: **< 200ms p95**

**From Sally (UX Designer):**

- Prototype React Flow FIRST (before full backend)
- Test custom node creation with 3-5 node types
- Validate save/load before building full flows domain

**From Barry (Quick Flow Dev):**

- Pre-configure Keycloak realm and export to `keycloak-realm-export.json`
- Use realm import in production (don't configure manually)
- Budget 1-2 days for Keycloak setup
