#!/usr/bin/env python3
"""Minimal EODHD API client helper (stdlib-only).

Examples:
  # End-of-day prices
  python eodhd_client.py --endpoint eod --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-01-31

  # Fundamentals
  python eodhd_client.py --endpoint fundamentals --symbol AAPL.US

  # Intraday data
  python eodhd_client.py --endpoint intraday --symbol AAPL.US --interval 5m --from-date 2025-01-15

  # Real-time quote
  python eodhd_client.py --endpoint real-time --symbol AAPL.US

  # Company news
  python eodhd_client.py --endpoint news --symbol AAPL.US --limit 10

  # Dividends
  python eodhd_client.py --endpoint dividends --symbol AAPL.US --from-date 2020-01-01

  # Earnings (by date window)
  python eodhd_client.py --endpoint calendar/earnings --from-date 2025-01-01 --to-date 2025-01-31

  # Earnings (by symbol — note: --symbol maps to API 'symbols=' param)
  python eodhd_client.py --endpoint calendar/earnings --symbol AAPL.US,MSFT.US

  # Earnings Trends (--symbol maps to API 'symbols=' param)
  python eodhd_client.py --endpoint calendar/trends --symbol AAPL.US,MSFT.US

  # Dividends Calendar
  python eodhd_client.py --endpoint calendar/dividends --symbol AAPL.US

  # Technical indicators
  python eodhd_client.py --endpoint technical --symbol AAPL.US --function sma --period 50

  # Macro indicators
  python eodhd_client.py --endpoint macro-indicator --symbol USA --indicator inflation_consumer_prices_annual

  # Exchanges list
  python eodhd_client.py --endpoint exchanges-list

  # Bulk EOD data for exchange
  python eodhd_client.py --endpoint eod-bulk-last-day --symbol US

  # Economic events (with country and comparison filters)
  python eodhd_client.py --endpoint economic-events --from-date 2025-01-01 --to-date 2025-01-31 --country US --comparison yoy

  # Screener with filters (filters = JSON array of [field, op, value]; dividend_yield is a fraction, 0.03 = 3%;
  # sort is field.direction e.g. market_capitalization.desc; add ["exchange","=","us"] to keep caps in USD)
  python eodhd_client.py --endpoint screener --filters '[["market_capitalization",">=",1000000000],["sector","=","Technology"],["exchange","=","us"]]' --sort market_capitalization.desc --limit 20

  # Sentiment data
  python eodhd_client.py --endpoint sentiment --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-01-31

  # News word weights (trending topics)
  python eodhd_client.py --endpoint news-word-weights --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-01-15 --limit 20

  # US extended quotes (Live v2) - single or multiple symbols
  python eodhd_client.py --endpoint us-quote-delayed --symbol AAPL.US
  python eodhd_client.py --endpoint us-quote-delayed --symbol AAPL.US,TSLA.US,MSFT.US

  # Bulk fundamentals for an exchange
  python eodhd_client.py --endpoint bulk-fundamentals --symbol NASDAQ --limit 100

  # Bulk fundamentals for specific symbols
  python eodhd_client.py --endpoint bulk-fundamentals --symbol NASDAQ --symbols AAPL.US,MSFT.US

  # User details (account info, API usage)
  python eodhd_client.py --endpoint user

  # US Treasury Bill Rates
  python eodhd_client.py --endpoint ust/bill-rates --filter-year 2012 --limit 100

  # US Treasury Long-Term Rates
  python eodhd_client.py --endpoint ust/long-term-rates --filter-year 2020

  # US Treasury Yield Rates (Par Yield Curve)
  python eodhd_client.py --endpoint ust/yield-rates --filter-year 2023

  # US Treasury Real Yield Rates (Par Real Yield Curve)
  python eodhd_client.py --endpoint ust/real-yield-rates --filter-year 2024

  # Credit & Sovereign Risk (JSON:API filter[...] + page[...])
  # filter[country] expects an ISO 3166-1 alpha-3 code (USA, DEU, FRA) — not a full name
  python eodhd_client.py --endpoint credit-risk/sovereign/risk-premium --filter-param country=USA
  python eodhd_client.py --endpoint credit-risk/sovereign/credit-ratings --filter-param country=DEU
  python eodhd_client.py --endpoint credit-risk/sovereign/cds-spreads --filter-param country=FRA
  python eodhd_client.py --endpoint credit-risk/sovereign/default-spreads --filter-param rating=Aaa
  python eodhd_client.py --endpoint credit-risk/corporate/cmdi --filter-param from=2026-01-01 --filter-param to=2026-06-01
  python eodhd_client.py --endpoint credit-risk/corporate/hqm-yields --filter-param tenor=2,5,10 --filter-param type=par
  python eodhd_client.py --endpoint credit-risk/cds-market/aggregates --filter-param metric=gross_notional --filter-param dimension=grade

  # Sanctions screening (BARE query params: source, type, program, q, active, imo, flag, ...)
  python eodhd_client.py --endpoint sanctions/entities --filter-param q=Ivanov --filter-param active=true
  python eodhd_client.py --endpoint sanctions/entities --filter-param program=RUSSIA-EO14024 --filter-param type=entity
  python eodhd_client.py --endpoint sanctions/vessels --filter-param flag=Panama
  python eodhd_client.py --endpoint sanctions/programs
  python eodhd_client.py --endpoint sanctions/sources

  # Interest Rates
  python eodhd_client.py --endpoint rates/reference-rates --filter-param code=SOFR --filter-param from=2025-01-01
  python eodhd_client.py --endpoint rates/policy-rates --filter-param central_bank=ECB
  python eodhd_client.py --endpoint spreads/funding-stress --filter-param code=EFFR_SOFR --filter-param from=2026-05-01 --filter-param to=2026-05-31

  # Real Estate — covered countries (which datasets each carries)
  python eodhd_client.py --endpoint real-estate/countries --limit 20

  # Real Estate — Selected Property Prices (SPP, headline harmonised) for a country
  python eodhd_client.py --endpoint real-estate --symbol US --re-type real --re-metric index

  # Real Estate — Detailed Property Prices (DPP, granular national series)
  python eodhd_client.py --endpoint real-estate/detailed --symbol AE --re-property-type 1

  # Real Estate — catalogue of available detailed (DPP) series for a country
  python eodhd_client.py --endpoint real-estate/detailed/series --symbol US
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://eodhd.com/api"


def _redact_token(url: str) -> str:
    """Redact the api_token query value so the secret never reaches stderr/logs.

    Matches the value exactly as it appears in the URL (handles URL-encoded
    tokens), unlike a naive ``url.replace(token, '***')`` which misses encoded
    or partially-quoted tokens. Anchored to a query-param boundary (``?``/``&``)
    and stops at the next ``&`` or ``#`` so it neither swallows a fragment nor
    matches a lookalike param such as ``backup_api_token=``.
    """
    return re.sub(r"([?&]api_token=)[^&#]*", r"\1***", url)


# JSON:API-style endpoints: no symbol; use filter[...] + page[offset]/page[limit].
# funding-stress has no pagination but shares the filter[...] convention.
FILTER_API_ENDPOINTS = {
    "credit-risk/sovereign/risk-premium",
    "credit-risk/sovereign/credit-ratings",
    "credit-risk/sovereign/cds-spreads",
    "credit-risk/sovereign/default-spreads",
    "credit-risk/corporate/cmdi",
    "credit-risk/corporate/hqm-yields",
    "credit-risk/cds-market/aggregates",
    "rates/reference-rates",
    "rates/policy-rates",
    "spreads/funding-stress",
}

# filter[...] endpoints whose prometheus-web controller forwards no pagination
# (only `filter`), so page[offset]/page[limit] must not be sent.
FILTER_NO_PAGINATION_ENDPOINTS = {
    "spreads/funding-stress",
}

# Generic CLI-derived query keys that the new REST families (credit-risk, rates,
# sanctions) never accept as-is — they take --filter-param (and, where allowed,
# page[...]). Stripped before building the query so a stray --interval/--period/
# --function/--indicator/--filter/--from-date/--to-date/--limit/--offset cannot
# leak into the request and silently violate the documented contract.
_GENERIC_QUERY_KEYS = (
    "from", "to", "limit", "offset",
    "interval", "period", "function", "indicator", "filter",
)

# Sanctions endpoints: no symbol; use BARE query params (source, type, program,
# q, active, imo, flag, ...) — NOT filter[...]. entities/vessels also paginate
# via page[offset]/page[limit]; programs/sources take no params (see below).
# Verified against prometheus-web request classes + live prod (2026-07).
SANCTIONS_API_ENDPOINTS = {
    "sanctions/entities",
    "sanctions/vessels",
    "sanctions/programs",
    "sanctions/sources",
}

# Sanctions reference endpoints that accept NO query params at all: the
# eodhd.com proxy forwards none of them (verified vs prometheus-web
# controllers, which proxy these with an empty param list) — not even
# pagination. They return the full reference list.
SANCTIONS_NO_PARAM_ENDPOINTS = {
    "sanctions/programs",
    "sanctions/sources",
}

# Endpoints that don't require a symbol
NO_SYMBOL_ENDPOINTS = {
    "screener",
    "exchanges-list",
    "calendar/earnings",
    "calendar/ipos",
    "calendar/splits",
    "calendar/dividends",
    "economic-events",
    "ust/bill-rates",
    "ust/long-term-rates",
    "ust/yield-rates",
    "ust/real-yield-rates",
    "real-estate/countries",
    "us-quote-delayed",
    "user",
} | FILTER_API_ENDPOINTS | SANCTIONS_API_ENDPOINTS

# Endpoints where --symbol means exchange code, not ticker
EXCHANGE_CODE_ENDPOINTS = {
    "exchange-symbol-list",
    "eod-bulk-last-day",
    "bulk-fundamentals",
}


class ClientError(RuntimeError):
    """Raised when user input or API response is invalid."""


def build_path(endpoint: str, symbol: str | None, function: str | None = None) -> str:
    """Build the API path for the given endpoint."""

    # Endpoints that don't need a symbol
    if endpoint in NO_SYMBOL_ENDPOINTS:
        if endpoint == "exchanges-list":
            return "/exchanges-list"
        if endpoint == "calendar/earnings":
            return "/calendar/earnings"
        if endpoint == "calendar/ipos":
            return "/calendar/ipos"
        if endpoint == "calendar/splits":
            return "/calendar/splits"
        if endpoint == "calendar/dividends":
            return "/calendar/dividends"
        if endpoint == "economic-events":
            return "/economic-events"
        if endpoint == "screener":
            return "/screener"
        if endpoint == "ust/bill-rates":
            return "/ust/bill-rates"
        if endpoint == "ust/long-term-rates":
            return "/ust/long-term-rates"
        if endpoint == "ust/yield-rates":
            return "/ust/yield-rates"
        if endpoint == "ust/real-yield-rates":
            return "/ust/real-yield-rates"
        if endpoint == "real-estate/countries":
            return "/real-estate/countries"
        if endpoint == "us-quote-delayed":
            return "/us-quote-delayed"
        if endpoint == "user":
            return "/user"
        return f"/{endpoint}"

    # Require symbol for all other endpoints
    if not symbol:
        raise ClientError(f"--symbol is required for endpoint={endpoint}")

    # Simple symbol-based endpoints
    if endpoint == "eod":
        return f"/eod/{symbol}"
    if endpoint == "intraday":
        return f"/intraday/{symbol}"
    if endpoint == "fundamentals":
        return f"/fundamentals/{symbol}"
    if endpoint == "real-time":
        return f"/real-time/{symbol}"
    if endpoint == "dividends":
        return f"/div/{symbol}"
    if endpoint == "splits":
        return f"/splits/{symbol}"
    if endpoint == "news":
        return f"/news"  # news uses 's' param, not path
    if endpoint == "sentiment":
        return "/sentiments"  # sentiments uses 's' param
    if endpoint == "news-word-weights":
        return "/news-word-weights"  # uses 's' param and special filter params
    if endpoint == "insider-transactions":
        return f"/insider-transactions"  # uses 'code' param
    if endpoint == "calendar/trends":
        return "/calendar/trends"  # uses 'symbols' param (comma-separated)
    if endpoint == "technical":
        if not function:
            raise ClientError("--function is required for endpoint=technical (e.g., sma, ema, rsi)")
        return f"/technical/{symbol}"
    if endpoint == "macro-indicator":
        return f"/macro-indicator/{symbol}"

    # Real Estate Data API — {code} is ISO alpha-2, case-insensitive (normalised to uppercase)
    if endpoint == "real-estate":
        return f"/real-estate/{symbol.upper()}"
    if endpoint == "real-estate/detailed":
        return f"/real-estate/{symbol.upper()}/detailed"
    if endpoint == "real-estate/detailed/series":
        return f"/real-estate/{symbol.upper()}/detailed/series"

    # Exchange code endpoints
    if endpoint == "exchange-symbol-list":
        return f"/exchange-symbol-list/{symbol}"
    if endpoint == "eod-bulk-last-day":
        return f"/eod-bulk-last-day/{symbol}"
    if endpoint == "bulk-fundamentals":
        return f"/bulk-fundamentals/{symbol}"

    # Index/exchange related
    if endpoint == "exchanges-details":
        return f"/exchanges/{symbol}"
    if endpoint == "index-components":
        return f"/fundamentals/{symbol}"  # index components via fundamentals

    raise ClientError(f"Unsupported endpoint: {endpoint}")


SUPPORTED_ENDPOINTS = [
    # Core market data
    "eod",
    "intraday",
    "real-time",
    "eod-bulk-last-day",
    # Fundamentals & company data
    "fundamentals",
    "bulk-fundamentals",
    "news",
    "sentiment",
    "news-word-weights",
    "insider-transactions",
    "dividends",
    "splits",
    # Technical analysis
    "technical",
    # Macro & economic
    "macro-indicator",
    "economic-events",
    # Calendar events
    "calendar/earnings",
    "calendar/trends",
    "calendar/ipos",
    "calendar/splits",
    "calendar/dividends",
    # Exchange/listing
    "exchange-symbol-list",
    "exchanges-list",
    "exchanges-details",
    "index-components",
    # Screening
    "screener",
    # US extended quotes (Live v2)
    "us-quote-delayed",
    # Account
    "user",
    # US Treasury rates
    "ust/bill-rates",
    "ust/long-term-rates",
    "ust/yield-rates",
    "ust/real-yield-rates",
    # Credit & Sovereign Risk
    "credit-risk/sovereign/risk-premium",
    "credit-risk/sovereign/credit-ratings",
    "credit-risk/sovereign/cds-spreads",
    "credit-risk/sovereign/default-spreads",
    "credit-risk/corporate/cmdi",
    "credit-risk/corporate/hqm-yields",
    "credit-risk/cds-market/aggregates",
    # Sanctions screening
    "sanctions/entities",
    "sanctions/vessels",
    "sanctions/programs",
    "sanctions/sources",
    # Interest rates
    "rates/reference-rates",
    "rates/policy-rates",
    "spreads/funding-stress",
    # Real Estate Data API (BIS property prices)
    "real-estate/countries",
    "real-estate",
    "real-estate/detailed",
    "real-estate/detailed/series",
]


def _lowercase_keys(obj):
    """Recursively lowercase all dict keys.

    Used to normalize endpoints that return PascalCase keys (e.g.
    macro-indicator's Date/Value/CountryCode) so downstream consumers can rely
    on the same lowercase keys every other endpoint uses.
    """
    if isinstance(obj, dict):
        return {str(k).lower(): _lowercase_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_lowercase_keys(v) for v in obj]
    return obj


def normalize_response(endpoint: str, parsed):
    """Smooth over per-endpoint response-shape inconsistencies (QA v0.4.2).

    Most list endpoints (eod, news, screener data, ...) return a bare array
    with lowercase keys. Two endpoints diverge and broke downstream parsing:

    - BUG-05: UST and Real Estate endpoints wrap rows in {"meta", "data", "links"}
      instead of a bare array, so naive `data[-1]` indexing raised KeyError.
      Unwrap to the bare `data` array (error payloads, which lack a list `data`,
      pass through).
    - BUG-06: macro-indicator returns PascalCase keys (Date/Value/CountryCode)
      while every other endpoint uses lowercase, so `d.get("date")` returned
      None. Lowercase the keys.

    Use --raw to bypass normalization and see the exact API payload.
    """
    if (endpoint.startswith("ust/") or endpoint.startswith("real-estate")) and isinstance(parsed, dict):
        data = parsed.get("data")
        if isinstance(data, list):
            return data

    if endpoint == "macro-indicator":
        return _lowercase_keys(parsed)

    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query EODHD API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported endpoints:
  Market Data:    eod, intraday, real-time, eod-bulk-last-day
  Fundamentals:   fundamentals, bulk-fundamentals, news, sentiment, news-word-weights, insider-transactions
  Corporate:      dividends, splits
  Technical:      technical (requires --function)
  Macro:          macro-indicator, economic-events
  Calendar:       calendar/earnings, calendar/trends, calendar/ipos, calendar/splits, calendar/dividends
  Exchange:       exchange-symbol-list, exchanges-list, exchanges-details
  Screening:      screener
  US Quotes:      us-quote-delayed (Live v2 extended quotes)
  Account:        user
  US Treasury:    ust/bill-rates, ust/long-term-rates, ust/yield-rates, ust/real-yield-rates
  Credit Risk:    credit-risk/sovereign/risk-premium, credit-risk/sovereign/credit-ratings,
                  credit-risk/sovereign/cds-spreads, credit-risk/sovereign/default-spreads,
                  credit-risk/corporate/cmdi, credit-risk/corporate/hqm-yields,
                  credit-risk/cds-market/aggregates (use --filter-param KEY=VALUE)
  Sanctions:      sanctions/entities, sanctions/vessels, sanctions/programs, sanctions/sources
  Interest Rates: rates/reference-rates, rates/policy-rates, spreads/funding-stress
  Real Estate:    real-estate/countries, real-estate, real-estate/detailed, real-estate/detailed/series

Note: news-word-weights may have longer response times due to AI processing.

Symbol format: {TICKER}.{EXCHANGE} (e.g., AAPL.US, MSFT.US, BMW.XETRA)
For exchange-symbol-list and eod-bulk-last-day, use exchange code (e.g., US, LSE)
        """,
    )
    parser.add_argument(
        "--endpoint",
        required=True,
        choices=SUPPORTED_ENDPOINTS,
        help="API endpoint to query",
    )
    parser.add_argument(
        "--symbol",
        help="Ticker with exchange suffix (e.g., AAPL.US) or exchange code for bulk endpoints",
    )
    parser.add_argument("--from-date", help="Start date YYYY-MM-DD")
    parser.add_argument("--to-date", help="End date YYYY-MM-DD")
    parser.add_argument("--interval", help="Intraday interval: 1m, 5m, 1h")
    parser.add_argument("--limit", type=int, help="Limit results")
    parser.add_argument("--offset", type=int, help="Offset for pagination")
    parser.add_argument(
        "--function",
        help="Technical indicator function (sma, ema, wma, rsi, macd, stoch, cci, adx, atr, bbands)",
    )
    parser.add_argument("--period", type=int, help="Period for technical indicators")
    parser.add_argument(
        "--indicator",
        help="Macro indicator code (e.g., inflation_consumer_prices_annual, gdp_current_usd)",
    )
    parser.add_argument(
        "--filter",
        help="Filter for specific fields (e.g., last_close, extended for earnings)",
    )
    parser.add_argument(
        "--symbols",
        help="Comma-separated symbols for bulk-fundamentals (e.g., AAPL.US,MSFT.US)",
    )
    parser.add_argument(
        "--version",
        help="API version for bulk-fundamentals (e.g., 1.2)",
    )
    parser.add_argument(
        "--country",
        help="ISO 3166-1 alpha-2 country code for economic-events (e.g., US, GB, DE)",
    )
    parser.add_argument(
        "--comparison",
        help="Comparison type for economic-events: mom, qoq, yoy",
    )
    parser.add_argument(
        "--filters",
        help='JSON filter array for screener (e.g., \'[["market_capitalization",">",1000000000]]\')',
    )
    parser.add_argument(
        "--sort",
        help="Sort for screener as field.direction (e.g., market_capitalization.desc, pe.asc)",
    )
    parser.add_argument(
        "--signals",
        help="Signal filter for screener (e.g., 200d_new_hi, bookvalue_neg)",
    )
    parser.add_argument(
        "--filter-year",
        type=int,
        help="Filter by year for UST endpoints (e.g., 2023)",
    )
    parser.add_argument(
        "--filter-param",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Filter for credit-risk/rates/sanctions endpoints, repeatable "
        "(e.g., --filter-param country=USA --filter-param from=2026-01-01). "
        "Sent as filter[KEY]=VALUE for credit-risk/rates; as bare KEY=VALUE for sanctions.",
    )
    # Real Estate Data API filters (map to filter[...] query params)
    parser.add_argument(
        "--re-type",
        help="Real Estate SPP price type: nominal, real (filter[type])",
    )
    parser.add_argument(
        "--re-metric",
        help="Real Estate SPP metric: index, yoy (filter[metric])",
    )
    parser.add_argument(
        "--re-area",
        help="Real Estate DPP covered-area dimension code (filter[area])",
    )
    parser.add_argument(
        "--re-property-type",
        help="Real Estate DPP property type code (filter[property_type])",
    )
    parser.add_argument(
        "--re-vintage",
        help="Real Estate DPP vintage code (filter[vintage])",
    )
    parser.add_argument(
        "--re-freq",
        help="Real Estate DPP frequency: Q, A, M, H (filter[freq])",
    )
    parser.add_argument(
        "--re-from",
        help="Real Estate period lower bound, e.g. 2020-Q1 or 2020-01 (filter[from])",
    )
    parser.add_argument(
        "--re-to",
        help="Real Estate period upper bound, e.g. 2024-Q4 or 2024-12 (filter[to])",
    )
    parser.add_argument("--base-url", default=BASE_URL, help="Override base URL")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output raw response without JSON formatting",
    )
    parser.add_argument(
        "--print-url",
        action="store_true",
        help="Build and print the request URL (api_token redacted) then exit, "
        "without calling the API — useful for debugging query construction. "
        "Note: the printed URL still contains filter values (e.g. sanctions q/imo/"
        "country) — avoid pasting it into public/CI logs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.getenv("EODHD_API_TOKEN")
    if not token:
        print("Error: EODHD_API_TOKEN environment variable is not set", file=sys.stderr)
        print("Get your API token at https://eodhd.com/", file=sys.stderr)
        return 2

    try:
        path = build_path(args.endpoint, args.symbol, args.function)
    except ClientError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    # Build query parameters
    params: dict[str, str | int] = {
        "api_token": token,
        "fmt": "json",
    }

    # Date range
    if args.from_date:
        params["from"] = args.from_date
    if args.to_date:
        params["to"] = args.to_date

    # Pagination
    if args.limit is not None:
        params["limit"] = args.limit
    if args.offset is not None:
        params["offset"] = args.offset

    # Intraday interval
    if args.interval:
        params["interval"] = args.interval

    # Intraday endpoint requires Unix timestamps for from/to (not YYYY-MM-DD)
    if args.endpoint == "intraday":
        for key in ("from", "to"):
            value = params.get(key)
            if isinstance(value, str) and "-" in value:
                try:
                    dt = datetime.datetime.strptime(value, "%Y-%m-%d")
                    params[key] = int(dt.replace(tzinfo=datetime.timezone.utc).timestamp())
                except ValueError:
                    pass  # Leave unchanged; API will surface the error

    # Technical indicators
    if args.function:
        params["function"] = args.function
    if args.period is not None:
        params["period"] = args.period

    # Macro indicator
    if args.indicator:
        params["indicator"] = args.indicator

    # Filter
    if args.filter:
        params["filter"] = args.filter

    # Special handling for news endpoint (uses 's' parameter)
    if args.endpoint == "news" and args.symbol:
        params["s"] = args.symbol

    # Special handling for sentiment endpoint
    if args.endpoint == "sentiment" and args.symbol:
        params["s"] = args.symbol

    # Special handling for insider-transactions endpoint
    if args.endpoint == "insider-transactions" and args.symbol:
        params["code"] = args.symbol

    # Special handling for news-word-weights endpoint (different param names)
    if args.endpoint == "news-word-weights":
        if args.symbol:
            params["s"] = args.symbol
        # news-word-weights uses filter[date_from], filter[date_to], page[limit]
        if args.from_date:
            params["filter[date_from]"] = params.pop("from", args.from_date)
        if args.to_date:
            params["filter[date_to]"] = params.pop("to", args.to_date)
        if args.limit is not None:
            params["page[limit]"] = params.pop("limit", args.limit)

    # Special handling for calendar/dividends endpoint (uses filter parameters)
    if args.endpoint == "calendar/dividends":
        if args.symbol:
            params["filter[symbol]"] = args.symbol
        # calendar/dividends uses filter[date_from], filter[date_to], page[limit], page[offset]
        if args.from_date:
            params["filter[date_from]"] = params.pop("from", args.from_date)
        if args.to_date:
            params["filter[date_to]"] = params.pop("to", args.to_date)
        if args.limit is not None:
            params["page[limit]"] = params.pop("limit", args.limit)
        if args.offset is not None:
            params["page[offset]"] = params.pop("offset", args.offset)

    # Special handling for economic-events endpoint (country, comparison)
    if args.endpoint == "economic-events":
        if args.country:
            params["country"] = args.country
        if args.comparison:
            params["comparison"] = args.comparison

    # Special handling for screener endpoint (filters, sort, signals)
    if args.endpoint == "screener":
        if args.filters:
            params["filters"] = args.filters
        if args.sort:
            params["sort"] = args.sort
        if args.signals:
            params["signals"] = args.signals

    # Special handling for calendar/trends endpoint (requires symbols parameter)
    if args.endpoint == "calendar/trends":
        if not args.symbol:
            print("Error: --symbol is required for calendar/trends (comma-separated)", file=sys.stderr)
            return 2
        params["symbols"] = args.symbol

    # Special handling for calendar/earnings endpoint (supports symbols parameter)
    if args.endpoint == "calendar/earnings" and args.symbol:
        params["symbols"] = args.symbol
        # When symbols is provided, remove from/to parameters
        params.pop("from", None)
        params.pop("to", None)

    # Special handling for calendar/splits endpoint (supports symbols parameter)
    if args.endpoint == "calendar/splits" and args.symbol:
        params["symbols"] = args.symbol

    # Special handling for us-quote-delayed endpoint (uses 's' param, page[limit], page[offset])
    if args.endpoint == "us-quote-delayed":
        if not args.symbol:
            print("Error: --symbol is required for us-quote-delayed (comma-separated for batch)", file=sys.stderr)
            return 2
        params["s"] = args.symbol
        if args.limit is not None:
            params["page[limit]"] = params.pop("limit", args.limit)
        if args.offset is not None:
            params["page[offset]"] = params.pop("offset", args.offset)

    # Special handling for bulk-fundamentals endpoint (symbols, version params)
    if args.endpoint == "bulk-fundamentals":
        if args.symbols:
            params["symbols"] = args.symbols
        if args.version:
            params["version"] = args.version

    # Special handling for UST endpoints (filter[year], page[limit], page[offset])
    if args.endpoint.startswith("ust/"):
        if args.filter_year is not None:
            params["filter[year]"] = args.filter_year
        if args.limit is not None:
            params["page[limit]"] = params.pop("limit", args.limit)
        if args.offset is not None:
            params["page[offset]"] = params.pop("offset", args.offset)

    # Special handling for JSON:API filter endpoints (credit-risk, rates).
    # Filters arrive as --filter-param KEY=VALUE and are sent as filter[KEY]=VALUE.
    # Pagination uses page[limit]/page[offset]; funding-stress has no pagination.
    if args.endpoint in FILTER_API_ENDPOINTS:
        # Strip every generic CLI-derived param: these endpoints take only
        # filter[...] (from --filter-param) and, where allowed, page[...].
        # Dates go via --filter-param from=/to= (rendered filter[from]/filter[to]).
        for _k in _GENERIC_QUERY_KEYS:
            params.pop(_k, None)
        for item in args.filter_param:
            if "=" not in item:
                print(f"Error: --filter-param must be KEY=VALUE, got '{item}'", file=sys.stderr)
                return 2
            key, _, value = item.partition("=")
            key = key.strip()
            if not key:
                print(f"Error: --filter-param missing key in '{item}'", file=sys.stderr)
                return 2
            params[f"filter[{key}]"] = value
        if args.endpoint not in FILTER_NO_PAGINATION_ENDPOINTS:
            if args.limit is not None:
                params["page[limit]"] = args.limit
            if args.offset is not None:
                params["page[offset]"] = args.offset

    # Special handling for sanctions endpoints. entities/vessels use BARE query
    # params (source, type, program, q, active, imo, flag, ...) — NOT filter[...]
    # — plus page[limit]/page[offset]. programs/sources take no params at all.
    if args.endpoint in SANCTIONS_API_ENDPOINTS:
        # Strip every generic CLI-derived param so nothing leaks; sanctions
        # endpoints have no date range and take only the keys below.
        for _k in _GENERIC_QUERY_KEYS:
            params.pop(_k, None)
        if args.endpoint in SANCTIONS_NO_PARAM_ENDPOINTS:
            # programs/sources forward no params upstream — reject any the user
            # passed rather than silently dropping them (false sense of filtering).
            if args.filter_param or args.limit is not None or args.offset is not None:
                print(
                    f"Error: endpoint '{args.endpoint}' accepts no query parameters "
                    "(no filters, no pagination); drop --filter-param/--limit/--offset",
                    file=sys.stderr,
                )
                return 2
        else:
            for item in args.filter_param:
                if "=" not in item:
                    print(f"Error: --filter-param must be KEY=VALUE, got '{item}'", file=sys.stderr)
                    return 2
                key, _, value = item.partition("=")
                key = key.strip()
                if not key:
                    print(f"Error: --filter-param missing key in '{item}'", file=sys.stderr)
                    return 2
                params[key] = value
            if args.limit is not None:
                params["page[limit]"] = args.limit
            if args.offset is not None:
                params["page[offset]"] = args.offset

    # Special handling for Real Estate Data API endpoints (BIS property prices).
    # Uses bracket-style filter[...] params, sort, and page[limit]/page[offset].
    if args.endpoint.startswith("real-estate"):
        if args.re_type:
            params["filter[type]"] = args.re_type
        if args.re_metric:
            params["filter[metric]"] = args.re_metric
        if args.re_area:
            params["filter[area]"] = args.re_area
        if args.re_property_type:
            params["filter[property_type]"] = args.re_property_type
        if args.re_vintage:
            params["filter[vintage]"] = args.re_vintage
        if args.re_freq:
            params["filter[freq]"] = args.re_freq
        if args.re_from:
            params["filter[from]"] = args.re_from
        if args.re_to:
            params["filter[to]"] = args.re_to
        if args.sort:
            params["sort"] = args.sort
        if args.limit is not None:
            params["page[limit]"] = params.pop("limit", args.limit)
        if args.offset is not None:
            params["page[offset]"] = params.pop("offset", args.offset)

    query = urllib.parse.urlencode(params)
    url = args.base_url.rstrip("/") + path + "?" + query

    if args.print_url:
        print(_redact_token(url))
        return 0

    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        print(f"HTTP Error {exc.code}: {exc.reason}", file=sys.stderr)
        print(f"URL: {_redact_token(url)}", file=sys.stderr)
        try:
            error_body = exc.read().decode("utf-8", errors="replace")
            print(f"Response: {error_body}", file=sys.stderr)
        except Exception:
            pass
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc.reason}", file=sys.stderr)
        print(f"URL: {_redact_token(url)}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        print(f"URL: {_redact_token(url)}", file=sys.stderr)
        return 1

    if args.raw:
        print(payload)
        return 0

    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        # Not JSON, print raw
        print(payload)
        return 0

    parsed = normalize_response(args.endpoint, parsed)
    print(json.dumps(parsed, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
