# US Options EOD (End-of-Day) API

Status: complete
Source: marketplace (US Stock Options Data API by Unicornbay)
Docs: https://eodhd.com/financial-apis/us-stock-options-data-api
Provider: EODHD Marketplace
Base URL: https://eodhd.com/api
Path: /mp/unicornbay/options/eod
Method: GET
Auth: api_token (query)

## Purpose

Returns all available end-of-day (EOD) trades or bid data for stock options contracts.
Provides historical daily snapshots including trade timestamps, prices, volumes, bid/ask prices,
Greeks, and contract details. Useful for analyzing daily performance, building historical
volatility surfaces, and backtesting options strategies.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key for authentication |
| filter[contract] | No | string | Filter by specific contract name (e.g., 'AAPL270115P00450000') |
| filter[underlying_symbol] | No | string | Filter by underlying stock symbol (e.g., 'AAPL') |
| filter[exp_date_eq] | No | string (YYYY-MM-DD) | Filter contracts expiring on exact date |
| filter[exp_date_from] | No | string (YYYY-MM-DD) | Filter contracts expiring from date onwards |
| filter[exp_date_to] | No | string (YYYY-MM-DD) | Filter contracts expiring up to date |
| filter[tradetime_eq] | No | string (YYYY-MM-DD) | Filter by exact trade time date |
| filter[tradetime_from] | No | string (YYYY-MM-DD) | Filter by trade time from date onwards |
| filter[tradetime_to] | No | string (YYYY-MM-DD) | Filter by trade time up to date |
| filter[type] | No | string | Contract type: 'put' or 'call' |
| filter[strike_eq] | No | number | Filter by exact strike price |
| filter[strike_from] | No | number | Filter by strike price from value onwards |
| filter[strike_to] | No | number | Filter by strike price up to value |
| sort | No | string | Sort order: 'exp_date', 'strike', '-exp_date', '-strike' |
| page[offset] | No | integer | Pagination offset (default: 0, max: 10000) |
| page[limit] | No | integer | Results per page (default: 1000, max: 1000) |
| fields[options-eod] | No | string | Comma-separated list of fields to include |
| compact | No | boolean | Enable compact mode (1=true) to minimize response size |

## Response (shape)

### Normal Mode

```json
{
  "meta": {
    "offset": 0,
    "limit": 5,
    "total": 355,
    "fields": ["contract", "underlying_symbol", "exp_date", "..."]
  },
  "data": [
    {
      "id": "AAPL270115P00450000-2026-02-06",
      "type": "options-eod",
      "attributes": {
        "contract": "AAPL270115P00450000",
        "underlying_symbol": "AAPL",
        "exp_date": "2027-01-15",
        "expiration_type": "monthly",
        "type": "put",
        "strike": 450,
        "exchange": "NASDAQ",
        "currency": "USD",
        "open": 0,
        "high": 0,
        "low": 0,
        "last": 245.9,
        "last_size": 0,
        "change": 0,
        "pctchange": 0,
        "previous": 0,
        "previous_date": null,
        "bid": 170.2,
        "bid_date": "2026-02-06 21:00:01",
        "bid_size": 11,
        "ask": 173.3,
        "ask_date": "2026-02-06 21:00:01",
        "ask_size": 111,
        "moneyness": 0.62,
        "volume": 0,
        "volume_change": 0,
        "volume_pctchange": 0,
        "open_interest": 0,
        "open_interest_change": 0,
        "open_interest_pctchange": 0,
        "volatility": 0,
        "volatility_change": 0,
        "volatility_pctchange": 0,
        "theoretical": 0,
        "delta": 0,
        "gamma": 0,
        "theta": 0,
        "vega": 0,
        "rho": 0,
        "tradetime": "2025-06-08",
        "vol_oi_ratio": 0,
        "dte": 342,
        "midpoint": 171.75
      }
    }
  ],
  "links": {
    "next": "https://eodhd.com/api/mp/unicornbay/options/eod?...&page[offset]=5"
  }
}
```

### Compact Mode (compact=1)

Returns data as arrays without field names to minimize response size:

```json
{
  "meta": {
    "fields": ["contract", "exp_date", "strike", "bid", "ask", "..."]
  },
  "data": [
    ["AAPL270115P00450000", "2027-01-15", 450, 170.2, 173.3, ...]
  ]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| contract | string | OCC contract identifier |
| underlying_symbol | string | Underlying stock ticker |
| exp_date | string (date) | Expiration date |
| expiration_type | string | 'monthly', 'weekly', 'quarterly' |
| type | string | 'call' or 'put' |
| strike | number | Strike price |
| exchange | string | Exchange code |
| currency | string | Currency (USD) |
| open | number | Opening price for the day |
| high | number | High price for the day |
| low | number | Low price for the day |
| last | number | Last traded price |
| last_size | integer | Size of last trade |
| change | number | Price change |
| pctchange | number | Percentage change |
| previous | number | Previous close |
| previous_date | string | Previous close date |
| bid | number | EOD bid price |
| bid_date | string | Bid timestamp |
| bid_size | integer | Bid size |
| ask | number | EOD ask price |
| ask_date | string | Ask timestamp |
| ask_size | integer | Ask size |
| moneyness | number | Moneyness ratio |
| volume | integer | Daily volume |
| volume_change | integer | Volume change |
| volume_pctchange | number | Volume % change |
| open_interest | integer | Open interest |
| open_interest_change | integer | OI change |
| open_interest_pctchange | number | OI % change |
| volatility | number | Implied volatility |
| volatility_change | number | IV change |
| volatility_pctchange | number | IV % change |
| theoretical | number | Theoretical price |
| delta | number | Delta Greek |
| gamma | number | Gamma Greek |
| theta | number | Theta Greek |
| vega | number | Vega Greek |
| rho | number | Rho Greek |
| tradetime | string (date) | Last market activity date |
| vol_oi_ratio | number | Volume/OI ratio |
| dte | integer | Days to expiration |
| midpoint | number | Bid/ask midpoint |

## Example Requests

```bash
# Historical EOD data for specific contract
curl "https://eodhd.com/api/mp/unicornbay/options/eod?filter[contract]=AAPL270115P00450000&page[limit]=5&sort=-exp_date&api_token=demo"

# EOD data with specific fields
curl "https://eodhd.com/api/mp/unicornbay/options/eod?filter[contract]=AAPL270115P00450000&fields[options-eod]=contract,bid_date,open,high,low,last&page[limit]=100&api_token=demo"

# EOD data in compact mode (reduced response size)
curl "https://eodhd.com/api/mp/unicornbay/options/eod?filter[underlying_symbol]=AAPL&filter[type]=call&compact=1&page[limit]=100&api_token=demo"

# Filter by tradetime range
curl "https://eodhd.com/api/mp/unicornbay/options/eod?filter[underlying_symbol]=AAPL&filter[tradetime_from]=2025-01-01&filter[tradetime_to]=2025-01-31&api_token=demo"
```

## Notes

- **Marketplace Product**: This is a marketplace API (path: `/mp/unicornbay/...`)
- **Historical Data**: Returns daily snapshots - each record represents one day's EOD data
- **ID Format**: `{contract}-{date}` (e.g., 'AAPL270115P00450000-2026-02-06')
- **Compact Mode**: Use `compact=1` to reduce response size for high-volume requests
- **Zero Values**: Greeks and volatility may be zero for illiquid contracts
- **Pagination**: Max 10,000 offset, 1,000 results per page
- **API call consumption**: 1 request = 10 API calls
- **Rate limits**: 100,000 calls/24h, 1,000 requests/minute
- **History**: 2-year historical depth available

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
