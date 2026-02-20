# Investverte ESG List Companies API

Status: complete
Source: marketplace (Investverte API)
Docs: https://eodhd.com/financial-apis/esg-data-api
Provider: Investverte via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/investverte`
Path: `/companies`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns the full list of companies available in the Investverte ESG dataset. Each entry contains a ticker symbol and company name, allowing users to discover which companies have ESG data and obtain the symbol needed to query detailed ESG ratings via the View Company endpoint.

**Use cases**:
- Discover which companies have ESG data available
- Obtain the correct symbol identifier for use with the ESG View Company endpoint
- Build a universe of ESG-rated companies for screening or portfolio construction
- Browse companies across global exchanges (US, HK, KS, KQ, SZ, SS, L, F, T, KL, TW, SA, etc.)

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

JSON array of company objects. Each object contains:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Ticker symbol with exchange suffix (e.g. `"AAPL.US"`, `"000001.SZ"`, `"0439.HK"`) |
| `name` | string | Full company name |

The symbol uses the standard EODHD format `{TICKER}.{EXCHANGE}` and can be passed directly to the ESG View Company endpoint.

## Example Request

```bash
curl "https://eodhd.com/api/mp/investverte/companies?api_token=YOUR_API_TOKEN"
```

## Example Response

```json
[
  {
    "symbol": "000001.SZ",
    "name": "Ping An Bank Co., Ltd."
  },
  {
    "symbol": "000002.SZ",
    "name": "China Vanke Co., Ltd."
  },
  {
    "symbol": "0439.HK",
    "name": "KuangChi Science Limited"
  },
  {
    "symbol": "044340.KQ",
    "name": "Winix Inc."
  },
  {
    "symbol": "ENEL.MI",
    "name": "Enel SpA"
  },
  {
    "symbol": "600600.SS",
    "name": "Tsingtao Brewery Company Limited"
  },
  {
    "symbol": "5285.KL",
    "name": "Sime Darby Plantation Berhad"
  }
]
```

## Notes

- **Marketplace product**: Requires a separate Investverte marketplace subscription, not included in main EODHD plans.
- **Global coverage**: Includes companies from many exchanges worldwide — US, HK, SZ, SS (China), KS/KQ (Korea), T (Japan), KL (Malaysia), TW/TWO (Taiwan), SA (Brazil), L/F (UK/Germany), MI (Italy), ST/HE (Nordics), OL (Norway), WA (Poland), MC (Spain), BO/NS (India), SN (Chile), and more.
- **Symbol format**: Uses standard EODHD `{TICKER}.{EXCHANGE}` format. The symbol value can be used directly with the Investverte ESG View Company endpoint.
- **No pagination parameters**: The endpoint returns the full list in a single response.
- **ESG Data by Investverte** provides detailed ESG ratings, comprehensive company information, and sector-specific analysis for sustainable investment decisions.

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
- Cache responses to reduce API calls — the company list doesn't change frequently
- Monitor your API usage in the user dashboard
