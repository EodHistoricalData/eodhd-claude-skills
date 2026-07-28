# Real Estate Data API — Selected Property Prices (SPP)

Status: complete
Source: financial-apis (Real Estate Data API, BIS property prices)
Docs: https://eodhd.com/financial-apis/real-estate-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /real-estate/{code}
Method: GET
Auth: api_token (query)

## Purpose

Returns the Selected Property Prices (SPP) series for a country — the BIS headline, harmonised residential property price series. The series is available as a nominal or real (inflation-adjusted) index, and as an index level or year-on-year percentage change. Underlying data is sourced from the Bank for International Settlements (BIS). Use this for cross-country comparable housing-market trends. Available in the All-In-One and Fundamentals Data plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| code (path) | Yes | string | ISO 3166-1 alpha-2 country code, case-insensitive (e.g. `US`) |
| filter[type] | No | string | Price type: `nominal`, `real` |
| filter[metric] | No | string | Metric: `index`, `yoy` |
| filter[from] | No | string | Period lower bound, format `YYYY-Qn` (e.g. `2020-Q1`) |
| filter[to] | No | string | Period upper bound, format `YYYY-Qn` (e.g. `2024-Q4`) |
| sort | No | string | Sort order: `period`, `-period`, `value`, `-value` |
| fmt | No | string | Output format: `json` (default) or `csv` |
| page[limit] | No | integer | Results per page, 1–500 (default 50; > 500 returns 422) |
| page[offset] | No | integer | Pagination offset, min 0 (default 0) |

## Response (shape)

```json
{
  "data": [
    {
      "period": "2024-Q1",
      "value": 158.3,
      "type": "real",
      "metric": "index"
    },
    {
      "period": "2024-Q2",
      "value": 159.1,
      "type": "real",
      "metric": "index"
    }
  ],
  "meta": {
    "country_code": "US",
    "country_name": "United States",
    "type": "real",
    "metric": "index",
    "base_year": "2010",
    "frequency": "Q",
    "source": "BIS",
    "total": 120,
    "from": "1995-Q1",
    "to": "2024-Q2",
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
| data | array | Array of SPP observations |
| meta | object | Series metadata + pagination |
| links | object | Pagination links (next page URL or null) |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| period | string | Observation period (`YYYY-Qn`) |
| value | number | Index level or year-on-year percentage change |
| type | string | Price type: `nominal` or `real` |
| metric | string | Metric: `index` or `yoy` |

**Meta fields:** `country_code`, `country_name`, `type`, `metric`, `base_year`, `frequency`, `source`, `total`, `from`, `to`, `offset`, `limit`.

## Example Requests

```bash
# Real index series for the US
curl "https://eodhd.com/api/real-estate/US?api_token=YOUR_TOKEN&filter[type]=real&filter[metric]=index"

# Nominal year-on-year change since 2020
curl "https://eodhd.com/api/real-estate/US?api_token=YOUR_TOKEN&filter[type]=nominal&filter[metric]=yoy&filter[from]=2020-Q1"

# Using the helper client
python eodhd_client.py --endpoint real-estate --symbol US --re-type real --re-metric index
```

## Notes

- The path `{code}` is an ISO 3166-1 alpha-2 country code and is case-insensitive (normalised to uppercase). An unknown code returns 404 (`Symbol not found`).
- `filter[from]` / `filter[to]` use the quarterly period format `YYYY-Qn`.
- `fmt=csv` is supported on this endpoint.
- With the helper client, `--symbol` carries the country `{code}`, and `--re-from` / `--re-to` map to `filter[from]` / `filter[to]`.
- API call consumption: 5 calls per request.
- **Helper client normalization**: the raw API wraps rows in a `{"data", "meta", "links"}` envelope, but
  `eodhd_client.py` unwraps it and returns the bare `data` array (consistent with other list endpoints, so
  `data[-1]` works). Pass `--raw` to see the full envelope with `meta` (base_year, frequency, source) and `links`.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **404** | Not Found | Unknown country code (`Symbol not found`). |
| **422** | Unprocessable Entity | Invalid filter key or `page[limit]` above 500. |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

### Error Response Format

When an error occurs, the API returns a JSON response with error details:

```json
{
  "error": "Error message description",
  "code": 404
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
