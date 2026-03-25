"""
vault/search.py — agentvault
Keyword search over vault_index.json.
Exposes FastAPI /search?q= endpoint.

Run: uvicorn vault.search:app --host 0.0.0.0 --port 8080
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone

try:
    from fastapi import FastAPI, Query
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:
    raise ImportError("pip install fastapi uvicorn")

INDEX_PATH = Path(os.environ.get("VAULT_INDEX_PATH", "vault_index.json"))
EXPORT_DIR = Path(os.environ.get("VAULT_EXPORT_DIR", "exports"))

app = FastAPI(title="AgentVault Search", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def load_index() -> dict:
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text())
    return {"entries": [], "hashes": []}


def keyword_match(entry: dict, query: str) -> bool:
    q = query.lower()
    if q in entry.get("filename", "").lower():
        return True
    if any(q in t.lower() for t in entry.get("key_topics", [])):
        return True
    fpath = EXPORT_DIR / entry["filename"]
    if fpath.exists():
        return q in fpath.read_text(errors="ignore").lower()
    return False


@app.get("/search")
def search(q: str = Query(..., description="Search query"), limit: int = 20):
    idx = load_index()
    results = [e for e in idx["entries"] if keyword_match(e, q)]
    return {
        "query": q,
        "count": len(results),
        "results": results[:limit],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/index")
def index_list(limit: int = 50):
    idx = load_index()
    return {"total": len(idx["entries"]), "entries": idx["entries"][-limit:]}


@app.get("/health")
def health():
    return {"status": "ok", "ts": datetime.now(timezone.utc).isoformat()}
