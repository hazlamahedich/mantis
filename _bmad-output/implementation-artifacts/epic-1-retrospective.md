# Epic 1 Retrospective: Authentication & Tenant Foundation

> **Facilitated by:** Bob (Scrum Master)  
> **Date:** 2026-02-01  
> **Epic Status:** ✅ Complete  

---

## Executive Summary

Epic 1 established secure authentication with Keycloak and multi-tenant data isolation using PostgreSQL Row-Level Security. All 3 stories were delivered successfully, though Story 1.2 (User Authentication) required significant debugging effort for Google OAuth integration.

| Metric | Value |
|--------|-------|
| Stories Delivered | 3/3 (100%) |
| Backend Tests | 64 |
| Frontend Tests | 19 (auth-related) |
| Code Review Issues Fixed | 3 (Database separation, healthcheck, RLS safety) |

---

## Story Delivery Summary

### Story 1.1: Database & Keycloak Setup ✅

**Agent:** Claude 4.7 (glm-4.7)

**What was delivered:**

- Keycloak 26.0 container with realm auto-import
- "mantis" realm with frontend/backend clients
- Alembic auto-migration on startup
- Keycloak health check integration

**Code Review Findings (2 issues fixed):**

1. **High Severity**: Separated Keycloak database from application database
2. **Medium Severity**: Added PostgreSQL `pg_isready` healthcheck

**Key Lesson:** Port 8081 used (8080 was occupied) - runtime discovery

---

### Story 1.2: User Authentication (Frontend + Backend) ✅

**Agent:** Claude 4 (Anthropic)

**What was delivered:**

- Keycloak OIDC integration with JWKS caching
- Frontend PKCE flow with BFF (server-side) pattern
- HTTP-only cookie token storage
- Google OAuth via Keycloak IdP
- 57 backend tests passing

**Debug Log - Multiple Issues Resolved:**

1. "Invalid Scopes" → Updated `defaultClientScopes` in realm JSON
2. "Identity Provider Error" → Hardcoded Google credentials (env var substitution failed)
3. `redirect_uri_mismatch` → Configured `KC_HOSTNAME` variables in docker-compose
4. Login loop → Migrated token storage to cookies for middleware compatibility

**This was the most challenging story of the epic.** The Keycloak-Google integration required multiple debugging cycles to resolve hostname and redirect URI configuration issues.

---

### Story 1.3: Multi-Tenancy & Row-Level Security ✅

**Agent:** Claude (glm-4.7) via Claude Code

**What was delivered:**

- PostgreSQL native RLS policies on `items` and `users` tables
- `TenantSession` with `contextvars` for async-safe tenant context
- `sudo_context` for admin bypass operations
- ARQ background job tenant hydration utilities
- 64 total backend tests

**Key Success:** RLS implementation went smoothly with clear patterns from architecture docs.

---

## 🟢 What Went Well

1. **RLS Implementation** - Story 1.3's PostgreSQL RLS pattern worked exactly as designed
2. **BFF Pattern Adoption** - Server-side token handling eliminated frontend security concerns
3. **Test Coverage Growth** - Backend tests grew from 51 → 64 across the epic
4. **Code Review Value** - Caught database separation issue in Story 1.1
5. **Pattern Documentation** - Dev notes captured implementation patterns for future reference

---

## 🟡 What Could Improve

1. **External IdP Configuration** - Keycloak + Google required trial-and-error debugging; could benefit from upfront configuration checklist
2. **Environment Variable Handling** - Keycloak realm import doesn't support env var substitution reliably
3. **E2E Testing Still Pending** - Auth flow would benefit from Playwright E2E tests (deferred from Epic 0)

---

## 🔴 Challenges Encountered

1. **Keycloak-Google OAuth Integration** - The main challenge of Epic 1:
   - Multiple hostname configuration variables required (`KC_HOSTNAME`, `KC_HOSTNAME_PORT`, `KC_HOSTNAME_URL`)
   - Google redirect URI must exactly match Keycloak's broker endpoint
   - Environment variable substitution in realm JSON is unreliable

2. **Keycloak 26 Behavior Differences** - No `/health/ready` endpoint by default; uses root endpoint check instead

3. **Token Storage Strategy** - Initial sessionStorage approach caused middleware issues; migrated to cookies

---

## ✅ Epic 0 Action Items - Follow Through

| Action Item | Committed | Status |
|-------------|-----------|--------|
| Add Playwright E2E to CI | Before Epic 2 | ⏳ **Still pending** |
| Create backlog for deferred work | Epic 0 | ✅ Done |
| Sentry integration | Deferred | ⏸️ Still deferred |
| Grafana dashboard | Deferred | ⏸️ Still deferred |

**Note:** E2E CI integration remains pending and should be prioritized before Epic 2.

---

## 📋 Action Items for Epic 2

| # | Action | Priority | Owner |
|---|--------|----------|-------|
| 1 | Add Playwright E2E to CI | **High** | Dev Team |
| 2 | Create Keycloak IdP configuration checklist | Medium | Bob (SM) |
| 3 | Document Keycloak hostname configuration patterns | Medium | Dev Team |

---

## Technical Debt Identified

1. **E2E Testing Gap** - Auth flow not yet tested end-to-end in CI
2. **Hardcoded Google Credentials** - In `mantis-realm.json` (env var substitution workaround)
3. **E2E Tests Deferred** - Story 1.2 skipped E2E test (7.3) - requires Playwright setup

---

## Next Epic Preview: Epic 2 - Bot Management & Reporting

Epic 2 focuses on the core bot management features:

- **Story 2.1:** Bot Dashboard (List Bots)
- **Story 2.2:** Create Bot from Template
- **Story 2.3:** Duplicate Bot
- **Story 2.4:** Import/Export Skills (API Only)
- **Story 2.5:** Daily Email Reporting
- **Story 2.6:** Workspace Switcher (Agency Support)
- **Story 2.7:** Client Onboarding (Tenant Provisioning)

**Dependencies on Epic 1:**

- ✅ Authentication with Keycloak (delivered)
- ✅ Multi-tenant data isolation via RLS (delivered)
- ✅ Tenant context in API requests (delivered)

**Preparation Needed:**

1. ✅ **E2E CI Integration** - Should be addressed before Epic 2 starts
2. Bot/Flow database models (will be created in Epic 2)
3. Template system design

---

## Retrospective Participants

- **Bob** (Scrum Master) - Facilitated retrospective
- **Alice** (Product Owner) - Validated completion status
- **Dev Agents** - Claude 4, Claude 4.7
- **team mantis** - Reviewed and approved findings

---

*Retrospective completed: 2026-02-01*
