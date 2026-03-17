# ─────────────────────────────────────────────────────────────────
# Data Freshness Check Script — SA Bank Trust Score
# Checks when data was last modified and flags if outdated.
# Author: Lindiwe Songelwa
# Org:    AZ400-DevOps-Portfolio
# ─────────────────────────────────────────────────────────────────

import os
import sys
from datetime import datetime, timezone

DATA_FILES = [
    "data/complaints.csv",
    "data/sanctions.csv",
    "data/sentiment.csv"
]

# Flag data as stale if older than this many days
STALE_THRESHOLD_DAYS = 180  # 6 months

print("\n── Data Freshness Report ────────────────────────────────")
print(f"  Check date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}")
print(f"  Stale threshold: {STALE_THRESHOLD_DAYS} days\n")

stale_files = []

for filepath in DATA_FILES:
    if not os.path.exists(filepath):
        print(f"  ❌ MISSING: {filepath}")
        stale_files.append(filepath)
        continue

    modified_timestamp = os.path.getmtime(filepath)
    modified_date      = datetime.fromtimestamp(modified_timestamp, tz=timezone.utc)
    age_days           = (datetime.now(timezone.utc) - modified_date).days

    if age_days > STALE_THRESHOLD_DAYS:
        print(f"  ⚠️  STALE:  {filepath} — last modified {age_days} days ago ({modified_date.strftime('%Y-%m-%d')})")
        stale_files.append(filepath)
    else:
        print(f"  ✅ FRESH:  {filepath} — last modified {age_days} days ago ({modified_date.strftime('%Y-%m-%d')})")

print("\n── Summary ──────────────────────────────────────────────")
if stale_files:
    print(f"  ⚠️  {len(stale_files)} file(s) are stale and need updating.")
    print("  A GitHub Issue will be opened automatically.")
    sys.exit(1)
else:
    print("  ✅ All data files are fresh. No action needed.")
    sys.exit(0)
