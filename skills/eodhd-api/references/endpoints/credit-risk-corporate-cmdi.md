# Credit & Sovereign Risk — Corporate Market-implied Default Index (CMDI) API

Status: complete
Source: financial-apis (Credit & Sovereign Risk Data API)
Docs: https://eodhd.com/financial-apis/credit-sovereign-risk-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /credit-risk/corporate/cmdi
Method: GET
Auth: api_token (query)

## Purpose

Corporate market-implied default index (CMDI) time series — an aggregate market gauge with
investment-grade (IG) and high-yield (HY) sub-indices. Used to track corporate credit stress and
default risk across the cycle. Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[from] | No | string (YYYY-MM-DD) | Start date |
| filter[to] | No | string (YYYY-MM-DD) | End date |
| page[offset] | No | integer | Zero-based pagination offset |
| page[limit] | No | integer | Page size |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    {
      "as_of_date": "2026-06-01",
      "market_cmdi": 1.42,
      "ig_cmdi": 0.61,
      "hy_cmdi": 4.87,
      "source": "EODHD"
    }
  ],
  "meta": { "total": 260 },
  "links": { "next": null }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| as_of_date | string (YYYY-MM-DD) | Observation date |
| market_cmdi | number | Aggregate market CMDI |
| ig_cmdi | number | Investment-grade sub-index |
| hy_cmdi | number | High-yield sub-index |
| source | string | Data provider |

## Example Requests

```bash
# CMDI time series for a date window
curl "https://eodhd.com/api/credit-risk/corporate/cmdi?api_token=YOUR_TOKEN&filter%5Bfrom%5D=2026-01-01&filter%5Bto%5D=2026-06-01"

# Using the helper client
python eodhd_client.py --endpoint credit-risk/corporate/cmdi --filter-param from=2026-01-01 --filter-param to=2026-06-01
```

## Notes

- Filters use JSON:API bracket syntax: `filter[from]`, `filter[to]`.
- Pagination uses `page[offset]` and `page[limit]`.
- Time series is keyed on `as_of_date`; higher CMDI values indicate greater implied default risk.
- Helper client: pass filters with repeatable `--filter-param KEY=VALUE`.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up, or your plan lacks endpoint access. |
| **403** | Forbidden | Invalid API key or plan lacks endpoint access. |
| **422** | Unprocessable Entity | Validation error (e.g. bad filter or pagination parameter). |
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
