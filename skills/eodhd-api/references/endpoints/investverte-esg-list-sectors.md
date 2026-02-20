# Investverte ESG List Sectors API

Status: complete
Source: marketplace (Investverte API)
Docs: https://eodhd.com/financial-apis/esg-data-api
Provider: Investverte via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/investverte`
Path: `/sectors`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns the full list of sectors available in the Investverte ESG dataset.
Each entry contains a sector name, allowing users to discover which sectors
have ESG data and obtain the sector identifier needed to query sector-level
ESG details via the View Sector endpoint.

**Use cases**:
- Discover which sectors have ESG data available
- Obtain the correct sector name for use with the ESG View Sector endpoint
- Filter or group ESG-rated companies by sector
- Build sector-level ESG analysis for portfolio construction or research

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

## Parameters

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key |

## Response (shape)

JSON array of sector objects. Each object contains:

| Field | Type | Description |
|-------|------|-------------|
| `sector` | string | Sector name (e.g. `"Technology"`, `"Banking"`, `"Healthcare"`) |

## Example Request

```bash
curl "https://eodhd.com/api/mp/investverte/sectors?api_token=YOUR_API_TOKEN"
```

## Example Response

```json
[
  {
    "sector": "Aerospace & Defense"
  },
  {
    "sector": "Banking"
  },
  {
    "sector": "Consumer Cyclical"
  },
  {
    "sector": "Energy"
  },
  {
    "sector": "Healthcare"
  },
  {
    "sector": "Industrials"
  },
  {
    "sector": "Real Estate"
  },
  {
    "sector": "Technology"
  },
  {
    "sector": "Unknown"
  },
  {
    "sector": "Utilities"
  }
]
```

## Notes

- **Marketplace product**: Requires a separate Investverte marketplace subscription, not included in main EODHD plans.
- **53 sectors**: The dataset covers 53 sectors ranging from broad categories (e.g. `Technology`, `Energy`, `Healthcare`) to specific industries (e.g. `Semiconductors`, `Biotechnology`, `Marine`).
- **"Unknown" sector**: Companies that cannot be classified into a specific sector are grouped under `"Unknown"`.
- **No pagination parameters**: The endpoint returns the full list in a single response.
- The `sector` value can be used with the Investverte ESG View Sector endpoint to retrieve sector-level ESG data.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
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
- Cache responses to reduce API calls — the sector list doesn't change frequently
- Monitor your API usage in the user dashboard
