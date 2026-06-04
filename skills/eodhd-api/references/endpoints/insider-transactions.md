# Insider Transactions API

Status: complete
Source: financial-apis (Insider Transactions API)
Docs: https://eodhd.com/financial-apis/insider-transactions-api
Provider: EODHD
Base URL: https://eodhd.com/api
Method: GET
Auth: api_token (query)

## Purpose

Fetches insider trading activity — purchases, sales, option exercises, grants, and gifts by
company executives, directors, and major shareholders. Useful for tracking insider sentiment,
identifying unusual trading patterns, and fundamental analysis.

EODHD exposes insider data through **two endpoints**:

| Endpoint | Path | Schema | Source | Use when |
|----------|------|--------|--------|----------|
| **SEC Form 4** (recommended) | `/sec-filings/{symbol}/form4` | Nested per-filing (non-derivative + derivative + footnotes) | SEC EDGAR Form 4 | You want the full filing detail, derivative transactions, footnotes, and deep history |
| **Legacy flat feed** | `/insider-transactions` | Flat per-transaction rows | EODHD aggregated feed | You want a simple flat list or a market-wide recent feed |

> **Coverage note (verified):** the two feeds do not always overlap. As of mid-2026, some large
> caps (e.g. `AAPL.US`) return data from the Form 4 endpoint but an empty array from the legacy
> flat feed, while others (e.g. `MSFT.US`, `TSLA.US`) return rows from both. For complete, current
> coverage prefer the **SEC Form 4** endpoint.

---

## Endpoint 1 (recommended): SEC Form 4

```
GET https://eodhd.com/api/sec-filings/{symbol}/form4
```

Returns SEC Form 4 filings (statements of changes in beneficial ownership), sourced directly from
SEC EDGAR, sorted by `filed_at` descending. Each filing carries both non-derivative (direct stock)
and derivative (options, RSUs, warrants) transaction arrays plus referenced footnotes.

### Parameters

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| api_token | Yes | string | — | Your API key |
| {symbol} | Yes | string (path) | — | US ticker, e.g. `AAPL` or `AAPL.US` (case-insensitive) |
| page[offset] | No | integer | 0 | Zero-based pagination offset |
| page[limit] | No | integer | 20 | Page size, range 1–100 |
| fmt | No | string | json | Output format |

### Response (shape)

```json
{
  "data": [
    {
      "accession_number": "0001140361-26-023363",
      "filed_at": "2026-05-29",
      "period_of_report": "2026-05-27",
      "non_derivative": [
        {
          "reporting_owner_cik": "0001214128",
          "reporting_owner_name": "LEVINSON ARTHUR D",
          "is_director": true,
          "is_officer": false,
          "is_ten_percent_owner": false,
          "is_other": false,
          "officer_title": null,
          "other_text": null,
          "security_title": "Common Stock",
          "transaction_date": "2026-05-27T00:00:00+00:00",
          "transaction_code": "S",
          "acquired_or_disposed": "D",
          "shares_amount": 50000,
          "price_per_share": 311.02,
          "shares_owned_after": 3764576,
          "total_value": 15551000
        }
      ],
      "derivative": [],
      "footnotes": [
        {
          "footnote_id": "F1",
          "text": "This transaction was executed in multiple trades at prices ranging from $310.76 to $311.42; the price reported above reflects the weighted average sale price."
        }
      ]
    }
  ],
  "meta": { "total": 595, "page": { "offset": 0, "limit": 1 } },
  "links": { "next": "https://eodhd.com/api/sec-filings/AAPL.US/form4?page%5Boffset%5D=1&page%5Blimit%5D=1" }
}
```

### Filing object

| Field | Type | Description |
|-------|------|-------------|
| accession_number | string | Unique SEC filing identifier |
| filed_at | string (date) | Submission date (YYYY-MM-DD) |
| period_of_report | string (date) | Reporting period (YYYY-MM-DD) |
| non_derivative | array | Direct stock transactions (see below) |
| derivative | array | Options, RSUs, warrants (see below) |
| footnotes | array | Referenced footnote objects (`footnote_id`, `text`) |

### Non-derivative transaction fields

| Field | Type | Description |
|-------|------|-------------|
| reporting_owner_cik | string | SEC Central Index Key of the insider |
| reporting_owner_name | string | Insider name |
| is_director | boolean | Board director |
| is_officer | boolean | Officer |
| is_ten_percent_owner | boolean | 10%+ owner |
| is_other | boolean | Other relationship |
| officer_title | string/null | Title if officer |
| other_text | string/null | Description of "other" relationship |
| security_title | string | Security name (e.g. "Common Stock") |
| transaction_date | string (datetime) | ISO-8601 transaction timestamp |
| transaction_code | string | SEC Section 16 code (see below) |
| acquired_or_disposed | string | 'A' (acquired) or 'D' (disposed) |
| shares_amount | number | Shares transacted |
| price_per_share | number/null | Price per share (0/null for gifts, awards) |
| shares_owned_after | number | Holdings after the transaction |
| total_value | number/null | Computed transaction value |

### Derivative transaction fields

| Field | Type | Description |
|-------|------|-------------|
| reporting_owner_cik | string | SEC CIK |
| reporting_owner_name | string | Insider name |
| security_title | string | Derivative name (e.g. "Non-Qualified Stock Option") |
| conversion_or_exercise_price | number/null | Exercise price |
| transaction_date | string (datetime) | ISO-8601 timestamp |
| transaction_code | string | SEC code |
| acquired_or_disposed | string | 'A' or 'D' |
| shares_amount | number | Derivative units transacted |
| price_per_share | number/null | Price per unit |
| shares_owned_after | number | Units held after the transaction |
| underlying_security_title | string/null | Underlying security |
| underlying_shares | number/null | Underlying share count |
| exercise_date | string (datetime)/null | Exercisability date |
| expiration_date | string (datetime)/null | Expiration date |

### Pagination

Forward navigation via `links.next` (a ready-to-use URL) and `meta.total` / `meta.page`. There is
no backward navigation; walk forward by following `links.next` or incrementing `page[offset]`.

### Example requests

```bash
# Most recent Form 4 filings for a company
curl "https://eodhd.com/api/sec-filings/AAPL.US/form4?api_token=YOUR_API_TOKEN&fmt=json"

# Page through results (offset/limit)
curl "https://eodhd.com/api/sec-filings/AAPL.US/form4?page%5Boffset%5D=20&page%5Blimit%5D=20&api_token=YOUR_API_TOKEN&fmt=json"
```

### Coverage & cost (Form 4)

- **Markets:** US-listed issuers only (Form 4 filers), sourced daily from SEC EDGAR.
- **History:** uneven — from ~12 months for recently-added tickers to 10+ years for major large caps.
- **API call consumption:** 10 calls per request.
- **Required plan:** Fundamentals Data Feed or All-In-One.

---

## Endpoint 2 (legacy flat feed): `/insider-transactions`

```
GET https://eodhd.com/api/insider-transactions
```

A simpler, flat per-transaction feed. Still operational; convenient for a market-wide recent feed
or a flat per-ticker list. For complete current coverage of a given issuer, prefer the Form 4
endpoint above.

### Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| code | No | string | Ticker symbol with exchange suffix (e.g. 'AAPL.US'). Omit for the market-wide recent feed |
| from | No | string (YYYY-MM-DD) | Start date |
| to | No | string (YYYY-MM-DD) | End date |
| limit | No | integer | Number of results. Default: 100 |
| fmt | No | string | 'json' or 'csv'. Default: 'json' |

### Response (shape)

```json
[
  {
    "code": "MSFT.US",
    "date": "2025-01-15",
    "reportDate": "2025-01-17",
    "ownerName": "John Smith",
    "ownerCik": "0001234567",
    "ownerTitle": "Chief Executive Officer",
    "transactionDate": "2025-01-15",
    "transactionCode": "P",
    "transactionAmount": 5000,
    "transactionPrice": 185.50,
    "transactionAcquiredDisposed": "A",
    "postTransactionAmount": 150000,
    "secLink": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=..."
  }
]
```

### Field descriptions

| Field | Type | Description |
|-------|------|-------------|
| code | string | Ticker symbol with exchange suffix |
| date | string (date) | Date record was added to the database |
| reportDate | string (date) | SEC filing date |
| ownerName | string | Name of the insider |
| ownerCik | string | SEC Central Index Key for the insider |
| ownerTitle | string | Position/title at the company |
| transactionDate | string (date) | Date the transaction was executed |
| transactionCode | string | SEC transaction code (see below) |
| transactionAmount | number | Number of shares in the transaction |
| transactionPrice | number/null | Price per share (null for gifts/awards) |
| transactionAcquiredDisposed | string | 'A' (acquired) or 'D' (disposed) |
| postTransactionAmount | number | Total shares held after the transaction |
| secLink | string | Link to the SEC filing |

### Example requests

```bash
# Market-wide recent insider transactions
curl "https://eodhd.com/api/insider-transactions?api_token=YOUR_API_TOKEN&fmt=json"

# Insider transactions for a specific company
curl "https://eodhd.com/api/insider-transactions?code=MSFT.US&api_token=YOUR_API_TOKEN&fmt=json"

# Date range
curl "https://eodhd.com/api/insider-transactions?code=MSFT.US&from=2025-01-01&to=2025-01-31&api_token=YOUR_API_TOKEN&fmt=json"

# Using the helper client (legacy flat feed)
python eodhd_client.py --endpoint insider-transactions --symbol MSFT.US --from-date 2025-01-01 --limit 50
```

> The bundled Python client implements the **legacy flat feed** (`--endpoint insider-transactions`).
> For the Form 4 endpoint, call it directly with `curl` or the MCP server.

### Coverage (legacy feed)

- **Markets:** US companies, sourced from SEC Form 4 filings via the EODHD aggregated feed.
- **History:** approximately the past year.
- **API call consumption:** 1 call per request.

---

## Transaction codes (SEC Section 16)

| Code | Description |
|------|-------------|
| P | Open-market or private purchase |
| S | Open-market or private sale |
| A | Grant, award, or other acquisition |
| D | Disposition to the issuer (e.g. under a plan) |
| F | Payment of exercise price or tax via share withholding |
| M | Exercise or conversion of a derivative security |
| C | Conversion of a derivative security |
| G | Bona fide gift |
| V | Transaction voluntarily reported earlier than required |
| J | Other acquisition or disposition (footnoted) |
| L | Small acquisition under Rule 16a-6 |
| E | Expiration of a short derivative position |
| H | Expiration of a long derivative position |
| O | Exercise of an out-of-the-money derivative |
| X | Exercise of an in-the-money or at-the-money derivative |

### Common owner titles

CEO, CFO, COO, Director, President, General Counsel, 10% Owner (major shareholder), VP (various).

## Analysis notes

- Insider transactions are filed with the SEC within 2 business days (Form 4).
- Codes `P` (purchase) and `S` (sale) are the most significant for sentiment.
- Large purchases by multiple insiders may signal confidence.
- Scheduled sales (Rule 10b5-1 plans) are less meaningful than discretionary sales.
- `price_per_share` / `transactionPrice` may be 0 or null for stock grants, awards, or gifts.
- Use `shares_owned_after` / `postTransactionAmount` to see total insider holdings.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Missing or invalid token. |
| **402** | Payment Required | API limit used up, or your plan lacks endpoint access. |
| **403** | Forbidden | Invalid API key or plan lacks endpoint access. |
| **404** | Not Found | Ticker not found (non-US or unknown symbol). |
| **422** | Unprocessable Entity | Validation error (e.g. bad pagination parameter). |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down. |

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
            print("Error: API limit exceeded. Please upgrade your plan.")
        elif e.response.status_code == 403:
            print("Error: Invalid API key. Check your credentials.")
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
- Cache responses to reduce API calls
- Monitor your API usage in the user dashboard
