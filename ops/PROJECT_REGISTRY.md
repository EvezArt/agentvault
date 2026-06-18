# EVEZ Project Registry

Purpose: channel the operation through distinct projects instead of letting repos, deployments, skills, and experiments blur together.

This registry is the first convergence layer. It does **not** assume that every repo is production-ready. It names what each lane is for, what resources currently appear attached to it, and what should be treated as the source of truth.

## Operating rule

- One project = one primary mission.
- Multiple repos/deployments may support that mission.
- Shared infrastructure belongs in the vault / registry / plugin layers, not scattered ad hoc.
- Unknown or unverified connections stay marked as **observed**, not silently upgraded to truth.

## Project lattice

### 1) EVEZOS / Operator Console
**Mission:** primary command surface for the autonomous network.

**Observed resources**
- Lovable project: `925ea23a-ab93-48f2-ad0b-1073508312f5`
- Vercel project: `evez-operator`
- Vercel project: `evez-os`
- Domain observed on Vercel: `evez.art`

**Role split**
- `evez-operator`: operator-first control plane, immersive console, live cycle control.
- `evez-os`: public shell / root OS surface / likely brand-facing edge.
- Lovable project: mobile-first build surface for the next console iteration.

**Should own**
- n8n webhook configuration
- workflow health surface
- cycle execution UI
- deliverables stream
- local ledger witness UI
- terminal / agent identity switching

**Do not mix with**
- crawler internals
- plugin registry internals
- search engine internals

---

### 2) Autonomizer
**Mission:** orchestration and automation experiments that feed or graduate into EVEZOS.

**Observed resources**
- Vercel project: `evez-autonomizer`

**Should own**
- agent cycle prototypes
- webhook relay experiments
- queue behavior tests
- pre-production automation flows

**Promotion rule**
- Once stable, move surfaced operator functions into `EVEZOS / Operator Console`.

---

### 3) Truth Seeker
**Mission:** autonomous exploratory agent focused on narrative, signals, and higher-order synthesis.

**Observed resources**
- GitHub repo: `EvezArt/evez-truth-seeker`
- Vercel project: `evez-truth-seeker`
- Related repos named in README: `quantum-consciousness-lord`, `CrawFather/OpenClaw`, `agentvault`

**Declared architecture from repo README**
- quantum substrate layer
- agent interface layer
- memory vault layer

**Should own**
- seeker agent personality and mission logic
- external signal exploration
- higher-order synthesis workflows
- seeker-specific deliverables and memory trails

**Dependency rule**
- shared memory belongs in AgentVault
- shared skills belong in ClawHub / plugin system
- public operator UI belongs in EVEZOS

---

### 4) AgentVault
**Mission:** memory, audit trail, registry, and controlled persistence layer.

**Observed resources**
- GitHub repo: `EvezArt/agentvault`
- Existing repo purpose: secure agent vault, version control, access management, audit logging

**Should own**
- project registry
- append-only operational notes
- memory schema and storage adapters
- audit surfaces
- cross-project identity map

**This file lives here on purpose**
- the vault is the right place for cross-project registry material because it is closer to memory and audit than to any single UI.

---

### 5) Plugin / Skill / Soul System
**Mission:** publish, version, search, and govern reusable agent capabilities.

**Observed resources**
- GitHub repo: `EvezArt/CrawFather`
- README indicates ClawHub is the public skill registry and onlycrabs.ai is the SOUL registry
- Linear project observed: `EVEZ Plugin System`

**Should own**
- `SKILL.md` / `SOUL.md` publication
- plugin discovery
- skill registry health
- soul registry governance
- reusable capability packaging

**Boundary**
- project-specific agent behavior can consume skills from here
- project-specific UI and telemetry should not be implemented here

---

### 6) Search / Intelligence Layer
**Mission:** search-heavy reasoning, retrieval, and generative exploration.

**Observed resources**
- GitHub repo: `EvezArt/blockche`
- Vercel project: `blockche`
- Repo README identifies it as Morphic: AI-powered search engine with generative UI

**Should own**
- search UX
- retrieval experiments
- model/provider switching for search tasks
- operator search copilots if later embedded into EVEZOS

**Integration rule**
- can be embedded into EVEZOS as a panel
- remains a separate system of record for search/retrieval experiments

---

### 7) Simulation Lane
**Mission:** run world-state and scenario experiments outside the operator core.

**Observed resources**
- Vercel projects: `evez-sim`, `evez-sim-6hvo`

**Should own**
- shadow-world simulation
- cycle outcome projection
- scenario testing before production routing

---

### 8) Chat / Terminal Sandbox
**Mission:** isolate chat and terminal interaction experiments before merging into the main console.

**Observed resources**
- GitHub repos: `nextjs-ai-chatbot`, `nextjs-ai-1chatbot`
- Vercel projects with matching names

**Should own**
- chat UX experiments
- terminal memory behavior
- provider switching patterns
- response safety and interaction tests

**Promotion rule**
- only stable terminal patterns graduate into EVEZOS chat.

---

### 9) Visual / Interface Experiments
**Mission:** preserve fast visual exploration without contaminating core product structure.

**Observed resources**
- GitHub repo: `animated-goggles`
- Vercel project: `animated-goggles`

**Should own**
- interaction prototypes
- visual effects tests
- immersive UI fragments

---

## Consolidation matrix

| Lane | Primary truth | Deploy edge | Shared dependencies |
|---|---|---|---|
| EVEZOS / Operator Console | Lovable + Git repo to be designated | Vercel (`evez-operator`, `evez-os`) | n8n, OpenAI, AgentVault |
| Autonomizer | automation repo / workflow set | Vercel (`evez-autonomizer`) | n8n, AgentVault |
| Truth Seeker | `evez-truth-seeker` | Vercel (`evez-truth-seeker`) | AgentVault, ClawHub, quantum layer |
| AgentVault | `agentvault` | optional internal UI | all projects |
| Plugin / Skill / Soul System | `CrawFather` + Linear plugin project | ClawHub / onlycrabs | all agent projects |
| Search / Intelligence | `blockche` | Vercel (`blockche`) | OpenAI/search providers |
| Simulation Lane | sim repo(s) to be designated | Vercel (`evez-sim*`) | EVEZOS, AgentVault |
| Chat / Terminal Sandbox | `nextjs-ai-*` repos | Vercel (`nextjs-ai-*`) | OpenAI / relay backend |
| Visual / Interface Experiments | `animated-goggles` | Vercel (`animated-goggles`) | EVEZOS design system |

## Immediate next actions

1. Designate a single Git repo as the canonical codebase for `EVEZOS / Operator Console`.
2. Treat `evez.art` / `evez-os` as the public shell and `evez-operator` as the authenticated operator plane unless proven otherwise.
3. Keep shared memory and registry logic inside AgentVault.
4. Keep skills / souls / plugins inside CrawFather + the Linear plugin system project.
5. Keep seeker behavior in `evez-truth-seeker`, with dependencies referenced rather than duplicated.
6. Use simulation and chat repos as feeder lanes, not permanent dumping grounds.

## Unknowns still needing verification

- Which Git repo should become the long-term canonical EVEZOS codebase.
- Whether `evez-os` or `evez-operator` should own the primary production domain.
- Which n8n workflows are already live versus merely intended.
- Whether simulation currently has a dedicated repo or only deployment artifacts.
- Whether additional tracking systems (Asana, Airtable, etc.) are active and should be attached here.

## Integrity note

This registry is intentionally conservative. It records observed structure and proposed boundaries. It does not fabricate missing ownership, telemetry, or integration state.
