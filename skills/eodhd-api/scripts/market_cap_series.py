#!/usr/bin/env python3
"""Calculate daily market-cap time series for any ticker on any exchange.

Method:
  market_cap = shares_outstanding * close_price

Data sources (EODHD API):
  - /eod/{SYMBOL}          → daily OHLCV (close price)
  - /fundamentals/{SYMBOL} → SharesOutstanding from Highlights

For US stocks only, an alternative --method=api flag uses the dedicated
/historical-market-cap/{SYMBOL} endpoint (weekly frequency, from 2019).

Requires:
  EODHD_API_TOKEN environment variable.

Examples:
  # Daily market cap for Apple, Q1 2025
  python market_cap_series.py --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-03-31

  # BMW on XETRA exchange
  python market_cap_series.py --symbol BMW.XETRA --from-date 2024-01-01 --to-date 2024-12-31

  # Use the dedicated EODHD endpoint (US stocks, weekly)
  python market_cap_series.py --symbol MSFT.US --from-date 2023-01-01 --to-date 2023-12-31 --method api

  # Output as CSV
  python market_cap_series.py --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-03-31 --csv
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

BASE_URL = "https://eodhd.com/api"


def fetch_json(url: str, timeout: int = 30) -> dict | list:
    """Fetch a URL and return parsed JSON."""
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def get_eod_prices(symbol: str, token: str, from_date: str, to_date: str) -> list[dict]:
    """Fetch daily end-of-day prices."""
    params = urllib.parse.urlencode({
        "api_token": token,
        "fmt": "json",
        "from": from_date,
        "to": to_date,
    })
    url = f"{BASE_URL}/eod/{symbol}?{params}"
    data = fetch_json(url)
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"EOD API error: {data['error']}")
    return data


def get_shares_outstanding(symbol: str, token: str) -> float | None:
    """Fetch SharesOutstanding from the Fundamentals API."""
    params = urllib.parse.urlencode({
        "api_token": token,
        "fmt": "json",
        "filter": "Highlights::SharesOutstanding",
    })
    url = f"{BASE_URL}/fundamentals/{symbol}?{params}"
    data = fetch_json(url)
    if isinstance(data, dict):
        if "error" in data:
            raise RuntimeError(f"Fundamentals API error: {data['error']}")
        val = data.get("SharesOutstanding")
        if val is not None:
            return float(val)
    return None


def get_historical_market_cap_api(symbol: str, token: str, from_date: str, to_date: str) -> list[dict]:
    """Fetch from the dedicated /historical-market-cap endpoint (US only, weekly)."""
    params = urllib.parse.urlencode({
        "api_token": token,
        "fmt": "json",
        "from": from_date,
        "to": to_date,
    })
    url = f"{BASE_URL}/historical-market-cap/{symbol}?{params}"
    data = fetch_json(url)
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"Historical Market Cap API error: {data['error']}")
    # Response is {"0": {"date": ..., "value": ...}, "1": ...}
    if isinstance(data, dict):
        rows = [v for _, v in sorted(data.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0)]
    else:
        rows = data
    return [{"date": r["date"], "market_cap": r["value"]} for r in rows if "date" in r]


def compute_market_cap_series(symbol: str, token: str, from_date: str, to_date: str) -> list[dict]:
    """Compute daily market cap = shares_outstanding * close price."""
    prices = get_eod_prices(symbol, token, from_date, to_date)
    if not prices:
        raise RuntimeError(f"No price data returned for {symbol} in {from_date}..{to_date}")

    shares = get_shares_outstanding(symbol, token)
    if shares is None or shares <= 0:
        raise RuntimeError(
            f"Could not retrieve SharesOutstanding for {symbol}. "
            "The fundamentals endpoint may not cover this instrument."
        )

    series = []
    for row in prices:
        close = row.get("close") or row.get("adjusted_close")
        if close is None:
            continue
        series.append({
            "date": row["date"],
            "close": close,
            "shares_outstanding": shares,
            "market_cap": shares * close,
        })
    return series


def format_value(val: float) -> str:
    """Human-readable market-cap string."""
    if val >= 1e12:
        return f"${val / 1e12:.2f}T"
    if val >= 1e9:
        return f"${val / 1e9:.2f}B"
    if val >= 1e6:
        return f"${val / 1e6:.2f}M"
    return f"${val:,.0f}"


def print_csv(series: list[dict]) -> None:
    """Print series as CSV to stdout."""
    print("date,close,shares_outstanding,market_cap")
    for row in series:
        print(f"{row['date']},{row['close']},{row['shares_outstanding']},{row['market_cap']}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate daily market-cap time series using EODHD API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Symbol format: {TICKER}.{EXCHANGE}  (e.g. AAPL.US, BMW.XETRA, VOD.LSE)",
    )
    parser.add_argument("--symbol", required=True, help="Ticker with exchange (e.g. AAPL.US)")
    parser.add_argument("--from-date", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--to-date", required=True, help="End date YYYY-MM-DD")
    parser.add_argument(
        "--method",
        choices=["compute", "api"],
        default="compute",
        help="'compute' = EOD price * shares (any exchange, daily). "
             "'api' = dedicated /historical-market-cap endpoint (US only, weekly). "
             "Default: compute",
    )
    parser.add_argument("--csv", action="store_true", help="Output as CSV instead of JSON")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    args = parser.parse_args()

    token = os.getenv("EODHD_API_TOKEN")
    if not token:
        print("Error: EODHD_API_TOKEN environment variable is not set", file=sys.stderr)
        return 2

    try:
        if args.method == "api":
            series = get_historical_market_cap_api(args.symbol, token, args.from_date, args.to_date)
        else:
            series = compute_market_cap_series(args.symbol, token, args.from_date, args.to_date)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except urllib.error.HTTPError as exc:
        print(f"HTTP Error {exc.code}: {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc.reason}", file=sys.stderr)
        return 1

    if not series:
        print("No data points produced.", file=sys.stderr)
        return 1

    if args.csv:
        print_csv(series)
    else:
        mcaps = [r["market_cap"] for r in series]
        summary = {
            "symbol": args.symbol,
            "from": args.from_date,
            "to": args.to_date,
            "method": args.method,
            "data_points": len(series),
            "start_market_cap": format_value(mcaps[0]),
            "end_market_cap": format_value(mcaps[-1]),
            "min_market_cap": format_value(min(mcaps)),
            "max_market_cap": format_value(max(mcaps)),
            "change_pct": round((mcaps[-1] / mcaps[0] - 1) * 100, 2),
        }
        output = {"summary": summary, "series": series}
        print(json.dumps(output, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
