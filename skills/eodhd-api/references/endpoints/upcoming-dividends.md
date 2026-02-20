# Historical & Upcoming Dividends API

Status: complete
Source: financial-apis (Calendar API)
Docs: https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /calendar/dividends
Method: GET
Auth: api_token (query)

## Purpose

Returns a calendar of dividend dates filtered by symbol or by date. Supports pagination. Available in All-In-One, Fundamentals Data Feed plans and via "Financial Events (Calendar) & News Feed" plans.

For dividend details, navigate to the Corporate Actions: Splits and Dividends API.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[symbol] | Conditional | string | Limit results to a single ticker. Required if filter[date_eq] is not provided |
| filter[date_eq] | Conditional | string (YYYY-MM-DD) | Exact dividend date. Required if filter[symbol] is not provided |
| filter[date_from] | No | string (YYYY-MM-DD) | Return dividends on or after this date |
| filter[date_to] | No | string (YYYY-MM-DD) | Return dividends on or before this date |
| page[limit] | No | integer (1–1000, default 1000) | Max results per page |
| page[offset] | No | integer (default 0) | Offset for pagination |
| fmt | No | string | json only |

## Response (shape)

```json
{
  "meta": {
    "total": 3,
    "offset": 0,
    "limit": 1000,
    "symbol": "AAPL.US",
    "date_eq": null
  },
  "data": [
    { "date": "2025-08-11", "symbol": "AAPL.US" },
    { "date": "2025-05-12", "symbol": "AAPL.US" },
    { "date": "2025-02-10", "symbol": "AAPL.US" }
  ],
  "links": {
    "next": null
  }
}
```

### Output Format

**Meta object:**

| Field | Type | Description |
|-------|------|-------------|
| total | integer | Total number of results across all pages |
| limit | integer | Max number of results returned in this page |
| offset | integer | Offset used for this page |
| symbol | string or null | Echo of requested symbol, if provided |
| date_eq | string or null | Echo of requested exact date, if provided |

**Data array:**

Each item in the data array:

| Field | Type | Description |
|-------|------|-------------|
| date | string (YYYY-MM-DD) | Dividend date |
| symbol | string | Ticker |

**Links object:**

| Field | Type | Description |
|-------|------|-------------|
| next | string or null | URL to the next page, or null if none |

## Example Requests

```bash
# By symbol
curl "https://eodhd.com/api/calendar/dividends?filter[symbol]=AAPL.US&api_token=demo&fmt=json"

# By date window
curl "https://eodhd.com/api/calendar/dividends?filter[symbol]=AAPL.US&filter[date_from]=2025-01-01&filter[date_to]=2025-12-31&api_token=demo&fmt=json"

# By exact date
curl "https://eodhd.com/api/calendar/dividends?filter[date_eq]=2026-01-01&api_token=demo&fmt=json"

# With pagination
curl "https://eodhd.com/api/calendar/dividends?filter[symbol]=AAPL.US&page[limit]=10&page[offset]=0&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint calendar/dividends --symbol AAPL.US
```

## Notes

- At least one of `filter[symbol]` or `filter[date_eq]` must be provided
- Use `page[limit]` and `page[offset]` for large datasets
- `filter[date_from]` and `filter[date_to]` can be used together (with `filter[symbol]`) to narrow the range
- The `links.next` field provides the URL for the next page of results
- JSON-only format
- This endpoint returns dates only; for full dividend details (amounts, payment dates, etc.), use the Corporate Actions: Splits and Dividends API
- API call consumption: 1 call per request
- **Dividend currency**: By default, the currency is the same as for end-of-day data in most cases. However, if it differs, the `currency` field in the dividend data indicates the actual currency.
- **YOC (Yield on Cost)**: EODHD provides dividends and daily stock prices. To calculate YOC, divide the latest dividend amount by the stock price on a given day. This must be calculated on your side.
- **Adjusted dividends**: All dividends provided by EODHD are **split-adjusted**.

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
