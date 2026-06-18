# Phased Convergence Plan

Purpose: turn the topology decision into concrete moves without collapsing distinct systems into one repo.

## North star

Preserve the real layers already present in the operation:
- public brand shell
- operator/API spine
- simulation lane
- memory/registry/audit layer
- plugin/skill/soul layer
- chat sandbox lane

The goal is convergence of **ownership and interfaces**, not reckless code fusion.

---

## Phase 0 — freeze the naming drift

### Problem
Deployment names and repo identities currently blur together.
The most dangerous confusion is that the live `evez-operator` deployment is sourced from `surething-offline`, while `evez-os` owns the public brand/domain surface.

### Actions
1. In all architecture docs, refer to:
   - `EvezArt/evez-os` as **brand shell / public surface**
   - `EvezArt/surething-offline` as **operator spine** with logical alias **evez-operator-api**
2. Stop referring to deployment names as though they are repository names.
3. Update future build briefs, README cross-links, and internal notes to use the same language.

### Exit criteria
- No core doc describes `evez-operator` as though it were a standalone canonical repo.
- All docs distinguish shell vs spine.

---

## Phase 1 — establish interface contracts

### A. Operator API contract
System of record: `surething-offline`

Define and stabilize:
- `/tools`
- `/spine/event`
- `/spine/verify`
- `/spine/events`
- `/contradictions`
- `/deploy/status`
- `/fire/anchor`

Add a single markdown contract doc that specifies:
- request shapes
- response shapes
- error states
- which fields are authoritative
- which fields are temporary placeholders

### B. Public shell contract
System of record: `evez-os`

Define what the shell does:
- identity / public product framing
- visual cognition layer surfaces
- public dashboard or landing shell
- embedded or proxied operator status cards

### C. Simulation contract
System of record: `evez-sim`

Define what can flow from sim into shell or spine:
- scenario output
- world-state snapshots
- cycle projections
- failure-surface summaries

### Exit criteria
- Shell, spine, and sim each have explicit API/content boundaries.
- Any UI work can now target known endpoints instead of folklore.

---

## Phase 2 — wire the mobile operator console correctly

### Problem
The new immersive operator console should not be pointed at the wrong repo or static shell artifacts.

### Actions
1. Treat the mobile operator console as a **client of the operator spine**.
2. Point live health, ledger, contradiction, and cycle surfaces at `surething-offline` endpoints first.
3. Use `evez-os` for brand shell and embedded operator entry points.
4. Keep simulation feeds optional and additive, not blocking.
5. Persist local-only UI state separately from system-of-record event history.

### Data priorities
1. authoritative live data from operator spine
2. derived status from simulation lane
3. local persisted UI state
4. dry-run state when integration is absent

### Exit criteria
- Console can run against live operator endpoints.
- Unconfigured states are explicit.
- Static fake telemetry is eliminated.

---

## Phase 3 — memory and audit hardening

System of record: `agentvault`

### Actions
1. Keep topology docs, ADRs, and registry material in AgentVault.
2. Add a canonical index of:
   - repos
   - deployments
   - domains
   - logical aliases
   - owning layer
3. Add append-only operational entries when major architecture moves happen.
4. Define a minimal schema for architectural decision records and registry updates.

### Exit criteria
- Cross-project memory lives in one place.
- Future analysis can read history instead of reconstructing it from scraps.

---

## Phase 4 — capability extraction

System of record: `CrawFather` / ClawHub / onlycrabs

### Actions
1. Extract reusable skills and souls from project-specific repos.
2. Keep project-specific behavior local unless it is truly reusable.
3. Link project repos to the shared skill registry instead of duplicating capability docs.

### Exit criteria
- Shared capability layer is real.
- Product repos stop pretending to be registries.

---

## Phase 5 — naming repair and migration

### Recommended order
1. Keep production stable.
2. Update docs and registry first.
3. Add README cross-links between `evez-os` and `surething-offline`.
4. Only then choose one of:
   - rename `surething-offline` to `evez-operator-api`, or
   - create a new `evez-operator-api` repo and migrate deliberately.

### Do not do
- do not merge shell and spine blindly
- do not rename live production repos before the docs and contracts are aligned
- do not move simulation into the shell repo just because it shares vocabulary

### Exit criteria
- Human-readable names match actual function.
- Production routing survives the rename.

---

## Immediate tasks

### 1. Docs
- [ ] Add README note in `evez-os` linking to operator spine
- [ ] Add README note in `surething-offline` identifying it as operator spine / logical `evez-operator-api`
- [ ] Keep ADR and registry in AgentVault current

### 2. Console integration
- [ ] Update build brief so mobile console targets operator spine endpoints
- [ ] Define dry-run vs live-run behavior explicitly
- [ ] Define expected response format for cycle and ledger surfaces

### 3. Deployment hygiene
- [ ] Audit which Vercel projects map to which repos
- [ ] Mark experiments vs production in registry
- [ ] Decide whether `evez.art` remains shell-only or becomes an entry shell to operator functions

### 4. Data model
- [ ] Define event schema for operator actions
- [ ] Define contradiction schema
- [ ] Define ledger entry schema
- [ ] Define workflow invocation schema

---

## Canonical ownership summary

| Layer | Canonical system |
|---|---|
| Brand shell / public surface | `EvezArt/evez-os` |
| Operator/API spine | `EvezArt/surething-offline` (logical: `evez-operator-api`) |
| Simulation | `EvezArt/evez-sim` |
| Memory / registry / audit | `EvezArt/agentvault` |
| Shared skills / souls / plugins | `EvezArt/CrawFather` |
| Chat sandbox | `EvezArt/nextjs-ai-chatbot`, `EvezArt/nextjs-ai-1chatbot` |

---

## Decision rule for future work

When a new feature appears, decide in this order:
1. Is it shared memory or registry? → AgentVault
2. Is it reusable capability? → CrawFather / ClawHub
3. Is it operator logic or system truth? → operator spine
4. Is it public shell / brand / visual cognition surface? → evez-os
5. Is it world-state or scenario simulation? → evez-sim
6. Is it merely experimental chat UX? → chat sandbox

If the answer is unclear, do not merge by instinct. Add it to the registry and classify first.
