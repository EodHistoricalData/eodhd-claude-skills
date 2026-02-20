# Insider Transactions API

Status: complete
Source: financial-apis (Insider Transactions API)
Docs: https://eodhd.com/financial-apis/insider-transactions-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /insider-transactions
Method: GET
Auth: api_token (query)

## Purpose

Fetches insider trading activity including purchases, sales, and option exercises by company
executives, directors, and major shareholders. Useful for tracking insider sentiment,
identifying unusual trading patterns, and fundamental analysis.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key for authentication |
| code | No | string | Ticker symbol with exchange suffix (e.g., 'AAPL.US') |
| from | No | string (YYYY-MM-DD) | Start date for transaction data |
| to | No | string (YYYY-MM-DD) | End date for transaction data |
| limit | No | integer | Number of results to return. Default: 100 |

## Response (shape)

```json
[
  {
    "code": "AAPL.US",
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

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| code | string | Ticker symbol with exchange suffix |
| date | string (date) | Date record was added to database |
| reportDate | string (date) | SEC filing date |
| ownerName | string | Name of the insider |
| ownerCik | string | SEC Central Index Key for the insider |
| ownerTitle | string | Position/title at the company |
| transactionDate | string (date) | Date transaction was executed |
| transactionCode | string | SEC transaction code (see below) |
| transactionAmount | number | Number of shares in transaction |
| transactionPrice | number/null | Price per share (null for gifts/awards) |
| transactionAcquiredDisposed | string | 'A' (acquired) or 'D' (disposed) |
| postTransactionAmount | number | Total shares held after transaction |
| secLink | string | Link to SEC filing |

### Transaction Codes

| Code | Description |
|------|-------------|
| P | Open market or private purchase |
| S | Open market or private sale |
| A | Grant, award, or acquisition (non-purchase) |
| D | Sale to issuer |
| F | Tax withholding |
| M | Exercise of derivative security |
| C | Conversion of derivative security |
| G | Gift |
| J | Other acquisition or disposition |
| K | Equity swap or similar transaction |
| V | Transaction voluntary reported earlier than required |

### Common Owner Titles

- Chief Executive Officer (CEO)
- Chief Financial Officer (CFO)
- Chief Operating Officer (COO)
- Director
- 10% Owner (major shareholder)
- President
- General Counsel
- VP, Sales/Engineering/etc.

## Example Requests

```bash
# All recent insider transactions
curl "https://eodhd.com/api/insider-transactions?api_token=demo&fmt=json"

# Insider transactions for specific company
curl "https://eodhd.com/api/insider-transactions?code=AAPL.US&api_token=demo&fmt=json"

# Transactions for date range
curl "https://eodhd.com/api/insider-transactions?code=MSFT.US&from=2025-01-01&to=2025-01-31&api_token=demo&fmt=json"

# Limit results
curl "https://eodhd.com/api/insider-transactions?code=TSLA.US&limit=50&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint insider-transactions --symbol AAPL.US --from-date 2025-01-01 --limit 50
```

## Notes

- Insider transactions are filed with SEC within 2 business days (Form 4)
- `transactionCode` 'P' (purchase) and 'S' (sale) are most significant for sentiment
- Large purchases by multiple insiders may signal confidence
- Scheduled sales (10b5-1 plans) are less meaningful than discretionary sales
- `transactionPrice` may be null for stock grants, awards, or gifts
- Use `postTransactionAmount` to see total insider holdings
- Required fields: code, ownerName, transactionDate, transactionCode, transactionAmount
- API call consumption: 1 call per request
- **Coverage**: Data is available for the **past year** for **US companies only**, sourced from SEC Form 4 filings. Non-US markets are not covered.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

### Error Response Format

When an error occurs, the API returns a JSON response with error details:

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
