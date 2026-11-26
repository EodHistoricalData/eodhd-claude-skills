# ETF Held-By API (funds holding a security) (beta)

Status: complete (beta)
Source: financial-apis (ETF Holdings API)
Docs: https://eodhd.com/financial-apis/etf-holdings-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /etf/security/{symbol}/held-by
Method: GET
Auth: api_token (query)

## Purpose

Reverse lookup for the ETF Holdings API: given a security, list the **US-listed ETFs** that hold it, with weight, shares and value in each fund, sorted by weight descending. Built from SEC N-PORT filings. The API is in **beta**.

The looked-up security can be a US ticker (`NVDA`, `XOM`) or a foreign ticker with an exchange suffix (`ASML.AS`). The funds in the result are always US-listed ETFs. For the full portfolio of one fund, see `etf-holdings.md`.

Available on the Fundamentals Data Feed and All-In-One plans. Each request costs **10 API calls**. **The demo token returns 403 here** (unlike `etf/holdings` for `VTI`). There is no `fmt` parameter.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API access token |
| symbol | Yes | string (path) | The security being looked up (not a fund), for example `NVDA`, `XOM`, `ASML.AS` |
| page[offset] | No | integer | Zero-based offset (default 0) |
| page[limit] | No | integer | Page size (default 100, range 1 to 5000; outside the range returns 422) |

## Response (shape)

```json
{
  "data": {
    "security": { "ticker": "NVDA", "exchange": "US", "name": "NVIDIA Corp" },
    "held_by_count": 791,
    "funds": [
      { "ticker": "VTI", "name": "...", "weight": 0, "shares": 0, "value_usd": 0, "report_date": "YYYY-MM-DD" }
    ]
  },
  "meta": { "total": 791, "offset": 0, "limit": 3 },
  "links": { "next": "/api/etf/security/NVDA/held-by?page[offset]=3&page[limit]=3" }
}
```

| Field | Type | Description |
|-------|------|-------------|
| data.security | object | `ticker`, `exchange`, `name` of the looked-up security |
| data.held_by_count | integer | Number of funds that hold it |
| data.funds[].ticker | string | Fund ticker |
| data.funds[].name | string | Fund name |
| data.funds[].weight | number | Weight of the security in the fund, percent |
| data.funds[].shares | number | Shares held |
| data.funds[].value_usd | number | Position value, USD |
| data.funds[].report_date | string (date) | End of the fund's filing period |
| meta.total / offset / limit | integer | Paging info |
| links.next | string or null | Relative URL of the next page, without the token (add `api_token` yourself); null on the last page |

`funds` is sorted by `weight` descending. A request past the end returns an empty `funds` list.

## Example Requests

```bash
# Top 3 funds by weight that hold NVDA
curl "https://eodhd.com/api/etf/security/NVDA/held-by?api_token=YOUR_TOKEN&page[offset]=0&page[limit]=3"

# Foreign security
curl "https://eodhd.com/api/etf/security/ASML.AS/held-by?api_token=YOUR_TOKEN&page[limit]=3"

# Using the helper client
python eodhd_client.py --endpoint etf/held-by --symbol XOM --limit 3 --offset 0
```

## Notes

- Beta. Funds in the result are US-listed ETFs only.
- Paginate with `page[offset]`/`page[limit]`, or follow `links.next` (prepend the host and add `api_token`).
- NVDA is held by 791 funds and XOM by 502 funds, so use a small `page[limit]` while testing.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. |
| **401** | Unauthorized | Plain text body `Unauthenticated`: missing or invalid token. |
| **403** | Forbidden | Plain text: the plan does not include this API, or the demo token was used. |
| **404** | Not Found | Unknown ticker. JSON error body, without a `code` field on this endpoint. |
| **422** | Unprocessable | Invalid paging, for example `{"errors":{"page.limit":["The page.limit may not be greater than 5000."]}}` |
| **429** | Too Many Requests | Rate limit of the plan. |
