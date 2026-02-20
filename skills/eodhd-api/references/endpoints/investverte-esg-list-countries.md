# Investverte ESG List Countries API

Status: complete
Source: marketplace (Investverte API)
Docs: https://eodhd.com/financial-apis/esg-data-api
Provider: Investverte via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/investverte`
Path: `/countries`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns the full list of countries available in the Investverte ESG dataset. Each entry contains a two-letter country code and a country name, allowing users to discover which countries have ESG data and obtain the code needed to query country-level ESG details via the View Country endpoint.

**Use cases**:
- Discover which countries have ESG data available
- Obtain the correct country code for use with the ESG View Country endpoint
- Filter or group ESG-rated companies by country
- Build geographic views of ESG coverage for research or portfolio construction

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

JSON array of country objects. Each object contains:

| Field | Type | Description |
|-------|------|-------------|
| `country_code` | string | Two-letter country code (generally ISO 3166-1 alpha-2, with some special codes) |
| `country_descr` | string | Human-readable country name |

### Special codes

| Code | Meaning |
|------|---------|
| `XX` | Not Recognized - Emerging |
| `XZ` | Not Recognized - Developed |

### Note on encoding

Some country names contain XML-encoded characters (e.g. `_x002C_` for commas, `_x0028_`/`_x0029_` for parentheses, `_x002F_` for slashes). These should be decoded when displaying to users.

## Example Request

```bash
curl "https://eodhd.com/api/mp/investverte/countries?api_token=YOUR_API_TOKEN"
```

## Example Response

```json
[
  {
    "country_code": "AD",
    "country_descr": "Andorra"
  },
  {
    "country_code": "AE",
    "country_descr": "United Arab Emirates"
  },
  {
    "country_code": "BR",
    "country_descr": "Brazil"
  },
  {
    "country_code": "CN",
    "country_descr": "China"
  },
  {
    "country_code": "DE",
    "country_descr": "Germany"
  },
  {
    "country_code": "GB",
    "country_descr": "United Kingdom"
  },
  {
    "country_code": "JP",
    "country_descr": "Japan"
  },
  {
    "country_code": "US",
    "country_descr": "United States of America"
  },
  {
    "country_code": "XX",
    "country_descr": "Not Recognized - Emerging"
  },
  {
    "country_code": "ZA",
    "country_descr": "South Africa"
  }
]
```

## Notes

- **Marketplace product**: Requires a separate Investverte marketplace subscription, not included in main EODHD plans.
- **Broad coverage**: Covers 170+ countries and territories worldwide, from major economies (US, GB, JP, CN, DE) to smaller territories (GI, GG, JE, IM, etc.).
- **Country codes**: Generally follow ISO 3166-1 alpha-2 standard. Two non-standard codes exist: `XX` (Not Recognized - Emerging) and `XZ` (Not Recognized - Developed) for companies that cannot be mapped to a specific country.
- **XML-encoded characters**: Some `country_descr` values contain XML entity references (e.g. `Congo_x002C_ The Democratic Republic of the`, `Croatia _x0028_Hrvatska_x0029_`). These should be decoded for display.
- **No pagination parameters**: The endpoint returns the full list in a single response.
- The `country_code` value can be used with the Investverte ESG View Country endpoint to retrieve country-level ESG data.

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
- Cache responses to reduce API calls — the country list doesn't change frequently
- Monitor your API usage in the user dashboard
