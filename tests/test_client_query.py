#!/usr/bin/env python3
"""Query-construction tests for eodhd_client.py (no network).

Stdlib-only. Uses the client's `--print-url` flag to build the request URL
without calling the API, then asserts the EXACT query string for the three new
endpoint families matches the prometheus-web contract:

  - credit-risk / rates use JSON:API filter[...] + page[offset]/page[limit]
  - sanctions/entities|vessels use BARE query params + page[offset]/page[limit]
  - spreads/funding-stress uses filter[...] but NO pagination
  - sanctions/programs|sources take NO query params at all

Positive cases assert on the parsed query map (not substrings), so stray
params are caught. Negative cases assert the client rejects unsupported input
before any HTTP call. A dummy EODHD_API_TOKEN is injected so the token check
passes; the URL is built and printed before any HTTP call, so this runs
offline and in CI.

Exit code: 0 if all cases pass, 1 otherwise.
"""

from __future__ import annotations

import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLIENT = REPO_ROOT / "skills" / "eodhd-api" / "scripts" / "eodhd_client.py"

DUMMY_TOKEN = "tok-EN_with.special~chars-123"


def build_url(extra_args: list[str], token: str = DUMMY_TOKEN) -> tuple[int, str, str]:
    env = dict(os.environ)
    env["EODHD_API_TOKEN"] = token
    proc = subprocess.run(
        [sys.executable, str(CLIENT), "--print-url", *extra_args],
        capture_output=True, text=True, env=env, timeout=30,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def query_map(url: str) -> dict[str, list[str]]:
    """Parsed query as {key: [values]} — keys/values are already URL-decoded."""
    qs = urllib.parse.urlsplit(url).query
    out: dict[str, list[str]] = {}
    for key, value in urllib.parse.parse_qsl(qs, keep_blank_values=True):
        out.setdefault(key, []).append(value)
    return out


# Positive cases: (name, args, expected_subset, forbidden_keys, exact_keys_or_None)
#   expected_subset  — {key: value} that MUST be present (exact value match)
#   forbidden_keys   — query keys that MUST NOT appear
#   exact_keys       — if set, the full key set must equal this (beyond api_token/fmt caught separately)
POSITIVE: list[tuple[str, list[str], dict[str, str], list[str], set[str] | None]] = [
    (
        "credit-risk filter[...] + pagination; stray generics dropped",
        ["--endpoint", "credit-risk/sovereign/risk-premium",
         "--filter-param", "country=USA", "--limit", "50", "--offset", "20",
         "--interval", "5m", "--period", "14", "--filter", "legacy"],
        {"filter[country]": "USA", "page[limit]": "50", "page[offset]": "20"},
        ["country", "interval", "period", "function", "indicator", "filter",
         "from", "to", "limit", "offset", "filter[from]", "filter[to]"],
        {"api_token", "fmt", "filter[country]", "page[limit]", "page[offset]"},
    ),
    (
        "cds-market filter[value]/filter[region]",
        ["--endpoint", "credit-risk/cds-market/aggregates",
         "--filter-param", "value=Cleared", "--filter-param", "region=Global"],
        {"filter[value]": "Cleared", "filter[region]": "Global"},
        ["value", "region"],
        {"api_token", "fmt", "filter[value]", "filter[region]"},
    ),
    (
        "rates reference-rates filter[...]",
        ["--endpoint", "rates/reference-rates",
         "--filter-param", "code=SOFR", "--filter-param", "from=2025-01-01"],
        {"filter[code]": "SOFR", "filter[from]": "2025-01-01"},
        ["code", "from"],
        {"api_token", "fmt", "filter[code]", "filter[from]"},
    ),
    (
        "sanctions/entities bare params + pagination; stray generic dropped",
        ["--endpoint", "sanctions/entities",
         "--filter-param", "q=Ivanov", "--filter-param", "active=true",
         "--limit", "10", "--interval", "5m"],
        {"q": "Ivanov", "active": "true", "page[limit]": "10"},
        ["filter[q]", "filter[active]", "interval"],
        {"api_token", "fmt", "q", "active", "page[limit]"},
    ),
    (
        "sanctions/vessels bare params",
        ["--endpoint", "sanctions/vessels", "--filter-param", "flag=Panama"],
        {"flag": "Panama"},
        ["filter[flag]"],
        {"api_token", "fmt", "flag"},
    ),
    (
        "funding-stress filter[...] but NO pagination",
        ["--endpoint", "spreads/funding-stress",
         "--filter-param", "code=EFFR_SOFR", "--limit", "50", "--offset", "5"],
        {"filter[code]": "EFFR_SOFR"},
        ["page[limit]", "page[offset]", "limit", "offset", "code"],
        {"api_token", "fmt", "filter[code]"},
    ),
    (
        "sanctions/programs takes exactly {api_token, fmt}",
        ["--endpoint", "sanctions/programs"],
        {},
        ["page[limit]", "page[offset]", "filter", "interval", "period"],
        {"api_token", "fmt"},
    ),
    (
        "sanctions/sources takes exactly {api_token, fmt}",
        ["--endpoint", "sanctions/sources"],
        {},
        ["page[limit]", "page[offset]", "filter"],
        {"api_token", "fmt"},
    ),
]

# Negative cases: (name, args) — client must exit 2 before any HTTP call.
NEGATIVE: list[tuple[str, list[str]]] = [
    ("programs rejects --filter-param",
     ["--endpoint", "sanctions/programs", "--filter-param", "q=x"]),
    ("programs rejects --limit",
     ["--endpoint", "sanctions/programs", "--limit", "5"]),
    ("programs rejects malformed --filter-param",
     ["--endpoint", "sanctions/programs", "--filter-param", "malformed"]),
    ("sources rejects --offset",
     ["--endpoint", "sanctions/sources", "--offset", "10"]),
    ("credit-risk rejects malformed --filter-param",
     ["--endpoint", "credit-risk/sovereign/risk-premium", "--filter-param", "malformed"]),
    ("credit-risk rejects empty filter key",
     ["--endpoint", "rates/policy-rates", "--filter-param", "=value"]),
]


def run() -> list[str]:
    fails: list[str] = []

    for name, args, expected, forbidden, exact in POSITIVE:
        code, out, err = build_url(args)
        if code != 0 or not out:
            fails.append(f"[+] {name}: exited {code} (stderr: {err or 'none'})")
            continue
        # Token must be redacted and the raw token must not appear anywhere.
        if DUMMY_TOKEN in out:
            fails.append(f"[+] {name}: raw token leaked into printed URL")
        if "api_token=***" not in out:
            fails.append(f"[+] {name}: api_token not redacted")
        qm = query_map(out)
        for key, value in expected.items():
            if qm.get(key) != [value]:
                fails.append(f"[+] {name}: expected {key}={value!r}, got {qm.get(key)!r}")
        for key in forbidden:
            if key in qm:
                fails.append(f"[+] {name}: forbidden key '{key}' present ({qm[key]!r})")
        if exact is not None and set(qm) != exact:
            fails.append(f"[+] {name}: key set {sorted(qm)} != expected {sorted(exact)}")

    for name, args in NEGATIVE:
        code, out, err = build_url(args)
        if code != 2:
            fails.append(f"[-] {name}: expected exit 2, got {code} (stdout: {out or 'none'})")

    return fails


def main() -> int:
    print("\n=== Client query construction (--print-url, offline) ===")
    if not CLIENT.exists():
        print(f"  ✗ client not found at {CLIENT}")
        return 1
    fails = run()
    if not fails:
        print(f"  ✓ OK ({len(POSITIVE)} positive + {len(NEGATIVE)} negative cases)")
    else:
        for f in fails:
            print(f"  ✗ {f}")
    print("\n" + "=" * 80)
    print(f"Total failures: {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
