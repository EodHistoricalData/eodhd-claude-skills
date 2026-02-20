# US Treasury Real Yield Rates API (Par Real Yield Curve)

Status: complete
Source: financial-apis (US Treasury API)
Docs: https://eodhd.com/financial-apis/us-treasury-interest-rates-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /ust/real-yield-rates
Method: GET
Auth: api_token (query)

## Purpose

Provides Daily Treasury Par Real Yield Curve Rates (real yield curve by tenor). Returns inflation-adjusted yields across maturities from 5 years to 30 years. Used for real return analysis, inflation expectations (comparing nominal vs real yields), TIPS pricing, and macro research. Available in All-In-One, EOD Historical Data: All World, EOD + Intraday: All World Extended, and Free plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[year] | No | integer | Filter by year (1900 – current year + 1). If not mentioned – current year |

## Response (shape)

```json
{
  "meta": {
    "total": 100
  },
  "data": [
    {
      "date": "2026-01-02",
      "tenor": "5Y",
      "rate": 1.46
    },
    {
      "date": "2026-01-02",
      "tenor": "7Y",
      "rate": 1.69
    },
    {
      "date": "2026-01-02",
      "tenor": "10Y",
      "rate": 1.94
    },
    {
      "date": "2026-01-02",
      "tenor": "20Y",
      "rate": 2.39
    },
    {
      "date": "2026-01-02",
      "tenor": "30Y",
      "rate": 2.63
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
| data | array | Array of real yield rate records |
| links | object | Pagination links (next page URL or null) |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| date | string (YYYY-MM-DD) | Observation date |
| tenor | string | Tenor (e.g., 5Y, 7Y, 10Y, 20Y, 30Y) |
| rate | number | Real yield for the given tenor |

## Example Requests

```bash
# Real yield rates for 2024
curl "https://eodhd.com/api/ust/real-yield-rates?api_token=YOUR_TOKEN&filter[year]=2024"

# Real yield rates for current year
curl "https://eodhd.com/api/ust/real-yield-rates?api_token=YOUR_TOKEN"

# Using the helper client
python eodhd_client.py --endpoint ust/real-yield-rates --filter-year 2024
```

## Notes

- Returns five tenors per observation date: 5Y, 7Y, 10Y, 20Y, and 30Y
- Real yields reflect inflation-adjusted returns (derived from TIPS)
- Comparing nominal yields (from yield-rates endpoint) with real yields gives implied inflation expectations (breakeven inflation)
- If `filter[year]` is omitted, defaults to the current year
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
