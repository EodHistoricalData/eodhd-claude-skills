# US Treasury Long-Term Rates API

Status: complete
Source: financial-apis (US Treasury API)
Docs: https://eodhd.com/financial-apis/us-treasury-interest-rates-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /ust/long-term-rates
Method: GET
Auth: api_token (query)

## Purpose

Provides long-term Treasury rates. This feed combines "Daily Treasury Real Long-Term Rate Averages" and "Daily Treasury Long-Term Rates" into one dataset. Rate types include BC_20year, Over_10_Years, and Real_Rate. Used for macro research, fixed-income analytics, discounting/cost of capital, and building risk-free rate baselines. Available in All-In-One, EOD Historical Data: All World, EOD + Intraday: All World Extended, and Free plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[year] | No | integer | Filter by year (1900 – current year + 1). If not mentioned – current year |

## Response (shape)

```json
{
  "meta": {
    "total": 60
  },
  "data": [
    {
      "date": "2026-01-02",
      "rate_type": "BC_20year",
      "rate": 4.81,
      "extrapolation_factor": null
    },
    {
      "date": "2026-01-02",
      "rate_type": "Over_10_Years",
      "rate": 4.78,
      "extrapolation_factor": null
    },
    {
      "date": "2026-01-02",
      "rate_type": "Real_Rate",
      "rate": 2.55,
      "extrapolation_factor": null
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
| data | array | Array of long-term rate records |
| links | object | Pagination links (next page URL or null) |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| date | string (YYYY-MM-DD) | Observation date |
| rate_type | string | Rate series identifier (BC_20year, Over_10_Years, Real_Rate) |
| rate | number | Rate value |
| extrapolation_factor | number or null | Extrapolation factor where applicable |

## Example Requests

```bash
# Long-term rates for 2020
curl "https://eodhd.com/api/ust/long-term-rates?api_token=YOUR_TOKEN&filter[year]=2020"

# Long-term rates for current year
curl "https://eodhd.com/api/ust/long-term-rates?api_token=YOUR_TOKEN"

# Using the helper client
python eodhd_client.py --endpoint ust/long-term-rates --filter-year 2020
```

## Notes

- Returns three rate types per observation date: BC_20year, Over_10_Years, and Real_Rate
- BC_20year: Treasury 20-year constant maturity rate
- Over_10_Years: Composite rate over 10-year maturity
- Real_Rate: Real long-term rate average
- If `filter[year]` is omitted, defaults to the current year
- The extrapolation_factor field may be null for most records
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
