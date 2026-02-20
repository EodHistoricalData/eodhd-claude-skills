# US Live Extended Quotes API (Live v2)

Status: complete
Source: financial-apis (Live Data API)
Docs: https://eodhd.com/financial-apis/live-realtime-stocks-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /us-quote-delayed
Method: GET
Auth: api_token (query)

## Purpose

Returns delayed quote snapshots for one or more US stock symbols. Each quote includes last trade price with event time, full bid/ask with sizes and timestamps, intraday change, rolling averages (50/100/200-day), 52-week extremes, market cap, P/E ratios, dividend data, and issuer reference fields. Batch requests are supported via comma-separated tickers. This is the "Live v2" endpoint, focused on US equities with richer quote-level detail than the Live v1 OHLCV endpoint. Available in All-In-One, EOD Historical Data: All World, EOD + Intraday: All World Extended, and Free plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API access token |
| s | Yes | string | One or more symbols separated by commas (e.g., AAPL.US or AAPL.US,TSLA.US) |
| page[limit] | No | integer | Number of symbols per page (max 100) |
| page[offset] | No | integer | Offset for pagination |
| fmt | No | string | Response format: json (default) or csv |

## Response (shape)

```json
{
  "meta": { "count": 2 },
  "data": {
    "AAPL.US": {
      "symbol": "AAPL.US",
      "exchange": "XNAS",
      "isoExchange": "XNAS",
      "bzExchange": "NASDAQ",
      "otcMarket": "",
      "otcTier": "",
      "type": "STOCK",
      "name": "Apple",
      "companyStandardName": "Apple Inc",
      "description": "Apple Inc. - Common Stock",
      "sector": "Information Technology",
      "industry": "Technology Hardware, Storage & Peripherals",
      "open": 204.505,
      "high": 207.88,
      "low": 201.675,
      "bidPrice": 203.28,
      "bidSize": 4,
      "bidTime": 1754339351000,
      "askPrice": 203.32,
      "askSize": 1,
      "askTime": 1754339341000,
      "size": 7225981,
      "lastTradePrice": 203.32,
      "lastTradeTime": 1754339340000,
      "volume": 73006032,
      "change": 0.94,
      "changePercent": 0.46,
      "previousClosePrice": 202.38,
      "previousCloseDate": "2026-02-12 16:00:00",
      "fiftyDayAveragePrice": 205.28,
      "hundredDayAveragePrice": 206.37,
      "twoHundredDayAveragePrice": 221.53,
      "averageVolume": 48512910,
      "fiftyTwoWeekHigh": 260.1,
      "fiftyTwoWeekLow": 169.2101,
      "marketCap": 3054287882360,
      "sharesOutstanding": 14681140000,
      "sharesFloat": 14672068878,
      "pe": 30.710167,
      "forwardPE": 25.974,
      "dividendYield": 0.51,
      "dividend": 1.04,
      "payoutRatio": 0.1304,
      "ethPrice": 203.32,
      "ethVolume": 8738316,
      "ethTime": 1754339340000,
      "currency": "USD",
      "issuerName": "Apple Inc",
      "primary": true,
      "shortDescription": "Ordinary Shares",
      "issuerShortName": "Apple",
      "timestamp": 1754339340
    },
    "TSLA.US": {
      "symbol": "TSLA.US",
      "exchange": "XNAS",
      "name": "Tesla Inc",
      "lastTradePrice": 245.11,
      "lastTradeTime": 1754339340000,
      "bidPrice": 245.09,
      "askPrice": 245.12,
      "volume": 51234567,
      "change": -1.22,
      "changePercent": -0.49,
      "currency": "USD",
      "timestamp": 1754339340
    }
  },
  "links": { "next": null }
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| meta.count | integer | Number of returned symbols |
| data | object | A per-symbol object keyed by requested symbols |
| links.next | string or null | URL to the next page of results, if available |

**Per-symbol fields (data[symbol]):**

| Field | Type | Description |
|-------|------|-------------|
| symbol | string | Instrument code (e.g., AAPL.US) |
| exchange | string | Exchange MIC code (e.g., XNAS) |
| isoExchange | string | ISO-style exchange identifier |
| bzExchange | string | Human-readable exchange name |
| otcMarket | string or null | OTC market name if applicable |
| otcTier | string or null | OTC market tier if applicable |
| type | string | Instrument type (e.g., STOCK) |
| name | string | Company name |
| companyStandardName | string | Standardized issuer name |
| description | string | Short description of the instrument |
| sector | string | GICS or internal sector mapping |
| industry | string | GICS or internal industry mapping |
| open | float | Session open price |
| high | float | Session high price |
| low | float | Session low price |
| bidPrice | float | Best bid price |
| bidSize | integer | Best bid size |
| bidTime | integer (ms) | Timestamp of last bid update (Unix ms) |
| askPrice | float | Best ask price |
| askSize | integer | Best ask size |
| askTime | integer (ms) | Timestamp of last ask update (Unix ms) |
| size | integer | Last trade size (if provided) |
| lastTradePrice | float | Last trade price |
| lastTradeTime | integer (ms) | Timestamp of last trade (Unix ms) |
| volume | float | Cumulative session volume |
| change | float | Absolute day change vs previous close |
| changePercent | float | Percent day change vs previous close |
| previousClosePrice | float | Previous close price |
| previousCloseDate | string (YYYY-MM-DD HH:MM:SS) | Previous close date and time (UTC) |
| fiftyDayAveragePrice | float | 50-day moving average price |
| hundredDayAveragePrice | float | 100-day moving average price |
| twoHundredDayAveragePrice | float | 200-day moving average price |
| averageVolume | integer | Average daily volume |
| fiftyTwoWeekHigh | float | 52-week high price |
| fiftyTwoWeekLow | float | 52-week low price |
| marketCap | integer | Market capitalization |
| sharesOutstanding | integer | Shares outstanding |
| sharesFloat | integer | Free float shares |
| pe | float | Trailing price-to-earnings ratio |
| forwardPE | float | Forward price-to-earnings ratio |
| dividendYield | float | Dividend yield (percent) |
| dividend | float | Dividend per share (TTM or latest) |
| payoutRatio | float | Dividend payout ratio (percent) |
| ethPrice | float | Extended hours last price (if available) |
| ethVolume | integer | Extended hours volume |
| ethTime | integer (ms) | Extended hours last trade time (Unix ms) |
| currency | string | Trading currency (ISO alpha-3) |
| issuerName | string | Issuer name |
| primary | boolean | Whether this is the primary listing |
| shortDescription | string | Short instrument description |
| issuerShortName | string | Short issuer name |
| timestamp | integer (s) | Snapshot timestamp (Unix seconds) |

## Example Requests

```bash
# Single symbol quote
curl "https://eodhd.com/api/us-quote-delayed?s=AAPL.US&api_token=YOUR_TOKEN&fmt=json"

# Multiple symbols in one request
curl "https://eodhd.com/api/us-quote-delayed?s=AAPL.US,TSLA.US,MSFT.US&api_token=YOUR_TOKEN&fmt=json"

# With pagination
curl "https://eodhd.com/api/us-quote-delayed?s=AAPL.US,TSLA.US&api_token=YOUR_TOKEN&page[limit]=50&page[offset]=0&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint us-quote-delayed --symbol AAPL.US

# Multiple symbols via helper client
python eodhd_client.py --endpoint us-quote-delayed --symbol AAPL.US,TSLA.US,MSFT.US
```

## Notes

- API call consumption: 1 API call per ticker in the request
- Quotes are delayed (exchange-compliant), not real-time
- Batch requests supported via comma-separated symbols (max 100 per page)
- JSON is the default format; CSV is also supported via `fmt=csv`
- The `data` field is an object keyed by symbol, not an array
- Extended hours fields (`ethPrice`, `ethVolume`, `ethTime`) are available when pre/post-market data exists
- Timestamps: `bidTime`, `askTime`, `lastTradeTime`, `ethTime` are in Unix milliseconds; `timestamp` is in Unix seconds
- **Live v2 vs Live v1**: Live v2 (this endpoint) provides quote-level detail (bid/ask, trade timestamps, fundamentals) for US stocks. Live v1 (`/real-time/{symbol}`) provides minute OHLCV bars across multiple asset classes without bid/ask or trade event timestamps

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
