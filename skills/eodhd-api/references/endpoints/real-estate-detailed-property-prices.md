# Real Estate Data API — Detailed Property Prices (DPP)

Status: complete
Source: financial-apis (Real Estate Data API, BIS property prices)
Docs: https://eodhd.com/financial-apis/real-estate-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /real-estate/{code}/detailed
Method: GET
Auth: api_token (query)

## Purpose

Returns the Detailed Property Prices (DPP) observations for a country — the granular national residential property price series from the BIS detailed dataset. Each series is described by dimensions such as covered area, property type, vintage, frequency, and unit of measure, letting you drill into a specific slice of a country's housing market. Underlying data is sourced from the Bank for International Settlements (BIS). Use `/real-estate/{code}/detailed/series` first to discover which dimension codes are available. Available in the All-In-One and Fundamentals Data plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| code (path) | Yes | string | ISO 3166-1 alpha-2 country code, case-insensitive (e.g. `AE`) |
| filter[area] | No | string | BIS covered-area dimension code |
| filter[property_type] | No | string | Property type code |
| filter[vintage] | No | string | Vintage code |
| filter[freq] | No | string | Frequency: `Q`, `A`, `M`, `H` |
| filter[from] | No | string | Period lower bound; format follows series frequency (e.g. `2020-01` or `2020-Q1`) |
| filter[to] | No | string | Period upper bound; format follows series frequency |
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
      "value": 112.4,
      "frequency": "Q",
      "covered_area": "0",
      "covered_area_label": "Whole country",
      "property_type": "1",
      "property_type_label": "All types of dwellings",
      "vintage": "0",
      "vintage_label": "All",
      "unit_measure": "628",
      "unit_measure_label": "Index, 2010 = 100"
    }
  ],
  "meta": {
    "country_code": "AE",
    "source": "BIS",
    "dataset": "DPP",
    "total": 96,
    "offset": 0,
    "limit": 50,
    "filters": {
      "property_type": "1"
    }
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
| data | array | Array of DPP observations |
| meta | object | Series metadata, applied filters, and pagination |
| links | object | Pagination links (next page URL or null) |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| period | string | Observation period (format follows series frequency) |
| value | number | Series value |
| frequency | string | Series frequency (`Q`, `A`, `M`, `H`) |
| covered_area | string | Covered-area dimension code |
| covered_area_label | string | Human-readable covered area |
| property_type | string | Property type code |
| property_type_label | string | Human-readable property type |
| vintage | string | Vintage code |
| vintage_label | string | Human-readable vintage |
| unit_measure | string | Unit-of-measure code |
| unit_measure_label | string \| null | Human-readable unit of measure (may be null) |

**Meta fields:** `country_code`, `source`, `dataset`, `total`, `offset`, `limit`, `filters`.

## Example Requests

```bash
# Detailed prices for the UAE, property type 1
curl "https://eodhd.com/api/real-estate/AE/detailed?api_token=YOUR_TOKEN&filter[property_type]=1"

# Quarterly whole-country series since 2020
curl "https://eodhd.com/api/real-estate/AE/detailed?api_token=YOUR_TOKEN&filter[freq]=Q&filter[from]=2020-Q1"

# Using the helper client
python eodhd_client.py --endpoint real-estate/detailed --symbol AE --re-property-type 1
```

## Notes

- The path `{code}` is an ISO 3166-1 alpha-2 country code and is case-insensitive (normalised to uppercase). An unknown code returns 404 (`Symbol not found`).
- Discover valid `filter[area]` / `filter[property_type]` / `filter[vintage]` codes via `/real-estate/{code}/detailed/series` (see `references/endpoints/real-estate-detailed-series.md`).
- All data-item fields are strings except `value`; `*_label` fields are human-readable and `unit_measure_label` may be null.
- `fmt=csv` is supported on this endpoint.
- With the helper client, `--symbol` carries the country `{code}`; `--re-area`, `--re-property-type`, `--re-vintage`, `--re-freq`, `--re-from`, `--re-to` map to the corresponding `filter[...]` params.
- API call consumption: 5 calls per request.
- **Helper client normalization**: the raw API wraps rows in a `{"data", "meta", "links"}` envelope, but
  `eodhd_client.py` unwraps it and returns the bare `data` array (consistent with other list endpoints, so
  `data[-1]` works). Pass `--raw` to see the full envelope with `meta` (dataset, source, applied filters) and `links`.

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
