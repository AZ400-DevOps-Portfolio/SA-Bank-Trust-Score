# ─────────────────────────────────────────────────────────────────
# Data Quality Check Script — SA Bank Trust Score
# Validates all three CSVs before the app is deployed.
# Author: Lindiwe Songelwa
# Org:    AZ400-DevOps-Portfolio
# ─────────────────────────────────────────────────────────────────

import pandas as pd
import sys

EXPECTED_BANKS = {
    "Standard Bank", "FNB", "Absa",
    "Nedbank", "Capitec", "TymeBank"
}

errors   = []
warnings = []

def fail(msg):
    errors.append(msg)
    print(f"  ❌ FAIL: {msg}")

def warn(msg):
    warnings.append(msg)
    print(f"  ⚠️  WARN: {msg}")

def ok(msg):
    print(f"  ✅ OK:   {msg}")


# ─────────────────────────────────────────────────────────────────
# CHECK 1 — complaints.csv
# ─────────────────────────────────────────────────────────────────
print("\n── complaints.csv ───────────────────────────────────────")
complaints = pd.read_csv("data/complaints.csv")

# All 6 banks present
missing_banks = EXPECTED_BANKS - set(complaints["bank"])
if missing_banks:
    fail(f"Missing banks in complaints.csv: {missing_banks}")
else:
    ok("All 6 banks present")

# No missing values in critical columns
critical_cols = [
    "referral_conversion_rate_pct",
    "cases_decided_consumer_favour_pct",
    "formal_cases_2021",
    "formal_cases_2022",
    "formal_cases_2023"
]
for col in critical_cols:
    nulls = complaints[col].isnull().sum()
    if nulls > 0:
        fail(f"complaints.csv — {col} has {nulls} missing value(s)")
    else:
        ok(f"{col} — no missing values")

# Referral conversion rate between 0-100
out_of_range = complaints[
    (complaints["referral_conversion_rate_pct"] < 0) |
    (complaints["referral_conversion_rate_pct"] > 100)
]
if not out_of_range.empty:
    fail(f"referral_conversion_rate_pct out of range (0-100): {out_of_range['bank'].tolist()}")
else:
    ok("referral_conversion_rate_pct within valid range (0-100)")

# Consumer favour rate between 0-100
out_of_range = complaints[
    (complaints["cases_decided_consumer_favour_pct"] < 0) |
    (complaints["cases_decided_consumer_favour_pct"] > 100)
]
if not out_of_range.empty:
    fail(f"cases_decided_consumer_favour_pct out of range: {out_of_range['bank'].tolist()}")
else:
    ok("cases_decided_consumer_favour_pct within valid range (0-100)")

# Formal cases non-negative
for year in ["formal_cases_2021", "formal_cases_2022", "formal_cases_2023"]:
    negative = complaints[complaints[year] < 0]
    if not negative.empty:
        fail(f"{year} has negative values: {negative['bank'].tolist()}")
    else:
        ok(f"{year} — no negative values")


# ─────────────────────────────────────────────────────────────────
# CHECK 2 — sanctions.csv
# ─────────────────────────────────────────────────────────────────
print("\n── sanctions.csv ────────────────────────────────────────")
sanctions = pd.read_csv("data/sanctions.csv")

# All sanctioned banks are known banks
unknown = set(sanctions["bank"]) - EXPECTED_BANKS
if unknown:
    fail(f"Unknown banks in sanctions.csv: {unknown}")
else:
    ok("All banks in sanctions.csv are recognised")

# No missing penalty values
nulls = sanctions["penalty_zar"].isnull().sum()
if nulls > 0:
    fail(f"sanctions.csv — penalty_zar has {nulls} missing value(s)")
else:
    ok("penalty_zar — no missing values")

# No negative penalties
negative = sanctions[sanctions["penalty_zar"] < 0]
if not negative.empty:
    fail(f"Negative penalty values found: {negative['bank'].tolist()}")
else:
    ok("penalty_zar — no negative values")

# Year column is valid
invalid_years = sanctions[
    (sanctions["year"] < 2000) | (sanctions["year"] > 2030)
]
if not invalid_years.empty:
    warn(f"Suspicious year values: {invalid_years['year'].tolist()}")
else:
    ok("year column — all values look valid")


# ─────────────────────────────────────────────────────────────────
# CHECK 3 — sentiment.csv
# ─────────────────────────────────────────────────────────────────
print("\n── sentiment.csv ────────────────────────────────────────")
sentiment = pd.read_csv("data/sentiment.csv")

# All 6 banks present
missing_banks = EXPECTED_BANKS - set(sentiment["bank"])
if missing_banks:
    fail(f"Missing banks in sentiment.csv: {missing_banks}")
else:
    ok("All 6 banks present")

# No missing values in critical columns
for col in ["dataeq_net_sentiment_pct", "sagaci_satisfaction_2025"]:
    nulls = sentiment[col].isnull().sum()
    if nulls > 0:
        fail(f"sentiment.csv — {col} has {nulls} missing value(s)")
    else:
        ok(f"{col} — no missing values")

# Sagaci satisfaction between 0-100
out_of_range = sentiment[
    (sentiment["sagaci_satisfaction_2025"] < 0) |
    (sentiment["sagaci_satisfaction_2025"] > 100)
]
if not out_of_range.empty:
    fail(f"sagaci_satisfaction_2025 out of range: {out_of_range['bank'].tolist()}")
else:
    ok("sagaci_satisfaction_2025 within valid range (0-100)")


# ─────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────
print("\n── Summary ──────────────────────────────────────────────")
print(f"  Errors:   {len(errors)}")
print(f"  Warnings: {len(warnings)}")

if errors:
    print("\n❌ DATA QUALITY CHECK FAILED — fix the errors above before deploying.")
    sys.exit(1)
else:
    print("\n✅ ALL DATA QUALITY CHECKS PASSED — data is clean and ready.")
    sys.exit(0)