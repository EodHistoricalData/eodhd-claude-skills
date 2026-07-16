# Congressional Trades API

Status: complete
Source: financial-apis (Congressional Trades API)
Docs: https://eodhd.com/financial-apis/congressional-trades-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /congressional-trades
Method: GET
Auth: api_token (query)

## Purpose

Returns US Congress stock-trade disclosures filed under the STOCK Act, collected from the two official government portals — the Senate Electronic Financial Disclosure (EFD) system and the House Clerk disclosure site — and normalised into one schema across both chambers. Each record pairs the trading member with the asset and the transaction, and adds derived fields: numeric bounds parsed from the disclosed amount range, days between the trade and its disclosure, a flag for filings that missed the 45-day STOCK Act window, and a link to the original filing. Available in the All-in-One plan. Each request costs 10 API calls.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| symbol | No | string | Filter by a single ticker symbol, e.g. AAPL |
| chamber | No | string | Filter by chamber: senate or house |
| bioguide_id | No | string | Filter by member Bioguide ID, e.g. S000250 (one letter + six digits) |
| transaction_type | No | string | One or more of purchase, sale, exchange (comma-separated for multiple) |
| transaction_date_from | No | string (YYYY-MM-DD) | Earliest transaction date, inclusive |
| transaction_date_to | No | string (YYYY-MM-DD) | Latest transaction date, inclusive (on or after transaction_date_from) |
| disclosure_date_from | No | string (YYYY-MM-DD) | Earliest disclosure date, inclusive |
| disclosure_date_to | No | string (YYYY-MM-DD) | Latest disclosure date, inclusive (on or after disclosure_date_from) |
| page[offset] | No | integer | Offset for pagination (default 0) |
| page[limit] | No | integer | Records per page (default 20, maximum 100) |

Filters are passed as flat query keys (e.g. `chamber=senate`), not `filter[...]`. Only pagination uses bracket notation (`page[offset]`, `page[limit]`).

## Response (shape)

```json
{
  "data": [
    {
      "chamber": "senate",
      "member": {
        "bioguide_id": "W000802",
        "first_name": "Sheldon",
        "last_name": "Whitehouse",
        "full_name": "Sheldon Whitehouse",
        "office": "Whitehouse, Sheldon (Senator)",
        "state": null,
        "party": null,
        "district": null
      },
      "asset": {
        "symbol": "NVDA",
        "description": "NVIDIA Corporation - Common Stock",
        "asset_type": "Stock"
      },
      "transaction": {
        "type": "sale",
        "transaction_date": "2026-06-30",
        "disclosure_date": "2026-07-08",
        "owner": "Self",
        "amount_range": "$15,001 - $50,000",
        "amount_low": 15001,
        "amount_high": 50000,
        "days_to_disclose": 8,
        "is_late": false,
        "comment": null
      },
      "source": {
        "filing_url": "https://efdsearch.senate.gov/search/view/ptr/5d9b1b8e-2ae1-442b-860c-e79b8a701dc6/",
        "source_system": "senate",
        "filing_identifier": "5d9b1b8e-2ae1-442b-860c-e79b8a701dc6"
      }
    }
  ],
  "meta": { "total": 44604, "page": { "offset": 0, "limit": 20 } },
  "links": { "next": "https://eodhd.com/api/congressional-trades?page[offset]=20&page[limit]=20" }
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| data | array | Array of trade records |
| meta | object | total (record count for the filter) and page (offset, limit) |
| links | object | next page URL, or null on the last page |

**Data item fields:**

| Field | Type | Description |
|-------|------|-------------|
| chamber | string | senate or house |
| member.bioguide_id | string or null | Bioguide identifier, when matched |
| member.first_name | string | Member first name |
| member.last_name | string | Member last name |
| member.full_name | string | Member full name as filed |
| member.office | string or null | Office label from the source filing |
| member.state | string or null | Two-letter US state code, when available |
| member.party | string or null | Political party, when available |
| member.district | integer or null | House district number; null for senators |
| asset.symbol | string or null | Ticker symbol; null for assets without a ticker |
| asset.description | string | Asset description as filed |
| asset.asset_type | string | Normalised asset class (Stock, Bond, Other) |
| transaction.type | string | purchase, sale, or exchange |
| transaction.transaction_date | string (YYYY-MM-DD) | Date the trade took place |
| transaction.disclosure_date | string (YYYY-MM-DD) | Date the trade was disclosed |
| transaction.owner | string or null | Self, Spouse, or Joint |
| transaction.amount_range | string | Disclosed amount band, as filed |
| transaction.amount_low | number or null | Lower bound of the amount range, USD |
| transaction.amount_high | number or null | Upper bound of the amount range, USD |
| transaction.days_to_disclose | integer | Days between transaction and disclosure |
| transaction.is_late | boolean | True if the filing missed the 45-day STOCK Act window |
| transaction.comment | string or null | Free-text note from the filing |
| source.filing_url | string | Link to the original filing on the official portal |
| source.source_system | string | senate or house |
| source.filing_identifier | string | Filing identifier at the source system |

## Example Requests

```bash
# Latest disclosures
curl "https://eodhd.com/api/congressional-trades?api_token=YOUR_TOKEN"

# Senate purchases and sales since 2026, first 5
curl "https://eodhd.com/api/congressional-trades?api_token=YOUR_TOKEN&chamber=senate&transaction_type=purchase,sale&transaction_date_from=2026-01-01&page[limit]=5"

# A single member's trades in AAPL
curl "https://eodhd.com/api/congressional-trades?api_token=YOUR_TOKEN&bioguide_id=S000250&symbol=AAPL"
```

## Notes

- Both chambers are returned together; use `chamber` to restrict to one.
- Derived fields (`amount_low`/`amount_high`, `days_to_disclose`, `is_late`) are computed by EODHD and are not part of the raw filing.
- Assets without a ticker (many bonds and other instruments) have `asset.symbol` set to null.
- Source data is reproduced as filed; occasional data-entry errors in the original disclosures are passed through. Use `source.filing_url` to verify against the official document.
- API call consumption: 10 calls per request.
- Access requires the All-in-One plan.
- Support tier: documented. This endpoint is described here for reference and MCP/agent guidance; the `eodhd_client.py` helper does not yet expose a dedicated subcommand for it.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Response body carries data, meta, and links. |
| **401** | Unauthorized | Missing or invalid `api_token`. |
| **403** | Forbidden | Token is valid but the plan does not include Congressional Trades (requires All-in-One). |
| **422** | Unprocessable Entity | Invalid parameter — malformed date, page[limit] out of range, reversed date range, or an unknown chamber/transaction type. |
| **429** | Too Many Requests | Exceeded rate limit. Slow down requests. |
