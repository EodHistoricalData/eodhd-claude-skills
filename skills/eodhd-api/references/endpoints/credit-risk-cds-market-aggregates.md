# Credit & Sovereign Risk — CDS Market Aggregates API

Status: complete
Source: financial-apis (Credit & Sovereign Risk Data API)
Docs: https://eodhd.com/financial-apis/credit-sovereign-risk-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /credit-risk/cds-market/aggregates
Method: GET
Auth: api_token (query)

## Purpose

Aggregate CDS market activity — e.g. gross notional outstanding — broken down by dimension such as
credit grade or cleared status. Used to monitor structural CDS-market size and composition. Returns
the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[metric] | No | string | Metric, e.g. `gross_notional` |
| filter[dimension] | No | string | Breakdown dimension: `grade` or `cleared_status` |
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
      "as_of_date": "2026-05-31",
      "release_date": "2026-06-07",
      "metric": "gross_notional",
      "breakdown_dimension": "grade",
      "breakdown_value": "Investment Grade",
      "region": "Global",
      "usd_notional_mn": 3820145.0,
      "source": "DTCC"
    }
  ],
  "meta": { "total": 480 },
  "links": { "next": null }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| as_of_date | string (YYYY-MM-DD) | Observation date |
| release_date | string (YYYY-MM-DD) | Data release date |
| metric | string | Metric name (e.g. `gross_notional`) |
| breakdown_dimension | string | Dimension used for the breakdown (`grade`, `cleared_status`) |
| breakdown_value | string | Value within the dimension (e.g. `Investment Grade`, `Cleared`) |
| region | string | Region scope |
| usd_notional_mn | number | Notional in USD millions |
| source | string | Data provider |

## Example Requests

```bash
# Gross notional by credit grade over a window
curl "https://eodhd.com/api/credit-risk/cds-market/aggregates?api_token=YOUR_TOKEN&filter%5Bmetric%5D=gross_notional&filter%5Bdimension%5D=grade&filter%5Bfrom%5D=2026-01-01&filter%5Bto%5D=2026-06-01"

# Using the helper client
python eodhd_client.py --endpoint credit-risk/cds-market/aggregates --filter-param metric=gross_notional --filter-param dimension=grade
```

## Notes

- Filters use JSON:API bracket syntax: `filter[metric]`, `filter[dimension]`, `filter[from]`, `filter[to]`.
- `filter[dimension]` supports `grade` and `cleared_status`.
- Notional is reported in USD millions (`usd_notional_mn`).
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
