# SEC Filings API

Status: complete
Source: financial-apis (SEC Filings API)
Docs: https://eodhd.com/financial-apis/sec-filings-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /sec-filings/{symbol} (overview), /sec-filings/{symbol}/10k, /sec-filings/{symbol}/10q, /sec-filings/{symbol}/8k
Method: GET
Auth: api_token (query)

## Purpose

Access parsed US SEC filings for a company. The **overview** endpoint (`/sec-filings/{symbol}`) returns a compact summary — counts, latest date, and a direct URL for each supported filing form (10-K, 10-Q, 8-K, Form 4). The three **per-form** endpoints return the parsed filings themselves:

- **10-K** — annual reports, with a full parsed income statement, balance sheet, and cash-flow statement per filing.
- **10-Q** — quarterly reports, same financial schema as 10-K plus fiscal-quarter metadata.
- **8-K** — material-event reports, with the triggering item codes, per-section text, and attached exhibits.

Form 4 (insider transactions) is a **separate product** — see `insider-transactions.md` for `/sec-filings/{symbol}/form4`.

Available on the All-In-One plan. Each request consumes **10 API calls**. JSON is the only supported format.

The `{symbol}` path segment is a ticker with exchange suffix, e.g. `AAPL.US`.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API access token |
| symbol | Yes | string (path) | Ticker with exchange suffix (e.g., AAPL.US) |
| page[offset] | No | integer | Pagination offset (default 0). Per-form endpoints only. |
| page[limit] | No | integer | Page size (default 20, max 100). Per-form endpoints only. |
| fmt | No | string | Response format: json (default). Only JSON is supported. |

The overview endpoint (`/sec-filings/{symbol}`) is **not** paginated and takes no `page[...]` parameters.

## Response (shape)

### Overview — `GET /sec-filings/{symbol}`

```json
{
  "data": {
    "ticker": "AAPL.US",
    "exchange": "US",
    "name": "Apple Inc",
    "cik": "0000320193",
    "filings": {
      "10k":   { "count": 5,   "latest": "2025-11-01", "url": "https://eodhd.com/api/sec-filings/AAPL.US/10k" },
      "10q":   { "count": 15,  "latest": "2026-05-02", "url": "https://eodhd.com/api/sec-filings/AAPL.US/10q" },
      "8k":    { "count": 42,  "latest": "2026-05-01", "url": "https://eodhd.com/api/sec-filings/AAPL.US/8k" },
      "form4": { "count": 128, "latest": "2026-04-30", "url": "https://eodhd.com/api/sec-filings/AAPL.US/form4" }
    }
  },
  "meta": {},
  "links": {}
}
```

`meta` and `links` are present but empty for the overview. There is no pagination.

### 10-K — `GET /sec-filings/{symbol}/10k`

```json
{
  "data": [
    {
      "accession_number": "0000320193-25-000123",
      "filed_at": "2025-11-01",
      "period_of_report": "2025-09-27",
      "fiscal_year_end": "2025-09-27",
      "revenue": 391035000000,
      "cost_of_revenue": 210352000000,
      "gross_profit": 180683000000,
      "research_and_development": 31370000000,
      "selling_general_admin": 26097000000,
      "operating_expenses": 57467000000,
      "operating_income": 123216000000,
      "interest_expense": null,
      "interest_income": null,
      "income_before_tax": 123485000000,
      "income_tax_expense": 29749000000,
      "net_income": 93736000000,
      "ebitda": 134661000000,
      "depreciation_amortization": 11445000000,
      "eps_basic": 6.11,
      "eps_diluted": 6.08,
      "weighted_avg_shares_basic": 15343783000,
      "weighted_avg_shares_diluted": 15408095000,
      "shares_outstanding": 15115823000,
      "cash_and_equivalents": 29943000000,
      "short_term_investments": 35228000000,
      "accounts_receivable": 33410000000,
      "inventory": 7286000000,
      "total_current_assets": 152987000000,
      "property_plant_equipment": 45680000000,
      "goodwill": null,
      "intangible_assets": null,
      "total_assets": 364980000000,
      "accounts_payable": 68960000000,
      "short_term_debt": 20879000000,
      "total_current_liabilities": 176392000000,
      "long_term_debt": 85750000000,
      "total_liabilities": 308030000000,
      "common_stock": 83276000000,
      "retained_earnings": -19154000000,
      "stockholders_equity": 56950000000,
      "total_equity": 56950000000,
      "operating_cash_flow": 118254000000,
      "capital_expenditure": -9447000000,
      "free_cash_flow": 108807000000,
      "investing_cash_flow": 2935000000,
      "financing_cash_flow": -108488000000,
      "dividends_paid": -15234000000,
      "share_repurchase": -94949000000
    }
  ],
  "meta": { "total": 5, "page": { "offset": 0, "limit": 20 } },
  "links": { "next": null }
}
```

### 10-Q — `GET /sec-filings/{symbol}/10q`

Identical envelope and financial schema to 10-K, except the two annual-period metadata fields are replaced by quarterly ones: `fiscal_year_end` is dropped, and each filing instead carries `fiscal_quarter_end` (string, e.g. `"2026-03-28"`) and `fiscal_quarter` (integer, the calendar quarter 1–4).

```json
{
  "data": [
    {
      "accession_number": "0000320193-26-000045",
      "filed_at": "2026-05-02",
      "period_of_report": "2026-03-28",
      "fiscal_quarter_end": "2026-03-28",
      "fiscal_quarter": 1,
      "revenue": 95359000000,
      "net_income": 23636000000,
      "operating_cash_flow": 29935000000,
      "free_cash_flow": 27860000000
    }
  ],
  "meta": { "total": 15, "page": { "offset": 0, "limit": 20 } },
  "links": { "next": "https://eodhd.com/api/sec-filings/AAPL.US/10q?page%5Boffset%5D=20&page%5Blimit%5D=20" }
}
```

(All financial fields listed for 10-K also apply here; only a subset is shown for brevity.)

### 8-K — `GET /sec-filings/{symbol}/8k`

```json
{
  "data": [
    {
      "accession_number": "0000320193-26-000041",
      "filed_at": "2026-05-01",
      "period_of_report": "2026-05-01",
      "items": ["2.02", "9.01"],
      "item_sections": [
        {
          "item": "2.02",
          "title": "Results of Operations and Financial Condition",
          "text": "On May 1, 2026, Apple Inc. issued a press release ..."
        }
      ],
      "exhibits": [
        { "number": "99.1", "description": "Press Release dated May 1, 2026" }
      ]
    }
  ],
  "meta": { "total": 42, "page": { "offset": 0, "limit": 20 } },
  "links": { "next": "https://eodhd.com/api/sec-filings/AAPL.US/8k?page%5Boffset%5D=20&page%5Blimit%5D=20" }
}
```

## Output Format

### Overview

| Field | Type | Description |
|-------|------|-------------|
| data.ticker | string | Ticker with exchange suffix |
| data.exchange | string | Exchange code |
| data.name | string | Company name |
| data.cik | string | SEC Central Index Key |
| data.filings | object | Per-form summary keyed by `10k`, `10q`, `8k`, `form4` |
| data.filings[form].count | integer | Number of available filings of this form |
| data.filings[form].latest | string (YYYY-MM-DD) | Filing date of the most recent filing |
| data.filings[form].url | string | Direct URL to the per-form endpoint for this symbol |
| meta | object | Empty for the overview |
| links | object | Empty for the overview |

### Per-form envelope (10-K / 10-Q / 8-K)

| Field | Type | Description |
|-------|------|-------------|
| data | array | List of filing objects |
| meta.total | integer | Total number of filings available (across all pages) |
| meta.page.offset | integer | Current page offset |
| meta.page.limit | integer | Current page size |
| links.next | string or null | URL of the next page, or null on the last page |

### 10-K / 10-Q filing object

**Metadata (strings):**

| Field | Type | Description |
|-------|------|-------------|
| accession_number | string | SEC accession number |
| filed_at | string (YYYY-MM-DD) | Date the filing was submitted |
| period_of_report | string (YYYY-MM-DD) | Reporting period end date |
| fiscal_year_end | string (YYYY-MM-DD) | Fiscal year end date (**10-K only**) |
| fiscal_quarter_end | string (YYYY-MM-DD) | Fiscal quarter end date (**10-Q only**) |
| fiscal_quarter | integer | Calendar quarter 1–4 (**10-Q only**) |

**Financials** — integer amounts unless noted; **any field may be null** when the filing does not report it:

| Field | Type | Statement |
|-------|------|-----------|
| revenue | integer | Income statement |
| cost_of_revenue | integer | Income statement |
| gross_profit | integer | Income statement |
| research_and_development | integer | Income statement |
| selling_general_admin | integer | Income statement |
| operating_expenses | integer | Income statement |
| operating_income | integer | Income statement |
| interest_expense | integer | Income statement |
| interest_income | integer | Income statement |
| income_before_tax | integer | Income statement |
| income_tax_expense | integer | Income statement |
| net_income | integer | Income statement |
| ebitda | integer | Income statement |
| depreciation_amortization | integer | Income statement |
| eps_basic | number | Income statement (per-share, decimal) |
| eps_diluted | number | Income statement (per-share, decimal) |
| weighted_avg_shares_basic | integer | Income statement |
| weighted_avg_shares_diluted | integer | Income statement |
| shares_outstanding | integer | Balance sheet |
| cash_and_equivalents | integer | Balance sheet |
| short_term_investments | integer | Balance sheet |
| accounts_receivable | integer | Balance sheet |
| inventory | integer | Balance sheet |
| total_current_assets | integer | Balance sheet |
| property_plant_equipment | integer | Balance sheet |
| goodwill | integer | Balance sheet |
| intangible_assets | integer | Balance sheet |
| total_assets | integer | Balance sheet |
| accounts_payable | integer | Balance sheet |
| short_term_debt | integer | Balance sheet |
| total_current_liabilities | integer | Balance sheet |
| long_term_debt | integer | Balance sheet |
| total_liabilities | integer | Balance sheet |
| common_stock | integer | Balance sheet |
| retained_earnings | integer | Balance sheet |
| stockholders_equity | integer | Balance sheet |
| total_equity | integer | Balance sheet |
| operating_cash_flow | integer | Cash-flow statement |
| capital_expenditure | integer | Cash-flow statement |
| free_cash_flow | integer | Cash-flow statement |
| investing_cash_flow | integer | Cash-flow statement |
| financing_cash_flow | integer | Cash-flow statement |
| dividends_paid | integer | Cash-flow statement |
| share_repurchase | integer | Cash-flow statement |

### 8-K filing object

| Field | Type | Description |
|-------|------|-------------|
| accession_number | string | SEC accession number |
| filed_at | string (YYYY-MM-DD) | Date the filing was submitted |
| period_of_report | string (YYYY-MM-DD) | Event / report period date |
| items | array of string | Triggering item codes (e.g., "2.02", "9.01") |
| item_sections | array of object | Parsed sections: each has `item`, `title`, `text` |
| exhibits | array of object | Attached exhibits: each has `number`, `description` |

## Example Requests

```bash
# Overview — counts, latest dates, and per-form URLs
curl "https://eodhd.com/api/sec-filings/AAPL.US?api_token=YOUR_API_TOKEN&fmt=json"

# Annual reports (10-K)
curl "https://eodhd.com/api/sec-filings/AAPL.US/10k?api_token=YOUR_API_TOKEN&fmt=json"

# Quarterly reports (10-Q), second page of 20
curl "https://eodhd.com/api/sec-filings/AAPL.US/10q?page%5Boffset%5D=20&page%5Blimit%5D=20&api_token=YOUR_API_TOKEN&fmt=json"

# Material events (8-K)
curl "https://eodhd.com/api/sec-filings/AAPL.US/8k?api_token=YOUR_API_TOKEN&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint sec-filings --symbol AAPL.US
python eodhd_client.py --endpoint sec-filings/10k --symbol AAPL.US
python eodhd_client.py --endpoint sec-filings/10q --symbol AAPL.US --limit 20 --offset 20
python eodhd_client.py --endpoint sec-filings/8k --symbol AAPL.US
```

## Notes

- API call consumption: **10 API calls per request**.
- Available on the All-In-One plan.
- JSON is the only supported response format.
- The overview endpoint is **not** paginated; the three per-form endpoints paginate via `page[offset]` (default 0) and `page[limit]` (default 20, max 100). Follow `links.next` to page through results.
- 10-K and 10-Q share the same financial schema (income statement, balance sheet, cash-flow statement). The only structural difference is the period metadata: 10-K carries `fiscal_year_end`; 10-Q carries `fiscal_quarter_end` and `fiscal_quarter`.
- Any financial field may be `null` when the underlying filing does not report that line item.
- **Form 4 is a separate product** — parsed insider transactions live at `/sec-filings/{symbol}/form4`; see `insider-transactions.md`.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Missing or invalid authentication. |
| **402** | Payment Required | API limit used up, or the plan does not include this endpoint. Upgrade plan or wait for limit reset. |
| **403** | Forbidden | Invalid API key, or the plan does not grant access. Check your `api_token`. |
| **404** | Not Found | Unknown symbol, or no filings of the requested form for this symbol. |
| **422** | Unprocessable Entity | Invalid request parameters (e.g., malformed pagination). |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

### Error Response Format

```json
{
  "error": "Error message description",
  "code": 403
}
```

### Handling Errors

**Python Example**:
```python
import requests

def make_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:
            print("Error: API limit exceeded or plan does not include this endpoint.")
        elif e.response.status_code == 403:
            print("Error: Invalid API key or insufficient plan access.")
        elif e.response.status_code == 404:
            print("Error: Symbol or filing not found.")
        elif e.response.status_code == 429:
            print("Error: Rate limit exceeded. Please slow down your requests.")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

**Best Practices**:
- Always check status codes before processing response data
- Implement exponential backoff for 429 errors
- Cache responses to reduce API calls (each request costs 10 API calls)
- Monitor your API usage in the user dashboard
