# Story 1.3: Multi-Tenancy & Row-Level Security

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a **Platform Operator**,
I want all database queries to be scoped by `tenant_id`,
so that user data is logically isolated.

## Acceptance Criteria

1. **Given** a user is authenticated
   **When** any database query is executed
   **Then** SQLAlchemy middleware automatically injects `tenant_id` filter
   **And** a user cannot access data from another tenant

2. **Given** an API request is made
   **When** the `tenant_id` header is missing or invalid
   **Then** the API returns 403 Forbidden

## Tasks / Subtasks

- [ ] Task 1: Add tenant_id to All Models (AC: 1) <!-- id: 1 -->
  - [ ] 1.1: Update `Item` model to include `tenant_id` column with foreign key to `tenants`
  - [ ] 1.2: Create migration to add `tenant_id` to `items` table
  - [ ] 1.3: Add `Tenant` model to `models.py` based on existing migration schema
  - [ ] 1.4: Add tenant relationship to `User` model

- [ ] Task 2: Implement Tenant Context Middleware (AC: 1, 2) <!-- id: 2 -->
  - [ ] 2.1: Create `app/core/tenant.py` with tenant context management
  - [ ] 2.2: Implement `TenantContext` using Python `contextvars` for async-safe storage
  - [ ] 2.3: Create FastAPI middleware to extract `tenant_id` from JWT claims
  - [ ] 2.4: Validate tenant_id exists in database (return 403 if invalid)
  - [ ] 2.5: Add structured logging for tenant context events

- [ ] Task 3: Implement RLS Query Filtering (AC: 1) <!-- id: 3 -->
  - [ ] 3.1: Create `TenantQueryMixin` class with automatic `tenant_id` filtering
  - [ ] 3.2: Implement SQLAlchemy event listeners for `before_compile`
  - [ ] 3.3: Override `get_async_session()` to inject tenant filter on all queries
  - [ ] 3.4: Create `TenantSession` class that wraps AsyncSession with automatic filtering
  - [ ] 3.5: Update all routes to use tenant-aware session

- [ ] Task 4: Update API Endpoints for Tenant Awareness (AC: 2) <!-- id: 4 -->
  - [ ] 4.1: Add `get_current_tenant` dependency to extract tenant from authenticated user
  - [ ] 4.2: Update `items` routes to use tenant-scoped queries
  - [ ] 4.3: Update `auth` routes to handle tenant provisioning on first login
  - [ ] 4.4: Create `/api/tenants/me` endpoint to get current tenant info
  - [ ] 4.5: Ensure 403 response when tenant_id is missing or invalid

- [ ] Task 5: Add Tenant Validation Tests (AC: 1, 2) <!-- id: 5 -->
  - [ ] 5.1: Write tests for tenant isolation (user cannot access other tenant's data)
  - [ ] 5.2: Write tests for missing tenant_id returns 403
  - [ ] 5.3: Write tests for invalid tenant_id returns 403
  - [ ] 5.4: Write tests for query filtering with multiple tenants
  - [ ] 5.5: Update existing tests to include tenant context

- [ ] Task 6: Frontend Tenant Integration (AC: 2) <!-- id: 6 -->
  - [ ] 6.1: Update API client to extract tenant_id from user session
  - [ ] 6.2: Add tenant info display to dashboard (tenant name/slug)
  - [ ] 6.3: Create error handler for 403 tenant errors
  - [ ] 6.4: Update AuthProvider to include tenant_id in user state

## Dev Notes

### Architecture Compliance

| Pattern | Implementation |
| ------- | -------------- |
| Multi-Tenancy Strategy | Row-Level Security (RLS) via SQLAlchemy middleware |
| Data Isolation | Every table MUST include `tenant_id` column |
| Context Storage | Python `contextvars` for async-safe tenant context |
| Query Filtering | SQLAlchemy event listeners + custom session |
| Auth Integration | tenant_id extracted from Keycloak JWT claims |

### Library/Framework Requirements

| Tool | Version | Purpose |
| ---- | ------- | ------- |
| SQLAlchemy | 2.x | ORM with event listeners for RLS |
| contextvars | stdlib | Async-safe context storage |
| structlog | ^23.x | Structured logging for tenant events |

### File Structure Requirements

```text
mantis/
├── fastapi_backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── tenant.py             # [NEW] Tenant context and RLS middleware
│   │   │   ├── deps.py               # [MODIFY] Add get_current_tenant dependency
│   │   │   └── auth.py               # [MODIFY] Extract tenant_id from JWT
│   │   ├── models.py                 # [MODIFY] Add Tenant model, update relationships
│   │   ├── database.py               # [MODIFY] Add TenantSession wrapper
│   │   ├── routes/
│   │   │   ├── items.py              # [MODIFY] Use tenant-scoped queries
│   │   │   └── tenants.py            # [NEW] Tenant info endpoints
│   │   └── main.py                   # [MODIFY] Add tenant middleware
│   ├── alembic_migrations/
│   │   └── versions/
│   │       └── c002_add_tenant_to_items.py  # [NEW] Migration for items.tenant_id
│   └── tests/
│       ├── core/
│       │   └── test_tenant.py        # [NEW] Tenant isolation tests
│       └── routes/
│           └── test_items.py         # [MODIFY] Add tenant context to tests
├── nextjs-frontend/
│   ├── components/
│   │   └── dashboard/
│   │       └── TenantInfo.tsx        # [NEW] Tenant info display
│   └── lib/
│       └── types/auth.ts             # [MODIFY] Add tenant_id to user type
```

### Previous Story Intelligence (1.2: User Authentication)

**From Story 1.2 Dev Notes and Completion Notes:**

1. **JWT Claims**: tenant_id is already mapped as a protocol mapper in Keycloak
2. **Token Extraction**: `app/core/auth.py` already extracts claims from JWT
3. **User Sync**: Users are synced to local DB on each authenticated request
4. **Cookie Auth**: Tokens stored in HTTP-only cookies (`auth_access_token`)
5. **Dependencies**: `get_current_user` in `app/core/deps.py` returns authenticated user

**Files to Reuse:**

- `fastapi_backend/app/core/auth.py` - JWT verification, add tenant_id extraction
- `fastapi_backend/app/core/deps.py` - Add `get_current_tenant` dependency
- `fastapi_backend/app/models.py` - Add Tenant model
- `keycloak/mantis-realm.json` - tenant_id mapper already configured

### Existing Database Infrastructure

**From Story 1.1 Migrations (c001_add_tenant_id.py):**

1. **Tenants Table**: Already created with `id`, `name`, `slug`, `is_active`, `created_at`, `updated_at`
2. **User.tenant_id**: Already added with foreign key to tenants
3. **Default Tenant**: UUID `00000000-0000-0000-0000-000000000001` with slug "default"
4. **Foreign Key**: `fk_user_tenant_id` already exists

**Current Model State (models.py):**

- `User` model exists with relationship to items
- `Item` model exists but does NOT have `tenant_id` column
- `Tenant` model does NOT exist in models.py (only in migration)

### Implementation Patterns

**Tenant Context Pattern:**

```python
# app/core/tenant.py
from contextvars import ContextVar
from uuid import UUID

tenant_context: ContextVar[UUID | None] = ContextVar("tenant_id", default=None)

def get_tenant_id() -> UUID | None:
    return tenant_context.get()

def set_tenant_id(tenant_id: UUID) -> None:
    tenant_context.set(tenant_id)
```

**RLS Query Filtering Pattern:**

```python
# SQLAlchemy event listener approach
from sqlalchemy import event
from sqlalchemy.orm import Query

@event.listens_for(Query, "before_compile", retval=True)
def filter_by_tenant(query):
    tenant_id = get_tenant_id()
    if tenant_id is None:
        return query  # Allow unfiltered for migrations, tests
    
    for desc in query.column_descriptions:
        entity = desc.get('entity')
        if entity and hasattr(entity, 'tenant_id'):
            query = query.filter(entity.tenant_id == tenant_id)
    return query
```

**Tenant Middleware Pattern:**

```python
# FastAPI middleware
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract tenant_id from JWT claims (already decoded in auth)
        tenant_id = getattr(request.state, 'tenant_id', None)
        if tenant_id:
            set_tenant_id(tenant_id)
        
        response = await call_next(request)
        return response
```

### Testing Requirements

**Backend Tests:**

```bash
cd fastapi_backend
pytest tests/core/test_tenant.py -v  # Tenant isolation tests
pytest tests/routes/test_items.py -v  # Tenant-scoped item tests
```

**Test Scenarios:**

1. User A creates item → User B cannot see it (different tenant)
2. User A creates item → User A can see it (same tenant)
3. Missing tenant_id in session → 403 Forbidden
4. Invalid tenant_id → 403 Forbidden
5. Query without active tenant context → returns all (for migrations)
6. Admin user → can query across tenants (future: super-admin role)

### Security Considerations

1. **Always Filter**: NEVER bypass RLS in production routes
2. **Tenant Validation**: Always verify tenant exists and is active
3. **Logging**: Log all cross-tenant access attempts as security events
4. **Migration Safety**: Disable RLS during migrations
5. **Test Isolation**: Each test should use isolated tenant context

### Troubleshooting Guide

| Issue | Solution |
| ----- | -------- |
| User sees other tenant's data | Verify RLS event listener is registered |
| 403 on all requests | Check tenant_id is in JWT claims (Keycloak mapper) |
| Empty results | Verify tenant_id is being set in context |
| Migration fails | Ensure RLS is disabled during migration |
| Tests see wrong data | Reset tenant context between tests |

### Git Commit Pattern

**Conventional commits for this story:**

- `feat(tenant): add Tenant model and relationships`
- `feat(rls): implement SQLAlchemy row-level security`
- `feat(middleware): add tenant context middleware`
- `test(tenant): add tenant isolation tests`

### References

- [Source: architecture.md#authentication--security](file:///Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/architecture.md#authentication--security)
- [Source: architecture.md#implementation-patterns--consistency-rules](file:///Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/architecture.md#implementation-patterns--consistency-rules)
- [Source: epics.md#story-13](file:///Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/epics.md#story-13-multi-tenancy--row-level-security)
- [Source: 1-2-user-authentication-frontend-backend.md](file:///Users/sherwingorechomante/mantis/_bmad-output/implementation-artifacts/1-2-user-authentication-frontend-backend.md)
- [Source: c001_add_tenant_id.py](file:///Users/sherwingorechomante/mantis/fastapi_backend/alembic_migrations/versions/c001_add_tenant_id.py)

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
