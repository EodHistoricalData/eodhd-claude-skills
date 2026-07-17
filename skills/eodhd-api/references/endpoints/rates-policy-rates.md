# Interest Rates — Policy Rates API

Status: complete
Source: financial-apis (Interest Rates API — SOFR, Fed Funds, ECB, BoE)
Docs: https://eodhd.com/financial-apis/interest-rates-api-sofr-fed-funds-ecb-boe-policy-rates
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /rates/policy-rates
Method: GET
Auth: api_token (query)

## Purpose

Central-bank policy-rate time series — official target / administered rates set by central banks
(e.g. Fed funds target, ECB deposit facility rate, BoE Bank Rate). Used for macro analysis, rate-path
tracking, and cross-country policy comparison. Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[code] | No | string | Policy-rate code(s), comma-separated (e.g. `ECB_DFR`) |
| filter[country] | No | string | Country / area (e.g. `US`, `EU`, `GB`) |
| filter[central_bank] | No | string | Central bank (e.g. `ECB`, `FED`, `BOE`) |
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
      "date": "2026-06-10",
      "code": "ECB_DFR",
      "country": "EU",
      "central_bank": "ECB",
      "rate": 2.0,
      "source": "ECB",
      "source_series_id": "FM/D.U2.EUR.4F.KR.DFR.LEV"
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
| code | string | Policy-rate code |
| country | string | Country / area |
| central_bank | string | Central bank |
| rate | number | Policy rate (percent) |
| source | string | Data provider |
| source_series_id | string | Upstream series identifier |

## Example Requests

```bash
# ECB policy rates from a start date
curl "https://eodhd.com/api/rates/policy-rates?api_token=YOUR_TOKEN&filter%5Bcentral_bank%5D=ECB&filter%5Bfrom%5D=2025-01-01"

# Using the helper client
python eodhd_client.py --endpoint rates/policy-rates --filter-param central_bank=ECB --filter-param from=2025-01-01
```

## Notes

- Filters use JSON:API bracket syntax: `filter[code]`, `filter[country]`, `filter[central_bank]`, `filter[from]`, `filter[to]`.
- `filter[code]` accepts a comma-separated list.
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
