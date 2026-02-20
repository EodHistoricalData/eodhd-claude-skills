# Investverte ESG View Sector API

Status: complete
Source: marketplace (Investverte API)
Docs: https://eodhd.com/financial-apis/esg-data-api
Provider: Investverte via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/investverte`
Path: `/sector/{symbol}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns ESG score time series for a specific sector, along with the parent
industry group for comparison. The response provides arrays of ESG scores
aligned to a `years` array of time period labels (`YYYY-FY` or `YYYY-Q#`),
covering both annual and quarterly data from 2015 onwards.

**Use cases**:
- Track a sector's ESG score trend over time
- Compare a sector's ESG performance to its parent industry group
- Identify which periods have data gaps (null values)
- Research sector-level ESG patterns for investment strategies
- Benchmark a company's ESG score against its sector average

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Sector name from the List Sectors endpoint (e.g. `Airlines`, `Technology`, `Banking`). URL-encode names with special characters (e.g. `Aerospace%20%26%20Defense`). |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key |

## Response (shape)

JSON object with three top-level fields:

| Field | Type | Description |
|-------|------|-------------|
| `find` | boolean | `true` if the sector was found, `false` otherwise |
| `industry` | object | ESG score arrays keyed by sector/industry name |
| `years` | array of strings | Time period labels aligned to the score arrays |

### `industry` object

Contains one or more keys, each mapping to an array of numbers (or `null`).
The keys are **sub-industries** and **related industry groups** within the
queried sector. For example:

- Querying `Airlines` returns keys like `"Airlines"` and `"Transportation"`.
- Querying `Technology` returns sub-industry keys like `"Software—Infrastructure"`, `"Semiconductors"`, `"Electronic Components"`, etc.
- Querying `Aerospace & Defense` returns keys like `"Capital Goods"` and `"Scientific & Technical Instruments"`.

Each array has the same length as the `years` array. Values are:
- A number (ESG score) when data is available for that period.
- `null` when no data is available for that period.

### `years` array

Strings in the format `"YYYY-FY"` or `"YYYY-Q#"` where `#` is 1-4. Example entries:
- `"2015-FY"` — Full year 2015
- `"2015-Q1"` — First quarter 2015
- `"2024-Q4"` — Fourth quarter 2024

The array covers all periods from 2015 to the current year, with 5 entries per year (FY + Q1-Q4).

## Example Request

```bash
curl "https://eodhd.com/api/mp/investverte/sector/Airlines?api_token=YOUR_API_TOKEN"
```

### URL-encoded sector name

```bash
curl "https://eodhd.com/api/mp/investverte/sector/Aerospace%20%26%20Defense?api_token=YOUR_API_TOKEN"
```

## Example Response

```json
{
  "find": true,
  "industry": {
    "Airlines": [
      77.46, 77.46, 77.46, 77.46, 77.46,
      77.46, 77.46, 77.46, 77.46, 77.46,
      77.46, 77.46, 77.46, 77.46, 77.46,
      77.46, 77.46, 77.46, 77.46, 77.46,
      77.46, 77.46, 77.46, 77.46, 77.46,
      77.46, 77.46, 77.46, 77.46, 77.46,
      77.46, 77.46, 77.46, 77.46, 77.46,
      null, 77.46, 77.46, null, null,
      null, null, null, null, null,
      null, null, null, null, null,
      null, null, null, null, null
    ],
    "Transportation": [
      65.23, null, null, null, null,
      62.84, null, null, null, null,
      63.98, null, null, null, null,
      63.06, null, null, null, null,
      62.59, null, null, null, null,
      60.2, null, null, null, null,
      61.53, null, null, null, null,
      67.66, null, null, null, null,
      null, null, null, null, null,
      null, null, null, null, null,
      null, null, null, null, null
    ]
  },
  "years": [
    "2015-FY", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4",
    "2016-FY", "2016-Q1", "2016-Q2", "2016-Q3", "2016-Q4",
    "2017-FY", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4",
    "2018-FY", "2018-Q1", "2018-Q2", "2018-Q3", "2018-Q4",
    "2019-FY", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4",
    "2020-FY", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4",
    "2021-FY", "2021-Q1", "2021-Q2", "2021-Q3", "2021-Q4",
    "2022-FY", "2022-Q1", "2022-Q2", "2022-Q3", "2022-Q4",
    "2023-FY", "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
    "2024-FY", "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
    "2025-FY", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4"
  ]
}
```

## Notes

- **Marketplace product**: Requires a separate Investverte marketplace subscription, not included in main EODHD plans.
- **Response format differs from other Investverte endpoints**: Unlike the View Company and View Country endpoints (which return arrays of flat records), this endpoint returns a structured object with parallel arrays.
- **Sub-industries**: The `industry` object keys are sub-industries and related groups within the queried sector. Simple sectors like `Airlines` may return the sector itself plus a parent group (e.g. `Transportation`). Broader sectors like `Technology` return many sub-industries (e.g. `Semiconductors`, `Software—Application`, etc.).
- **Null values**: `null` entries indicate no data is available for that time period. Quarterly data may have more nulls than annual (FY) data.
- **Score interpretation**: ESG scores are numeric values (typically in the 50-80 range). Higher scores indicate better ESG performance.
- **URL encoding**: Sector names containing spaces or special characters must be URL-encoded in the path (e.g. `Hotels%2C%20Restaurants%20%26%20Leisure`).
- **Data alignment**: To map scores to periods, zip the `industry[sector_name]` array with the `years` array — they are always the same length.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **404** | Not Found | Sector symbol not found. |
| **429** | Too Many Requests | Rate limit exceeded (1,000 req/min or 100,000 calls/24h). |

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
        if e.response.status_code == 401:
            print("Error: Invalid API key. Check your credentials.")
        elif e.response.status_code == 403:
            print("Error: No access to Investverte marketplace product.")
        elif e.response.status_code == 404:
            print("Error: Sector not found.")
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
- Cache responses to reduce API calls — sector ESG scores update infrequently
- Monitor your API usage in the user dashboard
