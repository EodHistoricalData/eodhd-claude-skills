# Interest Rates — Reference Rates API

Status: complete
Source: financial-apis (Interest Rates API — SOFR, Fed Funds, ECB, BoE)
Docs: https://eodhd.com/financial-apis/interest-rates-api-sofr-fed-funds-ecb-boe-policy-rates
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /rates/reference-rates
Method: GET
Auth: api_token (query)

## Purpose

Daily benchmark / reference interest-rate time series — overnight and term rates such as SOFR, EFFR,
OBFR, ESTR, SONIA. Used for floating-rate discounting, funding analysis, and derivatives pricing.
Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[code] | No | string | Rate code(s), comma-separated (e.g. `SOFR`, `EFFR`) |
| filter[currency] | No | string | Currency (e.g. `USD`, `EUR`, `GBP`) |
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
      "date": "2025-06-02",
      "code": "SOFR",
      "currency": "USD",
      "rate_type": "overnight",
      "rate": 4.31,
      "source": "New York Fed",
      "source_series_id": "SOFR"
    }
  ],
  "meta": { "total": 260 },
  "links": { "next": null }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| date | string (YYYY-MM-DD) | Observation date |
| code | string | Reference rate code |
| currency | string | Currency |
| rate_type | string | Rate type (e.g. overnight, term) |
| rate | number | Rate value (percent) |
| source | string | Data provider |
| source_series_id | string | Upstream series identifier |

## Example Requests

```bash
# SOFR over a window
curl "https://eodhd.com/api/rates/reference-rates?api_token=YOUR_TOKEN&filter%5Bcode%5D=SOFR&filter%5Bfrom%5D=2025-01-01&filter%5Bto%5D=2025-06-01"

# Using the helper client
python eodhd_client.py --endpoint rates/reference-rates --filter-param code=SOFR --filter-param from=2025-01-01
```

## Notes

- Filters use JSON:API bracket syntax: `filter[code]`, `filter[currency]`, `filter[from]`, `filter[to]`.
- `filter[code]` accepts a comma-separated list to fetch several rates at once.
- Pagination uses `page[offset]` and `page[limit]`.
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
