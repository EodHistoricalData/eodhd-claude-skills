# Cboe Index Data API

Status: complete
Source: financial-apis (CBOE Europe Indices API beta)
Docs: https://eodhd.com/financial-apis/cboe-europe-indices-api-beta
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /cboe/index
Method: GET
Auth: api_token (query)

## Purpose
Return detailed index feed data for a single CBOE index on a specific date and
feed type, including index-level fields and full component composition.

## Parameters
- Required:
  - filter[index_code]: CBOE index code (e.g., BAT20N).
  - filter[feed_type]: feed type (e.g., snapshot_official_closing).
  - filter[date]: YYYY-MM-DD.
  - api_token: EODHD API key.
- Optional:
  - fmt: json or xml (default json).

## Response (shape)
- meta.total: integer (usually 1).
- data[]: array of index feeds.
  - data[].id: feed identifier.
  - data[].type: "cboe-index".
  - data[].attributes.region: region of the index.
  - data[].attributes.index_code: CBOE index code.
  - data[].attributes.feed_type: feed type.
  - data[].attributes.date: YYYY-MM-DD.
  - data[].attributes.index_close: number.
  - data[].attributes.index_divisor: number.
  - data[].attributes.effective_date: nullable.
  - data[].attributes.review_date: nullable.
  - data[].components[]: list of constituents.
    - components[].id: component identifier.
    - components[].type: "cboe-index-component".
    - components[].attributes.symbol: ticker (often with suffix).
    - components[].attributes.isin: ISIN.
    - components[].attributes.name: company name.
    - components[].attributes.equity: equity identifier/description.
    - components[].attributes.sedol: nullable.
    - components[].attributes.cusip: CUSIP.
    - components[].attributes.country: issuer country.
    - components[].attributes.revenue_country: nullable.
    - components[].attributes.closing_price: number.
    - components[].attributes.currency: currency code.
    - components[].attributes.closing_factor: number.
    - components[].attributes.total_shares: integer.
    - components[].attributes.market_cap: number.
    - components[].attributes.market_cap_free_float: number.
    - components[].attributes.free_float_factor: number.
    - components[].attributes.weighting_cap_factor: number.
    - components[].attributes.index_weighting: number.
    - components[].attributes.index_shares: number.
    - components[].attributes.index_value: number.
    - components[].attributes.sector: string.

## Example request
```bash
curl "https://eodhd.com/api/cboe/index?filter[index_code]=BDE30P&filter[feed_type]=snapshot_official_closing&filter[date]=2017-02-01&api_token=YOUR_API_KEY&fmt=json"
```

## Notes
- API call consumption: 10 calls per request.
- Use `/cboe/indices` first to discover supported index_code values.

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
