# Pre-Move Context Protocol

Purpose: ensure future project moves start from the correct operating context instead of drifting, forgetting, or collapsing distinct layers by accident.

This protocol is required before making the next material move in any EVEZ project lane.

---

## Why this exists

The EVEZ operation spans multiple repos, deployments, and product lanes:
- public shell
- operator/API spine
- simulation
- registry/memory/audit
- plugin/skill/soul layer
- chat and interface experiments

The main failure mode is not lack of effort. It is **context drift**:
- forgetting which repo owns what
- confusing deployment names with repository identity
- pointing the console at the shell instead of the operator spine
- treating session-bound state as durable history
- re-solving decisions that were already made and recorded

This protocol is the guardrail against that.

---

## Required context sources

Before the next project move, load these in order:

### 1. Active context snapshot
Read:
- `ops/ACTIVE_CONTEXT_SNAPSHOT.md`

This is the fast-start state of the operation.

### 2. Canonical topology and ownership
Read:
- `ops/PROJECT_REGISTRY.md`
- `ops/ADR-0001-canonical-evezos-topology.md`
- `ops/PHASED_CONVERGENCE_PLAN.md`

These define the shell/spine/sim/vault/plugin split and the convergence path.

### 3. Repo-local truth docs
Read the repo-local documentation for the lane you are about to touch.

Minimum set:
- `evez-os`: `docs/OPERATOR_TOPOLOGY.md`
- `surething-offline`: `docs/OPERATOR_SPINE_IDENTITY.md`
- `surething-offline`: `docs/OPERATOR_API_CONTRACT.md`
- `surething-offline`: `docs/PERSISTENCE_AUTH_ROLLOUT.md`

### 4. Relevant open PR threads
Read the active PR that carries the lane you are changing.
At minimum, check:
- `agentvault` PR #4
- `evez-os` PR #30
- `surething-offline` PR #2

These PRs cross-link the current architecture decisions and implementation packages.

### 5. Recent conversation/project memory
Load recent project memory for:
- EVEZOS mobile console
- shell/spine topology
- current implementation packages
- pending next steps

Do this before deciding where a new change belongs.

---

## Non-negotiable current truths

Until superseded by a new ADR, the active truths are:

- `EvezArt/evez-os` = canonical brand shell / public surface
- `EvezArt/surething-offline` = live operator/API spine, logical `evez-operator-api`
- `EvezArt/evez-sim` = simulation lane
- `EvezArt/agentvault` = registry / memory / audit layer
- `EvezArt/CrawFather` = shared plugin / skill / soul layer

And:
- the mobile operator console targets the operator spine for live operator truth
- the shell is not the sole system of record for operator telemetry
- current spine durability must not be overstated unless durable storage is live and verified

---

## Classification step before every move

Before changing code/docs/builds, answer these questions explicitly:

### Q1. What layer is this change for?
Choose one:
- shell / public surface
- operator spine / API truth
- simulation
- registry / audit / memory
- reusable skill/plugin/soul
- chat experiment / interface experiment

### Q2. What is the system of record?
Name the repo that should own the change.

### Q3. What truth level does the feature require?
Choose one:
- authoritative live truth
- durable stored truth
- session-bound truth
- diagnostic/static placeholder
- local UI state only

### Q4. What must not be overclaimed?
State the honesty boundary explicitly.

If any of these answers are unclear, do not proceed by instinct. Update the registry/context first.

---

## Required output after each material move

After making a meaningful change, update at least one of the following:
- `ops/ACTIVE_CONTEXT_SNAPSHOT.md`
- relevant repo-local topology/contract docs
- PR comments that cross-link the move back to the registry and topology package

The rule is simple:
**No major move should exist only in code or only in chat. It must also leave a context trace.**

---

## Context handoff standard

When handing work from one lane to another, record:
- what changed
- which repo/layer owns it
- what remains pending
- what truth level applies now
- which docs/PRs are the current source of truth

This keeps the next move from starting cold.

---

## Stop conditions

Do not proceed with a change if any of the following is true:
- repo ownership is ambiguous
- shell vs spine responsibility is unclear
- a feature requires durability but only ephemeral state exists
- a UI would need to fake live telemetry to look complete
- the current state would be misrepresented to users

In those cases, first update the contract/registry/rollout docs or add the missing implementation package.

---

## Short version

Before every next move:
1. load the active snapshot
2. load topology + ADR + convergence plan
3. load repo-local truth docs
4. load relevant PRs
5. classify the move by layer and truth level
6. make the change
7. leave a context trace

That is the anti-drift protocol.
