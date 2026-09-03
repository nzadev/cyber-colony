import os
import sys
import json
import time
from datetime import datetime

CHANGELOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "changelog.json")
RETENTION_DAYS = 14
MAX_ENTRIES = 50

def load_changelog():
    if not os.path.exists(CHANGELOG_FILE):
        return []
    try:
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_changelog(data):
    with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def prune_and_add(title, changes=None, category="UPDATE", version="v1.5.2"):
    entries = load_changelog()
    now_ms = int(time.time() * 1000)
    max_age_ms = RETENTION_DAYS * 24 * 60 * 60 * 1000

    # 1. Filter out items older than 14 days
    valid_entries = [e for e in entries if (now_ms - e.get("timestamp", now_ms)) <= max_age_ms]

    if title:
        new_entry = {
            "id": int(time.time()),
            "version": version,
            "title": title,
            "category": category,
            "timestamp": now_ms,
            "date_str": datetime.now().strftime("%d %b %Y, %H:%M WIB"),
            "changes": changes if changes else [title]
        }
        valid_entries.insert(0, new_entry)

    # 2. Limit to 50 newest
    if len(valid_entries) > MAX_ENTRIES:
        valid_entries = valid_entries[:MAX_ENTRIES]

    save_changelog(valid_entries)
    print(f"✅ Changelog updated & pruned ({len(valid_entries)} active entries in last 14 days)")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else ""
    ver = sys.argv[2] if len(sys.argv) > 2 else "v1.5.2"
    cat = sys.argv[3] if len(sys.argv) > 3 else "UPDATE"
    if msg:
        prune_and_add(msg, [msg], cat, ver)
    else:
        prune_and_add("", None)
