# ASX Corporate Actions API

Status: complete
Source: financial-apis (ASX Corporate Actions Data API)
Docs: https://eodhd.com/financial-apis/asx-corporate-actions
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /asx-corporate-actions
Method: GET
Auth: api_token (query)

## Purpose

Corporate actions for Australian Securities Exchange (ASX) listed securities — dividends, splits,
bonus issues, rights issues, buybacks, capital returns, share purchase plans (SPP) and other events.
Used to track distributions and capital-structure changes for `.AU` tickers. Returns the standard
JSON envelope `{data, meta, links}` with pagination.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| type | No | string | Corporate-action type: `dividends`, `splits`, `bonus-issues`, `rights-issues`, `buybacks`, `capital-returns`, `spp`, `other` |
| symbol | No | string | ASX ticker with `.AU` suffix (e.g. `BHP.AU`) |
| date_from | No | string (YYYY-MM-DD) | Start date |
| date_to | No | string (YYYY-MM-DD) | End date |
| page[offset] | No | integer | Zero-based pagination offset (default 0) |
| page[limit] | No | integer | Page size, 1–1000 (default 100) |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    {
      "symbol": "BHP.AU",
      "type": "dividends",
      "ex_date": "2026-03-05",
      "record_date": "2026-03-06",
      "payment_date": "2026-03-27",
      "value": 0.98,
      "currency": "AUD"
    }
  ],
  "meta": { "total": 240, "page": { "offset": 0, "limit": 100 } },
  "links": { "next": "https://eodhd.com/api/asx-corporate-actions?page%5Boffset%5D=100" }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| symbol | string | ASX ticker with `.AU` suffix |
| type | string | Corporate-action type (see `type` parameter) |
| ex_date | string (YYYY-MM-DD) | Ex-date of the corporate action |
| record_date | string (YYYY-MM-DD) | Record date |
| payment_date | string (YYYY-MM-DD) | Payment / effective date |
| value | number | Action value (e.g. dividend amount or split ratio), where applicable |
| currency | string | Currency of `value`, where applicable |

## Example Requests

```bash
# Dividends for a single ASX ticker
curl "https://eodhd.com/api/asx-corporate-actions?api_token=YOUR_TOKEN&type=dividends&symbol=BHP.AU"

# Splits over a date window (bare query params, page pagination)
curl "https://eodhd.com/api/asx-corporate-actions?api_token=YOUR_TOKEN&type=splits&date_from=2026-01-01&date_to=2026-06-30&page%5Blimit%5D=100&page%5Boffset%5D=0"

# Using the helper client
python eodhd_client.py --endpoint asx-corporate-actions --filter-param type=dividends --filter-param symbol=BHP.AU
python eodhd_client.py --endpoint asx-corporate-actions --filter-param type=splits --filter-param date_from=2026-01-01 --filter-param date_to=2026-06-30
```

## Notes

- Parameters are BARE query params (`type`, `symbol`, `date_from`, `date_to`) — NOT JSON:API `filter[...]` brackets.
- Pagination uses `page[offset]` (default 0) and `page[limit]` (1–1000, default 100).
- `type` accepts `dividends`, `splits`, `bonus-issues`, `rights-issues`, `buybacks`, `capital-returns`, `spp`, `other`.
- `symbol` is an ASX ticker with the `.AU` suffix (e.g. `BHP.AU`).
- One API call is consumed per request.
- Helper client: pass parameters with repeatable `--filter-param KEY=VALUE`; they are sent as bare query params.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up, or your plan lacks endpoint access. |
| **403** | Forbidden | Invalid API key or plan lacks endpoint access. |
| **422** | Unprocessable Entity | Validation error (e.g. bad type or pagination parameter). |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down. |

### Error Response Format

```json
{
  "error": "Error message description",
  "code": 403
}
```

### Handling Errors

**Best Practices**:
- Always check status codes before processing response data
- Implement exponential backoff for 429 errors
- Cache responses to reduce API calls
- Monitor your API usage in the user dashboard
