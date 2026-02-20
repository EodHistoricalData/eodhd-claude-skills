# Tick Data API

Status: complete
Source: financial-apis (Intraday Historical Data API)
Docs: https://eodhd.com/financial-apis/intraday-historical-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /ticks/{SYMBOL}
Method: GET
Auth: api_token (query)

## Purpose

Fetches tick-by-tick trade data for a symbol, providing the most granular level of market data.
Each tick represents a single trade execution with timestamp, price, and volume. Useful for
high-frequency analysis, market microstructure research, and detailed intraday pattern analysis.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| {SYMBOL} | Yes | path | Ticker symbol with exchange suffix (e.g., 'AAPL.US') |
| api_token | Yes | string | Your API key for authentication |
| from | No | integer/string | Start time (Unix timestamp) or date (YYYY-MM-DD) |
| to | No | integer/string | End time (Unix timestamp) or date (YYYY-MM-DD) |
| limit | No | integer | Number of ticks to return. Default: 100, Max: 10000 |
| fmt | No | string | Output format: 'json' or 'csv'. Default: 'json' |

## Response (shape)

```json
[
  {
    "timestamp": 1704888000,
    "gmtoffset": -18000,
    "datetime": "2025-01-10 09:30:00",
    "price": 185.25,
    "volume": 500
  },
  {
    "timestamp": 1704888001,
    "gmtoffset": -18000,
    "datetime": "2025-01-10 09:30:01",
    "price": 185.30,
    "volume": 200
  },
  {
    "timestamp": 1704888002,
    "gmtoffset": -18000,
    "datetime": "2025-01-10 09:30:02",
    "price": 185.28,
    "volume": 1000
  }
]
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| timestamp | integer | Unix timestamp of the trade |
| gmtoffset | integer | GMT offset in seconds for the exchange |
| datetime | string | Human-readable datetime (YYYY-MM-DD HH:MM:SS) |
| price | number | Trade execution price |
| volume | integer | Number of shares traded |

## Example Requests

```bash
# Recent ticks for AAPL (last 100)
curl "https://eodhd.com/api/ticks/AAPL.US?api_token=demo&fmt=json"

# Ticks with limit
curl "https://eodhd.com/api/ticks/AAPL.US?limit=1000&api_token=demo&fmt=json"

# Ticks for specific date (Unix timestamps)
curl "https://eodhd.com/api/ticks/MSFT.US?from=1704888000&to=1704974400&api_token=demo&fmt=json"

# Ticks for date range
curl "https://eodhd.com/api/ticks/GOOGL.US?from=2025-01-10&to=2025-01-10&limit=5000&api_token=demo&fmt=json"
```

## Notes

- Tick data provides trade-level granularity (every individual trade)
- Data volume is very high; use `limit` parameter to control response size
- Unix timestamps in `from`/`to` allow precise time windows
- `gmtoffset` helps convert to local exchange time
- Not all symbols have tick data available; primarily US equities
- Data retention varies; recent data is most reliably available
- For OHLCV bars, use the intraday endpoint instead
- API call consumption: Higher than standard endpoints due to data volume
- Maximum 10,000 ticks per request
- **Building OHLCV from ticks**: Aggregating OHLCV data from tick data is not simply taking the first/max/min/last prices. The process depends on the **sale-condition** of each tick — many ticks may be excluded from the calculation based on conditions from the exchanges. See: https://www.utpplan.com/DOC/UtpBinaryOutputSpec.pdf
- **Timestamps: seconds vs milliseconds**: The `from` and `to` parameters must be specified in **seconds** (Unix timestamp). The result timestamps are returned in **milliseconds**.
- **Dark pool ticks**: Ticks where the market center (`mkt`) field contains `D` are **dark pool** trades (off-exchange).
- **Market center (`mkt`) field codes**:

| Code | Exchange |
|------|----------|
| X | NASDAQ |
| T | NASDAQ |
| B | NASDAQ |
| Q | NASDAQ |
| R | NASDAQ |
| N | NYSE |
| C | NYSE |
| P | NYSE |
| A | NYSE |
| K | CBOE |
| Y | CBOE |
| J | CBOE |
| W | CBOE |
| Z | CBOE |
| V | IEX |
| S, u, U, ?, a | OTC |

## Use Cases

- **Market microstructure analysis**: Study bid-ask spreads, order flow
- **High-frequency patterns**: Identify sub-minute trading patterns
- **Trade execution analysis**: Compare execution prices to market
- **Volume profile**: Analyze volume at specific price levels
- **Event studies**: Precise timing around news/earnings

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

### Error Response Format

When an error occurs, the API returns a JSON response with error details:

```json
{
  "error": "Error message description",
  "code": 403
}
```

### Handling Errors

**Python Example**:
```python
import requests

def make_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:
            print("Error: API limit exceeded. Please upgrade your plan.")
        elif e.response.status_code == 403:
            print("Error: Invalid API key. Check your credentials.")
        elif e.response.status_code == 429:
            print("Error: Rate limit exceeded. Please slow down your requests.")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

**Best Practices**:
- Always check status codes before processing response data
- Implement exponential backoff for 429 errors
- Cache responses to reduce API calls
- Monitor your API usage in the user dashboard
