---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics, step-03-create-stories, step-04-review-finalize]
inputDocuments:
  - /Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/prd.md
  - /Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/architecture.md
  - /Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/ux-design-specification.md
---

# Mantis - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Mantis, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-001 (Dashboard): User can view a list of "My Bots" with status (Active/Draft).
FR-002 (Auth): User can Sign Up / Login via Email & Password or Google OAuth.
FR-003 (Cloning): User can "Duplicate" an existing bot to start a new project quickly.
FR-010 (Canvas): Visual, drag-and-drop editor (ReactFlow) with specific supported node types.
FR-011 (Nodes): Support Start, Send Text, User Input, AI Response, Handover nodes.
FR-012 (Limits): Hard limit of 30 Nodes per flow.
FR-013 (Safety): "Test/Preview" simulator window available inside the builder.
FR-020 (Webhook): Handles incoming Facebook Messenger webhooks.
FR-021 (State): Maintains conversation state (Context, Variables) for active sessions.
FR-022 (Routing): Executes logic: If Keyword Match -> Jump to Node; Else -> AI Response.
FR-023 (Handover): If Handover Node reached -> Stop auto-responses until timeout or Admin reset.
FR-030 (Email): System sends a daily HTML summary to the registered Account Email.
FR-040 (Definition): A Skill is a reusable package of Logic (Flow) + Configuration (Variables).
FR-041 (Composition): Users generally do not "build from scratch"; they instantiate Templates, which are pre-configured collections of Skills.
FR-042 (Marketplace Prep): The architecture must support importing/exporting Skills as standalone units (Phase 2).

### NonFunctional Requirements

NFR-001 (Webhook Latency): The Runtime Engine must acknowledge a Messenger webhook (200 OK) within 2 seconds (P95).
NFR-002 (Editor Responsiveness): The ReactFlow Builder must render the initial graph (30 nodes) in under 500ms.
NFR-003 (AI Latency): The "Typing Indicator" must be displayed immediately (within 200ms) while waiting for the LLM response.
NFR-010 (Tenant Isolation): Data access must be "Logically Isolated" via ORM Middleware (RLS).
NFR-011 (Token Encryption): All Facebook Page Access Tokens and OpenAI/Anthropic Keys must be encrypted at rest (AES-256).
NFR-020 (Meta 24h Rule): Strict Enforcement. Block "Proactive Messages" sent to a user who has not interacted in the last 24 hours.
NFR-021 (AI Disclosure): The "Start" node of every template must include default text: "I am an AI assistant...".
NFR-030 (Uptime): 99.5% Availability during business hours.

### Additional Requirements

**Technical (Architecture):**

- **Starter Template**: Vinta's NextJS-FastAPI Template (Monorepo, Docker, Postgres, Redis).
- **Backend Stack**: Python 3.11+, FastAPI, SQLAlchemy 2, Alembic, ARQ (jobs).
- **Frontend Stack**: Next.js 15, React 19, Zustand, Tailwind CSS v4, React Flow.
- **Auth Strategy**: Keycloak 26.x with OIDC/OAuth2 + RLS for Multi-tenancy.
- **AI Pipeline**: LiteLLM with "Context Stuffing" (Extract -> Truncate -> Inject).
- **Skills System**: Domain for logic + config packaging; imported into Templates.
- **Real-Time**: WebSocket for Chat Simulator and Preview.
- **Security**: HMAC signature validation for Webhooks.

**UX (Design Specification):**

- **Layout**: Resizable Split Screen (60% Canvas / 40% Simulator) on Desktop.
- **Mobile**: "Inspector Mode" (List View) for on-the-go edits; no graph editing.
- **Onboarding**: "Knowledge-First" flow (PDF Upload -> Auto-fill).
- **Context UI**: "Token Meter" visualizer for "Brain Capacity" during upload.
- **Skills UI**: "Skill Tiles/Badges" on Template cards with simplified config sheet.
- **Simulator**: "Idempotent Replay" (mock side-effects), "Prune History".
- **Visuals**: shadcn/ui components, "Pulse" animation for active nodes.

### FR Coverage Map

FR-002: Epic 1 - Authentication & Security
FR-001: Epic 2 - Dashboard (List Bots)
FR-003: Epic 2 - Bot Cloning
FR-030: Epic 2 - Email Reporting
FR-041: Epic 2 - Template Instantiation
FR-042: Epic 2 - Import/Export Skills
FR-010: Epic 3 - Canvas Editor
FR-011: Epic 3 - Supported Nodes
FR-012: Epic 3 - Node Limits
FR-040: Epic 3 - Skill Configuration UI
FR-020: Epic 4 - Messenger Webhook
FR-021: Epic 4 - State Management
FR-022: Epic 4 - Routing Logic
FR-023: Epic 4 - Human Handover
FR-013: Epic 5 - Chat Simulator
NFR-030: Epic 0 - Observability & Health Monitoring

## Epic List

### Epic 0: Foundation & Quality Infrastructure

Establishes project skeleton, test framework, CI/CD quality gates, and observability infrastructure.
**NFRs covered:** NFR-030 (Uptime), cross-cutting quality requirements. (4 stories)

### Epic 1: Authentication & Tenant Foundation

Establishes secure authentication and multi-tenant data model.
**FRs covered:** FR-002 (Auth) + NFR-010, NFR-011. (3 stories)

### Epic 2: Bot Management & Reporting

Enables users to manage their fleet of bots (Create, List, Duplicate, Import) and view business performance.
**FRs covered:** FR-001, FR-003, FR-030, FR-041, FR-042.

### Epic 3: Visual Flow Builder & Skills System

Provides the visual canvas for designing conversation flows and configuring reusable Skills.
**FRs covered:** FR-010, FR-011, FR-012, FR-040.

### Epic 4: Runtime Engine & Messenger Integration

The core engine that processes actual conversation traffic, manages state, and integrates with Messenger.
**FRs covered:** FR-020, FR-021, FR-022, FR-023.

### Epic 5: Simulator & Testing Tools

Ensures users can safely test and debug their bots before deployment, including "Context Stuffing" validation.
**FRs covered:** FR-013 + UX Requirements (Token Meter, Replay).

---

## Epic 0: Foundation & Quality Infrastructure

Establishes the project skeleton, test framework, CI/CD quality gates, and observability infrastructure that all subsequent epics depend on.

### Story 0.1: Project Skeleton & Docker Environment

As a **Developer**,
I want to initialize the Next.js/FastAPI monorepo with Docker,
So that the development environment runs consistently across all machines.

**Acceptance Criteria:**

**Given** the repository is cloned
**When** I run `docker compose up`
**Then** the Next.js frontend, FastAPI backend, Postgres, and Redis containers start successfully
**And** the frontend is accessible at `http://localhost:3000`
**And** the backend API health check returns 200 at `http://localhost:8000/health`

### Story 0.2: Test Framework Setup

As a **Developer**,
I want a configured test framework with fixtures and utilities,
So that all subsequent stories can include comprehensive tests.

**Acceptance Criteria:**

**Given** the monorepo is initialized
**When** I run `npm test` (frontend) or `pytest` (backend)
**Then** test runners execute with proper configuration
**And** test fixtures for users, bots, and conversations are available
**And** coverage thresholds are enforced (minimum 80%)

### Story 0.3: CI/CD Pipeline with Quality Gates

As a **Developer**,
I want automated CI/CD pipelines that run tests on every push,
So that code quality is enforced before merging.

**Acceptance Criteria:**

**Given** a pull request is opened
**When** the CI pipeline runs
**Then** all unit tests, integration tests, and linters execute
**And** the PR is blocked if any quality gate fails
**And** coverage reports are generated

### Story 0.4: Observability & Health Monitoring

As a **Platform Operator**,
I want health endpoints and structured logging,
So that I can monitor uptime and diagnose issues (NFR-030).

**Acceptance Criteria:**

**Given** the application is running
**When** I call `GET /health`
**Then** the endpoint returns 200 with service status (DB, Redis, Keycloak)
**And** structured JSON logs are emitted for all requests
**And** error rates and latency metrics are exposed for Prometheus/Grafana

---

## Epic 1: Authentication & Tenant Foundation

Establishes secure authentication and the multi-tenant data model.

### Story 1.1: Database & Keycloak Setup

As a **Developer**,
I want Postgres, Redis, and Keycloak containers provisioned with initial migrations,
So that authentication and data persistence are available for development.

**Acceptance Criteria:**

**Given** Docker Compose is running
**When** Keycloak container starts
**Then** the Keycloak admin console is accessible at `http://localhost:8080`
**And** a "mantis" realm is created with client credentials
**And** Alembic migrations run automatically against Postgres

### Story 1.2: User Authentication (Frontend + Backend)

As a **User**,
I want to sign up and log in via Email & Password or Google OAuth,
So that I can securely access my bot dashboard.

**Acceptance Criteria:**

**Given** I am on the login page
**When** I enter valid credentials and click "Sign In"
**Then** I am redirected to the dashboard
**And** a valid JWT is stored in an HTTP-only cookie
**And** protected API routes return 401 without a valid token

**Given** I click "Sign in with Google"
**When** I complete the OAuth flow
**Then** I am authenticated and redirected to the dashboard

### Story 1.3: Multi-Tenancy & Row-Level Security

As a **Platform Operator**,
I want all database queries to be scoped by `tenant_id`,
So that user data is logically isolated.

**Acceptance Criteria:**

**Given** a user is authenticated
**When** any database query is executed
**Then** SQLAlchemy middleware automatically injects `tenant_id` filter
**And** a user cannot access data from another tenant

**Given** an API request is made
**When** the `tenant_id` header is missing or invalid
**Then** the API returns 403 Forbidden

---

## Epic 2: Bot Management & Reporting

Enables users to manage their fleet of bots (Create, List, Duplicate, Import) and view business performance.

### Story 2.1: Bot Dashboard (List Bots)

As a **User**,
I want to view a list of "My Bots" with their status (Active/Draft),
So that I can quickly see and manage my bot portfolio.

**Acceptance Criteria:**

**Given** I am authenticated and on the dashboard
**When** the page loads
**Then** I see a grid/list of my bots with name, status badge (Active/Draft), and last modified date
**And** each bot card is clickable to enter the builder

### Story 2.2: Create Bot from Template

As a **User**,
I want to create a new bot by selecting a pre-built Template,
So that I can get started quickly without building from scratch.

**Acceptance Criteria:**

**Given** I click "Create New Bot"
**When** I am presented with a Template selection modal
**Then** I see available templates with descriptions and Skill Tiles
**And** selecting a template and clicking "Create" provisions a new bot with the template's flow and settings

### Story 2.3: Duplicate Bot

As a **User**,
I want to duplicate an existing bot,
So that I can quickly start a new project based on an existing one.

**Acceptance Criteria:**

**Given** I am viewing a bot on the dashboard
**When** I click the "Duplicate" action from the bot's context menu
**Then** a new bot is created with the name "[Original Name] - Copy"
**And** all flow nodes, settings, and knowledge are copied to the new bot

### Story 2.4: Import/Export Skills (API Only)

As a **Developer**,
I want API endpoints for importing and exporting Skills as JSON packages,
So that the architecture supports a future Skill Marketplace.

**Acceptance Criteria:**

**Given** a Skill exists in a bot
**When** I call `POST /api/skills/{skill_id}/export`
**Then** I receive a JSON file containing the Skill's logic (node graph) and configuration (variables)

**Given** I have a valid Skill JSON package
**When** I call `POST /api/skills/import` with the package
**Then** the Skill is created in my tenant and can be added to Templates

### Story 2.5: Daily Email Reporting

As a **User**,
I want to receive a daily HTML summary of my bot's performance,
So that I can track lead generation and engagement.

**Acceptance Criteria:**

**Given** I have an active bot
**When** the daily cron job runs (e.g., 6 AM local time)
**Then** an HTML email is sent to my registered account email
**And** the email includes: Total Conversations, New Leads Captured, Handovers Requested

### Story 2.6: Workspace Switcher (Agency Support)

As an **Agency User**,
I want to switch between my clients' workspaces,
So that I can manage multiple tenants from a single account.

**Acceptance Criteria:**

**Given** I have access to 2+ tenants
**When** the dashboard loads
**Then** a Workspace Switcher dropdown appears in the header
**And** clicking it shows a list of my accessible tenants with names and icons
**And** selecting a tenant reloads the dashboard filtered to that tenant's bots

**Given** I have access to exactly 1 tenant
**When** the dashboard loads
**Then** the Workspace Switcher is hidden (self-service mode)

### Story 2.7: Client Onboarding (Tenant Provisioning)

As an **Agency User**,
I want to create a new client (tenant),
So that I can onboard and manage bots for my clients.

**Acceptance Criteria:**

**Given** I am on the dashboard
**When** I click "Add Client" (visible in Workspace Switcher area)
**Then** a modal opens with fields: Client Name, Contact Email (optional)
**And** submitting the form provisions a new tenant via the API
**And** I am granted Owner access to the new tenant
**And** the Workspace Switcher updates to include the new client

---

## Epic 3: Visual Flow Builder & Skills System

Provides the visual canvas for designing conversation flows and configuring reusable Skills.

### Story 3.1: ReactFlow Canvas Setup

As a **User**,
I want a split-screen builder with a visual canvas,
So that I can design my bot's conversation flow intuitively.

**Acceptance Criteria:**

**Given** I open a bot in the builder
**When** the page loads
**Then** I see a resizable split-screen layout (60% Canvas / 40% Simulator placeholder)
**And** the canvas uses ReactFlow with pan, zoom, and minimap controls
**And** the initial graph renders in under 500ms (NFR-002)

### Story 3.2: Node Palette & Drag-and-Drop

As a **User**,
I want to drag nodes from a palette onto the canvas,
So that I can build my conversation flow visually.

**Acceptance Criteria:**

**Given** I am viewing the canvas
**When** I drag a node type from the palette
**Then** a new node of that type is created on the canvas
**And** the palette includes: Start, Send Text, User Input, AI Response, Handover

### Story 3.3: Node Configuration Panel

As a **User**,
I want to click a node and edit its properties in a side panel,
So that I can configure the bot's behavior.

**Acceptance Criteria:**

**Given** I click on a node
**When** the configuration panel opens
**Then** I see editable fields for the node's properties (e.g., text, prompt, keywords)
**And** changes are debounced and auto-saved

### Story 3.4: 30-Node Limit Enforcement

As a **User**,
I want to see a node counter and be warned before exceeding the limit,
So that I keep my bot performant and maintainable.

**Acceptance Criteria:**

**Given** I have 30 nodes on the canvas
**When** I try to add another node
**Then** I see a toast notification: "Node limit reached (30/30)"
**And** the drag-and-drop action is blocked

### Story 3.5: Skill Configuration UI

As a **User**,
I want to see Skill Tiles on my Template and configure them via a sheet,
So that I can customize Skills without editing the underlying flow.

**Acceptance Criteria:**

**Given** I am viewing a bot created from a Template
**When** I click on a Skill Tile
**Then** a configuration sheet opens with the Skill's editable variables (e.g., "Business Hours", "Greeting Text")
**And** saving the sheet updates the bot's active configuration

---

## Epic 4: Runtime Engine & Messenger Integration

The core engine that processes actual conversation traffic, manages state, and integrates with Messenger.

### Story 4.1: Messenger Webhook Endpoint

As a **Platform Operator**,
I want a webhook endpoint to receive Facebook Messenger events,
So that the bot can respond to user messages.

**Acceptance Criteria:**

**Given** a valid Messenger webhook request is received
**When** the HMAC signature is validated
**Then** the request is acknowledged with 200 OK within 2 seconds (NFR-001)
**And** the message is queued for processing via ARQ

**Given** an invalid HMAC signature
**When** the webhook request is received
**Then** the API returns 403 Forbidden

### Story 4.2: Conversation State Management

As a **User**,
I want the bot to remember conversation context across messages,
So that the interaction feels coherent.

**Acceptance Criteria:**

**Given** a user sends a message
**When** the runtime processes the message
**Then** conversation state (variables, history) is loaded from Redis
**And** state is updated and persisted after each response

### Story 4.3: Routing Logic (Keywords & AI)

As a **User**,
I want the bot to route messages based on keywords or AI,
So that the conversation follows the designed flow.

**Acceptance Criteria:**

**Given** a user message matches a keyword in the current node
**When** the routing logic runs
**Then** the conversation jumps to the configured target node

**Given** no keywords match
**When** the routing logic runs
**Then** the message is sent to LiteLLM with context-stuffed knowledge
**And** the AI response is sent to the user with a typing indicator (NFR-003)

### Story 4.4: Human Handover

As a **User**,
I want to be connected to a human agent when needed,
So that complex issues are resolved by a real person.

**Acceptance Criteria:**

**Given** the conversation reaches a Handover node
**When** the node is executed
**Then** auto-responses are stopped for this conversation
**And** the conversation is flagged for admin attention
**And** auto-responses resume after admin reset or a 24-hour timeout

### Story 4.5: Meta 24h Rule Enforcement

As a **Platform Operator**,
I want to block proactive messages outside the 24h window,
So that the platform complies with Meta's policies.

**Acceptance Criteria:**

**Given** an attempt to send a proactive message
**When** the user's last interaction was more than 24 hours ago
**Then** the message is blocked and logged
**And** the admin is notified of the compliance issue

---

## Epic 5: Simulator & Testing Tools

Ensures users can safely test and debug their bots before deployment, including "Context Stuffing" validation.

### Story 5.1: Chat Simulator Panel

As a **User**,
I want to test my bot in a simulator panel without affecting live users,
So that I can verify the flow before publishing.

**Acceptance Criteria:**

**Given** I am in the builder with a bot flow
**When** I type a message in the Simulator panel
**Then** the bot responds based on the current flow and knowledge
**And** the conversation is displayed with sender labels (User/Bot)
**And** the active node is highlighted on the canvas with a "Pulse" animation

### Story 5.2: Idempotent Replay

As a **User**,
I want to replay simulator conversations without side-effects,
So that I can test the same flow multiple times safely.

**Acceptance Criteria:**

**Given** I click "Replay" on a simulator session
**When** the replay starts
**Then** the conversation is re-executed from the beginning
**And** no actual API calls (e.g., to LLM or external services) are made (mock mode)

### Story 5.3: Token Meter (Brain Capacity)

As a **User**,
I want to see a "Brain Capacity" meter during knowledge upload,
So that I understand how much context is being used.

**Acceptance Criteria:**

**Given** I am uploading a PDF for knowledge
**When** the file is processed
**Then** a Token Meter shows the current usage vs. the ~50k token limit
**And** a warning is displayed if the limit is exceeded

### Story 5.4: Prune History

As a **User**,
I want to clear or trim conversation history in the simulator,
So that I can test fresh scenarios.

**Acceptance Criteria:**

**Given** I have an active simulator session
**When** I click "Clear History"
**Then** the conversation log is cleared
**And** the conversation state is reset to the Start node
