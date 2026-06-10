#!/usr/bin/env python3
"""Regression tests for the edge-case fixes in market_cap_series.py and the
token-redaction hardening in eodhd_client.py.

Stdlib-only, no network (the network functions are monkeypatched). Exit 0 if
clean, 1 on any failure — matches the convention of the other tests/ suites.

Covers:
  - BUG-1: get_historical_market_cap_api must skip rows missing "value"
           (previously KeyError).
  - BUG-2: a zero opening market cap must not raise ZeroDivisionError
           (change_pct → None).
  - BUG-3: a legitimate close of 0.0 must be kept, not dropped by `a or b`.
  - HARDENING: _redact_token never leaks the api_token, incl. URL-encoded.
"""
from __future__ import annotations

import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "skills" / "eodhd-api" / "scripts"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mcs = _load("market_cap_series", "market_cap_series.py")
client = _load("eodhd_client", "eodhd_client.py")

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> None:
    if cond:
        print(f"  ok: {msg}")
    else:
        FAILURES.append(msg)
        print(f"  FAIL: {msg}")


def test_historical_skips_missing_value() -> None:
    """BUG-1: rows lacking 'value' are skipped, not crashing with KeyError."""
    payload = {
        "0": {"date": "2020-01-01", "value": 100},
        "1": {"date": "2020-01-08"},           # missing value → must be skipped
        "2": {"value": 300},                    # missing date → must be skipped
        "3": {"date": "2020-01-15", "value": 200},
    }
    mcs.fetch_json = lambda url, timeout=30: payload
    rows = mcs.get_historical_market_cap_api("AAPL.US", "tok", "2020-01-01", "2020-02-01")
    check(rows == [
        {"date": "2020-01-01", "market_cap": 100},
        {"date": "2020-01-15", "market_cap": 200},
    ], "get_historical_market_cap_api skips rows missing 'value'/'date'")


def test_compute_keeps_zero_close() -> None:
    """BUG-3: a close of exactly 0.0 is kept (not treated as missing)."""
    mcs.get_eod_prices = lambda *a, **k: [
        {"date": "2020-01-02", "close": 0.0},
        {"date": "2020-01-03", "close": 10.0},
    ]
    mcs.get_shares_outstanding = lambda *a, **k: 5.0
    series = mcs.compute_market_cap_series("X.US", "tok", "2020-01-01", "2020-01-31")
    check(len(series) == 2, "compute keeps the row with close=0.0")
    check(series[0]["close"] == 0.0 and series[0]["market_cap"] == 0.0,
          "close=0.0 yields market_cap=0.0 (not dropped/substituted)")


def test_change_pct_zero_open_no_crash() -> None:
    """BUG-2: zero opening market cap → change_pct None, no ZeroDivisionError."""
    mcs.compute_market_cap_series = lambda *a, **k: [
        {"date": "2020-01-02", "close": 0.0, "shares_outstanding": 5.0, "market_cap": 0.0},
        {"date": "2020-01-03", "close": 10.0, "shares_outstanding": 5.0, "market_cap": 50.0},
    ]
    argv = sys.argv
    sys.argv = ["market_cap_series.py", "--symbol", "X.US",
                "--from-date", "2020-01-01", "--to-date", "2020-01-31"]
    import os
    os.environ["EODHD_API_TOKEN"] = "dummy"
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            rc = mcs.main()
    finally:
        sys.argv = argv
    check(rc == 0, "main() exits 0 with a zero opening market cap (no crash)")
    out = json.loads(buf.getvalue())
    check(out["summary"]["change_pct"] is None,
          "change_pct is None when opening market cap is 0")


def test_redact_token() -> None:
    """HARDENING: _redact_token removes the secret in plain and encoded forms."""
    plain = "https://eodhd.com/api/eod/AAPL.US?api_token=5f3e2a1bDEAD&fmt=json"
    check("5f3e2a1bDEAD" not in client._redact_token(plain)
          and "api_token=***" in client._redact_token(plain),
          "_redact_token redacts a plain alphanumeric token")
    enc = "https://eodhd.com/api/eod/AAPL.US?api_token=a%2Bb%2Fc%3Dd&fmt=json"
    check("a%2Bb%2Fc%3Dd" not in client._redact_token(enc),
          "_redact_token redacts a URL-encoded token (the naive replace missed this)")


def main() -> int:
    for fn in (
        test_historical_skips_missing_value,
        test_compute_keeps_zero_close,
        test_change_pct_zero_open_no_crash,
        test_redact_token,
    ):
        print(f"\n{fn.__name__}:")
        fn()
    print()
    if FAILURES:
        print(f"FAILED ({len(FAILURES)}): " + "; ".join(FAILURES))
        return 1
    print("All market_cap_series / redaction regression tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
