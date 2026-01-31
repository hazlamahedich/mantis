---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments:
  - /Users/sherwingorechomante/mantis/Mantis_Bot_PRD.md
  - /Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/brainstorming/brainstorming-session-2026-01-31.md
  - /Users/sherwingorechomante/mantis/_bmad-output/planning-artifacts/architecture.md
date: 2026-01-31
author: team mantis
workflowType: 'product-brief'
status: 'in-progress'
---

# Product Brief: Mantis Bot

> **The chatbot builder that knows what it's trying to accomplish.**

---

## Executive Summary

Mantis Bot is a goal-driven, open-source chatbot automation platform that helps small business owners build intelligent, explainable conversational systems for Messenger and Telegram — without writing code.

**The Problem:** SMEs lose up to 40% of customer inquiries after hours because chatbot builders either require technical skills they don't have, or lock them into expensive platforms they can't control. Traditional builders focus on *message flows*, not *business outcomes*.

**The Solution:** A platform where bots are defined by **business goals**, not rigid scripts. Every bot decision is traceable. Every conversation serves a purpose. Users choose between **managed hosting** for simplicity or **self-hosting** for complete data ownership.

**Why Now:** The rise of LLMs makes conversational AI accessible, but creates new trust and transparency challenges. Mantis Bot addresses this by making AI decisions explainable and auditable — while letting users bring their own LLM (Ollama, OpenAI, or any provider).

---

## Core Vision

### Problem Statement

Small business owners and privacy-conscious organizations face a painful choice:

1. **Complex platforms** that require developers or expensive agencies
2. **Simple builders** that lack real business intelligence and lock users into vendor ecosystems
3. **Generic chatbots** that frustrate customers with rigid, unpredictable responses

This leaves SMEs losing customer opportunities after hours, and privacy-focused organizations unable to trust third-party platforms with their data.

### Who Experiences This Problem

#### Primary: Small Business Owner

- Laundry shops, clinics, online sellers
- Wants automation that "just works"
- Needs to serve customers 24/7 without hiring staff
- Values transparency and simplicity

#### Secondary: Bot Builder / Freelancer

- Builds bots for multiple clients
- Needs reusable, transparent components
- Wants to scale without reinventing the wheel

#### Tertiary: Privacy-Conscious Organization

- Requires data isolation and auditability
- Must comply with data sovereignty requirements
- Prefers self-hosted, open-source solutions

### Proposed Solution

Mantis Bot is "Canva for chatbots" — making professional-grade automation accessible to non-developers while providing the power and flexibility that technical users demand.

**Core Principles:**

1. **Goal-Driven Design** — Bots optimize toward business outcomes, not just message delivery
2. **Explainable Decisions** — Every bot response can be traced back to its reasoning
3. **Your Data, Your Control** — Self-hosted OR managed, with full data portability
4. **Flexible AI** — Bring your own LLM (Ollama self-hosted or cloud providers)

### Key Differentiators

| Feature | What Makes It Special |
|---------|----------------------|
| **Goal-Driven Flows** | Bots understand WHY they're responding, not just WHAT to say |
| **Explainable Decisions** | Full trace from user input to bot response |
| **Conversation Simulator** | Test and debug conversations before going live |
| **Skill-Based Architecture** | Reusable bot behaviors across multiple bots |
| **Partner Experience** | Platform learns your business and suggests improvements |
| **Deployment Flexibility** | Self-hosted for control OR managed for simplicity |

## Target Users

### Primary Users

#### Maria — The Small Business Owner (SME)

**"I just want to answer customers while I'm resting — without hiring anyone or learning code."**

- **Context:** Runs a laundry shop in Quezon City with 2 staff. Uses Facebook Messenger for everything.
- **Tech Level:** Smartphone-first user; uses laptop only for "heavy" admin (payroll/inventory). Comfortable with Canva/Excel, intimidated by "coding".
- **Pain:** Loses 3-5 customer inquiries nightly; can't afford a dedicated VA (Virtual Assistant); tried ManyChat but got stuck on complex logic flows.
- **Goal:** Automation that handles pricing questions, pickup scheduling, and order status updates so she can sleep.
- **Success Moment:** Wakes up to 3 confirmed bookings that happened automatically overnight.

#### Paolo — The Bot Builder / Freelancer (Distribution Partner)

**"I need something I can reuse across clients without rebuilding from scratch."**

- **Context:** Builds bots for 5+ Philippine SME clients; charges ₱10-30k per bot.
- **Role:** Power User & Force Multiplier (1 Paolo = 10 Marias).
- **Pain:** Every new client requires starting from zero; no central visibility when client bots break; hard to justify retainer fees without ongoing value.
- **Goal:** A platform with reusable skills/templates and a multi-tenant dashboard to manage all clients.
- **Success Moment:** Deploys a complex new client bot in 2 hours instead of 2 weeks using his own template library.

### Secondary Users

#### Dr. Santos — Privacy-Conscious Organization

- **Context:** Medical clinic director; needs appointment booking.
- **Pain:** HIPAA-adjacent concerns; cannot trust cloud platforms with patient names/conditions.
- **Requirement:** Must self-host; full data ownership is non-negotiable.

#### The Staff Member (End User)

- **Role:** Maria's employee who receives the handoff from the bot.
- **Context:** Needs to see "Bot handled this" vs "Needs human attention".
- **Goal:** Easy escalation; seamless takeover of conversation without confusing the customer.

### User Journey (Maria's path)

| Stage | Activity | Emotional State | Failure/Recovery Path |
|-------|----------|----------------|-----------------------|
| **Discovery** | Finds Mantis Bot via Paolo's recommendation or Facebook ad. | *Curious but skeptical* | |
| **Onboarding** | Sign up -> Select "Laundry Shop" template -> Connect Page. | *Relieved* ("It's not code!") | **Failure:** Template setup fails.<br>**Recovery:** "Self-repair" suggestions or instant chat with support. |
| **Core Usage** | Bot answers FAQs, schedules pickups. Maria checks daily summary. | *Confident* | **Failure:** Bot answers wrongly.<br>**Recovery:** Trace view shows *why* → Maria updates rule easily. |
| **Aha Moment** | Sees dashboard: "15 bookings automated this week" (₱4k value). | *Empowered* | |
| **Long-term** | Adds complex promos; Paolo upsells advanced "Loyalty Skill". | *Expert / Dependent* | |

### Party Mode Insights Applied

**From Sally (UX):** Added Maria's "Smartphone-first" context.
**From Ana (BA):** Defined Paolo as a "Distribution Partner" / Force Multiplier.
**From Barty (Dev):** Added "Staff Member" persona for human-handoff handling.
**From Murat (QA):** Added "Failure/Recovery" columns to the User Journey.

## Success Metrics

### User Success Metrics (Outcomes)

#### For Maria (SME Owner)

- **"The Sleep Metric":** 0 inquiries lost between 10 PM and 6 AM.
- **Conversion Impact:** >10% of automated chats result in a confirmed booking/order.
- **Effort Reduction:** <5 minutes spent per day reviewing bot conversations.

#### For Paolo (Bot Builder)

- **Deployment Velocity:** Time to deploy a new client bot reduced from 2 weeks to <4 hours.
- **Reuse Rate:** >60% of bot logic reused across multiple clients (via templates).
- **Maintenance Load:** <1 hour/month spent on detailed maintenance per active bot.

### Business Objectives (The "Why")

1. **Validate the "Distribution Partner" Model:** Prove that empowering 1 Paolo is more efficient than selling to 10 Marias directly.
2. **Establish "Self-Hostable" Credibility:** Win trust from privacy-conscious users (Dr. Santos) to differentiate from SaaS competitors.
3. **Create "Sticky" Templates:** Build a library of community-shared templates that makes switching away from Mantis difficult.

## MVP Scope

### Core Features (The "Must-Haves")

1. **Visual Flow Builder (The "Canva"):** Drag-and-drop canvas to build bot logic. No JSON editing.
2. **3 Essential Skills (Pre-built):**
    - **FAQ Skill:** Keyword -> Answer (e.g., "Price" -> "₱35/kg").
    - **Scheduler Skill:** Calendar picker for pickups.
    - **Broadcast Skill:** Send "Promo Alert" to past customers.
3. **✨ Hybrid AI Engine (Rule + LLM Fallback):**
    - **Architecture:** LiteLLM router handles distinct flow types (Command -> Rule -> RAG -> Fallback).
    - **Safety:** Mandatory "Grounding Prompt" to preventing hallucination (e.g., "Do not answer math questions").
    - **Context Strategy:** **"Context Stuffing"** (No RAG). We extract raw text from uploads and inject it directly into the LLM's context window.
    - **Billing:** "Bring Your Own Key" (BYOK) model to avoid complex metering in MVP.
4. **Paolo’s Dashboard (Multi-tenant):** Single view to manage 10+ disconnected client bots.
5. **Deployment:** One-click deploy to Facebook Messenger.
6. **Analytics:** "The Sleep Metric" dashboard.

### 4. Skill & Template Strategy

- **Skills:** Reusable logic blocks (e.g., "Calculator", "Scheduler").
- **Templates:** Pre-packaged collections of Skills + Flows (e.g., "Salon Template" = Scheduler Skill + FAQ Flow).

### Out of Scope for MVP

- **Token Billing/Metering System:** Users must provide their own API keys.
- **Voice/Audio Support:** Text-only for launch.
- **Payment Gateway Integration:** Offline payments only.
- **WhatsApp/Instagram:** Messenger only (90% market share).
- **Complex Agentic Actions:** No autonomous web browsing or external API execution beyond simple webhooks.

### MVP Success Criteria

- **Functional:** A non-technical user (Maria) can edit a flow text in < 2 minutes.
- **Reliability:** LLM Fallback creates < 1% "hallucination complaints" (monitored via "Thumbs Down" feedback).
- **Adoption:** 2 "Paolo" partners onboard 10 active bots in first month.

### Future Vision (The "Dream")

- **The "Skill Store":** Marketplace for Paolos to sell templates.
- **"Auto-Pilot" Mode:** Fully autonomous agent handling complex support tickets.
- **Omnichannel:** One flow deploys to Messenger, Insta, Telegram, and Viber.

### Party Mode Insights Applied

**From Winston (Arch):** Added LiteLLM routing requirement.
**From Barry (Dev):** Enforced BYOK to avoid billing complexity.
**From Murat (QA):** Added Mandatory Grounding Prompts for safety.
**From Sally (UX):** Requirement to visually distinguish AI vs. Rule responses.
