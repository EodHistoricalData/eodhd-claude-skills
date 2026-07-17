# Credit & Sovereign Risk — Rating-based Default Spreads API

Status: complete
Source: financial-apis (Credit & Sovereign Risk Data API)
Docs: https://eodhd.com/financial-apis/credit-sovereign-risk-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /credit-risk/sovereign/default-spreads
Method: GET
Auth: api_token (query)

## Purpose

Default spread by credit rating — a lookup table mapping each rating bucket (e.g. `Aaa`, `Baa2`) to a
default spread. Used to derive a cost-of-debt or country/company risk premium from a rating. Returns
the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[rating] | No | string | Rating bucket (e.g. `Aaa`, `Baa2`) |
| filter[as_of] | No | string (YYYY-MM-DD) | As-of date; defaults to the latest snapshot |
| page[offset] | No | integer | Zero-based pagination offset |
| page[limit] | No | integer | Page size |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    {
      "rating": "Aaa",
      "as_of_date": "2026-01-01",
      "default_spread": 0.0059,
      "source": "Damodaran"
    }
  ],
  "meta": { "total": 20 },
  "links": { "next": null }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| rating | string | Rating bucket (Moody's-style scale) |
| as_of_date | string (YYYY-MM-DD) | Snapshot date |
| default_spread | number | Default spread for the rating (fraction) |
| source | string | Data provider |

## Example Requests

```bash
# Default spread for the Aaa rating bucket
curl "https://eodhd.com/api/credit-risk/sovereign/default-spreads?api_token=YOUR_TOKEN&filter%5Brating%5D=Aaa"

# Using the helper client
python eodhd_client.py --endpoint credit-risk/sovereign/default-spreads --filter-param rating=Aaa
```

## Notes

- Filters use JSON:API bracket syntax: `filter[rating]`, `filter[as_of]`.
- Pagination uses `page[offset]` and `page[limit]`.
- `default_spread` is returned as a fraction (0.0059 = 59 bps).
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
