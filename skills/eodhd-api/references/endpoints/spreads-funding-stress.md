# Interest Rates — Funding Stress Spreads API

Status: complete
Source: financial-apis (Interest Rates API — SOFR, Fed Funds, ECB, BoE)
Docs: https://eodhd.com/financial-apis/interest-rates-api-sofr-fed-funds-ecb-boe-policy-rates
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /spreads/funding-stress
Method: GET
Auth: api_token (query)

## Purpose

Pre-computed funding-stress spreads between reference rates (e.g. EFFR-SOFR, OBFR-EFFR), expressed in
basis points, with the two legs and their underlying rates. Used to monitor money-market funding
pressure and short-term liquidity stress. Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[code] | No | string | Spread code(s), comma-separated (e.g. `EFFR_SOFR`, `OBFR_EFFR`) |
| filter[from] | No | string (YYYY-MM-DD) | Start date |
| filter[to] | No | string (YYYY-MM-DD) | End date |
| fmt | No | string | Output format: 'json' |

> This endpoint has **no pagination** (`page[offset]` / `page[limit]` are not used); narrow the result
> set with `filter[code]` and a date window instead.

## Response (shape)

```json
{
  "data": [
    {
      "date": "2026-05-15",
      "code": "EFFR_SOFR",
      "value_bps": 2.0,
      "formula": "EFFR - SOFR",
      "leg_a": "EFFR",
      "leg_b": "SOFR",
      "leg_a_rate": 4.33,
      "leg_b_rate": 4.31
    }
  ],
  "meta": { "total": 21 },
  "links": { "next": null }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| date | string (YYYY-MM-DD) | Observation date |
| code | string | Spread code |
| value_bps | number | Spread value in basis points |
| formula | string | Human-readable formula (e.g. `EFFR - SOFR`) |
| leg_a | string | First leg rate code |
| leg_b | string | Second leg rate code |
| leg_a_rate | number | Rate value of leg A (percent) |
| leg_b_rate | number | Rate value of leg B (percent) |

## Example Requests

```bash
# EFFR-SOFR and OBFR-EFFR spreads over a window
curl "https://eodhd.com/api/spreads/funding-stress?api_token=YOUR_TOKEN&filter%5Bcode%5D=EFFR_SOFR,OBFR_EFFR&filter%5Bfrom%5D=2026-05-01&filter%5Bto%5D=2026-05-31"

# Using the helper client
python eodhd_client.py --endpoint spreads/funding-stress --filter-param code=EFFR_SOFR --filter-param from=2026-05-01 --filter-param to=2026-05-31
```

## Notes

- Filters use JSON:API bracket syntax: `filter[code]`, `filter[from]`, `filter[to]`.
- `filter[code]` accepts a comma-separated list of spread codes.
- No pagination — the helper client does not send `page[limit]` / `page[offset]` for this endpoint.
- `value_bps` is in basis points; `leg_a_rate` / `leg_b_rate` are the underlying rates in percent.
- Helper client: pass filters with repeatable `--filter-param KEY=VALUE`.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up, or your plan lacks endpoint access. |
| **403** | Forbidden | Invalid API key or plan lacks endpoint access. |
| **422** | Unprocessable Entity | Validation error (e.g. bad filter parameter). |
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
