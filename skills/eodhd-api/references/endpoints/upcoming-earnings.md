# Historical & Upcoming Earnings API

Status: complete
Source: financial-apis (Calendar Earnings API)
Docs: https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /calendar/earnings
Method: GET
Auth: api_token (query)

## Purpose

Returns historical and upcoming earnings dates with key fields (company symbol, report date/time, and additional metadata when available). Use either a date window or a symbol list. Available in All-In-One, Fundamentals Data Feed plans and via "Financial Events (Calendar) & News Feed" plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key for authentication |
| from | No | string (YYYY-MM-DD) | Start date. Default: today |
| to | No | string (YYYY-MM-DD) | End date. Default: today + 7 days |
| symbols | No | string | One or more tickers (comma-separated). If set, from/to are ignored. Example: AAPL.US,MSFT.US,AI.PA |
| fmt | No | string | Output format: json or csv (default) |

## Response (shape)

```json
{
  "type": "Earnings",
  "description": "Historical and upcoming Earnings",
  "from": "2018-12-02",
  "to": "2018-12-06",
  "earnings": [
    {
      "code": "PIGEF.US",
      "report_date": "2018-12-02",
      "date": "2018-09-30",
      "before_after_market": "AfterMarket",
      "currency": "USD",
      "actual": 34.52,
      "estimate": 36.73,
      "difference": -2.21,
      "percent": -6.0169
    },
    {
      "code": "ANTM.JK",
      "report_date": "2018-12-02",
      "date": "2018-09-30",
      "before_after_market": "AfterMarket",
      "currency": "IDR",
      "actual": 11.9295,
      "estimate": null,
      "difference": 0,
      "percent": null
    }
  ]
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| type | string | Constant label of the payload (example: "Earnings") |
| description | string | Human-readable description of the dataset |
| from | string (YYYY-MM-DD), optional | Start date of the requested range (present for date-window queries) |
| to | string (YYYY-MM-DD), optional | End date of the requested range (present for date-window queries) |
| symbols | string, optional | Comma-separated list of requested tickers (present for symbol-list queries) |
| earnings | array of objects | List of earnings records returned by the query |

**Earnings record fields:**

| Field | Type | Description |
|-------|------|-------------|
| code | string | Ticker in EODHD format |
| report_date | string (YYYY-MM-DD) | Date when the company reported/announced results |
| date | string (YYYY-MM-DD) | Fiscal period end date the result refers to |
| before_after_market | string or null | Report timing relative to market hours (e.g., BeforeMarket, AfterMarket), or null if unknown |
| currency | string or null | Reporting currency for EPS |
| actual | number or null | Reported EPS (or metric used by the feed) |
| estimate | number or null | Consensus EPS estimate, if available |
| difference | number or null | actual − estimate |
| percent | number or null | Surprise in percent (difference / estimate * 100), when estimate is available |

## Example Requests

```bash
# By symbol
curl "https://eodhd.com/api/calendar/earnings?symbols=AAPL.US,MSFT.US,AI.PA&api_token=demo&fmt=json"

# By date window
curl "https://eodhd.com/api/calendar/earnings?from=2026-02-10&to=2026-02-10&api_token=demo&fmt=json"

# Default (today + 7 days)
curl "https://eodhd.com/api/calendar/earnings?api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint calendar/earnings --from-date 2026-02-10 --to-date 2026-02-10
```

## Notes

- Without dates, default window is "today +7 days"
- When using `symbols` parameter, `from` and `to` parameters are ignored
- `before_after_market` indicates when earnings are released relative to market hours
- `actual` will be null for upcoming (not yet reported) earnings
- `percent` shows earnings surprise: positive = beat, negative = miss
- API call consumption: 1 call per request
- Data available from the beginning up to several months into the future

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
