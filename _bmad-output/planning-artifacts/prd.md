---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish']
inputDocuments:
  - /Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/product-brief-mantis-2026-01-31.md
  - /Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/brainstorming/brainstorming-session-2026-01-31.md
---

# Product Requirements Document (PRD): Mantis Bot

> **Version:** 1.0 (MVP)
> **Status:** Approved for Implementation
> **Project Type:** SaaS / Agency-in-a-Box
> **Core Concept:** "The 15-Minute AI Agency"

---

## 2. Vision & Problem Statement

**Mantis** is a specialized, "Agency-in-a-Box" chatbot platform designed for **Distributors (Agencies)** to rapidly deploy AI assistants for **SMEs (Clients)**. Unlike generic builders (ManyChat) that require hours of configuration, Mantis focuses on **speed**, **simplicity**, and **vertical-specific templates**.

**The Problem:**

- **Agencies (Paolo):** Cannot scale because building custom bots takes too long and client hand-holding is expensive.
- **SMEs (Maria):** Cannot afford expensive custom dev and find tools like ManyChat too complex to self-manage.

**The Solution:**
A "Cookie-Cutter" Factory. Paolo selects a "Salon Template", uploads Maria's price list, and deploys. *Fast, compliant, and strictly scoped for lead capture.*

---

## 3. Success Criteria

### User Success (The "Wow" Moment)

- **Distributor (Paolo):** Can deploy a fully functional bot for a new client in under **15 minutes**.
- **Client (Maria):** Receives her first "Qualified Lead" (Name, Phone, Service Interest) via email within **24 hours** of launch.

### Business Success (KPIs)

- **Activation Rate:** 40% of deployed bots process >10 conversations in Week 1.
- **Support Load:** < 1 Support Ticket per 5 Deployed Bots per Month (Prove reliability).

### Technical Success

- **Stability:** **99.5% Uptime** for the Runtime Engine.
- **Performance:** **< 5s Latency** for Webhook Acknowledgement (Meta Requirement).

---

## 4. User Personas & Journeys

### Persona A: Paolo (The Distributor / Power User)

*An entrepreneur running a "Micro-SaaS Agency". He is technically literate but time-poor. He wants to sell subscriptions, not hours.*

**Journey: The "15-Minute Deployment"**

1. **Login:** Paolo logs into his Mantis Dashboard.
2. **Create:** Clicks "New Bot" -> Selects "Hair Salon Template".
3. **Config:** Uploads Maria's "Service Menu.pdf" into the Knowledge Base.
4. **Connect:** Scans the QR code to connect Maria's Facebook Page.
5. **Test:** Uses the "Preview" chat to verify the AI knows the prices.
6. **Handover:** Shares the credentials (or keeps them managed) and tells Maria "It's live!".

### Persona B: Maria (The SME Client / End User)

*A salon owner. Non-technical. Wants more bookings, less chatting.*

**Journey: The "Hidden Beneficiary"**

1. **Receive:** Maria gets a "Morning Report" email summarizing yesterday's chats.
2. **Optional Access:** Maria *can* log in to view the bot, but primarily relies on Paolo or the email reports.
3. **Result:** She sees her calendar filling up without touching her phone.

---

## 5. Domain Requirements & Constraints

### 5.1 Meta Platform Policy (Strict Compliance)

- **24-Hour Rule:** The bot MUST NOT send proactive messages to users who haven't interacted in the last 24 hours.
- **Handover Protocol:** The bot must essentially "pause" if a human admin seeks to intervene (via Inbox).

### 5.2 AI Safety

- **Hallucination Control:** Low Temperature (0.2) and strict System Prompts to prevent the bot from offering discounts or services not in the Knowledge Base.
- **Disclosure:** The bot must identify itself as an AI (EU AI Act Compliance).

---

## 6. Strategic "Agency-in-a-Box" Scope (MVP)

To achieve the "15-Minute" promise, we make specific scope trade-offs:

| Feature | Scope Decision (MVP) | Rationale |
| :--- | :--- | :--- |
| **Channels** | **Facebook Messenger ONLY** | WhatsApp/IG require complex Business Verification (KYB/KYC) that blocks rapid MVP adoption. |
| **Builder** | **Strict 30-Node Limit** | Prevents "Spaghetti Bots". Forces simplicity and reliability. |
| **Templates** | **Pre-Baked JSONs** | Paolo clones "Salon V1" to create "Salon V2". No public marketplace yet. |
| **Auth** | **Unified Account** | Simple Email/Pass. Paolo can own it, or Maria can own it. No complex RBAC tiers yet. |
| **AI** | **Context Stuffing** | No Vector DB (RAG) for MVP. Raw text is extracted and injected into the System Prompt. Limit: ~50k tokens. |

---

## 7. Functional Requirements

### 7.1 The Dashboard & Account

- **FR-001 (Dashboard):** User can view a list of "My Bots" with status (Active/Draft).
- **FR-002 (Auth):** User can Sign Up / Login via Email & Password or Google OAuth.
- **FR-003 (Cloning):** User can "Duplicate" an existing bot to start a new project quickly.

### 7.2 The Builder (ReactFlow Canvas)

- **FR-010 (Canvas):** Visual, drag-and-drop editor.
- **FR-011 (Nodes):** specific supported node types:
  - `Start` (Trigger)
  - `Send Text` (Static response)
  - `User Input` (Wait for reply + Variable Capture)
  - `AI Response` (LLM Generation)
  - `Handover` (Pause Bot, Notify Admin)
- **FR-012 (Limits):** Hard limit of **30 Nodes** per flow.
- **FR-013 (Safety):** "Test/Preview" window available inside the builder.

### 7.3 The Runtime Engine

- **FR-020 (Webhook):** Handles incoming Facebook Messenger webhooks.
- **FR-021 (State):** Maintains conversation state (Context, Variables) for active sessions.
- **FR-022 (Routing):** Executes logic: If *Keyword Match* -> Jump to Node; Else -> AI Response.
- **FR-023 (Handover):** If Handover Node reached -> Stop auto-responses until timeout (e.g., 30m) or Admin reset.

### 7.4 Reporting

- **FR-030 (Email):** System sends a daily HTML summary to the registered Account Email.
  - Metrics: Total Conversations, Leads Captured.

### 7.5 Skills System

- **FR-040 (Definition):** A Skill is a reusable package of Logic (Flow) + Configuration (Variables).
- **FR-041 (Composition):** Users generally do not "build from scratch"; they instantiate Templates, which are pre-configured collections of Skills.
- **FR-042 (Marketplace Prep):** The architecture must support importing/exporting Skills as standalone units (Phase 2).

---

## 8. Non-Functional Requirements (Quality Attributes)

### Performance

- **NFR-001 (Webhook Latency):** The Runtime Engine must acknowledge a Messenger webhook (200 OK) within **2 seconds** (P95).
- **NFR-002 (Editor Responsiveness):** The ReactFlow Builder must render the initial graph (30 nodes) in under **500ms**.
- **NFR-003 (AI Latency):** The "Typing Indicator" must be displayed immediately (within 200ms) while waiting for the LLM response.

### Security

- **NFR-010 (Tenant Isolation):** Data access must be "Logically Isolated" via ORM Middleware. A query from Account A *cannot* physically return rows from Account B.
- **NFR-011 (Token Encryption):** All Facebook Page Access Tokens and OpenAI/Anthropic Keys must be encrypted at rest (AES-256).

### Compliance (Meta & AI)

- **NFR-020 (Meta 24h Rule):** **Strict Enforcement.** The system must block "Proactive Messages" sent to a user who has not interacted in the last **24 hours**. No "Message Tags" supported in MVP.
- **NFR-021 (AI Disclosure):** The "Start" node of every template must include default text: *"I am an AI assistant..."* (EU AI Act).

### Reliability

- **NFR-030 (Uptime):** 99.5% Availability during business hours.

---

## 9. Future Roadmap (Post-MVP)

- **Phase 2 (Growth):** Instagram/WhatsApp Integration, RAG (Vector DB) for large PDF support, Team Permissions (RBAC).
- **Phase 3 (Expansion):** Template Marketplace, Voice AI Integration, CRM Integrations (HubSpot/Salesforce).
