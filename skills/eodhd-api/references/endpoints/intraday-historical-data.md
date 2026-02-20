# Intraday Historical Data API

Status: complete
Source: financial-apis (Intraday Historical Data API)
Docs: https://eodhd.com/financial-apis/intraday-historical-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /intraday/{SYMBOL}
Method: GET
Auth: api_token (query)

## Purpose

Fetches intraday historical OHLCV data for a symbol with configurable intervals (1m, 5m, 1h).
Essential for day traders, algorithmic traders, and analysts who need short-term price data
for backtesting strategies, identifying volatility periods, and analyzing rapid market movements.

## Data Availability

### US Stocks (NYSE and NASDAQ)
- **1-minute interval**: Available since 2004, includes pre-market and after-hours trading
- **5-minute and 1-hour intervals**: Available from October 2020

### Other Exchanges
- **5-minute and 1-hour intervals**: Available from October 2020
- **1-minute interval**: May be available depending on ticker and exchange (not guaranteed)

### FOREX & Cryptocurrencies
- **1-minute interval**: Available since 2009
- **5-minute and 1-hour intervals**: Available from October 2020

### Data Updates
- Intraday data is delayed and finalized approximately 2-3 hours after market close
- For US tickers, 1-minute data is updated 2-3 hours after after-hours trading ends

## Time Range Limitations

| Interval | Maximum Range (from → to) |
|----------|---------------------------|
| 1m | 120 days |
| 5m | 600 days |
| 1h | 7200 days |

**Note**: If no `from`/`to` is specified, default is last 120 days.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| {SYMBOL} | Yes | path | Symbol with exchange suffix (e.g., 'AAPL.US', 'AAPL.MX') |
| api_token | Yes | string | Your API key for authentication |
| interval | No | string | Interval: '1m' (1-minute), '5m' (5-minute), '1h' (1-hour). Default: '5m' |
| fmt | No | string | Output format: 'json' or 'csv'. Default: 'json' |
| from | No | integer | Start time as Unix timestamp (UTC) |
| to | No | integer | End time as Unix timestamp (UTC) |
| split-dt | No | integer | If set to 1, splits datetime into separate 'date' and 'time' fields (for Zorro software) |

## Response (shape)

### Standard Response (JSON)

```json
[
  {
    "timestamp": 1627911000,
    "gmtoffset": 0,
    "datetime": "2021-08-02 13:30:00",
    "open": 146.36,
    "high": 146.949996,
    "low": 146.089996,
    "close": 146.419998,
    "volume": 3930530
  },
  {
    "timestamp": 1627911300,
    "gmtoffset": 0,
    "datetime": "2021-08-02 13:35:00",
    "open": 146.449798,
    "high": 146.449798,
    "low": 145.539993,
    "close": 145.580001,
    "volume": 2639916
  }
]
```

### With split-dt=1 (separate date/time fields)

```json
[
  {
    "timestamp": 1627911000,
    "gmtoffset": 0,
    "date": "2021-08-02",
    "time": "13:30:00",
    "open": 146.36,
    "high": 146.949996,
    "low": 146.089996,
    "close": 146.419998,
    "volume": 3930530
  }
]
```

### CSV Response

```csv
Timestamp,Gmtoffset,Datetime,Open,High,Low,Close,Volume
1627911000,0,"2021-08-02 13:30:00",146.36,146.949996,146.089996,146.419998,3930530
1627911300,0,"2021-08-02 13:35:00",146.449798,146.449798,145.539993,145.580001,2639916
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| timestamp | integer | Unix timestamp (UTC) |
| gmtoffset | integer | GMT offset applied (usually 0 for UTC) |
| datetime | string | Timestamp in 'YYYY-MM-DD HH:MM:SS' format (UTC) |
| date | string | Date only (when split-dt=1) |
| time | string | Time only (when split-dt=1) |
| open | number | Opening price of the interval |
| high | number | Highest price within the interval |
| low | number | Lowest price within the interval |
| close | number | Closing price of the interval |
| volume | integer | Trading volume during the interval |

## Example Requests

```bash
# 5-minute bars for AAPL (default interval)
curl "https://eodhd.com/api/intraday/AAPL.US?api_token=demo&fmt=json"

# 1-minute bars
curl "https://eodhd.com/api/intraday/AAPL.US?api_token=demo&fmt=json&interval=1m"

# 1-hour bars
curl "https://eodhd.com/api/intraday/AAPL.US?api_token=demo&fmt=json&interval=1h"

# Specific date range (Unix timestamps)
curl "https://eodhd.com/api/intraday/AAPL.US?api_token=demo&fmt=json&from=1627896900&to=1627916900"

# Split date and time (for Zorro software)
curl "https://eodhd.com/api/intraday/AAPL.US?api_token=demo&fmt=json&from=1627896900&to=1627916900&split-dt=1"

# CSV format
curl "https://eodhd.com/api/intraday/AAPL.US?api_token=demo&fmt=csv&from=1627896900&to=1627916900"

# Using the helper client
python eodhd_client.py --endpoint intraday --symbol AAPL.US --interval 5m
```

## Unix Timestamp Conversion

Example: `from=1627896900&to=1630575300` corresponds to:
- **from**: 2021-08-02 09:35:00 UTC
- **to**: 2021-09-02 09:35:00 UTC

Use online converters or programming languages to convert between dates and Unix timestamps.

## Notes

- **All data is in UTC timezone** - timestamps are Unix format, gmtoffset is typically 0
- **API call consumption**: 5 calls per request
- **Plans required**: EOD+Intraday - All World Extended, All-in-One
- **US stocks**: Include pre-market and after-hours data (for 1m interval)
- **Data finalization**: 2-3 hours after market close
- **Volume**: Actual traded volume for that interval
- **Gaps**: Data may have gaps for low-volume periods or market closures
- **Default range**: Last 120 days if no from/to specified
- **Intraday data is unadjusted**: Prices are not adjusted for splits or dividends. To adjust, use the splits/dividends data (https://eodhd.com/financial-apis/api-splits-dividends) or obtain a coefficient from the EOD API: `k = adjusted_close / close`, then `adjusted_open = open * k`, `adjusted_high = high * k`, `adjusted_low = low * k`. Calculate `k` for **each day** as it changes on every split or dividend. See also the [Data Adjustment Guide](../general/data-adjustment-guide.md).
- **Timestamp meaning**: The timestamp is the **opening** of the candle. The data relates to the interval starting at that timestamp.
- **Missing 1-minute bars**: Pre-market 1-minute data for stocks can have gaps due to low volume. Data within regular market hours is usually complete for top stocks.
- **Null values**: Low-volume stocks that may have no trades for several days can return null values in intraday data.
- **Funds**: Intraday data is available for funds.
- **UTC vs EST offset**: UTC does not observe daylight saving time, but New York does. The difference between UTC and Eastern time is either 5 hours (EST, November–March) or 4 hours (EDT, March–November). Account for this when converting timestamps.
- **1-minute vs 5-minute data sources**: 1-minute and 5-minute data currently come from different sources. 1-minute data comes from the consolidated CTA/UTP feed (aggregated from all US exchanges, including pre/post-market). 5-minute data comes from a single venue. EODHD recommends using **1-minute intervals** as the more comprehensive and precise option.
- **1-minute close vs EOD close**: The daily closing price is formed from the closing auction, while the last 1-minute candle is simply the last candle of the day. These may differ. The Intraday API is not intended for obtaining the official daily close price.
- **CTA/UTP consolidated data**: EODHD uses consolidated data from CTA/UTP feeds, which aggregates data from all US exchanges. Minor discrepancies with other sources may occur if they use data from a single exchange only.

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
