# Credit & Sovereign Risk — Sovereign Risk Premium API

Status: complete
Source: financial-apis (Credit & Sovereign Risk Data API)
Docs: https://eodhd.com/financial-apis/credit-sovereign-risk-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /credit-risk/sovereign/risk-premium
Method: GET
Auth: api_token (query)

## Purpose

Country-level risk-premium dataset: adjusted default spread, country risk premium (CRP), and equity
risk premium (ERP) per country, alongside the Moody's sovereign rating, corporate tax rate, and
sovereign CDS. Used for cost-of-equity / discount-rate modelling, cross-border valuation, and
country-risk analysis. Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[country] | No | string | Country name or ISO3 (e.g. `USA`, `Germany`) |
| filter[region] | No | string | Region name (e.g. `Europe`) |
| filter[as_of] | No | string (YYYY-MM-DD) | As-of date; defaults to the latest available snapshot |
| page[offset] | No | integer | Zero-based pagination offset |
| page[limit] | No | integer | Page size |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    {
      "country_iso3": "USA",
      "country_name": "United States",
      "as_of_date": "2026-01-01",
      "moodys_rating": "Aaa",
      "adj_default_spread": 0.0,
      "country_risk_premium": 0.0,
      "equity_risk_premium": 0.043,
      "corporate_tax_rate": 0.21,
      "sovereign_cds": 0.0032,
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
| adj_default_spread | number | Adjusted default spread (fraction) |
| country_risk_premium | number | Country risk premium (fraction) |
| equity_risk_premium | number | Equity risk premium (fraction) |
| corporate_tax_rate | number | Marginal corporate tax rate (fraction) |
| sovereign_cds | number | Sovereign CDS level |
| source | string | Data provider |

## Example Requests

```bash
# Latest risk premium for the United States
curl "https://eodhd.com/api/credit-risk/sovereign/risk-premium?api_token=YOUR_TOKEN&filter%5Bcountry%5D=USA"

# Using the helper client
python eodhd_client.py --endpoint credit-risk/sovereign/risk-premium --filter-param country=USA
```

## Notes

- Filters use JSON:API bracket syntax: `filter[country]`, `filter[region]`, `filter[as_of]`.
- Pagination uses `page[offset]` and `page[limit]`.
- `equity_risk_premium`, `country_risk_premium`, and tax rates are returned as fractions (0.043 = 4.3%).
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
