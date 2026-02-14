# agentvault (Evez AgentOS)

This repository is a private **vault + indexer** for your exported ChatGPT and Perplexity conversations, with GitHub as the control plane for autonomous “draft-first” work.

## What it does (today)

- Stores your exported chat archives in `vault/`.
- Ingests supported formats into a local SQLite database (`data/agentvault.sqlite`).
- Builds a full-text index (FTS5) so an agent can retrieve relevant past context without stuffing everything into one prompt.
- Runs nightly in GitHub Actions to rebuild the index and post a **draft queue** issue (no destructive actions).

## Quick start

Follow `docs/SETUP.md`.

## Safety model

- No secrets belong in chat threads.
- API keys (if you later add LLM calls) must be stored as GitHub Actions secrets.
- Default mode is **draft-only**: the system writes proposed actions as issues/comments; you decide what to merge/execute.
