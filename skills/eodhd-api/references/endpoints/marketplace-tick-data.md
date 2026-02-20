# Marketplace Tick Data API (US Stock Market)

Status: complete
Source: marketplace (Unicorn Bay)
Provider: Unicorn Bay via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/unicornbay/tickdata`
Path: `/ticks`
Method: GET
Auth: `api_token` query parameter

> **Important**: This is a **Marketplace** product with its own path (`/api/mp/unicornbay/tickdata/ticks`). Do **not** confuse it with the base EODHD tick endpoint at `/api/ticks/` — they are separate APIs.

## Purpose

Provides comprehensive **tick-by-tick** (trade-level) data for US stock market tickers with millisecond-precision timestamps, prices, and volumes. Each tick record represents an individual trade execution.

**Use cases**:
- High-frequency trading analysis
- Backtesting strategies at trade-level granularity
- Market microstructure research
- Order flow and liquidity analysis
- Spread and slippage studies

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

## Parameters

### Required

| Parameter | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `api_token` | string | — | Your API key |
| `s` | string | max 30 chars | Ticker symbol (e.g., `AAPL`, `MSFT`, `GOOGL`) |

### Optional

| Parameter | Type | Constraints | Default | Description |
|-----------|------|-------------|---------|-------------|
| `from` | integer | max 4294967295 | Yesterday start of day | Start timestamp (Unix timestamp in **seconds**) |
| `to` | integer | max 4294967295 | Yesterday end of day | End timestamp (Unix timestamp in **seconds**) |
| `limit` | integer | 1–10000 | All ticks in range | Maximum number of ticks to return. If 0 or omitted, returns all ticks in the time range |

## Response (shape)

The response contains **columnar arrays** — each field is an array of values aligned by index (index 0 across all fields = first tick, index 1 = second tick, etc.):

```json
{
  "ts": [1694077201147, 1694077206102, 1694077206102],
  "price": [177.88, 177.95, 177.97],
  "shares": [1, 50, 50],
  "mkt": ["K", "Q", "Q"],
  "seq": [1434370, 1436393, 1436394],
  "sl": ["@ TI", "@ TI", "@ TI"],
  "sub_mkt": ["", "", ""]
}
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `ts` | integer[] | Timestamp in **milliseconds** (Unix epoch). Note: `from`/`to` params are in seconds, but response timestamps are in milliseconds |
| `price` | float[] | Trade execution price |
| `shares` | integer[] | Number of shares traded in this tick |
| `mkt` | string[] | Market identifier code (exchange where the trade executed) |
| `seq` | integer[] | Sequence number (unique ordering of trades within the day) |
| `sl` | string[] | Source/location identifier |
| `sub_mkt` | string[] | Sub-market identifier (may be empty) |

### Market Identifier Codes (`mkt`)

Common values for the `mkt` field:

| Code | Exchange |
|------|----------|
| `Q` | NASDAQ |
| `K` | NYSE (Arca) |
| `P` | NYSE Arca |
| `N` | NYSE |
| `Z` | BATS |
| `V` | IEX |

## Example Requests

### Get 10 ticks for AAPL in a time window

```bash
curl "https://eodhd.com/api/mp/unicornbay/tickdata/ticks?s=AAPL&from=1694077200&to=1694080800&limit=10&api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/unicornbay/tickdata/ticks?s=AAPL&from=1694077200&to=1694080800&limit=10&api_token=demo"
```

### Python (requests)

```python
import requests
from datetime import datetime, timedelta

# Define time range (e.g., yesterday 9:30 AM to 10:00 AM ET)
url = "https://eodhd.com/api/mp/unicornbay/tickdata/ticks"
params = {
    "s": "AAPL",
    "from": 1694077200,    # Unix timestamp in seconds
    "to": 1694080800,      # Unix timestamp in seconds
    "limit": 100,
    "api_token": "YOUR_API_TOKEN"
}

response = requests.get(url, params=params)
data = response.json()

# Data is columnar — iterate by index
for i in range(len(data["ts"])):
    ts_ms = data["ts"][i]
    price = data["price"][i]
    shares = data["shares"][i]
    mkt = data["mkt"][i]
    ts_str = datetime.fromtimestamp(ts_ms / 1000).strftime("%H:%M:%S.%f")[:-3]
    print(f"{ts_str} | ${price:.2f} | {shares:>5} shares | {mkt}")
```

**Output example**:
```
09:00:01.147 | $177.88 |     1 shares | K
09:00:06.102 | $177.95 |    50 shares | Q
09:00:06.102 | $177.97 |    50 shares | Q
09:00:06.102 | $177.96 |    50 shares | P
09:00:06.102 | $177.97 |    50 shares | P
09:00:06.102 | $177.97 |     6 shares | P
09:00:06.996 | $177.98 |    10 shares | Q
09:00:06.996 | $177.98 |    50 shares | Q
09:00:06.996 | $177.99 |    40 shares | Q
09:00:06.996 | $177.98 |    50 shares | P
```

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Tick data returned. |
| **401** | Unauthorized | Invalid or missing API key |
| **403** | Forbidden | No access to this marketplace product |
| **422** | Unprocessable Entity | Invalid parameters (e.g., bad ticker, invalid timestamp) |
| **429** | Too Many Requests | Rate limit exceeded (1,000 req/min or 100,000 calls/24h) |

## Notes

- **Columnar response format**: Unlike most EODHD endpoints that return arrays of objects, this endpoint returns an object of arrays (columnar). All arrays are the same length and aligned by index.
- **Timestamp units differ**: `from`/`to` parameters use **seconds**, but response `ts` field is in **milliseconds**. Divide `ts` by 1000 to convert to seconds.
- **US stocks only**: Covers thousands of US stock tickers (NYSE, NASDAQ, etc.)
- **Demo tickers**: Test with `api_token=demo` using AAPL, MSFT, GOOGL, and other popular US stocks.
- **Marketplace rate limits**: The 24-hour call limit is counted separately from your main EODHD plan quota.
- **Default time range**: If `from`/`to` are omitted, defaults to yesterday's full trading day.
- **Coverage**: Historical tick data with millisecond precision. Each tick = one individual trade execution.
