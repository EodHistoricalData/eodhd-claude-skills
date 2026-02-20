# Praams Bank Balance Sheet by ISIN API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/financial-apis/equity-risk-return-scoring-api
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/bank/balance_sheet/isin/{isin}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns the balance sheet data for a bank based on the specified ISIN code.
The response provides both annual (FY) and quarterly balance sheet data formatted
specifically for bank analysis, using a unique methodology created and validated
by CFA charterholders with 20+ years of experience in bank analysis.

This is the ISIN-based variant of the Bank Balance Sheet API. It returns the
same data structure as the ticker-based endpoint but accepts an ISIN identifier
instead. The ISIN is resolved to the corresponding bank and the same balance
sheet data is returned.

Unlike standard corporate balance sheets, this endpoint presents bank financials
in a format that reflects the business specifics of banking institutions,
including key banking metrics such as loans (gross and net with provisions),
deposits, interest-earning assets, interest-bearing liabilities, securities
REPO positions, and investment portfolio.

**Use cases**:
- Analyze bank balance sheets using ISIN identifiers for international lookups
- Track loan book growth and provisioning adequacy (gross loans, provisions, net loans)
- Monitor deposit base and funding stability
- Evaluate interest-earning assets vs interest-bearing liabilities (NIM analysis)
- Assess securities REPO positions (both asset and liability side)
- Track investment portfolio size and composition
- Analyze capital adequacy via total equity trends
- Monitor debt structure (short-term vs long-term)
- Build financial models for banking institutions

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with ISINs `US46625H1005` (JPMorgan Chase & Co), `US0605051046` (Bank of America Corporation), or `US9497461015` (Wells Fargo & Company).

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `isin` | string | ISIN code of the bank (e.g. `US46625H1005`, `US0605051046`, `US9497461015`) |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key (or `demo` for demo ISINs) |

## Response (shape)

JSON object with top-level envelope:

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` if request succeeded |
| `message` | string | Status message (empty on success) |
| `errors` | array | Error objects with `code` and `description` (empty on success) |
| `items` | array | Array of balance sheet records (annual and quarterly) |

> **Note**: The response uses `items` (plural), not `item` (singular) as in the PRAAMS equity/bond endpoints.

### `items[]` record fields

Each record in the `items` array represents one reporting period. All monetary values are in the bank's reporting currency (typically USD).

#### Period identification

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Period end date in ISO 8601 format (e.g. `"2024-12-31T00:00:00"`) |
| `period` | string | Period identifier: `"FY"` for full year, `"Q1"`–`"Q4"` for quarters |
| `isQuarter` | boolean | `true` for quarterly data, `false` for annual data |

#### Loan book

| Field | Type | Description |
|-------|------|-------------|
| `loansGross` | number \| null | Gross loans before provisions. May be absent in some older quarterly records. |
| `loanProvisions` | number \| null | Loan loss provisions (allowance for credit losses). May be absent in some older quarterly records. |
| `netLoan` | number \| null | Net loans after provisions (`loansGross - loanProvisions`). May be absent in some older quarterly records. |

#### Cash and interbank

| Field | Type | Description |
|-------|------|-------------|
| `cashAndEquivalents` | number \| null | Cash and cash equivalents. May be absent in some older quarterly records. |
| `depositsWithBanksNet` | number \| null | Net deposits with other banks. May be absent in some older quarterly records. |

#### Securities and investments

| Field | Type | Description |
|-------|------|-------------|
| `securitiesRepoAssets` | number \| null | Securities purchased under agreements to resell (repo assets). May be absent in some older quarterly records. |
| `longTermInvestments` | number | Long-term investments |
| `investmentPortfolio` | number | Investment portfolio (same value as `longTermInvestments`) |

#### Total assets

| Field | Type | Description |
|-------|------|-------------|
| `totalAssets` | number | Total assets |
| `receivables` | number | Receivables |
| `otherAssets` | number | Other assets (balancing item; may be negative) |

#### Liabilities — deposits and funding

| Field | Type | Description |
|-------|------|-------------|
| `deposits` | number \| null | Customer deposits. May be absent in some older quarterly records. |
| `securitiesRepoEquity` | number \| null | Securities sold under agreements to repurchase (repo liabilities). May be absent in some older quarterly records. |
| `tradingLiabilities` | number \| null | Trading liabilities. May be absent in some older quarterly records. |
| `securityLiabilities` | number \| null | Security liabilities (same value as `tradingLiabilities`). May be absent in some older quarterly records. |
| `payables` | number \| null | Payables. May be absent in some older quarterly records. |

#### Liabilities — debt

| Field | Type | Description |
|-------|------|-------------|
| `shortTermDebt` | number | Short-term debt |
| `longTermDebt` | number | Long-term debt |

#### Equity and totals

| Field | Type | Description |
|-------|------|-------------|
| `totalEquity` | number | Total shareholders' equity |
| `totalEquityAndLiabilities` | number | Total equity and liabilities (should equal `totalAssets`) |
| `otherLiabilities` | number | Other liabilities (balancing item; may be negative) |

#### Analytical aggregates

| Field | Type | Description |
|-------|------|-------------|
| `interestEarningAssets` | number | Total interest-earning assets |
| `interestBearingLiabilities` | number | Total interest-bearing liabilities |

## Example Request

```bash
curl "https://eodhd.com/api/mp/praams/bank/balance_sheet/isin/US46625H1005?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/praams/bank/balance_sheet/isin/US46625H1005?api_token=demo"
```

## Example Response (abbreviated)

```json
{
  "success": true,
  "message": "",
  "errors": [],
  "items": [
    {
      "date": "2024-12-31T00:00:00",
      "period": "FY",
      "isQuarter": false,
      "loansGross": 1347988000000.0,
      "loanProvisions": 24345000000.0,
      "netLoan": 1323643000000.0,
      "cashAndEquivalents": 23372000000.0,
      "depositsWithBanksNet": 445945000000.0,
      "securitiesRepoAssets": 295001000000.0,
      "longTermInvestments": 1598111000000.0,
      "totalAssets": 4002814000000.0,
      "receivables": 101223000000.0,
      "investmentPortfolio": 1598111000000.0,
      "otherAssets": 215519000000.0,
      "tradingLiabilities": 153222000000.0,
      "deposits": 2406032000000.0,
      "securitiesRepoEquity": 296835000000.0,
      "payables": 305933000000.0,
      "shortTermDebt": 64475000000.0,
      "longTermDebt": 389836000000.0,
      "totalEquity": 344758000000.0,
      "securityLiabilities": 153222000000.0,
      "totalEquityAndLiabilities": 4002814000000.0,
      "otherLiabilities": 41723000000.0,
      "interestEarningAssets": 3662700000000.0,
      "interestBearingLiabilities": 3310400000000.0
    },
    {
      "date": "2025-06-30T00:00:00",
      "period": "Q2",
      "isQuarter": true,
      "loansGross": 1411992000000.0,
      "loanProvisions": 24953000000.0,
      "netLoan": 1387039000000.0,
      "cashAndEquivalents": 23759000000.0,
      "depositsWithBanksNet": 396568000000.0,
      "securitiesRepoAssets": 470589000000.0,
      "longTermInvestments": 1647598000000.0,
      "totalAssets": 4552482000000.0,
      "receivables": 124463000000.0,
      "investmentPortfolio": 1647598000000.0,
      "otherAssets": 502466000000.0,
      "tradingLiabilities": 173292000000.0,
      "deposits": 2562380000000.0,
      "securitiesRepoEquity": 595340000000.0,
      "payables": 48110000000.0,
      "shortTermDebt": 65293000000.0,
      "longTermDebt": 419802000000.0,
      "totalEquity": 356924000000.0,
      "securityLiabilities": 173292000000.0,
      "totalEquityAndLiabilities": 4552482000000.0,
      "otherLiabilities": 331341000000.0,
      "interestEarningAssets": 3901794000000.0,
      "interestBearingLiabilities": 3816107000000.0
    },
    {
      "date": "2020-12-31T00:00:00",
      "period": "Q4",
      "isQuarter": true,
      "longTermInvestments": 1186346000000.0,
      "totalAssets": 3384757000000.0,
      "receivables": 90503000000.0,
      "investmentPortfolio": 1186346000000.0,
      "otherAssets": 2107908000000.0,
      "shortTermDebt": 260417000000.0,
      "longTermDebt": 281685000000.0,
      "totalEquity": 279354000000.0,
      "totalEquityAndLiabilities": 3384757000000.0,
      "otherLiabilities": 2563301000000.0,
      "interestEarningAssets": 1186346000000.0,
      "interestBearingLiabilities": 542102000000.0
    }
  ]
}
```

## Notes

- **Marketplace product**: Requires a separate PRAAMS Bank Financials marketplace subscription, not included in main EODHD plans.
- **ISIN-based variant**: This endpoint returns identical data to the ticker-based endpoint (`/bank/balance_sheet/ticker/{ticker}`) but accepts an ISIN code instead. For example, `US46625H1005` resolves to the same data as ticker `JPM`.
- **Bank-specific format**: Unlike standard corporate balance sheets, this endpoint uses a banking-specific methodology. Key banking metrics include Loans (gross/net with provisions), Deposits, Securities REPO (assets and liabilities), Investment Portfolio, Interest-Earning Assets, and Interest-Bearing Liabilities.
- **Demo ISINs**: `US46625H1005` (JPMorgan Chase), `US0605051046` (Bank of America), and `US9497461015` (Wells Fargo) are available with `api_token=demo`.
- **Coverage**: All regional and global banks and banking financial institutions, including banking conglomerates from North America, Europe, UK, and Asia.
- **Mixed annual and quarterly data**: The `items` array contains both FY (annual) and Q1–Q4 (quarterly) records. Use `isQuarter` or `period` to filter.
- **Record ordering**: Records are returned with annual (FY) records first, followed by quarterly records. Within each group, records are ordered chronologically by `date`.
- **Incomplete older quarterly records**: Some older quarterly records (particularly Q4 2020, Q4 2021) contain significantly fewer fields — typically only `longTermInvestments`, `investmentPortfolio`, `totalAssets`, `receivables`, `otherAssets`, `shortTermDebt`, `longTermDebt`, `totalEquity`, `totalEquityAndLiabilities`, `otherLiabilities`, `interestEarningAssets`, and `interestBearingLiabilities`. Fields like `loansGross`, `netLoan`, `deposits`, `cashAndEquivalents`, `depositsWithBanksNet`, `securitiesRepoAssets`, `tradingLiabilities`, `securitiesRepoEquity`, and `payables` are absent in these records.
- **Balancing items**: `otherAssets` and `otherLiabilities` serve as balancing items and may be negative. In older quarterly records with fewer breakdowns, these values can be very large as they absorb all unbroken-out items.
- **Duplicate fields**: `investmentPortfolio` always equals `longTermInvestments`. `securityLiabilities` always equals `tradingLiabilities`. Both pairs are provided for convenience.
- **Balance sheet identity**: `totalAssets` should equal `totalEquityAndLiabilities` in each record.
- **Key metric definitions**:
  - **Net Loans** = Gross Loans − Loan Provisions
  - **Interest-Earning Assets** = assets that generate interest income (loans, investments, interbank deposits, repo assets)
  - **Interest-Bearing Liabilities** = liabilities that incur interest expense (deposits, debt, repo liabilities)
  - **NIM proxy**: Use `interestEarningAssets` and `interestBearingLiabilities` together with income statement data to compute net interest margin
- **Currency**: All monetary values are in the bank's reporting currency (USD for US banks).
- **Related endpoints**: Use the Bank Balance Sheet by Ticker endpoint for ticker-based lookups (see praams-bank-balance-sheet-by-ticker.md). Use the Bank Income Statement endpoints for complementary income statement data.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **415** | Wrong Token | Token format is invalid. |
| **420** | Operation Cancelled | Request was cancelled. |
| **430** | Data Not Found | ISIN not found in PRAAMS bank database. |

### Error Response Format

When an error occurs, the API returns a JSON response:

```json
{
  "success": false,
  "message": "Error description",
  "errors": [
    {
      "code": "ERROR_CODE",
      "description": "Detailed error description"
    }
  ],
  "items": null
}
```

### Handling Errors

**Python Example**:
```python
import requests

def make_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get("success"):
            errors = data.get("errors", [])
            for err in errors:
                print(f"API Error [{err.get('code')}]: {err.get('description')}")
            return None
        return data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Error: Invalid API key. Check your credentials.")
        elif e.response.status_code == 415:
            print("Error: Wrong token format.")
        elif e.response.status_code == 430:
            print("Error: ISIN not found in PRAAMS bank database.")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

**Best Practices**:
- Always check `success` field in the response before processing `items`
- Implement exponential backoff for rate limit errors
- Cache responses to reduce API calls — bank financials update quarterly
- Use `isQuarter` to separate annual and quarterly data for analysis
- Monitor your API usage in the user dashboard
