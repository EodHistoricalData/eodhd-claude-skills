# Sanctions — Vessels API

Status: complete
Source: financial-apis (Sanctions Screening API)
Docs: https://eodhd.com/financial-apis
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /sanctions/vessels
Method: GET
Auth: api_token (query)

## Purpose

Sanctioned vessels list — ships designated under sanctions programs, keyed by IMO number and MMSI and
linked back to the owning sanctioned entity. Used for maritime trade compliance, shipping-counterparty
screening, and vessel due diligence. Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| filter[name] | No | string | Vessel name (partial match) |
| filter[imo_number] | No | string | IMO number |
| filter[flag] | No | string | Flag state (e.g. `Panama`) |
| filter[program] | No | string | Sanctions program code |
| filter[country] | No | string | Associated country |
| filter[source] | No | string | Source list |
| page[offset] | No | integer | Zero-based pagination offset |
| page[limit] | No | integer | Page size |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    {
      "call_sign": "3EXX9",
      "vessel_type": "Crude Oil Tanker",
      "flag": "Panama",
      "tonnage": 159000,
      "gross_tonnage": 84000,
      "owner": "Example Shipping Co",
      "imo_number": "9700001",
      "mmsi": "352000000",
      "entity_source_uid": "12345",
      "entity_name": "Example Shipping Co",
      "source": "OFAC",
      "programs": ["IRAN"],
      "country": "Iran",
      "is_active": true
    }
  ],
  "meta": { "total": 900 },
  "links": { "next": "https://eodhd.com/api/sanctions/vessels?page%5Boffset%5D=20&page%5Blimit%5D=20" }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| call_sign | string | Radio call sign |
| vessel_type | string | Vessel type |
| flag | string | Flag state |
| tonnage | number | Deadweight tonnage |
| gross_tonnage | number | Gross tonnage |
| owner | string | Registered owner |
| imo_number | string | IMO number |
| mmsi | string | Maritime Mobile Service Identity |
| entity_source_uid | string | source_uid of the linked sanctioned entity |
| entity_name | string | Name of the linked sanctioned entity |
| source | string | Source list |
| programs | array | Sanctions program codes |
| country | string | Associated country |
| is_active | boolean | Whether the designation is currently active |

## Example Requests

```bash
# Sanctioned vessels by flag state
curl "https://eodhd.com/api/sanctions/vessels?api_token=YOUR_TOKEN&filter%5Bflag%5D=Panama"

# Using the helper client
python eodhd_client.py --endpoint sanctions/vessels --filter-param flag=Panama
```

## Notes

- Filters use JSON:API bracket syntax: `filter[name]`, `filter[imo_number]`, `filter[flag]`, `filter[program]`, `filter[country]`, `filter[source]`.
- Pagination uses `page[offset]` and `page[limit]`.
- `entity_source_uid` links a vessel back to its owning entity in `/sanctions/entities`.
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
