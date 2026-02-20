# Exchange Symbol List API

Status: complete
Source: financial-apis (Exchanges API)
Docs: https://eodhd.com/financial-apis/exchanges-api-list-of-tickers-and-trading-hours
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /exchange-symbol-list/{EXCHANGE}
Method: GET
Auth: api_token (query)

## Purpose

Fetches the complete list of ticker symbols available on a specific exchange, including
symbol codes, names, countries, exchanges, currencies, and instrument types. Useful for
discovering tradable instruments and building symbol universes.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| {EXCHANGE} | Yes | path | Exchange code (e.g., 'US', 'LSE', 'XETRA') |
| api_token | Yes | string | Your API key for authentication |
| fmt | No | string | Output format: 'json' or 'csv'. Defaults to 'json' |

## Response (shape)

```json
[
  {
    "Code": "AAPL",
    "Name": "Apple Inc",
    "Country": "USA",
    "Exchange": "NASDAQ",
    "Currency": "USD",
    "Type": "Common Stock",
    "Isin": "US0378331005"
  },
  {
    "Code": "MSFT",
    "Name": "Microsoft Corporation",
    "Country": "USA",
    "Exchange": "NASDAQ",
    "Currency": "USD",
    "Type": "Common Stock",
    "Isin": "US5949181045"
  },
  {
    "Code": "SPY",
    "Name": "SPDR S&P 500 ETF Trust",
    "Country": "USA",
    "Exchange": "NYSE ARCA",
    "Currency": "USD",
    "Type": "ETF",
    "Isin": "US78462F1030"
  }
]
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| Code | string | Ticker symbol |
| Name | string | Company or instrument name |
| Country | string | Country of incorporation/listing |
| Exchange | string | Specific exchange within the market |
| Currency | string | Trading currency |
| Type | string | Instrument type (see below) |
| Isin | string/null | International Securities Identification Number |

### Instrument Types

| Type | Description |
|------|-------------|
| Common Stock | Regular equity shares |
| ETF | Exchange Traded Fund |
| FUND | Mutual fund |
| Preferred Stock | Preferred equity shares |
| REIT | Real Estate Investment Trust |
| Bond | Fixed income security |
| Index | Market index |
| Currency | Foreign exchange pair |
| Cryptocurrency | Digital currency |

## Example Requests

```bash
# All US tickers
curl "https://eodhd.com/api/exchange-symbol-list/US?api_token=demo&fmt=json"

# London Stock Exchange tickers
curl "https://eodhd.com/api/exchange-symbol-list/LSE?api_token=demo&fmt=json"

# Frankfurt (XETRA) tickers
curl "https://eodhd.com/api/exchange-symbol-list/XETRA?api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint exchange-symbol-list --symbol US
```

## Notes

- Full symbol format: `{Code}.{EXCHANGE}` (e.g., `AAPL.US`, `BMW.XETRA`)
- US exchange includes NYSE, NASDAQ, and AMEX (8000+ symbols)
- Large exchanges may return thousands of symbols
- `Type` field helps filter by instrument category
- `Isin` provides cross-reference to international databases
- Some symbols may be delisted but still in historical data
- API call consumption: 1 call per request
- Consider caching results as symbol lists don't change frequently

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
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
