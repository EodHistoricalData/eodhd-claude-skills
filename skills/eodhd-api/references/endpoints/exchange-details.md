# Exchange Details API (Trading Hours, Stock Market Holidays)

Status: complete
Source: financial-apis
Provider: EODHD
Base URL: `https://eodhd.com/api`
Path: `/exchange-details/{EXCHANGE_CODE}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Get detailed information about a specific exchange, including:

- **Timezone** — the timezone of the exchange
- **isOpen** — boolean indicating if the exchange is open right now or closed
- **Trading hours and working days** — open/close hours in exchange timezone (may include lunch hours)
- **Exchange holidays** — official and bank holidays (6 months back and 6 months forward by default)
- **Early close days** — days when the exchange closes early
- **ActiveTickers** — tickers with any activity for the past two months
- **UpdatedTickers** — tickers updated for the current day
- **PreviousDayUpdatedTickers** — tickers updated the previous day

## Plans & API Calls

- **Available in**: All-In-One, EOD+Intraday — All World Extended plans
- **API call consumption**: 5 API calls per ticker (per request)

## Parameters

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key |

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `EXCHANGE_CODE` | string | Exchange code (e.g., `US`, `LSE`, `XETRA`) |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `from` | string | 6 months before today | Start date for holidays (`YYYY-MM-DD`) |
| `to` | string | 6 months after today | End date for holidays (`YYYY-MM-DD`) |
| `fmt` | string | `csv` | Response format: `json` or `csv` |

## Response (shape)

```json
{
  "Name": "USA Stocks",
  "Code": "US",
  "OperatingMIC": "XNAS, XNYS, OTCM",
  "Country": "USA",
  "Currency": "USD",
  "Timezone": "America/New_York",
  "isOpen": true,
  "TradingHours": {
    "Open": "09:30:00",
    "Close": "16:00:00",
    "OpenUTC": "14:30:00",
    "CloseUTC": "21:00:00",
    "WorkingDays": "Mon,Tue,Wed,Thu,Fri"
  },
  "ExchangeHolidays": {
    "0": {
      "Holiday": "Labour Day",
      "Date": "2025-09-01",
      "Type": "official"
    },
    "1": {
      "Holiday": "Thanksgiving Day",
      "Date": "2025-11-27",
      "Type": "official"
    }
  },
  "ExchangeEarlyCloseDays": {},
  "ActiveTickers": 49762,
  "PreviousDayUpdatedTickers": 48278,
  "UpdatedTickers": 0
}
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | Full exchange name |
| `Code` | string | Exchange short code |
| `OperatingMIC` | string | Market Identifier Code(s) |
| `Country` | string | Country of the exchange |
| `Currency` | string | Primary trading currency |
| `Timezone` | string | Exchange timezone (IANA format) |
| `isOpen` | boolean | Whether the exchange is currently open |
| `TradingHours` | object | Open/close times in local and UTC |
| `TradingHours.Open` | string | Market open time (local timezone, `HH:MM:SS`) |
| `TradingHours.Close` | string | Market close time (local timezone, `HH:MM:SS`) |
| `TradingHours.OpenUTC` | string | Market open time (UTC, `HH:MM:SS`) |
| `TradingHours.CloseUTC` | string | Market close time (UTC, `HH:MM:SS`) |
| `TradingHours.WorkingDays` | string | Comma-separated trading days |
| `ExchangeHolidays` | object | Map of holidays with name, date, and type |
| `ExchangeHolidays.*.Holiday` | string | Holiday name |
| `ExchangeHolidays.*.Date` | string | Holiday date (`YYYY-MM-DD`) |
| `ExchangeHolidays.*.Type` | string | Holiday type: `official` or `bank` |
| `ExchangeEarlyCloseDays` | object | Map of early close days (same structure as holidays) |
| `ActiveTickers` | integer | Tickers with activity in past 2 months |
| `PreviousDayUpdatedTickers` | integer | Tickers updated previous day |
| `UpdatedTickers` | integer | Tickers updated today |

### Holiday Types

| Type | Description |
|------|-------------|
| `official` | Official market holiday — exchange fully closed |
| `bank` | Bank holiday — some countries (e.g., UK) have these; exchange may still operate |

## Example Requests

### Get exchange details with default holiday range

```bash
curl "https://eodhd.com/api/exchange-details/US?api_token=YOUR_API_TOKEN&fmt=json"
```

### Get exchange details with custom holiday date range

```bash
curl "https://eodhd.com/api/exchange-details/US?api_token=YOUR_API_TOKEN&fmt=json&from=2017-01-01&to=2021-01-01"
```

### Python client

```bash
python eodhd_client.py --endpoint exchanges-details --symbol US
```

### Python (requests)

```python
import requests

url = "https://eodhd.com/api/exchange-details/US"
params = {
    "api_token": "YOUR_API_TOKEN",
    "fmt": "json"
}
response = requests.get(url, params=params)
data = response.json()

# Check if exchange is open
print(f"Exchange open: {data['isOpen']}")
print(f"Trading hours: {data['TradingHours']['Open']} - {data['TradingHours']['Close']}")
print(f"Active tickers: {data['ActiveTickers']}")

# List upcoming holidays
for key, holiday in data['ExchangeHolidays'].items():
    print(f"  {holiday['Date']}: {holiday['Holiday']} ({holiday['Type']})")
```

## Notes

- Exchange holidays default to 6 months back and 6 months forward from the current date
- Use `from` and `to` parameters to query historical or future holiday data
- Holiday types: `official` (exchange fully closed) and `bank` (varies by country)
- `TradingHours` may include lunch hours for exchanges that have trading breaks (e.g., some Asian markets)
- `isOpen` reflects the real-time status at the time of the API call
- All exchanges supported by EODHD are available through this endpoint

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
