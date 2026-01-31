---
stepsCompleted: [1, 2]
inputDocuments:
  - /Users/sherwingorechomante/mantis/Mantis_Bot_PRD.md
session_topic: 'Mantis Bot - Skills System Evolution & Differentiation/Positioning'
session_goals: 'Generate innovative reusable skill ideas for marketplace and identify unique positioning against ManyChat, Chatfuel, and other chatbot builders'
selected_approach: 'ai-recommended'
techniques_used:
  - Reverse Brainstorming
  - Cross-Pollination
  - Future Self Interview
ideas_generated: []
context_file: '/Users/sherwingorechomante/mantis/_bmad/bmm/data/project-context-template.md'
---

# Brainstorming Session Results

**Facilitator:** team mantis
**Date:** 2026-01-31

## Session Overview

**Topic:** Mantis Bot - Skills System Evolution & Differentiation/Positioning

**Goals:**

1. Generate innovative reusable skill ideas for the marketplace
2. Identify unique positioning strategies against competitors (ManyChat, Chatfuel, etc.)

### Context: Mantis Bot PRD Summary

Mantis Bot is an **open-source, self-hosted chatbot automation platform** with these core differentiators:

| Feature | Description |
|---------|-------------|
| Goal-Driven Flows | Bots optimize toward business outcomes (not rigid message trees) |
| Explainable Decisions | Every bot message can be traced to why it was sent |
| Conversation Simulator | Test conversations before deployment |
| Skill-Based Architecture | Reusable bot behaviors that can be imported, versioned, and shared |
| Security-First UX | Privacy controls exposed to users, self-hosted by default |

**Target Users:** Small business owners, bot builders/freelancers, privacy-conscious organizations

**Current MVP Skills Examples:** Lead qualification, appointment booking, complaint handling, phone number capture

---

## Technique Selection

**Approach:** AI-Recommended Techniques
**Analysis Context:** Skills System + Differentiation with strategic and innovative focus

**Recommended Techniques:**

| Phase | Technique | Category | Purpose |
|-------|-----------|----------|---------|
| 1 | Reverse Brainstorming | Creative | Identify competitor weaknesses as differentiation opportunities |
| 2 | Cross-Pollination | Creative | Steal innovative ideas from other ecosystems (Shopify, Figma, etc.) |
| 3 | Future Self Interview | Introspective | Anchor long-term vision and identify killer skill concepts |

**AI Rationale:** This sequence moves from understanding the competitive landscape → innovating beyond it → anchoring a compelling future vision.

---

## Phase 1: Reverse Brainstorming - Competitive Intelligence Mining

**Technique:** Generate problems instead of solutions to identify hidden opportunities.

**Guiding Questions:**

- What annoys users most about existing chatbot builders?
- How could we make Mantis Bot *worse* than competitors?
- What do competitors promise but fail to deliver?

### Ideas Generated

#### Competitor Pain Points Identified

**[Pain Point #1]**: Spaghetti Flow Syndrome
*Problem*: Visual flow editors become cluttered and unmanageable as bot complexity grows. Lines crossing everywhere, nodes scattered randomly.
*Differentiation Opportunity*: Goal-driven flows that don't require visual spaghetti—behavior emerges from rules, not line drawings.

**[Pain Point #2]**: The "Why Did It Say That?" Mystery
*Problem*: When bots behave unexpectedly, users can't trace the decision path. Debugging is guesswork.
*Differentiation Opportunity*: Mantis Bot's Explainability Layer shows exactly which rule triggered, what alternatives were skipped, and current goal progress.

**[Pain Point #3]**: Contact-Based Hostage Pricing
*Problem*: Platforms charge extra as contact lists grow—punishing success.
*Differentiation Opportunity*: Self-hosted = unlimited contacts. No per-contact fees ever.

**[Pain Point #4]**: AI as Afterthought
*Problem*: Limited AI integration despite obvious potential for intent detection, smart responses, and conversation optimization.
*Differentiation Opportunity*: Phase 2 roadmap includes AI intent detection—but with explainability built-in.

---

#### Skill/Feature Concepts Emerging

**[Skill Concept #1]**: Auto-Generated Conversation Map
*Concept*: Rules create the bot behavior, but a visual "conversation map" auto-generates to show possible paths. It's read-only (not editable like competitor flows) but provides the mental model users expect.
*Novelty*: "Write rules, see the map" inverts the competitor model of "draw the map, configure nodes."
*Test/Preview Integration*: Click any node on the map to jump directly to that conversation state in the Simulator.

**[Skill Concept #2]**: Time-Travel Debugger
*Concept*: Replay any historical conversation step-by-step, seeing exactly which rule fired at each moment. "Rewind" to any point and change variables to explore "what if" scenarios.
*Novelty*: No competitor offers true conversation debugging. This transforms support from "guess and apologize" to "understand and fix."
*Use Case*: User complains about weird bot behavior → Open their history → Replay and identify the exact rule that misfired.

---

#### "Make It Worse" Inversions (Reverse Brainstorming)

**[Inversion #1]**: Complexity Despite Visuals → **True No-Code Simplicity**
*Anti-Pattern*: Visual flow builder that still requires code for advanced actions.
*Mantis Opportunity*: Every action achievable through forms/templates. Code is optional for power users, never required.

**[Inversion #2]**: Unfriendly/Illogical UI → **Plain-Language UX**
*Anti-Pattern*: Interface designed by developers for developers.
*Mantis Opportunity*: PRD already mentions "Plain-language UI"—double down on this as a core differentiator.

**[Inversion #3]**: Limited Platform Connections → **Connector Ecosystem**
*Anti-Pattern*: Messenger-only or limited platform support.
*Mantis Opportunity*: MVP has Messenger + Telegram. Phase 2: Plugin architecture for community-built connectors (WhatsApp, LINE, Instagram DMs, etc.)

**[Inversion #4]**: Linear-Only Thinking → **Non-Linear Goal Optimization**
*Anti-Pattern*: Bots that can only follow one path from start to finish.
*Mantis Opportunity*: Goal-driven architecture naturally supports non-linear conversations. Bot can handle interruptions, topic switches, and return to goals.

**[Skill Concept #3]**: Goal-Aware Interrupt Handler
*Concept*: Gracefully handles off-topic questions, loops back to the main goal, and tracks progress through chaotic conversations.
*Novelty*: Competitors reset or crash on interrupts. Mantis treats them as natural conversation.

**[Skill Concept #4]**: Flexible LLM Provider Integration
*Concept*: Support both self-hosted LLMs (via Ollama) AND cloud providers (OpenAI, Anthropic, etc.). User chooses based on privacy needs, cost, or performance.
*Novelty*: True "bring your own AI" model. Privacy-conscious users keep data local; others get cloud convenience.
*Marketplace Angle*: Skills can be LLM-agnostic OR optimized for specific providers.

---

## Phase 2: Cross-Pollination — Stealing from Other Industries

**Technique:** Borrow successful patterns from unrelated industries and apply them to chatbot/skill development.

**Industries to Raid:**

- 🛍️ **Shopify** — App ecosystem, themes, merchant tools
- 🎨 **Figma** — Plugins, community files, collaboration
- 🎵 **Spotify** — Playlists, discovery, personalization
- 📦 **npm/GitHub** — Package management, versioning, dependencies
- 🎮 **Gaming** — Mods, user-generated content, progression

### Ideas Generated

**[Cross-Pollination #1]**: Skill Packs (from Shopify App Bundles)
*Source*: Shopify's app bundles for specific merchant types
*Mantis Translation*: Curated skill bundles for industries/use cases
*Examples*: E-commerce Pack, Healthcare Pack, Real Estate Pack
*Value*: Faster onboarding—users start with verified, compatible skills

**[Cross-Pollination #2]**: One-Click Install + Simulator Preview (from Shopify)
*Source*: One-click app install with free trials
*Mantis Translation*: Import skill instantly; test in Simulator before going live
*Value*: Reduces fear of breaking production bots

**[Cross-Pollination #3]**: Fork & Customize (from Figma Community)
*Source*: Figma's "Duplicate to your drafts" for community files
*Mantis Translation*: Fork any public skill, customize it, keep your changes
*Value*: Learn from others' work; never start from scratch

**[Cross-Pollination #4]**: Skill Versioning + Inheritance (from Figma/npm)
*Source*: Figma component instances + npm package versioning
*Mantis Translation*: Skills can inherit from "master" skills; pull updates while keeping customizations
*Value*: Marketplace skills stay updated; users don't lose customizations

**[Cross-Pollination #5]**: Gamification + Achievement System (from Gaming)
*Source*: Steam achievements, player progression, badges
*Mantis Translation*: Badges for milestones (first skill, 1K convos, marketplace publisher)
*Value*: Makes bot building fun; drives community engagement

**[Cross-Pollination #6]**: Skill Conflict Detector (from Mod Load Order)
*Source*: Gaming mod managers that detect conflicts before breaking games
*Mantis Translation*: Pre-install check warns when skills might conflict
*Value*: Prevents "it worked until I added that skill" disasters

**[Cross-Pollination #7]**: Smart Skill Recommendations (from Spotify Discovery)
*Source*: Spotify's "Discover Weekly" and "Because you listened to..."
*Mantis Translation*: AI suggests skills based on your bot's goals, industry, and current setup
*Value*: Turns "I don't know what I need" into guided discovery

**[Cross-Pollination #8]**: Skill Playlists by Power Users (from Spotify Playlists)
*Source*: User-curated playlists shared publicly
*Mantis Translation*: Top builders share skill combinations ("Maria's Real Estate Stack")
*Value*: Social proof + real-world tested combinations

**[Key Positioning Insight]**: App as Partner, Not Tool
*Insight*: Mantis Bot should feel like a knowledgeable partner that learns your business, suggests improvements, and grows with you—not just a static tool you configure.
*Differentiation*: Competitors are "draw a flow, hope it works." Mantis is "your bot-building partner."

---

## Phase 3: Future Self Interview — Anchoring the Vision

**Technique:** Imagine Mantis Bot 3 years from now, wildly successful. Interview your future self to uncover what made it work.

### Future Self Prompts

**[Future Vision #1]**: The Trifecta That Won
*Question*: What made users fall in love?
*Answer*: **Flexibility + Intelligence + Personalization** — The app became a partner, not just a tool.
*Core Thesis*: "Partner, not tool" is the positioning north star.

---

**[Future Vision #2]**: E-commerce as Blueprint Industry
*Question*: What was the breakthrough skill?
*Answer*: **E-commerce skills** — highly transferable patterns (order tracking, returns, recommendations) that creators adapt for other industries.
*Strategic Implication*: Build e-commerce as the "reference implementation" for the marketplace.

---

**[Future Vision #3]**: The Integration Gap Regret
*Question*: What was your biggest regret?
*Answer*: **Limited connectors at launch** — Should have prioritized plugin architecture. Missing: Facebook post triggers, Instagram DMs, WhatsApp.
*Lesson*: Build connector plugin architecture into Phase 2. Community can extend faster than core team.

---

## Session Summary

**Total Ideas Generated: 25+**

### Key Themes Emerged

1. **"Partner, Not Tool"** — Core positioning thesis
2. **Explainability as Differentiator** — Time-Travel Debugger, conversation maps
3. **Skill Marketplace Innovation** — Packs, versioning, inheritance, recommendations
4. **Gamification** — Achievements to drive engagement
5. **Flexible AI** — Ollama + cloud providers
6. **E-commerce as Blueprint** — Reference implementation for other industries
7. **Integration Priority** — Plugin architecture critical for Phase 2
