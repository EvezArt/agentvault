# Active Context Snapshot

Last updated: 2026-03-19
Status: active bootstrap context for future project moves.

Use this file first before touching any EVEZ project lane.

---

## Current architecture truth

### Canonical layer split
- `EvezArt/evez-os` → canonical brand shell / public surface
- `EvezArt/surething-offline` → live operator/API spine, logical `evez-operator-api`
- `EvezArt/evez-sim` → simulation lane
- `EvezArt/agentvault` → registry / memory / audit layer
- `EvezArt/CrawFather` → shared skills / souls / plugin layer

### Current product rule
The immersive EVEZOS mobile operator console is a **client of the operator spine**.
It must not treat `evez-os` as the system of record for live operator telemetry.

---

## What has already been done

### In `agentvault`
Open PR: #4

Added:
- `ops/PROJECT_REGISTRY.md`
- `ops/ADR-0001-canonical-evezos-topology.md`
- `ops/PHASED_CONVERGENCE_PLAN.md`
- `ops/PREMOVE_CONTEXT_PROTOCOL.md`
- `ops/ACTIVE_CONTEXT_SNAPSHOT.md`

Meaning:
The convergence package, ownership boundaries, and anti-drift protocol now live in the vault layer.

### In `evez-os`
Open PR: #30

Added:
- `docs/OPERATOR_TOPOLOGY.md`

Meaning:
The shell repo now states that it is the canonical public/brand shell and not the sole operator truth layer.

### In `surething-offline`
Open PR: #2

Added:
- `docs/OPERATOR_SPINE_IDENTITY.md`
- `docs/OPERATOR_API_CONTRACT.md`
- `docs/PERSISTENCE_AUTH_ROLLOUT.md`
- `api/durable_spine.py`
- `api/auth_guard.py`

Meaning:
The operator spine identity is documented, the current HTTP contract is pinned, and the first persistence/auth implementation package exists.

### In Lovable / mobile console work
The EVEZOS mobile console brief has been corrected so that:
- it targets the operator spine for live truth
- it uses honesty labels such as `ephemeral`, `diagnostic`, `disconnected`, `dry run`
- it does not fake telemetry where the backend does not yet support it

---

## Current honesty boundary

These statements are true **right now**:

- the operator API route contract is real
- event canonicalization and hashing are real
- the current live `_spine` in `api/index.py` is still in-memory unless patched
- `/contradictions` and `/deploy/status` currently have authoritative shapes but largely diagnostic/static payloads
- durable history is not yet live until `api/index.py` is rewired to the SQLite-backed durable store and deployed on persistent storage
- optional auth guard exists in code package form, but is not yet wired into the live route layer

### What must not be claimed yet
Do not claim:
- durable operator history
- authenticated writes
- externally verified deployment health
- workflow truth beyond what the current operator contract actually exposes

---

## Active next step queue

### Highest-priority next implementation step
Patch `surething-offline/api/index.py` so the live routes use:
- `DurableSpineStore` from `api/durable_spine.py`
- `require_operator_token` from `api/auth_guard.py`

This is the step that upgrades the operator spine from documented/session-bound to actually durable/auth-capable.

### After that
1. deploy with known storage semantics
2. verify whether storage survives restart/redeploy
3. update contract docs to move from `ephemeral` to `durable` only if verified
4. update the mobile console to consume the stronger truth labels

### Parallel safe work
- improve repo-local readmes with shell/spine cross-links
- define additive metadata like `storage_mode`, `auth_mode`, `durability_scope`
- add active health probing to replace static deploy diagnostics later

---

## Current source-of-truth docs by lane

### Registry / architecture
- `agentvault/ops/PROJECT_REGISTRY.md`
- `agentvault/ops/ADR-0001-canonical-evezos-topology.md`
- `agentvault/ops/PHASED_CONVERGENCE_PLAN.md`

### Anti-drift bootstrap
- `agentvault/ops/PREMOVE_CONTEXT_PROTOCOL.md`
- `agentvault/ops/ACTIVE_CONTEXT_SNAPSHOT.md`

### Shell-side truth
- `evez-os/docs/OPERATOR_TOPOLOGY.md`

### Operator-spine truth
- `surething-offline/docs/OPERATOR_SPINE_IDENTITY.md`
- `surething-offline/docs/OPERATOR_API_CONTRACT.md`
- `surething-offline/docs/PERSISTENCE_AUTH_ROLLOUT.md`

---

## PR map

- `agentvault` PR #4 → convergence package and active context layer
- `evez-os` PR #30 → shell-side topology note
- `surething-offline` PR #2 → operator-spine identity, API contract, persistence/auth rollout package

These PRs are cross-linked and should be read together.

---

## Mandatory reminder for future moves

Before any future material move:
- read this file
- read `PREMOVE_CONTEXT_PROTOCOL.md`
- identify the layer
- identify the truth level
- avoid overclaiming
- leave a context trace after the move

That is the current anti-forgetting mechanism.
