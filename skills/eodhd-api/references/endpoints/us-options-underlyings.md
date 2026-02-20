# US Options Underlying Symbols API

Status: complete
Source: marketplace (US Stock Options Data API by Unicornbay)
Docs: https://eodhd.com/financial-apis/us-stock-options-data-api
Provider: EODHD Marketplace
Base URL: https://eodhd.com/api
Path: /mp/unicornbay/options/underlying-symbols
Method: GET
Auth: api_token (query)

## Purpose

Retrieves a list of all US stock tickers for which options data is available. Returns
the complete universe of supported underlying symbols for the options API. Essential for
discovering which stocks have options coverage before making contract or EOD data requests.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key for authentication |

## Response (shape)

```json
{
  "meta": {
    "total": 6479,
    "fields": ["underlying_symbol"],
    "compact": true
  },
  "data": [
    "A",
    "AA",
    "AAAU",
    "AACT",
    "AADI",
    "AAL",
    "AAMI",
    "AAN",
    "AAOI",
    "AAON",
    "AAP",
    "AAPB",
    "AAPD",
    "AAPL",
    "AAPU",
    "AAPW",
    "AAPX",
    "AAPY",
    "..."
  ],
  "links": {
    "next": null
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| meta.total | integer | Total number of supported underlying symbols |
| meta.fields | array | Fields included in response |
| meta.compact | boolean | Response is in compact format |
| data | array | List of ticker symbols with options data |
| links.next | string/null | URL for next page (null if all data returned) |

## Example Requests

```bash
# Get all underlying symbols with options data
curl "https://eodhd.com/api/mp/unicornbay/options/underlying-symbols?api_token=demo"
```

## Response Details

The API returns a flat array of ticker symbols in compact format. Each symbol in the `data` array
represents a US stock that has options contracts available through the options API.

### Sample Coverage (6,479 tickers as of 2026)

Common symbols include:
- **Tech Giants**: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
- **ETFs**: SPY, QQQ, IWM, EEM, XLF, GLD, TLT
- **Financials**: JPM, BAC, GS, MS, C, WFC
- **Healthcare**: JNJ, PFE, UNH, MRK, ABBV
- **Energy**: XOM, CVX, COP, SLB, OXY
- **Industrials**: BA, CAT, GE, HON, UPS

## Use Cases

1. **Symbol Validation**: Check if a ticker has options data before querying contracts
2. **Coverage Discovery**: Find all available tickers for options analysis
3. **Universe Building**: Build a watchlist of optionable stocks
4. **Integration**: Validate user input against supported symbols

## Example Workflow

```bash
# Step 1: Get list of supported symbols
curl "https://eodhd.com/api/mp/unicornbay/options/underlying-symbols?api_token=YOUR_TOKEN"

# Step 2: Query contracts for a supported symbol
curl "https://eodhd.com/api/mp/unicornbay/options/contracts?filter[underlying_symbol]=AAPL&api_token=YOUR_TOKEN"

# Step 3: Get historical EOD for specific contract
curl "https://eodhd.com/api/mp/unicornbay/options/eod?filter[contract]=AAPL270115C00150000&api_token=YOUR_TOKEN"
```

## Notes

- **Coverage**: 6,000+ US tickers with options data
- **Marketplace Product**: This is a marketplace API (path: `/mp/unicornbay/...`)
- **Compact Format**: Response is always in compact array format
- **Complete List**: Returns all symbols in a single response (no pagination needed typically)
- **Update Frequency**: Symbol list updated as new options become available
- **API call consumption**: 1 request = 10 API calls
- **Rate limits**: 100,000 calls/24h, 1,000 requests/minute
- **Caching**: Symbol list is relatively stable; cache results when appropriate

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
