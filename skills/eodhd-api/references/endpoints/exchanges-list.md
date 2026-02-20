# Exchanges List API

Status: complete
Source: financial-apis (Exchanges API)
Docs: https://eodhd.com/financial-apis/exchanges-api-list-of-tickers-and-டrading-hours
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /exchanges-list
Method: GET
Auth: api_token (query)

## Purpose

Fetches a list of all supported stock exchanges with their codes, names, countries,
currencies, and operating hours. Useful for discovering available markets and understanding
exchange metadata before querying market data.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key for authentication |
| fmt | No | string | Output format: 'json' or 'csv'. Defaults to 'json' |

## Response (shape)

```json
[
  {
    "Name": "USA Stocks",
    "Code": "US",
    "OperatingMIC": "XNAS, XNYS, OTCM",
    "Country": "USA",
    "Currency": "USD",
    "CountryISO2": "US",
    "CountryISO3": "USA"
  },
  {
    "Name": "London Exchange",
    "Code": "LSE",
    "OperatingMIC": "XLON",
    "Country": "UK",
    "Currency": "GBP",
    "CountryISO2": "GB",
    "CountryISO3": "GBR"
  },
  {
    "Name": "Government Bonds",
    "Code": "GBOND",
    "OperatingMIC": null,
    "Country": "Unknown",
    "Currency": "Unknown",
    "CountryISO2": "",
    "CountryISO3": ""
  }
]
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| Name | string | Full name of the exchange |
| Code | string | EODHD exchange code (used in symbol suffix) |
| OperatingMIC | string or null | ISO 10383 Market Identifier Code(s). Can be comma-separated for combined exchanges (e.g., `"XNAS, XNYS, OTCM"`), or `null` for virtual exchanges (GBOND, MONEY, EUFUND) |
| Country | string | Country name (or `"Unknown"` for virtual exchanges) |
| Currency | string | Primary trading currency (or `"Unknown"` for virtual exchanges) |
| CountryISO2 | string | ISO 3166-1 alpha-2 country code (empty string for virtual exchanges) |
| CountryISO3 | string | ISO 3166-1 alpha-3 country code (empty string for virtual exchanges) |

### Common Exchange Codes

| Code | Exchange |
|------|----------|
| US | USA Stocks (NYSE, NASDAQ, OTC Markets combined) |
| LSE | London Exchange |
| XETRA | XETRA Stock Exchange (Germany) |
| PA | Euronext Paris |
| TO | Toronto Exchange |
| TW | Taiwan Stock Exchange |
| KO | Korea Stock Exchange |
| SHG | Shanghai Stock Exchange |
| SHE | Shenzhen Stock Exchange |
| AU | Australian Securities Exchange |
| SA | Sao Paulo Exchange (B3) |
| MC | Madrid Exchange |
| AS | Euronext Amsterdam |
| JSE | Johannesburg Exchange |
| FOREX | Forex |
| CC | Cryptocurrencies |
| GBOND | Government Bonds |

## Example Requests

```bash
# List all exchanges
curl "https://eodhd.com/api/exchanges-list?api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint exchanges-list
```

## Notes

- Exchange codes are used as suffixes in symbol identifiers (e.g., `AAPL.US`, `BMW.XETRA`)
- The `US` code combines NYSE, NASDAQ, and AMEX into a single virtual exchange
- MIC codes follow ISO 10383 standard for market identification
- Exchange list is relatively static; cache results when appropriate
- Use exchange codes with `exchange-symbol-list` endpoint to get tickers
- API call consumption: 1 call per request

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

### Error Response Format

For authentication errors (invalid/expired token), the API returns plain text `Unauthenticated` (not JSON). For other errors, the API may return JSON:

```
Unauthenticated
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
