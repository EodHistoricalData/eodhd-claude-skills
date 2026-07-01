# Credit & Sovereign Risk — Sovereign Credit Ratings API

Status: complete
Source: financial-apis (Credit & Sovereign Risk Data API)
Docs: https://eodhd.com/financial-apis/credit-sovereign-risk-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /credit-risk/sovereign/credit-ratings
Method: GET
Auth: api_token (query)

## Purpose

Sovereign credit ratings from the three major agencies (Moody's, S&P, Fitch) per country. Used for
credit-quality screening, mapping ratings to spreads, and eligibility / covenant checks. Returns the
standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[country] | No | string | Country name or ISO3 (e.g. `Germany`, `DEU`) |
| filter[as_of] | No | string (YYYY-MM-DD) | As-of date; defaults to the latest snapshot |
| page[offset] | No | integer | Zero-based pagination offset |
| page[limit] | No | integer | Page size |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    {
      "country_iso3": "DEU",
      "country_name": "Germany",
      "as_of_date": "2026-01-01",
      "moodys_rating": "Aaa",
      "sp_rating": "AAA",
      "fitch_rating": "AAA",
      "source": "Damodaran"
    }
  ],
  "meta": { "total": 190 },
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
| sp_rating | string | S&P sovereign rating |
| fitch_rating | string | Fitch sovereign rating |
| source | string | Data provider |

## Example Requests

```bash
# Latest sovereign ratings for Germany
curl "https://eodhd.com/api/credit-risk/sovereign/credit-ratings?api_token=YOUR_TOKEN&filter%5Bcountry%5D=Germany"

# Using the helper client
python eodhd_client.py --endpoint credit-risk/sovereign/credit-ratings --filter-param country=Germany
```

## Notes

- Filters use JSON:API bracket syntax: `filter[country]`, `filter[as_of]`.
- Pagination uses `page[offset]` and `page[limit]`.
- Ratings are agency-native strings (e.g. Moody's `Aaa`, S&P/Fitch `AAA`).
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
