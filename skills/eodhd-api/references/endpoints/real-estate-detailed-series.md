# Real Estate Data API — Detailed Series Catalogue

Status: complete
Source: financial-apis (Real Estate Data API, BIS property prices)
Docs: https://eodhd.com/financial-apis/real-estate-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /real-estate/{code}/detailed/series
Method: GET
Auth: api_token (query)

## Purpose

Returns the catalogue of Detailed Property Prices (DPP) series available for a country — each entry describes one addressable slice of the BIS detailed dataset (covered area, property type, vintage, compiling organisation, priced unit, seasonal adjustment, unit of measure, and a human-readable title). Use this catalogue to discover the dimension codes to pass as `filter[...]` params to `/real-estate/{code}/detailed`. Available in the All-In-One and Fundamentals Data plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| code (path) | Yes | string | ISO 3166-1 alpha-2 country code, case-insensitive (e.g. `US`) |

This is a parameterless catalogue — it takes no query filters, sort, or pagination.

## Response (shape)

```json
{
  "data": [
    {
      "covered_area": "0",
      "covered_area_label": "Whole country",
      "property_type": "1",
      "property_type_label": "All types of dwellings",
      "vintage": "0",
      "vintage_label": "All",
      "compiling_org": "Central bank",
      "priced_unit": "Per dwelling",
      "seasonal_adj": "Not seasonally adjusted",
      "unit_measure": "628",
      "unit_measure_label": "Index, 2010 = 100",
      "title": "Whole country, all dwellings, index 2010=100"
    }
  ],
  "meta": {
    "country_code": "US",
    "total": 24
  }
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| data | array | Array of available DPP series descriptors |
| meta | object | `country_code` and `total` series count |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| covered_area | string | Covered-area dimension code |
| covered_area_label | string | Human-readable covered area |
| property_type | string | Property type code |
| property_type_label | string | Human-readable property type |
| vintage | string | Vintage code |
| vintage_label | string | Human-readable vintage |
| compiling_org | string | Compiling organisation |
| priced_unit | string | Priced unit |
| seasonal_adj | string | Seasonal-adjustment status |
| unit_measure | string | Unit-of-measure code |
| unit_measure_label | string | Human-readable unit of measure |
| title | string | Human-readable series title |

## Example Requests

```bash
# Catalogue of detailed series for the US
curl "https://eodhd.com/api/real-estate/US/detailed/series?api_token=YOUR_TOKEN"

# Using the helper client
python eodhd_client.py --endpoint real-estate/detailed/series --symbol US
```

## Notes

- The path `{code}` is an ISO 3166-1 alpha-2 country code and is case-insensitive (normalised to uppercase). An unknown code returns 404 (`Symbol not found`).
- Response envelope is `{"data", "meta"}` only — there is no `links` object.
- `fmt=csv` is NOT honoured on this endpoint; it always returns JSON.
- The `covered_area` / `property_type` / `vintage` codes here are the exact values to feed into the `filter[area]` / `filter[property_type]` / `filter[vintage]` params of `/real-estate/{code}/detailed`.
- API call consumption: 5 calls per request.
- **Helper client normalization**: the raw API wraps rows in a `{"data", "meta"}` envelope, but
  `eodhd_client.py` unwraps it and returns the bare `data` array (consistent with other list endpoints, so
  `data[-1]` works). Pass `--raw` to see the full envelope with the `meta` count.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **404** | Not Found | Unknown country code (`Symbol not found`). |
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
