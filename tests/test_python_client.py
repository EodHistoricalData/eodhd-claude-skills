#!/usr/bin/env python3
"""End-to-end smoke tests for eodhd_client.py against the live EODHD API.

Stdlib-only. Requires EODHD_API_TOKEN env var.

Each test case calls eodhd_client.py with realistic args and checks:
  - exit code 0
  - stdout is valid JSON
  - response is non-empty (or matches expected shape)

Subscription-gated endpoints (marketplace add-ons) that return 402/403
are reported as SKIP, not FAIL.

Exit code: 0 if no FAILs (SKIPs are OK), 1 otherwise.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLIENT = REPO_ROOT / "skills" / "eodhd-api" / "scripts" / "eodhd_client.py"

# Each case: (name, extra args). All cases use the same eodhd_client.py.
CASES: list[tuple[str, list[str]]] = [
    # Core market data
    ("eod", ["--endpoint", "eod", "--symbol", "AAPL.US",
             "--from-date", "2025-01-01", "--to-date", "2025-01-31"]),
    ("intraday", ["--endpoint", "intraday", "--symbol", "AAPL.US",
                  "--interval", "5m", "--from-date", "2025-01-15"]),
    ("real-time", ["--endpoint", "real-time", "--symbol", "AAPL.US"]),
    ("eod-bulk-last-day", ["--endpoint", "eod-bulk-last-day", "--symbol", "US"]),
    # Fundamentals & company data
    ("fundamentals", ["--endpoint", "fundamentals", "--symbol", "AAPL.US"]),
    ("bulk-fundamentals", ["--endpoint", "bulk-fundamentals", "--symbol", "NASDAQ",
                           "--symbols", "AAPL.US,MSFT.US"]),
    ("news", ["--endpoint", "news", "--symbol", "AAPL.US", "--limit", "3"]),
    ("sentiment", ["--endpoint", "sentiment", "--symbol", "AAPL.US",
                   "--from-date", "2025-01-01", "--to-date", "2025-01-31"]),
    ("news-word-weights", ["--endpoint", "news-word-weights", "--symbol", "AAPL.US",
                           "--from-date", "2025-01-01", "--to-date", "2025-01-15",
                           "--limit", "5"]),
    ("insider-transactions", ["--endpoint", "insider-transactions",
                              "--symbol", "AAPL.US", "--limit", "5"]),
    ("dividends", ["--endpoint", "dividends", "--symbol", "AAPL.US",
                   "--from-date", "2024-01-01", "--to-date", "2025-01-31"]),
    ("splits", ["--endpoint", "splits", "--symbol", "AAPL.US",
                "--from-date", "2020-01-01"]),
    # Technical
    ("technical(sma)", ["--endpoint", "technical", "--symbol", "AAPL.US",
                        "--function", "sma", "--period", "50",
                        "--from-date", "2025-01-01", "--to-date", "2025-01-31"]),
    # Macro
    ("macro-indicator", ["--endpoint", "macro-indicator", "--symbol", "USA",
                         "--indicator", "inflation_consumer_prices_annual"]),
    ("economic-events", ["--endpoint", "economic-events",
                         "--from-date", "2025-01-01", "--to-date", "2025-01-15",
                         "--country", "US", "--limit", "5"]),
    # Calendar
    ("calendar/earnings", ["--endpoint", "calendar/earnings",
                           "--symbol", "AAPL.US,MSFT.US"]),
    ("calendar/trends", ["--endpoint", "calendar/trends",
                         "--symbol", "AAPL.US,MSFT.US"]),
    ("calendar/ipos", ["--endpoint", "calendar/ipos",
                       "--from-date", "2025-01-01", "--to-date", "2025-01-31"]),
    ("calendar/splits", ["--endpoint", "calendar/splits",
                         "--from-date", "2025-01-01", "--to-date", "2025-01-31"]),
    ("calendar/dividends", ["--endpoint", "calendar/dividends",
                            "--symbol", "AAPL.US", "--limit", "5"]),
    # Exchange
    ("exchanges-list", ["--endpoint", "exchanges-list"]),
    ("exchanges-details", ["--endpoint", "exchanges-details", "--symbol", "US"]),
    ("exchange-symbol-list", ["--endpoint", "exchange-symbol-list", "--symbol", "US"]),
    # Screener
    ("screener", ["--endpoint", "screener",
                  "--filters", '[["market_capitalization",">",100000000000]]',
                  "--limit", "5"]),
    # US Live v2
    ("us-quote-delayed", ["--endpoint", "us-quote-delayed", "--symbol", "AAPL.US"]),
    # Account
    ("user", ["--endpoint", "user"]),
    # US Treasury
    ("ust/bill-rates", ["--endpoint", "ust/bill-rates",
                        "--filter-year", "2024", "--limit", "5"]),
    ("ust/long-term-rates", ["--endpoint", "ust/long-term-rates",
                             "--filter-year", "2024", "--limit", "5"]),
    ("ust/yield-rates", ["--endpoint", "ust/yield-rates",
                         "--filter-year", "2024", "--limit", "5"]),
    ("ust/real-yield-rates", ["--endpoint", "ust/real-yield-rates",
                              "--filter-year", "2024", "--limit", "5"]),
]


def classify_stderr(stderr: str) -> str:
    """Classify an error stderr blob - return 'skip' for subscription-gated,
    'fail' for everything else."""
    s = stderr.lower()
    if "402" in s or "403" in s or "subscription" in s or "not authorized" in s or "forbidden" in s:
        return "skip"
    return "fail"


def shape_summary(data) -> str:
    """One-line description of response shape."""
    if isinstance(data, list):
        return f"list[{len(data)}]"
    if isinstance(data, dict):
        keys = list(data.keys())[:5]
        more = "..." if len(data) > 5 else ""
        return f"dict({len(data)} keys: {', '.join(keys)}{more})"
    return f"{type(data).__name__}"


def run_case(name: str, args: list[str], timeout: int = 30) -> tuple[str, str]:
    """Returns (status, detail). status in {pass, skip, fail}."""
    t0 = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, str(CLIENT), *args],
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return ("fail", f"timeout after {timeout}s")

    elapsed = time.time() - t0
    if proc.returncode != 0:
        kind = classify_stderr(proc.stderr)
        first_line = (proc.stderr.strip().splitlines() or [""])[0][:160]
        return (kind, f"exit={proc.returncode} ({elapsed:.1f}s) - {first_line}")

    if not proc.stdout.strip():
        return ("fail", f"empty stdout ({elapsed:.1f}s)")

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return ("fail", f"invalid JSON ({elapsed:.1f}s): {exc}")

    # Detect API-level error in JSON body (some endpoints return 200 with error text)
    if isinstance(data, dict) and data.get("error"):
        kind = classify_stderr(str(data["error"]))
        return (kind, f"api error ({elapsed:.1f}s): {str(data['error'])[:120]}")

    return ("pass", f"{shape_summary(data)} ({elapsed:.1f}s)")


def main() -> int:
    if not os.getenv("EODHD_API_TOKEN"):
        print("ERROR: EODHD_API_TOKEN env var not set", file=sys.stderr)
        return 2

    results: dict[str, list[tuple[str, str]]] = {"pass": [], "skip": [], "fail": []}
    width = max(len(n) for n, _ in CASES) + 2

    print(f"\nRunning {len(CASES)} e2e cases against live EODHD API\n")
    print(f"{'CASE':<{width}} STATUS  DETAIL")
    print("-" * 100)
    for name, args in CASES:
        status, detail = run_case(name, args)
        results[status].append((name, detail))
        marker = {"pass": "PASS", "skip": "SKIP", "fail": "FAIL"}[status]
        print(f"{name:<{width}} {marker:<5} {status.upper():<5}  {detail}")

    print()
    print("=" * 100)
    print(f"Total: {len(CASES)} | "
          f"PASS: {len(results['pass'])} | "
          f"SKIP: {len(results['skip'])} (subscription) | "
          f"FAIL: {len(results['fail'])}")

    if results["fail"]:
        print("\nFAILURES:")
        for n, d in results["fail"]:
            print(f"  - {n}: {d}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
