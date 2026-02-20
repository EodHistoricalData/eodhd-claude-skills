# Historical & Upcoming IPOs API

Status: complete
Source: financial-apis (Calendar API)
Docs: https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /calendar/ipos
Method: GET
Auth: api_token (query)

## Purpose

Returns historical and upcoming IPOs in a date window. Items may include filing/amended dates, expected or effective first trading date, price range or offer price, and share count. The response supports JSON (recommended for full field coverage). Available in All-In-One, Fundamentals Data Feed plans and via "Financial Events (Calendar) & News Feed" plans.

Data available from January 2015 and up to 2-3 weeks into the future.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| from | No | string (YYYY-MM-DD) | Start date of the query window. Default: today. This parameter uses start of a trade |
| to | No | string (YYYY-MM-DD) | End date of the query window. Default: today + 7 days. This parameter uses start of a trade |
| fmt | No | string | json or csv (default) |

## Response (shape)

```json
{
  "type": "IPOs",
  "description": "Historical and upcoming IPOs",
  "from": "2018-12-02",
  "to": "2018-12-06",
  "ipos": [
    {
      "code": "603629.SHG",
      "name": "Jiangsu Lettall Electronic Co Ltd",
      "exchange": "Shanghai",
      "currency": "CNY",
      "start_date": "2018-12-11",
      "filing_date": "2017-06-15",
      "amended_date": "2018-12-03",
      "price_from": 0,
      "price_to": 0,
      "offer_price": 0,
      "shares": 25000000,
      "deal_type": "Expected"
    },
    {
      "code": "SPK.MC",
      "name": "Solarpack Corporacion Tecnologica S.A",
      "exchange": "MCE",
      "currency": "EUR",
      "start_date": "2018-12-03",
      "filing_date": "2018-11-05",
      "amended_date": "2018-11-20",
      "price_from": 0,
      "price_to": 0,
      "offer_price": 0,
      "shares": 0,
      "deal_type": "Expected"
    }
  ]
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| type | string | Constant label of the payload (example: IPOs) |
| description | string | Human-readable description of the dataset |
| from | string (YYYY-MM-DD) | Start date used for the query |
| to | string (YYYY-MM-DD) | End date used for the query |
| ipos | array of objects | List of IPO records for the window |

**IPO record fields:**

| Field | Type | Description |
|-------|------|-------------|
| code | string | Ticker in EODHD format |
| name | string or null | Company name |
| exchange | string or null | Listing exchange |
| currency | string or null | Trading currency |
| start_date | string (YYYY-MM-DD) or null | Expected/effective first trading date (if known) |
| filing_date | string (YYYY-MM-DD) or null | Initial filing date |
| amended_date | string (YYYY-MM-DD) or null | Latest amended filing date |
| price_from | number | Lower end of indicated price range (0 if not provided) |
| price_to | number | Upper end of indicated price range (0 if not provided) |
| offer_price | number | Final priced offer (0 if not priced yet) |
| shares | number | Shares offered (0 if not provided) |
| deal_type | string | Lifecycle state such as Filed, Expected, Amended, Priced |

## Example Requests

```bash
# IPOs for default window (today + 7 days)
curl "https://eodhd.com/api/calendar/ipos?api_token=demo&fmt=json"

# IPOs for specific date range
curl "https://eodhd.com/api/calendar/ipos?from=2018-12-02&to=2018-12-06&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint calendar/ipos --from-date 2026-02-10 --to-date 2026-02-17
```

## Notes

- Numbers may be 0 when the value is unknown or not yet set (for example before pricing)
- `start_date` may be null for filings without a scheduled first trading date
- Use `deal_type` to track lifecycle changes (for example, Amended or Priced updates)
- Deal type values include: Filed, Expected, Amended, Priced
- `offer_price` is 0 until the IPO is priced (usually day before or day of listing)
- `price_from` and `price_to` represent the expected pricing range from prospectus
- Data available from January 2015 and up to 2-3 weeks into the future
- API call consumption: 1 call per request
- **N/A on upcoming IPOs**: A `n/a` value for the ticker code means the future ticker was not yet known when the entry was added. Some filed IPOs never become listed (e.g., a company may file but never get approved). To find the actual ticker code for a successful IPO, use the company name from this API to look it up via the **Search API**.
- **Bulk calendar for IPOs**: The Calendar IPO API is essentially a bulk endpoint — it provides data for upcoming IPOs across **all exchanges** when no symbol filter is applied.

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
