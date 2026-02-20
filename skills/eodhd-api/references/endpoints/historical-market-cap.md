# Historical Market Capitalization API

Status: complete
Source: financial-apis
Docs: https://eodhd.com/financial-apis/historical-market-capitalization-api
Provider: EODHD
Base URL: `https://eodhd.com/api`
Path: `/historical-market-cap/{TICKER_CODE}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Provides weekly market capitalization data for US stocks (NYSE and NASDAQ) from 2019 onward. Useful for historical trend analysis, portfolio management, backtesting, and cross-company valuation comparisons.

**Key characteristics**:
- **Weekly frequency** — one data point per week (typically Thursday/Friday)
- **US stocks only** — NYSE and NASDAQ listed stocks
- **Historical depth** — data available from 2019 onward
- **Values in raw USD** — not millions or billions (divide by `1e9` for billions)

## Plans & API Calls

- **Available in**: All-In-One, Fundamentals Data Feed
- **API call consumption**: 10 API calls per request (regardless of date range)

## Parameters

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| `{TICKER_CODE}` | path string | Ticker with exchange suffix (e.g., `AAPL.US`). For US stocks, suffix can be omitted (`AAPL`) |
| `api_token` | string | Your API key |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `from` | string | `2019-01-01` | Start date (`YYYY-MM-DD`). Earliest available data if omitted |
| `to` | string | Latest | End date (`YYYY-MM-DD`). Latest available data if omitted |
| `fmt` | string | `json` | Output format: `json` or `csv` |

## Response (shape)

Returns a JSON object with numeric keys, where each entry contains a date and market cap value:

```json
{
  "0": {
    "date": "2020-01-09",
    "value": 1357426280000
  },
  "1": {
    "date": "2020-01-16",
    "value": 1382020671500
  },
  "2": {
    "date": "2020-01-23",
    "value": 1396784480400
  }
}
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Weekly date (`YYYY-MM-DD`) |
| `value` | number | Market capitalization in raw USD. Example: `1357426280000` = $1.357 trillion |

### CSV Response

When using `fmt=csv`:

```csv
date,value
2020-01-09,1357426280000
2020-01-16,1382020671500
2020-01-23,1396784480400
```

## Example Requests

### Get all available data for Apple

```bash
curl "https://eodhd.com/api/historical-market-cap/AAPL.US?api_token=demo&fmt=json"
```

### Specific date range

```bash
curl "https://eodhd.com/api/historical-market-cap/AAPL.US?api_token=demo&from=2020-01-05&to=2020-03-10&fmt=json"
```

### US ticker shorthand (omit .US)

```bash
curl "https://eodhd.com/api/historical-market-cap/AAPL?api_token=demo&from=2023-01-01&to=2023-12-31"
```

### Python (requests)

```python
import requests

url = "https://eodhd.com/api/historical-market-cap/AAPL.US"
params = {
    "api_token": "YOUR_API_TOKEN",
    "from": "2023-01-01",
    "to": "2023-12-31",
    "fmt": "json"
}
response = requests.get(url, params=params)
data = response.json()

# Iterate over weekly data points
for key, entry in data.items():
    value_billions = entry["value"] / 1e9
    print(f"{entry['date']}: ${value_billions:.2f}B")
```

## Notes

- **Weekly data** — not daily. Typically one point per week on Thursday/Friday
- **US only** — NYSE and NASDAQ. International stocks not currently supported
- **Values in raw USD** — divide by `1e9` for billions, `1e12` for trillions
- **10 API calls per request** — plan accordingly for multi-ticker analysis (10 tickers = 100 calls)
- **From 2019** — no data available before 2019
- **Ticker shorthand** — for US stocks, `.US` suffix can be omitted
- **Demo access** — `api_token=demo` works for `AAPL.US` only
- **Fundamentals API alternative** — for current/quarterly market cap, use the Fundamentals API (`/fundamentals/{SYMBOL}`), which provides more precise point-in-time values synchronized with earnings. This endpoint is better for weekly trend analysis over longer periods

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
