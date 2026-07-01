# Sanctions — Programs API

Status: complete
Source: financial-apis (Sanctions Screening API)
Docs: https://eodhd.com/financial-apis
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /sanctions/programs
Method: GET
Auth: api_token (query)

## Purpose

Distinct list of sanctions programs with the count of designated entities per program. Use it to
enumerate valid `program` values for `/sanctions/entities` and `/sanctions/vessels`, and to
gauge program size. Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| page[offset] | No | integer | Zero-based pagination offset |
| page[limit] | No | integer | Page size |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    { "program": "RUSSIA-EO14024", "count": 5321 },
    { "program": "IRAN", "count": 2874 }
  ],
  "meta": { "total": 180 },
  "links": { "next": null }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| program | string | Sanctions program code |
| count | integer | Number of designated entities in the program |

## Example Requests

```bash
# List all sanctions programs with counts
curl "https://eodhd.com/api/sanctions/programs?api_token=YOUR_TOKEN"

# Using the helper client
python eodhd_client.py --endpoint sanctions/programs
```

## Notes

- No filters; supports `page[offset]` / `page[limit]` pagination.
- Feeds valid values into the `program` parameter of `/sanctions/entities` and `/sanctions/vessels`.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up, or your plan lacks endpoint access. |
| **403** | Forbidden | Invalid API key or plan lacks endpoint access. |
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
