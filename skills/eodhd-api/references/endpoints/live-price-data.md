# Live/Real-Time Price Data API

Status: complete
Source: financial-apis (Live Stock Prices API)
Docs: https://eodhd.com/financial-apis/live-realtime-stocks-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /real-time/{SYMBOL}
Method: GET
Auth: api_token (query)

## Purpose
Return real-time (delayed 15-20 minutes for most exchanges) quote data
for a symbol including last price, change, volume, and trading range.

## Parameters
- Required:
  - api_token: EODHD API key
  - {SYMBOL}: Symbol with exchange suffix (e.g., AAPL.US)
- Optional:
  - fmt: csv or json (default csv)
  - s: Additional symbols for batch request (comma-separated)
  - ex: Set to `US` to fetch aggregated live data for all U.S. exchanges in a single request (consumes 100 API calls)

## Response (shape)
Single quote object or array for batch requests:

```json
{
  "code": "AAPL",
  "timestamp": 1609459200,
  "gmtoffset": -18000,
  "open": 132.43,
  "high": 134.50,
  "low": 131.80,
  "close": 133.72,
  "volume": 98425000,
  "previousClose": 131.96,
  "change": 1.76,
  "change_p": 1.33
}
```

For batch requests with `s` parameter:
```json
[
  {"code": "AAPL", "close": 133.72, ...},
  {"code": "MSFT", "close": 222.42, ...}
]
```

## Example request
```bash
# Single symbol real-time quote
curl "https://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json"

# Batch request for multiple symbols
curl "https://eodhd.com/api/real-time/AAPL.US?s=MSFT.US,GOOGL.US&api_token=demo&fmt=json"

# Bulk request for all US exchanges (consumes 100 API calls)
curl "https://eodhd.com/api/real-time/AAPL.US?ex=US&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint real-time --symbol AAPL.US
```

## Notes
- Data is delayed 15-20 minutes for most exchanges (real-time requires premium)
- `change` is absolute price change from previous close
- `change_p` is percentage change from previous close
- Timestamp is Unix epoch in seconds
- During market hours, data updates frequently; after hours shows last traded
- Batch requests support up to 15-20 symbols per call
- Works for stocks, ETFs, indices, forex, and crypto (exchange-dependent)
- API call consumption: 1 call per ticker in the request (e.g., 10 symbols = 10 calls)
- **Premarket data**: This API only works during trading hours. For pre-market and after-hours data, use the WebSockets API.
- **"Close" is the live price**: In this API, the `close` field represents the current live price during market hours.
- **Bulk live (real-time) API**: Add `ex=US` to the URL to fetch aggregated live data for all U.S. exchanges in a single request. Only available for US exchanges. Consumes **100 API calls** per request. Available in: All-In-One, EOD Historical Data: All World, EOD+Intraday: All World Extended, and Free plans.
- **Mutual funds live data**: Live data is not available for mutual funds. Mutual fund prices do not change during the day (see OHLC data for mutual funds). The live API's "current" price for mutual funds is updated at end of day — same as EOD data.

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
