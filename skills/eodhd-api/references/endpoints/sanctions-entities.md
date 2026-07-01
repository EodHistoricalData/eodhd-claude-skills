# Sanctions — Entities API

Status: complete
Source: financial-apis (Sanctions Screening API)
Docs: https://eodhd.com/financial-apis
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /sanctions/entities
Method: GET
Auth: api_token (query)

## Purpose

Consolidated sanctions entity list — persons, companies, and organizations designated across major
sanctions programs and sources (e.g. OFAC, EU, UN). Used for KYC / AML screening, counterparty
checks, and compliance workflows. Returns the standard JSON envelope `{data, meta, links}`.

## Parameters

> **Query params are bare keys, not `filter[...]`.** Sanctions endpoints use plain query params
> (`source`, `type`, `program`, ...) while credit-risk and interest-rate endpoints use JSON:API
> `filter[...]`. Pagination still uses `page[limit]` / `page[offset]`.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| source | No | string | Source list. Currently only `ofac` |
| type | No | string | Entity type: `individual`, `entity`, `vessel`, or `aircraft` |
| program | No | string | Sanctions program code (e.g. `RUSSIA-EO14024`) |
| country | No | string | Country associated with the entity |
| q | No | string | Free-text search (minimum 2 characters) |
| active | No | boolean | Whether the listing is currently active (`true`/`false`) |
| page[offset] | No | integer | Zero-based pagination offset |
| page[limit] | No | integer | Page size |
| fmt | No | string | Output format: 'json' |

## Response (shape)

```json
{
  "data": [
    {
      "source": "OFAC",
      "source_uid": "12345",
      "entity_type": "entity",
      "name": "Example Trading LLC",
      "programs": ["RUSSIA-EO14024"],
      "country": "Russia",
      "remarks": "Designated pursuant to E.O. 14024.",
      "listed_date": "2024-02-24",
      "is_active": true,
      "aliases": ["Example Trading", "ETL"],
      "identifiers": [
        { "type": "Tax ID", "value": "7701234567" }
      ]
    }
  ],
  "meta": { "total": 42000 },
  "links": { "next": "https://eodhd.com/api/sanctions/entities?page%5Boffset%5D=20&page%5Blimit%5D=20" }
}
```

### Data item fields

| Field | Type | Description |
|-------|------|-------------|
| source | string | Source list that designated the entity |
| source_uid | string | Unique id within the source list |
| entity_type | string | Type of entity (individual, entity, ...) |
| name | string | Primary name |
| programs | array | Sanctions program codes |
| country | string | Associated country |
| remarks | string | Free-text remarks / designation notes |
| listed_date | string (YYYY-MM-DD) | Date first listed |
| is_active | boolean | Whether the listing is currently active |
| aliases | array | Known aliases / alternate spellings |
| identifiers | array | Structured identifiers (tax ID, passport, registration, ...) |

## Example Requests

```bash
# Search active entities in a program (bare query params)
curl "https://eodhd.com/api/sanctions/entities?api_token=YOUR_TOKEN&program=RUSSIA-EO14024&type=entity&active=true"

# Free-text search
curl "https://eodhd.com/api/sanctions/entities?api_token=YOUR_TOKEN&q=Ivanov"

# Using the helper client (--filter-param maps to bare keys for sanctions)
python eodhd_client.py --endpoint sanctions/entities --filter-param program=RUSSIA-EO14024 --filter-param type=entity --filter-param active=true
```

## Notes

- Query params are **bare keys** (`source`, `type`, `program`, `country`, `q`, `active`) — **not** `filter[...]`.
- `source` currently supports only `ofac`.
- `type` accepts `individual`, `entity`, `vessel`, or `aircraft`.
- `q` requires a minimum of 2 characters.
- Pagination uses `page[offset]` and `page[limit]`.
- `aliases` and `identifiers` are arrays; screen against all aliases, not just `name`.
- Use `/sanctions/programs` and `/sanctions/sources` to enumerate valid program / source values.
- Helper client: pass filters with repeatable `--filter-param KEY=VALUE` (sent as bare `KEY=VALUE`).

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
