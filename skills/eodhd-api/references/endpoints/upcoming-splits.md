# Historical & Upcoming Splits API

Status: complete
Source: financial-apis (Calendar API)
Docs: https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /calendar/splits
Method: GET
Auth: api_token (query)

## Purpose

Returns historical and upcoming stock splits and reverse splits for selected symbols or a date window. Each item includes the effective split date and the ratio (for example 4:1). Available in All-In-One, Fundamentals Data Feed plans and via "Financial Events (Calendar) & News Feed" plans.

Data available from January 2015 to several months into the future. For full historical data, see the Splits and Dividends API.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| symbols | No | string | Ticker in EODHD format (e.g., TSLA.US) |
| from | Conditional | string (YYYY-MM-DD) | Start of the calendar window. Required if symbols not provided |
| to | Conditional | string (YYYY-MM-DD) | End of the calendar window. Required if symbols not provided |
| fmt | No | string | json or csv (default) |

## Response (shape)

```json
{
  "type": "Splits",
  "description": "Historical and upcoming splits",
  "from": "2025-10-13",
  "to": "2025-10-20",
  "splits": [
    {
      "code": "0698.HK",
      "split_date": "2025-10-13",
      "optionable": "N",
      "old_shares": 50,
      "new_shares": 1
    },
    {
      "code": "1449.TW",
      "split_date": "2025-10-13",
      "optionable": "N",
      "old_shares": 1000,
      "new_shares": 1032
    }
  ]
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| type | string | Constant label of the payload (example: Splits) |
| description | string | Human-readable description of the dataset |
| from | string (YYYY-MM-DD) | Start date of the requested range |
| to | string (YYYY-MM-DD) | End date of the requested range |
| splits | array of objects | List of split records within the range |

**Split record fields:**

| Field | Type | Description |
|-------|------|-------------|
| code | string | Ticker in EODHD format |
| split_date | string (YYYY-MM-DD) | Effective date of the split |
| optionable | string | Indicates if the stock is optionable: "Y" or "N" |
| old_shares | number | Number of old shares before the split |
| new_shares | number | Number of new shares after the split |

### Understanding Split Ratios

- **Forward split**: Each share becomes multiple shares (new_shares > old_shares)
  - Example: old_shares: 1, new_shares: 5 (5-for-1 split)
  - Price divides: $1000 stock becomes $200 after 5-for-1 split

- **Reverse split**: Multiple shares become fewer shares (new_shares < old_shares)
  - Example: old_shares: 65, new_shares: 1 (1-for-65 reverse split)
  - Price multiplies: $2 stock becomes $130 after 1-for-65 reverse split

## Example Requests

```bash
# By symbol with date window (CSV format)
curl "https://eodhd.com/api/calendar/splits?symbols=TSLA.US&from=2010-01-01&to=2030-01-01&api_token=demo"

# By symbol with date window (JSON format)
curl "https://eodhd.com/api/calendar/splits?symbols=TSLA.US&from=2010-01-01&to=2030-01-01&api_token=demo&fmt=json"

# By date window (all symbols)
curl "https://eodhd.com/api/calendar/splits?from=2024-01-01&to=2024-01-03&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint calendar/splits --symbols TSLA.US --from-date 2010-01-01 --to-date 2030-01-01
```

## Notes

- Forward splits (new_shares > old_shares) are more common for high-priced stocks
- Reverse splits (new_shares < old_shares) often indicate struggling companies trying to meet exchange listing requirements
- Historical prices are typically split-adjusted automatically in EOD data
- Use `old_shares`/`new_shares` for split ratio calculations
- Data available from January 2015 to several months into the future
- For full historical data, use the Splits and Dividends API
- When using `symbols` parameter, you can also specify `from` and `to` dates for filtering
- API call consumption: 1 call per request
- **Historical splits before 2015**: The Calendar Splits API was designed primarily for **upcoming** splits. It does not support splits before 2015. For historical split data, use the **Splits and Dividends API** (`/div/{TICKER}` or `/splits/{TICKER}`) or the **EOD Bulk API** with `type=splits`. The Calendar API is recommended for upcoming splits; the other APIs for historical data.
- **Historical splits by exchange**: To download historical splits for an entire exchange, use the Bulk API: https://eodhd.com/knowledgebase/bulk-api-eod-splits-dividends/

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
