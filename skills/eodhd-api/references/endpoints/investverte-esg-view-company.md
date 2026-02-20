# Investverte ESG View Company API

Status: complete
Source: marketplace (Investverte API)
Docs: https://eodhd.com/financial-apis/esg-data-api
Provider: Investverte via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/investverte`
Path: `/esg/{symbol}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns detailed ESG (Environmental, Social, Governance) ratings for a
specific company. Provides individual E, S, and G pillar scores plus the
composite ESG score, broken down by year and reporting frequency (full year
or quarterly). When called without filters, returns the full historical time
series across all available years and frequencies.

**Use cases**:
- Assess a company's ESG performance across all three pillars
- Track ESG score trends over time (annual and quarterly)
- Compare E, S, G pillar strengths and weaknesses within a company
- Benchmark a company's ESG profile against peers or country/sector averages
- Support ESG-driven investment screening and due diligence

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
| `symbol` | string | Company ticker symbol (e.g. `AAPL`, `MSFT`, `000039.SZ`). Use tickers from the List Companies endpoint. Note: the exchange suffix is included for non-US symbols but omitted for US symbols. |

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
| `e` | number | Environmental pillar score |
| `s` | number | Social pillar score |
| `g` | number | Governance pillar score |
| `esg` | number | Composite ESG score |
| `year` | integer | Year of the data point |
| `frequency` | string | Reporting frequency: `"FY"`, `"Q1"`, `"Q2"`, `"Q3"`, or `"Q4"` |

## Example Requests

### Get all historical ESG data for a US company

```bash
curl "https://eodhd.com/api/mp/investverte/esg/AAPL?api_token=YOUR_API_TOKEN"
```

### Get ESG data for a specific year and frequency

```bash
curl "https://eodhd.com/api/mp/investverte/esg/AAPL?year=2021&frequency=FY&api_token=YOUR_API_TOKEN"
```

### Get ESG data for a non-US company

```bash
curl "https://eodhd.com/api/mp/investverte/esg/000039.SZ?api_token=YOUR_API_TOKEN"
```

## Example Responses

### Filtered by year and frequency (single record)

```json
[
  {
    "e": 58.97,
    "s": 68.66,
    "g": 65.21,
    "esg": 64.09,
    "year": 2021,
    "frequency": "FY"
  }
]
```

### Full time series (no filters, truncated)

```json
[
  {
    "e": 62.26,
    "s": 67.38,
    "g": 66.53,
    "esg": 65.07,
    "year": 2022,
    "frequency": "FY"
  },
  {
    "e": 51.38,
    "s": 68.38,
    "g": 64.61,
    "esg": 60.45,
    "year": 2022,
    "frequency": "Q1"
  },
  {
    "e": 54.65,
    "s": 66.9,
    "g": 65.74,
    "esg": 61.66,
    "year": 2021,
    "frequency": "FY"
  },
  {
    "e": 51.38,
    "s": 68.38,
    "g": 64.61,
    "esg": 60.45,
    "year": 2021,
    "frequency": "Q4"
  },
  {
    "e": 55.84,
    "s": 66.54,
    "g": 64.43,
    "esg": 61.63,
    "year": 2012,
    "frequency": "FY"
  }
]
```

## Notes

- **Marketplace product**: Requires a separate Investverte marketplace subscription, not included in main EODHD plans.
- **Symbol format**: US companies use the bare ticker (e.g. `AAPL`, `MSFT`). Non-US companies include the exchange suffix (e.g. `000039.SZ`, `0439.HK`). Use the List Companies endpoint to get the correct symbol.
- **Data range**: Historical data can span over 10 years (e.g. 2012–2024), varying by company.
- **Quarterly vs annual scores**: Quarterly (Q1-Q4) scores may remain constant between annual updates; the FY score typically reflects updated analysis.
- **Score interpretation**: All scores (E, S, G, ESG) are numeric values typically in the 50-70 range. Higher scores indicate better performance.
- **Pillar scores**: `e` = Environmental, `s` = Social, `g` = Governance. The composite `esg` is derived from all three pillars.
- **Full time series**: Without `year`/`frequency` filters, the response includes 5 records per year (FY + Q1-Q4) across all available years — potentially 50+ records per company.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **404** | Not Found | Company symbol not found. |
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
            print("Error: Company symbol not found.")
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
- Cache responses to reduce API calls — company ESG scores update infrequently
- Monitor your API usage in the user dashboard
