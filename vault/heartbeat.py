#!/usr/bin/env python3
"""
agentvault Heartbeat — 15-minute pulse.
Checks vault index health, emits status to evez-autonomous-ledger.
"""
import os, json, datetime, hashlib, requests, base64

GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
ABLY_KEY = os.environ.get("ABLY_KEY", "")
OWNER = "EvezArt"

HEADERS = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"


def get_vault_contents():
    url = f"https://api.github.com/repos/{OWNER}/agentvault/contents/exports"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return len(r.json())
    return 0


def post_heartbeat(count):
    event = {
        "type": "vault_heartbeat",
        "source": "agentvault",
        "timestamp": now_iso(),
        "export_count": count,
        "hash": hashlib.sha256(f"vault_{count}_{now_iso()}".encode()).hexdigest()[:16],
    }
    content = json.dumps(event, indent=2)
    encoded = base64.b64encode(content.encode()).decode()
    ts = now_iso().replace(":", "-").replace(".", "-")
    url = f"https://api.github.com/repos/{OWNER}/evez-autonomous-ledger/contents/DECISIONS/{ts}_vault_heartbeat.json"
    requests.put(url, headers=HEADERS, json={
        "message": f"🦠 vault heartbeat @ {event['timestamp']}",
        "content": encoded,
    })
    if ABLY_KEY:
        key_id, key_secret = ABLY_KEY.split(":")
        requests.post(
            "https://rest.ably.io/channels/evez-ops/messages",
            json={"name": "vault_heartbeat", "data": json.dumps(event)},
            auth=(key_id, key_secret)
        )


def main():
    print(f"\n🦠 agentvault Heartbeat — {now_iso()}")
    count = get_vault_contents()
    print(f"  Export count: {count}")
    post_heartbeat(count)
    print("  ✅ Vault pulse written to ledger.")


if __name__ == "__main__":
    main()
