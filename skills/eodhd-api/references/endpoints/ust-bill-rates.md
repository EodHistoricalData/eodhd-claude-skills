# US Treasury Bill Rates API

Status: complete
Source: financial-apis (US Treasury API)
Docs: https://eodhd.com/financial-apis/us-treasury-interest-rates-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /ust/bill-rates
Method: GET
Auth: api_token (query)

## Purpose

Provides Daily Treasury Bill Rates (T-Bills): discount and coupon rates, average rates, maturity, and CUSIP. These time series are widely used for macro research, fixed-income analytics, discounting/cost of capital, yield curve modeling, and building risk-free rate baselines in trading/portfolio systems. Available in All-In-One, EOD Historical Data: All World, EOD + Intraday: All World Extended, and Free plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[year] | No | integer | Filter by year (1900 – current year + 1). If not mentioned – current year |
| page[limit] | No | integer | Number of records per page |
| page[offset] | No | integer | Offset for pagination |

## Response (shape)

```json
{
  "meta": {
    "total": 120
  },
  "data": [
    {
      "date": "2026-01-02",
      "tenor": "4WK",
      "discount": 3.58,
      "coupon": 3.64,
      "avg_discount": 3.58,
      "avg_coupon": 3.64,
      "maturity_date": "2026-02-03",
      "cusip": "912797SJ7"
    },
    {
      "date": "2026-01-02",
      "tenor": "8WK",
      "discount": 3.57,
      "coupon": 3.64,
      "avg_discount": 3.57,
      "avg_coupon": 3.64,
      "maturity_date": "2026-03-03",
      "cusip": "912797ST5"
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
| data | array | Array of bill rate records |
| links | object | Pagination links (next page URL or null) |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| date | string (YYYY-MM-DD) | Observation date |
| tenor | string | Bill tenor (e.g., 4WK, 8WK, 13WK, 17WK, 26WK, 52WK) |
| discount | number | Discount rate |
| coupon | number | Coupon equivalent rate |
| avg_discount | number | Average discount rate |
| avg_coupon | number | Average coupon equivalent rate |
| maturity_date | string (YYYY-MM-DD) | Maturity date |
| cusip | string | CUSIP identifier |

## Example Requests

```bash
# Bill rates for 2012
curl "https://eodhd.com/api/ust/bill-rates?api_token=YOUR_TOKEN&filter[year]=2012&page[limit]=100&page[offset]=0"

# Bill rates for current year
curl "https://eodhd.com/api/ust/bill-rates?api_token=YOUR_TOKEN"

# Using the helper client
python eodhd_client.py --endpoint ust/bill-rates --filter-year 2012 --limit 100
```

## Notes

- Returns data grouped by date and tenor
- Common tenors include 4WK, 8WK, 13WK, 17WK, 26WK, and 52WK
- If `filter[year]` is omitted, defaults to the current year
- Pagination is supported via `page[limit]` and `page[offset]`
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
