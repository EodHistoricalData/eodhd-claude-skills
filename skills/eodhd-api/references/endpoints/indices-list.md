# List of Indices with Details API

Status: complete
Source: marketplace (Indices Historical Constituents Data API)
Docs: https://eodhd.com/financial-apis/indices-constituents-api
Provider: EODHD (via Unicorn Bay / S&P Global)
Base URL: https://eodhd.com/api
Path: /mp/unicornbay/spglobal/list
Method: GET
Auth: api_token (query)

## Purpose
Return end-of-day essential details for 100+ indices: Global S&P and Dow Jones
Indexes, including S&P 500, 600, 100, 400, and 21 Key Industry indices with
fields such as Value, Market Cap, Divisor, Daily Return, Adjusted Market Cap
and more. Data is sourced from S&P Global and structured in JSON format.

## Parameters
- Required:
  - api_token: EODHD API key.
- Optional:
  - fmt: "json" (default and only supported format).

## Response (shape)
JSON array of index objects. Each object contains:
- ID: string - full index identifier (e.g. "GSPC.INDX").
- Code: string - short index code (e.g. "GSPC").
- Name: string - human-readable index name (e.g. "S&P 500").
- Constituents: integer - number of current constituents.
- Value: number - current index value.
- MarketCap: number or null - total market cap.
- Divisor: number or null - index divisor.
- DailyReturn: number - daily return as a decimal (e.g. -0.0043).
- Dividend: number or null - dividend value.
- AdjustedMarketCap: number or null - adjusted market cap.
- AdjustedDivisor: number or null - adjusted divisor.
- AdjustedConstituents: integer - adjusted number of constituents.
- CurrencyCode: string - ISO currency code (e.g. "USD", "ILS", "CAD", "JPY").
- CurrencyName: string - full currency name (e.g. "US Dollar").
- CurrencySymbol: string - currency symbol (e.g. "$").
- LastUpdate: string - date of last update in YYYY-MM-DD format.

## Example request
```bash
curl "https://eodhd.com/api/mp/unicornbay/spglobal/list?fmt=json&api_token=YOUR_API_KEY"
```

## Example response
```json
[
  {
    "ID": "GSPC.INDX",
    "Code": "GSPC",
    "Name": "S&P 500",
    "Constituents": 502,
    "Value": 21947.6275,
    "MarketCap": 9953830971.3261,
    "Divisor": 453526.5125,
    "DailyReturn": -0.0043,
    "Dividend": 0.9391,
    "AdjustedMarketCap": 9953830971.3261,
    "AdjustedDivisor": 453526.5125,
    "AdjustedConstituents": 502,
    "CurrencyCode": "USD",
    "CurrencyName": "US Dollar",
    "CurrencySymbol": "$",
    "LastUpdate": "2026-02-13"
  },
  {
    "ID": "DJI.INDX",
    "Code": "DJI",
    "Name": "Dow Jones Industrial Average",
    "Constituents": 30,
    "Value": 49500.9288,
    "MarketCap": 8040.22,
    "Divisor": 0.1624,
    "DailyReturn": 0.001,
    "Dividend": null,
    "AdjustedMarketCap": 8040.22,
    "AdjustedDivisor": 0.1624,
    "AdjustedConstituents": 30,
    "CurrencyCode": "USD",
    "CurrencyName": "US Dollar",
    "CurrencySymbol": "$",
    "LastUpdate": "2026-02-13"
  }
]
```

## Notes
- This is a Marketplace product: 1 API request = 10 API calls.
- Limits: 100,000 API calls per 24 hours; 1,000 API requests per minute.
- Only JSON format is supported.
- Covers 100+ indices including S&P 500, S&P 600, S&P 100, S&P 400, and
  21 key industry indices, plus Dow Jones Industrial, Transportation,
  Utility, and Composite averages.
- Indices are available in multiple currencies (USD, CAD, ILS, JPY) and
  variants (Price, Total Return, Net Total Return, Hedged).
- The ID field (e.g. "GSPC.INDX") is used as the symbol parameter for the
  Index Components endpoint.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **403** | Forbidden | Access denied. Check your subscription. |
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
