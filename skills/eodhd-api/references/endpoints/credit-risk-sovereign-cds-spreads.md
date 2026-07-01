# Credit & Sovereign Risk — Sovereign CDS Spreads API

Status: complete
Source: financial-apis (Credit & Sovereign Risk Data API)
Docs: https://eodhd.com/financial-apis/credit-sovereign-risk-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /credit-risk/sovereign/cds-spreads
Method: GET
Auth: api_token (query)

## Purpose

Sovereign credit default swap (CDS) spreads per country, including the raw CDS spread and the spread
net of the Switzerland (near-riskless) benchmark. Used for sovereign-risk pricing, default-probability
estimation, and relative-value analysis. Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[country] | No | string | Country name or ISO3 (e.g. `France`, `FRA`) |
| filter[as_of] | No | string (YYYY-MM-DD) | As-of date; defaults to the latest snapshot |
| page[offset] | No | integer | Zero-based pagination offset |
| page[limit] | No | integer | Page size |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    {
      "country_iso3": "FRA",
      "country_name": "France",
      "as_of_date": "2026-01-01",
      "moodys_rating": "Aa2",
      "cds_spread": 0.0041,
      "cds_spread_net_of_switzerland": 0.0037,
      "source": "Damodaran"
    }
  ],
  "meta": { "total": 90 },
  "links": { "next": null }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| country_iso3 | string | ISO 3166-1 alpha-3 country code |
| country_name | string | Country name |
| as_of_date | string (YYYY-MM-DD) | Snapshot date |
| moodys_rating | string | Moody's sovereign rating |
| cds_spread | number | Sovereign CDS spread (fraction) |
| cds_spread_net_of_switzerland | number | CDS spread net of the Switzerland benchmark (fraction) |
| source | string | Data provider |

## Example Requests

```bash
# Latest sovereign CDS spreads for France
curl "https://eodhd.com/api/credit-risk/sovereign/cds-spreads?api_token=YOUR_TOKEN&filter%5Bcountry%5D=France"

# Using the helper client
python eodhd_client.py --endpoint credit-risk/sovereign/cds-spreads --filter-param country=France
```

## Notes

- Filters use JSON:API bracket syntax: `filter[country]`, `filter[as_of]`.
- Pagination uses `page[offset]` and `page[limit]`.
- Spreads are returned as fractions (0.0041 = 41 bps).
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
