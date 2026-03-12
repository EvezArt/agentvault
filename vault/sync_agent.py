#!/usr/bin/env python3
"""
sync_agent.py — Auto-sync vault exports.

Watches for new .json/.md exports, indexes them, hashes them,
appends to vault_index.json.
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime, timezone

VAULT_DIR = Path("vault/exports")
INDEX_FILE = Path("vault/vault_index.json")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _extract_topics(content: str) -> list:
    """Extract key topics from content via simple keyword extraction."""
    words = set(content.lower().split())
    # Remove common words
    stopwords = {"the","a","an","and","or","but","in","on","at","to","for","of","with","by"}
    keywords = [w for w in words if len(w) > 5 and w not in stopwords]
    return keywords[:10]


def load_index() -> list:
    if not INDEX_FILE.exists():
        return []
    return json.loads(INDEX_FILE.read_text())


def save_index(entries: list):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(entries, indent=2))


def sync():
    """Scan vault/exports for new files and index them."""
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    existing = load_index()
    existing_hashes = {e["hash"] for e in existing}
    new_entries = []

    for f in VAULT_DIR.glob("**/*"):
        if f.suffix not in (".json", ".md", ".txt"):
            continue
        h = _file_hash(f)
        if h in existing_hashes:
            continue
        content = f.read_text(errors="replace")
        entry = {
            "file": str(f.relative_to(VAULT_DIR)),
            "hash": h,
            "size_bytes": f.stat().st_size,
            "indexed_at": _now(),
            "topics": _extract_topics(content[:2000]),
        }
        new_entries.append(entry)
        print(f"[VAULT] Indexed: {entry['file']} | {h}")

    if new_entries:
        all_entries = existing + new_entries
        save_index(all_entries)
        print(f"[VAULT] {len(new_entries)} new entries. Total: {len(all_entries)}")
    else:
        print(f"[VAULT] No new files. Index has {len(existing)} entries.")

    return new_entries


def search(query: str) -> list:
    """Simple keyword search over vault index."""
    entries = load_index()
    q = query.lower()
    results = []
    for e in entries:
        score = sum(1 for t in e.get("topics", []) if q in t)
        if q in e.get("file", "").lower():
            score += 3
        if score > 0:
            results.append({**e, "score": score})
    return sorted(results, key=lambda x: x["score"], reverse=True)[:20]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        q = " ".join(sys.argv[2:])
        results = search(q)
        for r in results:
            print(f"[{r['score']}] {r['file']} | {r['hash']} | {r.get('indexed_at','')}")
    else:
        sync()
