# US Treasury Yield Rates API (Par Yield Curve)

Status: complete
Source: financial-apis (US Treasury API)
Docs: https://eodhd.com/financial-apis/us-treasury-interest-rates-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /ust/yield-rates
Method: GET
Auth: api_token (query)

## Purpose

Provides Daily Treasury Par Yield Curve Rates (nominal yield curve by tenor). Returns the full nominal yield curve across multiple maturities from 1 month to 30 years. Used for yield curve modeling, fixed-income pricing, term structure analysis, and macro research. Available in All-In-One, EOD Historical Data: All World, EOD + Intraday: All World Extended, and Free plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[year] | No | integer | Filter by year (1900 – current year + 1). If not mentioned – current year |

## Response (shape)

```json
{
  "meta": {
    "total": 280
  },
  "data": [
    {
      "date": "2026-01-02",
      "tenor": "1M",
      "rate": 3.72
    },
    {
      "date": "2026-01-02",
      "tenor": "3M",
      "rate": 3.65
    },
    {
      "date": "2026-01-02",
      "tenor": "6M",
      "rate": 3.58
    },
    {
      "date": "2026-01-02",
      "tenor": "1Y",
      "rate": 3.47
    },
    {
      "date": "2026-01-02",
      "tenor": "2Y",
      "rate": 3.24
    },
    {
      "date": "2026-01-02",
      "tenor": "10Y",
      "rate": 3.15
    },
    {
      "date": "2026-01-02",
      "tenor": "30Y",
      "rate": 3.40
    }
  ],
  "links": {
    "next": null
  }
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| meta | object | Metadata including total record count |
| data | array | Array of yield rate records |
| links | object | Pagination links (next page URL or null) |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| date | string (YYYY-MM-DD) | Observation date |
| tenor | string | Tenor (e.g., 1M, 1.5M, 2M, 3M, 4M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 20Y, 30Y) |
| rate | number | Par yield for the given tenor |

## Example Requests

```bash
# Yield rates for 2023
curl "https://eodhd.com/api/ust/yield-rates?api_token=YOUR_TOKEN&filter[year]=2023"

# Yield rates for current year
curl "https://eodhd.com/api/ust/yield-rates?api_token=YOUR_TOKEN"

# Using the helper client
python eodhd_client.py --endpoint ust/yield-rates --filter-year 2023
```

## Notes

- Returns multiple tenors per observation date, covering the full yield curve
- Available tenors include: 1M, 1.5M, 2M, 3M, 4M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 20Y, 30Y
- If `filter[year]` is omitted, defaults to the current year
- Useful for constructing yield curves, calculating spreads (e.g., 2Y-10Y spread), and term structure analysis
- API call consumption: 1 call per request
- Part of the US Treasury (UST) Interest Rates API (beta)

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
