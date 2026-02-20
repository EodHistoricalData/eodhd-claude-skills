# Symbol Change History API

Status: complete
Source: financial-apis
Provider: EODHD
Base URL: `https://eodhd.com/api`
Path: `/symbol-change-history`
Method: GET
Auth: `api_token` query parameter

## Purpose

Get the history of ticker symbol changes (renames). When a company rebrands, merges, or restructures, its ticker symbol may change. This endpoint tracks those changes so you can maintain data continuity.

**Key details**:
- History available from **2022-07-22** onward
- Updated on a **daily** basis
- **US exchanges only** for now (other exchanges coming)

## Plans & API Calls

- **Available in**: All World Extended, All-In-One plans
- **API call consumption**: 5 API calls per ticker (per request)

## Parameters

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `from` | string | — | Start date (`YYYY-MM-DD`). History starts from `2022-07-22` |
| `to` | string | — | End date (`YYYY-MM-DD`) |
| `fmt` | string | `csv` | Response format: `json` or `csv` |

## Response (shape)

Returns a JSON array of symbol change records:

```json
[
  {
    "exchange": "US",
    "old_symbol": "CBTX",
    "new_symbol": "STEL",
    "company_name": "Stellar Bancorp, Inc. Common Stock",
    "effective": "2022-10-03"
  },
  {
    "exchange": "US",
    "old_symbol": "XPER",
    "new_symbol": "ADEA",
    "company_name": "Adeia Inc. Common Stock",
    "effective": "2022-10-03"
  },
  {
    "exchange": "US",
    "old_symbol": "LLL",
    "new_symbol": "JXJT",
    "company_name": "JX Luxventure Limited Common Stock",
    "effective": "2022-10-10"
  }
]
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `exchange` | string | Exchange code (currently always `US`) |
| `old_symbol` | string | Previous ticker symbol |
| `new_symbol` | string | New ticker symbol |
| `company_name` | string | Full company name |
| `effective` | string | Date the change took effect (`YYYY-MM-DD`) |

## Example Requests

### Get symbol changes for a date range

```bash
curl "https://eodhd.com/api/symbol-change-history?from=2022-10-01&to=2022-10-15&api_token=YOUR_API_TOKEN&fmt=json"
```

### Get recent symbol changes (with demo key)

```bash
curl "https://eodhd.com/api/symbol-change-history?from=2022-10-01&api_token=demo&fmt=json"
```

### Python (requests)

```python
import requests

url = "https://eodhd.com/api/symbol-change-history"
params = {
    "api_token": "YOUR_API_TOKEN",
    "from": "2022-10-01",
    "to": "2022-10-15",
    "fmt": "json"
}
response = requests.get(url, params=params)
changes = response.json()

for change in changes:
    print(f"{change['effective']}: {change['old_symbol']} → {change['new_symbol']} ({change['company_name']})")
```

## Use Cases

- **Data continuity**: Map old tickers to new ones when maintaining historical databases
- **Portfolio tracking**: Detect when held symbols change and update portfolio records
- **Backtesting**: Ensure historical analysis uses correct symbols for the time period
- **Compliance**: Track corporate actions involving ticker changes

## Notes

- History starts from **2022-07-22** — no data available before this date
- **US exchanges only** — other exchanges are planned
- Updated daily
- Includes all types of symbol changes: rebrands, mergers, SPACs, ETF renames
- Warrants and other derivative instruments are also tracked (e.g., `CNTQW` → `DFLIW`)

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
