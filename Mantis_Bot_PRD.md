# 📘 Product Requirements Document (PRD)

## Project Name: **Mantis Bot**  

*A Secure, Goal-Driven, Open-Source Chatbot Automation Platform*

---

## 1. Overview

### 1.1 Product Vision

Mantis Bot is an open-source, self-hosted chatbot automation platform designed to help non-technical users build **goal-driven, explainable, and secure conversational systems** for Messenger and Telegram.

Unlike traditional chatbot builders that rely on rigid message flows, Mantis Bot focuses on:

- Business goals
- Conversation state
- Transparency and trust
- Security-by-design

---

## 2. Goals & Objectives

### 2.1 Primary Goals

- Enable users to build chatbots **without coding**
- Make bot behavior **explainable and debuggable**
- Provide **enterprise-grade security** using only open-source tools
- Allow full **data ownership** via self-hosting

### 2.2 Non-Goals (MVP)

- No AI-generated conversations
- No payment processing
- No drag-and-drop visual editor (form-based first)
- No multi-language NLP

---

## 3. Target Users

### 3.1 Personas

#### A. Small Business Owner

- Laundry shops
- Clinics
- Online sellers
- Wants automation without complexity

#### B. Bot Builder / Freelancer

- Builds bots for clients
- Needs reusable components
- Wants transparency and control

#### C. Privacy-Conscious Organization

- Needs data isolation
- Requires auditability
- Prefers self-hosted solutions

---

## 4. Core Differentiators

| Feature | Description |
|------|------------|
| Goal-Driven Flows | Bots optimize toward business outcomes |
| Explainable Decisions | Every bot message can be traced |
| Conversation Simulator | Test conversations before deployment |
| Skill-Based Architecture | Reusable bot behaviors |
| Security-First UX | Privacy controls exposed to users |
| Partner Experience | App learns your business, suggests improvements, grows with you |
| Flexible AI | Bring your own LLM (Ollama self-hosted OR cloud providers) |

---

## 5. Functional Requirements

### 5.1 Authentication & Authorization

- Role-based access control (RBAC)
- Roles:
  - Admin
  - Bot Manager
  - Read-only Viewer
- OAuth2 / JWT-based authentication
- Powered by **Keycloak**

---

### 5.2 Bot Management

- Create / edit / delete bots
- Assign platform connectors
- Enable / disable bots
- Environment separation (test / live)

---

### 5.3 Platform Connectors

#### Supported Platforms (MVP)

- Facebook Messenger
- Telegram

#### Connector Requirements

- Webhook validation
- Token rotation
- Platform abstraction layer
- Rate limiting

---

### 5.4 Flow System (Goal-Driven)

#### Flow Definition

Each flow consists of:

- Goal
- Entry condition
- Rules
- Actions
- Exit conditions

Example Goal:
> Collect user phone number

---

### 5.5 Rules Engine

Supported rule types:

- Keyword match
- Button click
- Tag exists
- Variable value
- Fallback timeout

Rules are evaluated in priority order.

---

### 5.6 Actions

Supported actions:

- Send text message
- Send button options
- Save variable
- Add / remove tag
- Jump to flow
- Trigger webhook

---

### 5.7 Skills System

Skills are reusable mini-flows.

#### MVP Skills (E-commerce Blueprint)

- Lead qualification
- Appointment booking
- Complaint handling
- Phone number capture
- Order status tracking
- Returns handling

#### Skill Capabilities

- **Import** — One-click install with Simulator preview
- **Version** — Track changes, rollback if needed
- **Share** — Publish to marketplace
- **Fork** — Customize public skills while keeping your changes

#### Marketplace Features (Phase 2+)

- **Skill Packs** — Curated bundles for industries (E-commerce, Healthcare, Real Estate)
- **Smart Recommendations** — AI suggests skills based on your bot's goals
- **Skill Playlists** — Community-curated collections

---

### 5.8 Conversation State Management

Each user has:

- Current goal
- Active flow
- Variables
- Tags
- Interaction history

State is persisted in PostgreSQL.

---

### 5.9 Conversation Simulator

- Simulated chat UI
- Shows:
  - Triggered rules
  - Goal progress
  - Fallback usage
- Allows step-by-step replay

---

### 5.10 Explainability Layer

For every bot message:

- Why it was sent
- Which rule triggered
- What alternatives were skipped
- Current goal completion %

#### Advanced Explainability Features

- **Auto-Generated Conversation Map** — Visual read-only map shows all possible paths; click any node to test in Simulator
- **Time-Travel Debugger** — Replay historical conversations step-by-step; see exactly which rule fired at each moment

---

### 5.11 Broadcasting

- Send message to:
  - All users
  - Users with tags
- Throttling and rate limits
- Opt-out handling

---

## 6. Security Requirements

### 6.1 Webhook Security

- Signature validation
- Replay protection
- IP allow-listing

### 6.2 Data Protection

- Tenant-based data isolation
- PII masking
- Optional auto-delete policies

### 6.3 Rate Limiting

- Per-user
- Per-bot
- Per-platform

---

## 7. Non-Functional Requirements

### 7.1 Performance

- Message processing < 300ms
- Scales horizontally

### 7.2 Reliability

- Graceful degradation
- Retry queues

### 7.3 Maintainability

- Modular architecture
- Clear separation of concerns

---

## 8. Tech Stack

| Layer | Technology |
|----|-----------|
| Backend | FastAPI |
| Database | PostgreSQL |
| Cache / Queue | Redis |
| Auth | Keycloak |
| Frontend | Svelte or React |
| Containerization | Docker |
| Messaging Queue | Celery / RQ |

---

## 9. API Design (High-Level)

- `/auth/*`
- `/bots/*`
- `/flows/*`
- `/skills/*`
- `/messages/*`
- `/simulator/*`

All APIs are REST-first.

---

## 10. MVP Scope

### Included

- Bot creation
- Goal-driven flows
- Rule-based engine
- Messenger + Telegram
- Simulator
- Explainability UI (including Auto-Generated Conversation Map)
- Security basics
- **Flexible LLM Integration** (Ollama self-hosted + cloud providers)
- E-commerce skill pack (reference implementation)

### Excluded

- Full AI/NLP intent engine (Phase 2)
- Payments
- Drag-and-drop UI
- Multi-language

---

## 11. Future Roadmap

### Phase 2

- Visual flow editor
- AI intent detection (building on Flexible LLM foundation)
- Full skill marketplace with:
  - Skill Packs (industry bundles)
  - Smart Recommendations
  - Fork & Customize
  - Versioning + Inheritance
- Connector plugin architecture (WhatsApp, Instagram DMs, Facebook posts)
- Gamification system (achievements, badges, creator levels)
- Time-Travel Debugger

### Phase 3

- Analytics dashboard
- Voice bots
- CRM integrations
- Advanced skill marketplace (recommendations, playlists)

---

## 12. Success Metrics

- Time to first working bot < 15 minutes
- Bot creation success rate
- Simulator usage
- Error rate reduction

---

## 13. Risks & Mitigations

| Risk | Mitigation |
|----|-----------|
| Complexity creep | Strict MVP scope |
| Security misconfig | Defaults + audits |
| UX confusion | Plain-language UI |

---

## 14. Appendix

- Open-source license: AGPL or Apache 2.0
- Self-hosted by default
- Cloud optional

---

**End of PRD**
