# Real Estate Data API — Covered Countries

Status: complete
Source: financial-apis (Real Estate Data API, BIS property prices)
Docs: https://eodhd.com/financial-apis/real-estate-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /real-estate/countries
Method: GET
Auth: api_token (query)

## Purpose

Lists the countries covered by the Real Estate Data API and which datasets each country carries — Selected Property Prices (SPP, headline harmonised residential index) and/or Detailed Property Prices (DPP, granular national series). Underlying data is sourced from the Bank for International Settlements (BIS) residential property price statistics. Use this endpoint to discover coverage before querying a specific country. Available in the All-In-One and Fundamentals Data plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| sort | No | string | Sort order: `code`, `-code`, `name`, `-name` |
| fmt | No | string | Output format: `json` (default) or `csv` |
| page[limit] | No | integer | Results per page, 1–500 (default 50; > 500 returns 422) |
| page[offset] | No | integer | Pagination offset, min 0 (default 0) |

## Response (shape)

```json
{
  "data": [
    {
      "code": "US",
      "name": "United States",
      "has_spp": true,
      "has_dpp": true
    },
    {
      "code": "AE",
      "name": "United Arab Emirates",
      "has_spp": true,
      "has_dpp": true
    }
  ],
  "meta": {
    "total": 60,
    "offset": 0,
    "limit": 50
  },
  "links": {
    "next": null
  }
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| data | array | Array of covered-country records |
| meta | object | Pagination metadata (total, offset, limit) |
| links | object | Pagination links (next page URL or null) |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| code | string | ISO 3166-1 alpha-2 country code |
| name | string | Country name |
| has_spp | boolean | Country carries Selected Property Prices (SPP) data |
| has_dpp | boolean | Country carries Detailed Property Prices (DPP) data |

## Example Requests

```bash
# All covered countries
curl "https://eodhd.com/api/real-estate/countries?api_token=YOUR_TOKEN&fmt=json"

# Sorted by name, first 20
curl "https://eodhd.com/api/real-estate/countries?api_token=YOUR_TOKEN&sort=name&page[limit]=20"

# Using the helper client
python eodhd_client.py --endpoint real-estate/countries --limit 20
```

## Notes

- Country codes are ISO 3166-1 alpha-2 and case-insensitive (normalised to uppercase).
- `has_spp` / `has_dpp` tell you which of the two per-country endpoints will return data.
- `fmt=csv` is supported on this endpoint.
- API call consumption: 5 calls per request.
- **Helper client normalization**: the raw API wraps rows in a `{"data", "meta", "links"}` envelope, but
  `eodhd_client.py` unwraps it and returns the bare `data` array (consistent with other list endpoints, so
  `data[-1]` works). Pass `--raw` to see the full envelope with `meta`/`links` pagination info.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **422** | Unprocessable Entity | Invalid filter key or `page[limit]` above 500. |
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
