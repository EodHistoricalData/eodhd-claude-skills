# Credit & Sovereign Risk — HQM Corporate Bond Yields API

Status: complete
Source: financial-apis (Credit & Sovereign Risk Data API)
Docs: https://eodhd.com/financial-apis/credit-sovereign-risk-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /credit-risk/corporate/hqm-yields
Method: GET
Auth: api_token (query)

## Purpose

High Quality Market (HQM) corporate bond yield curve — par and spot yields by tenor. Used for
discounting long-dated liabilities (e.g. pension obligations) and corporate term-structure analysis.
Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[tenor] | No | string | Tenor(s) in years, comma-separated (e.g. `2,5,10`) |
| filter[type] | No | string | Yield type: `par` or `spot` |
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
      "series_id": "HQMCB2YRP",
      "tenor_years": 2,
      "yield_type": "par",
      "as_of_date": "2026-06-01",
      "yield_value": 4.12,
      "source": "US Treasury / Federal Reserve"
    }
  ],
  "meta": { "total": 360 },
  "links": { "next": null }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| series_id | string | HQM series identifier |
| tenor_years | number | Tenor in years |
| yield_type | string | `par` or `spot` |
| as_of_date | string (YYYY-MM-DD) | Observation date |
| yield_value | number | Yield for the tenor (percent) |
| source | string | Data provider |

## Example Requests

```bash
# Par HQM yields for 2Y, 5Y, 10Y over a window
curl "https://eodhd.com/api/credit-risk/corporate/hqm-yields?api_token=YOUR_TOKEN&filter%5Btenor%5D=2,5,10&filter%5Btype%5D=par&filter%5Bfrom%5D=2026-01-01&filter%5Bto%5D=2026-06-01"

# Using the helper client
python eodhd_client.py --endpoint credit-risk/corporate/hqm-yields --filter-param tenor=2,5,10 --filter-param type=par
```

## Notes

- Filters use JSON:API bracket syntax: `filter[tenor]`, `filter[type]`, `filter[from]`, `filter[to]`.
- `filter[type]` accepts `par` (par yield curve) or `spot` (spot yield curve).
- `filter[tenor]` accepts a comma-separated list of tenors in years.
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
