#!/usr/bin/env python3
"""Publish a verifiable AgentVault heartbeat without inspecting local exports.

The ignored local vault is not available to GitHub Actions. This job deliberately
does not count, upload, or disclose those files. Cross-repository writes require
a dedicated LEDGER_GITHUB_TOKEN; the job-scoped GITHUB_TOKEN is not reused for
the ledger. Ably publication is separately opt-in.
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import re
import sys
from typing import Any

import requests

OWNER = "EvezArt"
LEDGER_REPO = "evez-autonomous-ledger"
LEDGER_GITHUB_TOKEN = os.environ.get("LEDGER_GITHUB_TOKEN", "").strip()
ENABLE_ABLY_HEARTBEAT = os.environ.get("ENABLE_ABLY_HEARTBEAT", "false").strip().lower()
ABLY_KEY = os.environ.get("ABLY_KEY", "").strip()
REQUEST_TIMEOUT_SECONDS = 15


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_event() -> dict[str, Any]:
    """Build a self-describing event; do not infer access to the local vault."""
    event: dict[str, Any] = {
        "type": "vault_heartbeat",
        "source": "agentvault",
        "timestamp": now_iso(),
        "status": "HEARTBEAT_ONLY",
        "local_vault_access": "NOT_ACCESSED",
        "note": (
            "GitHub Actions does not inspect gitignored local vault/ or data/ files; "
            "no local export count is asserted."
        ),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "1"),
        "commit_sha": os.environ.get("GITHUB_SHA", "UNKNOWN"),
    }
    canonical = json.dumps(event, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    event["sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return event


def _safe_identifier(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "-", value)
    return cleaned[:80] or "unknown"


def post_heartbeat(event: dict[str, Any]) -> str:
    """Write the receipt only with an explicitly configured cross-repo token."""
    if not LEDGER_GITHUB_TOKEN:
        raise RuntimeError(
            "LEDGER_GITHUB_TOKEN is not configured; no ledger receipt was written"
        )

    stamp = dt.datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00")).strftime(
        "%Y%m%dT%H%M%SZ"
    )
    run_id = _safe_identifier(str(event.get("workflow_run_id", "local")))
    attempt = _safe_identifier(str(event.get("workflow_run_attempt", "1")))
    path = f"DECISIONS/{stamp}_agentvault_heartbeat_{run_id}_{attempt}.json"
    url = f"https://api.github.com/repos/{OWNER}/{LEDGER_REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {LEDGER_GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    encoded = base64.b64encode(
        json.dumps(event, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    response = requests.put(
        url,
        headers=headers,
        json={
            "message": f"Record AgentVault heartbeat {stamp} run {run_id}",
            "content": encoded,
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    if response.status_code not in (200, 201):
        raise RuntimeError(f"ledger write rejected with HTTP {response.status_code}")
    return path


def post_ably(event: dict[str, Any]) -> bool:
    """Send a small heartbeat event externally only when explicitly enabled."""
    if ENABLE_ABLY_HEARTBEAT != "true":
        print("Ably publication: DISABLED (no external message sent)")
        return False
    if not ABLY_KEY:
        raise RuntimeError(
            "ENABLE_ABLY_HEARTBEAT=true but ABLY_KEY is not configured"
        )
    if ":" not in ABLY_KEY:
        raise RuntimeError("ABLY_KEY has an invalid format")

    key_id, key_secret = ABLY_KEY.split(":", 1)
    response = requests.post(
        "https://rest.ably.io/channels/evez-ops/messages",
        json={
            "name": "vault_heartbeat",
            "data": json.dumps(event, sort_keys=True, separators=(",", ":")),
        },
        auth=(key_id, key_secret),
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    if response.status_code not in (200, 201, 202, 204):
        raise RuntimeError(f"Ably publication rejected with HTTP {response.status_code}")
    print("Ably publication: ACCEPTED")
    return True


def main() -> int:
    event = build_event()
    print(f"AgentVault heartbeat: {event['timestamp']}")
    print(f"Local vault access: {event['local_vault_access']}")
    print(f"Event SHA-256: {event['sha256']}")

    try:
        path = post_heartbeat(event)
    except Exception as exc:
        print(f"ERROR: ledger receipt not verified: {exc}", file=sys.stderr)
        return 1

    print(f"VERIFIED: ledger accepted the receipt at {LEDGER_REPO}/{path}")

    try:
        post_ably(event)
    except Exception as exc:
        print(f"ERROR: ledger receipt exists, but Ably delivery failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
