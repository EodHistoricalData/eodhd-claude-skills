# US Options Contracts API

Status: complete
Source: marketplace (US Stock Options Data API by Unicornbay)
Docs: https://eodhd.com/financial-apis/us-stock-options-data-api
Provider: EODHD Marketplace
Base URL: https://eodhd.com/api
Path: /mp/unicornbay/options/contracts
Method: GET
Auth: api_token (query)

## Purpose

Fetches a list of options contracts based on various filters such as underlying symbol,
expiration dates, strike price range, and contract type (call or put). Includes current
pricing, Greeks, volume, open interest, and 40+ fields of options data. Covers 6,000+
US tickers with 2-year history and 1.5M daily bid/ask/trade events.

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
| fields[options-contracts] | No | string | Comma-separated list of fields to include |

## Response (shape)

```json
{
  "meta": {
    "offset": 0,
    "limit": 2,
    "total": 19058,
    "fields": ["contract", "underlying_symbol", "exp_date", "type", "strike", "..."]
  },
  "data": [
    {
      "id": "AAPL270115C00450000",
      "type": "options-contracts",
      "attributes": {
        "contract": "AAPL270115C00450000",
        "underlying_symbol": "AAPL",
        "exp_date": "2027-01-15",
        "expiration_type": "monthly",
        "type": "call",
        "strike": 450,
        "exchange": "NASDAQ",
        "currency": "USD",
        "open": 0.95,
        "high": 1.00,
        "low": 0.89,
        "last": 0.89,
        "last_size": 1,
        "change": -0.03,
        "pctchange": -3.26,
        "previous": 0.92,
        "previous_date": "2026-02-06",
        "bid": 0.89,
        "bid_date": "2026-02-06 20:59:59",
        "bid_size": 37,
        "ask": 0.92,
        "ask_date": "2026-02-06 20:59:59",
        "ask_size": 17,
        "moneyness": -0.62,
        "volume": 180,
        "volume_change": 95,
        "volume_pctchange": 111.76,
        "open_interest": 16229,
        "open_interest_change": 2,
        "open_interest_pctchange": 0.01,
        "volatility": 0.2445,
        "volatility_change": -0.0042,
        "volatility_pctchange": -1.69,
        "theoretical": 0.89,
        "delta": 0.036776,
        "gamma": 0.001221,
        "theta": -0.008551,
        "vega": 0.216526,
        "rho": 0.087534,
        "tradetime": "2026-02-06",
        "vol_oi_ratio": 0.01,
        "dte": 342,
        "midpoint": 0.91
      }
    }
  ],
  "links": {
    "next": "https://eodhd.com/api/mp/unicornbay/options/contracts?...&page[offset]=2"
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| contract | string | OCC contract identifier (SYMBOL + YYMMDD + C/P + strike*1000) |
| underlying_symbol | string | Underlying stock ticker |
| exp_date | string (date) | Expiration date (YYYY-MM-DD) |
| expiration_type | string | Expiration type: 'monthly', 'weekly', 'quarterly' |
| type | string | Contract type: 'call' or 'put' |
| strike | number | Strike price |
| exchange | string | Exchange (e.g., 'NASDAQ') |
| currency | string | Currency (e.g., 'USD') |
| open | number | Opening price |
| high | number | High price |
| low | number | Low price |
| last | number | Last traded price |
| last_size | integer | Size of last trade |
| change | number | Price change from previous |
| pctchange | number | Percentage change |
| previous | number | Previous day's close |
| previous_date | string | Date of previous close |
| bid | number | Current bid price |
| bid_date | string | Timestamp of bid |
| bid_size | integer | Bid size |
| ask | number | Current ask price |
| ask_date | string | Timestamp of ask |
| ask_size | integer | Ask size |
| moneyness | number | Moneyness ratio (negative = OTM, positive = ITM) |
| volume | integer | Trading volume |
| volume_change | integer | Volume change from previous |
| volume_pctchange | number | Volume percentage change |
| open_interest | integer | Open interest |
| open_interest_change | integer | OI change from previous |
| open_interest_pctchange | number | OI percentage change |
| volatility | number | Implied volatility |
| volatility_change | number | IV change |
| volatility_pctchange | number | IV percentage change |
| theoretical | number | Theoretical option price |
| delta | number | Delta Greek |
| gamma | number | Gamma Greek |
| theta | number | Theta Greek (time decay) |
| vega | number | Vega Greek (volatility sensitivity) |
| rho | number | Rho Greek (interest rate sensitivity) |
| tradetime | string (date) | Date of last market activity |
| vol_oi_ratio | number | Volume/Open Interest ratio |
| dte | integer | Days to expiration |
| midpoint | number | Midpoint of bid/ask |

## Example Requests

```bash
# All options contracts for AAPL
curl "https://eodhd.com/api/mp/unicornbay/options/contracts?filter[underlying_symbol]=AAPL&api_token=demo&page[limit]=10"

# Specific contract
curl "https://eodhd.com/api/mp/unicornbay/options/contracts?filter[contract]=AAPL270115C00450000&api_token=demo"

# AAPL puts with strike $450 expiring on specific date
curl "https://eodhd.com/api/mp/unicornbay/options/contracts?filter[underlying_symbol]=AAPL&filter[strike_eq]=450&filter[type]=put&filter[exp_date_eq]=2027-01-15&api_token=demo"

# Calls with strikes between $120-$130
curl "https://eodhd.com/api/mp/unicornbay/options/contracts?filter[underlying_symbol]=AAPL&filter[type]=call&filter[strike_from]=120&filter[strike_to]=130&api_token=demo"

# Sorted by expiration date descending, specific fields only
curl "https://eodhd.com/api/mp/unicornbay/options/contracts?filter[underlying_symbol]=AAPL&sort=-exp_date&fields[options-contracts]=contract,bid_date,open,high,low,last&page[limit]=5&api_token=demo"
```

## Notes

- **Marketplace Product**: This is a marketplace API (path: `/mp/unicornbay/...`)
- **Coverage**: 6,000+ US tickers, 1.5M daily events, 2-year history
- **Tradetime field**: May represent actual trade or last bid/ask update - check volume > 0 to confirm actual trade
- **Null values**: Some fields return null if data unavailable
- **Pagination**: Max 10,000 offset, 1,000 results per page
- **Sorting**: Use '-' prefix for descending order (e.g., '-exp_date')
- **API call consumption**: 1 request = 10 API calls
- **Rate limits**: 100,000 calls/24h, 1,000 requests/minute

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
