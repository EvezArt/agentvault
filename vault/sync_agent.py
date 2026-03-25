"""
vault/sync_agent.py — agentvault
Watches configured export directory for new .json/.md files.
Indexes them, computes content hash, appends to vault_index.json,
and emails rubikspubes69@gmail.com on each new file.

Usage:
  python -m vault.sync_agent          # one-shot scan
  python -m vault.sync_agent --watch  # continuous 60s poll
"""

import os
import sys
import json
import hashlib
import time
import smtplib
import argparse
from datetime import datetime, timezone
from pathlib import Path
from email.mime.text import MIMEText

EXPORT_DIR = Path(os.environ.get("VAULT_EXPORT_DIR", "exports"))
INDEX_PATH = Path(os.environ.get("VAULT_INDEX_PATH", "vault_index.json"))
WATCH_INTERVAL = int(os.environ.get("VAULT_WATCH_INTERVAL", "60"))
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "rubikspubes69@gmail.com")
GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_PASS = os.environ.get("GMAIL_PASS", "")


def load_index() -> dict:
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text())
    return {"entries": [], "hashes": []}


def save_index(idx: dict):
    INDEX_PATH.write_text(json.dumps(idx, indent=2))


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:16]


def extract_topics(text: str, n: int = 5) -> list[str]:
    """Naive keyword extraction — top N most-frequent long words."""
    import re
    words = re.findall(r'[a-zA-Z]{5,}', text.lower())
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return sorted(freq, key=freq.__getitem__, reverse=True)[:n]


def send_email(subject: str, body: str):
    if not GMAIL_USER or not GMAIL_PASS:
        print(f"[sync_agent] EMAIL SKIP (no creds): {subject}")
        return
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = NOTIFY_EMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())
        print(f"[sync_agent] Email sent: {subject}")
    except Exception as e:
        print(f"[sync_agent] Email error: {e}")


def scan_once() -> list[dict]:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    idx = load_index()
    known_hashes = set(idx.get("hashes", []))
    new_entries = []

    for ext in ("*.json", "*.md"):
        for fpath in sorted(EXPORT_DIR.glob(ext)):
            fhash = file_hash(fpath)
            if fhash in known_hashes:
                continue
            text = fpath.read_text(errors="ignore")
            topics = extract_topics(text)
            entry = {
                "filename": fpath.name,
                "hash": fhash,
                "size_bytes": fpath.stat().st_size,
                "key_topics": topics,
                "indexed_at": datetime.now(timezone.utc).isoformat(),
            }
            idx["entries"].append(entry)
            idx["hashes"].append(fhash)
            known_hashes.add(fhash)
            new_entries.append(entry)
            print(f"[sync_agent] Indexed: {fpath.name} | {fhash} | {topics}")
            send_email(
                f"[AgentVault] New export indexed: {fpath.name}",
                f"Filename : {fpath.name}\nHash     : {fhash}\nSize     : {entry['size_bytes']} bytes\nTopics   : {', '.join(topics)}\nIndexed  : {entry['indexed_at']}",
            )

    if new_entries:
        save_index(idx)
    return new_entries


def watch():
    print(f"[sync_agent] Watching {EXPORT_DIR} every {WATCH_INTERVAL}s...")
    while True:
        scan_once()
        time.sleep(WATCH_INTERVAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()
    if args.watch:
        watch()
    else:
        results = scan_once()
        print(f"[sync_agent] Done. {len(results)} new entries indexed.")
