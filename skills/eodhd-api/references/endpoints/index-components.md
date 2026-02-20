# Index Components API

Status: complete
Source: marketplace (Indices Historical Constituents Data API)
Docs: https://eodhd.com/financial-apis/indices-constituents-api
Provider: EODHD (via Unicorn Bay / S&P Global)
Base URL: https://eodhd.com/api
Path: /mp/unicornbay/spglobal/comp/{symbol}
Method: GET
Auth: api_token (query)

## Purpose
Return the current list of components for each of the 100+ indices from the
"List of Indices with Details" endpoint. For 30 major S&P and Dow Jones indices,
the endpoint offers 2-12 years of historical changes, marking each addition and
exclusion of a component with the corresponding date. For minor indices, data
completeness varies.

## Parameters
- Required:
  - symbol: index ID from the List of Indices endpoint (e.g. "GSPC.INDX").
    Placed in the URL path.
  - api_token: EODHD API key.
- Optional:
  - fmt: "json" (default and only supported format).

## Response (shape)
JSON object with three top-level sections:

### General
- Code: string - short index code (e.g. "GSPC").
- Type: string - always "INDEX".
- Name: string - full index name (e.g. "S&P 500 Index").
- Exchange: string - always "INDX".
- MarketCap: number - total market cap of the index.
- CurrencyCode: string - ISO currency code (e.g. "USD").
- CurrencyName: string - full currency name (e.g. "US Dollar").
- CurrencySymbol: string - currency symbol (e.g. "$").
- CountryName: string - country name (e.g. "USA") or "Unknown".
- CountryISO: string - ISO country code (e.g. "US") or "NA".
- OpenFigi: string or null - OpenFIGI identifier.

### Components
Object keyed by sequential string indices ("0", "1", ...). Each entry:
- Code: string - ticker symbol (e.g. "AAPL").
- Exchange: string - exchange code (e.g. "US").
- Name: string - company name.
- Sector: string or null - sector classification.
- Industry: string or null - industry classification.
- Weight: number or null - component weight in the index.

### HistoricalTickerComponents
Object keyed by sequential string indices ("0", "1", ...). Each entry:
- Code: string - ticker symbol.
- Name: string - company name.
- StartDate: string or null - date added to the index (YYYY-MM-DD).
- EndDate: string or null - date removed from the index (YYYY-MM-DD), null if still active.
- IsActiveNow: integer - 1 if the company is currently part of the index, 0 otherwise.
- IsDelisted: integer - 1 if the company is no longer traded in general, 0 otherwise.

## Example request
```bash
curl "https://eodhd.com/api/mp/unicornbay/spglobal/comp/GSPC.INDX?fmt=json&api_token=YOUR_API_KEY"
```

## Example response
```json
{
  "General": {
    "Code": "GSPC",
    "Type": "INDEX",
    "Name": "S&P 500 Index",
    "Exchange": "INDX",
    "MarketCap": 58416977484403.47,
    "CurrencyCode": "USD",
    "CurrencyName": "US Dollar",
    "CurrencySymbol": "$",
    "CountryName": "USA",
    "CountryISO": "US",
    "OpenFigi": "BBG000H4FSM0"
  },
  "Components": {
    "0": {
      "Code": "AAPL",
      "Exchange": "US",
      "Name": "Apple Inc",
      "Sector": "Technology",
      "Industry": "Consumer Electronics",
      "Weight": null
    },
    "1": {
      "Code": "MSFT",
      "Exchange": "US",
      "Name": "Microsoft Corporation",
      "Sector": "Technology",
      "Industry": "Software - Infrastructure",
      "Weight": null
    }
  },
  "HistoricalTickerComponents": {
    "0": {
      "Code": "AAPL",
      "Name": "Apple Inc",
      "StartDate": "1982-11-30",
      "EndDate": null,
      "IsActiveNow": 1,
      "IsDelisted": 0
    },
    "1": {
      "Code": "AAL",
      "Name": "American Airlines Group",
      "StartDate": "2015-03-23",
      "EndDate": "2024-09-23",
      "IsActiveNow": 0,
      "IsDelisted": 0
    }
  }
}
```

## Notes
- This is a Marketplace product: 1 API request = 10 API calls.
- Limits: 100,000 API calls per 24 hours; 1,000 API requests per minute.
- Only JSON format is supported.
- The symbol parameter value comes from the ID field of the List of Indices
  endpoint (e.g. "GSPC.INDX", "DJI.INDX", "SPSIAD.INDX").
- IsActiveNow indicates whether the company is still part of the index.
- IsDelisted indicates whether the company is still being traded in general.
- For 30 major S&P and DJ indices, historical data spans 2-12 years.
- EODHD users with access to Fundamental data (All-in-one & Fundamental data
  plans) can also access the same Index Components data via the Fundamental
  endpoint: /api/fundamentals/{symbol}?api_token={EODToken}

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **403** | Forbidden | Access denied. Check your subscription. |
| **404** | Not Found | Index symbol not found. Check the symbol parameter. |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

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
            print("Error: Access denied. Check your subscription.")
        elif e.response.status_code == 404:
            print("Error: Index symbol not found.")
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
