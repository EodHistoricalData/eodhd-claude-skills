# Investverte ESG View Country API

Status: complete
Source: marketplace (Investverte API)
Docs: https://eodhd.com/financial-apis/esg-data-api
Provider: Investverte via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/investverte`
Path: `/country/{symbol}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns ESG ratings aggregated at the country level. Provides the mean and
median ESG scores for all companies in a given country, broken down by year
and reporting frequency (full year or quarterly). When called without filters,
returns the full historical time series across all available years and
frequencies.

**Use cases**:
- Track a country's ESG performance over time
- Compare ESG trends across countries
- Analyze quarterly vs annual ESG score fluctuations
- Research geographic ESG patterns for investment strategies
- Benchmark a company's ESG score against its country's average

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
| `symbol` | string | Country code from the List Countries endpoint (e.g. `US`, `GB`, `DE`, `JP`) |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key |

### Query (optional)

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `year` | number | e.g. `2014`, `2021`, `2024` | Filter to a specific year |
| `frequency` | string | `FY`, `Q1`, `Q2`, `Q3`, `Q4` | Filter to a specific reporting frequency |

- `FY` = Full Year
- `Q1`..`Q4` = Quarterly periods
- When both `year` and `frequency` are provided, a single record is returned.
- When neither is provided, the full time series (all years, all frequencies) is returned.

## Response (shape)

JSON array of ESG rating objects. Each object contains:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Country code (e.g. `"US"`) |
| `name` | string | Country name (e.g. `"United States of America"`) |
| `mean` | number | Mean ESG score across all companies in the country for the period |
| `median` | number | Median ESG score across all companies in the country for the period |
| `year` | integer | Year of the data point |
| `frequency` | string | Reporting frequency: `"FY"`, `"Q1"`, `"Q2"`, `"Q3"`, or `"Q4"` |

## Example Requests

### Get all historical ESG data for a country

```bash
curl "https://eodhd.com/api/mp/investverte/country/US?api_token=YOUR_API_TOKEN"
```

### Get ESG data for a specific year and frequency

```bash
curl "https://eodhd.com/api/mp/investverte/country/US?year=2021&frequency=FY&api_token=YOUR_API_TOKEN"
```

### Get ESG data for a specific year (all frequencies)

```bash
curl "https://eodhd.com/api/mp/investverte/country/GB?year=2022&api_token=YOUR_API_TOKEN"
```

## Example Responses

### Filtered by year and frequency (single record)

```json
[
  {
    "symbol": "US",
    "name": "United States of America",
    "mean": 63.2928294103373,
    "median": 63.32,
    "year": 2021,
    "frequency": "FY"
  }
]
```

### Full time series (no filters, truncated)

```json
[
  {
    "symbol": "US",
    "name": "United States of America",
    "mean": 64.40246550347815,
    "median": 64.4,
    "year": 2015,
    "frequency": "FY"
  },
  {
    "symbol": "US",
    "name": "United States of America",
    "mean": 64.22745346472705,
    "median": 64.25,
    "year": 2015,
    "frequency": "Q1"
  },
  {
    "symbol": "US",
    "name": "United States of America",
    "mean": 62.81467922437673,
    "median": 62.8,
    "year": 2016,
    "frequency": "FY"
  },
  {
    "symbol": "US",
    "name": "United States of America",
    "mean": 67.26301903655376,
    "median": 67.54,
    "year": 2022,
    "frequency": "FY"
  },
  {
    "symbol": "US",
    "name": "United States of America",
    "mean": 62.77384615384615,
    "median": 62.49,
    "year": 2024,
    "frequency": "FY"
  }
]
```

## Notes

- **Marketplace product**: Requires a separate Investverte marketplace subscription, not included in main EODHD plans.
- **Data range**: Historical data spans from 2015 to the current year, with both annual (FY) and quarterly (Q1-Q4) breakdowns.
- **Country codes**: Use the two-letter codes from the List Countries endpoint (e.g. `US`, `GB`, `DE`, `JP`, `CN`).
- **Score interpretation**: ESG scores are numeric values (typically in the 50-70 range based on observed US data). Higher scores indicate better ESG performance.
- **Mean vs median**: The `mean` gives the average ESG score across all companies in the country; the `median` gives the middle value, which is less affected by outliers.
- **Full time series**: Without `year`/`frequency` filters, the response includes 5 records per year (FY + Q1-Q4) across all available years — potentially 50+ records.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **404** | Not Found | Country symbol not found. |
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
            print("Error: Country symbol not found.")
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
- Cache responses to reduce API calls — country ESG scores update infrequently
- Monitor your API usage in the user dashboard
