"""
vault/sync_agent.py — agentvault

Watches a configured export directory for new .json/.md files, indexes filenames,
content hashes, sizes, and topic summaries, and can optionally email that metadata.

Privacy defaults:
- Email notifications are disabled unless AGENTVAULT_EMAIL_NOTIFICATIONS=true.
- No default recipient is configured; NOTIFY_EMAIL must be supplied explicitly.
- The email body contains metadata and extracted topics, not the export's raw text.
- Keep exports and generated indexes out of version control.

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
EMAIL_NOTIFICATIONS_ENABLED = (
    os.environ.get("AGENTVAULT_EMAIL_NOTIFICATIONS", "false").strip().lower() == "true"
)
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "").strip()
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

    words = re.findall(r"[a-zA-Z]{5,}", text.lower())
    freq: dict[str, int] = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return sorted(freq, key=freq.__getitem__, reverse=True)[:n]


def send_email(subject: str, body: str):
    if not EMAIL_NOTIFICATIONS_ENABLED:
        print("[sync_agent] EMAIL SKIP (notifications disabled; explicit opt-in required)")
        return
    if not NOTIFY_EMAIL:
        print("[sync_agent] EMAIL SKIP (NOTIFY_EMAIL not configured)")
        return
    if not GMAIL_USER or not GMAIL_PASS:
        print("[sync_agent] EMAIL SKIP (GMAIL_USER/GMAIL_PASS not configured)")
        return

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = NOTIFY_EMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())
        print(f"[sync_agent] Email sent: {subject}")
    except Exception as exc:
        print(f"[sync_agent] Email error ({type(exc).__name__}); notification not confirmed")


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
                f"Filename : {fpath.name}\nHash     : {fhash}\nSize     : {entry['size_bytes']} bytes\n"
                f"Topics   : {', '.join(topics)}\nIndexed  : {entry['indexed_at']}",
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
