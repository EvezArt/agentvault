# AgentVault

AgentVault is a prototype for local-first agent records and operator-controlled evidence workflows.

## Status: prototype; live operation must be verified

This repository contains scheduled GitHub Actions workflows, but the presence of a workflow is not proof that its work completed or that a remote service is healthy.

- `.github/workflows/autonomous-core.yml` emits a status message; it does not implement continuous issue/PR/workflow monitoring, AI analysis, or automated fixes.
- `.github/workflows/autonomous_loop.yml` publishes a heartbeat to `EvezArt/evez-autonomous-ledger` only when that cross-repository write succeeds and is checked.
- The heartbeat job does **not** read, count, or upload the operator's local exports. The `vault/**` and `data/**` paths are ignored by Git (apart from the explicitly unignored README and placeholder), and a hosted runner cannot see files that exist only on the operator's device.
- Email notifications from `vault/sync_agent.py` are disabled unless `AGENTVAULT_EMAIL_NOTIFICATIONS=true`, `NOTIFY_EMAIL`, and mail credentials are explicitly supplied.
- Optional Ably notification is disabled by default and requires an explicit repository variable plus a secret.
- Auto-merge is opt-in: an owner PR must have the `swarm` label and at least one approval.

Use the actual GitHub Actions run and ledger receipt as evidence of a successful run. A README status or a scheduled trigger is not a live health check.

## Local-data boundary

Recommended local layout:

- `vault/chatgpt/` — personal ChatGPT exports
- `vault/perplexity/` — personal Perplexity exports
- `data/` — local index and derived data

These paths and the legacy `exports/` path are excluded from version control by `.gitignore`. Before adding or syncing anything, verify the local repository state:

```bash
git status --short
git status --short --ignored
git check-ignore -v vault/chatgpt data exports
```

Do not commit conversation exports, access tokens, OAuth credentials, private keys, or account recovery information. A local ignore rule does not remove content that was committed or pushed previously; review Git history separately.

## Heartbeat configuration

The cross-repository receipt requires a dedicated `LEDGER_GITHUB_TOKEN` secret, scoped as narrowly as possible to write only to `EvezArt/evez-autonomous-ledger`. The workflow's automatic `GITHUB_TOKEN` is kept read-only and is not treated as permission to write across repositories.

Ably delivery is off unless the repository variable `ENABLE_ABLY_HEARTBEAT` is set to the literal value `true` and the `ABLY_KEY` secret is present. Enabling it sends heartbeat metadata to the external Ably service; do not enable it unless that data flow is intentionally approved.

## Verification rules

- A failed or unauthorized API request is a failure, not an empty result.
- The heartbeat digest covers the canonical JSON event body; it is an integrity check, not proof that the event is true or that the local vault was inspected.
- Missing cross-repository credentials must be reported explicitly. No success message is emitted for a write that was not accepted.
- Local exports remain local unless the operator explicitly chooses a separate sync path.

## Project links

- [GitHub Actions](https://github.com/EvezArt/agentvault/actions)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
