# Praams Bank Income Statement by Ticker API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/financial-apis/equity-risk-return-scoring-api
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/bank/income_statement/ticker/{ticker}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns the income statement data for a bank based on the specified ticker
symbol. The response provides both annual (FY) and quarterly financial data
formatted specifically for bank analysis, using a unique methodology created
and validated by CFA charterholders with 20+ years of experience in bank
analysis.

Unlike standard corporate income statements, this endpoint presents bank
financials in a format that reflects the business specifics of banking
institutions, including key banking metrics such as net interest income,
net fee & commission income, RIBPT, IBPT, and provisioning.

**Use cases**:
- Analyze bank income statements in a proper banking format (not corporate format)
- Track core revenue trends (net interest income + net fee & commission income)
- Monitor net interest income and interest margin dynamics
- Evaluate provisioning levels and credit loss trends
- Assess recurring vs non-recurring income composition
- Compare RIBPT (Recurring Income Before Provisioning and Taxes) across periods
- Track dividend per share (DPS) history
- Analyze quarterly and annual financial trends for banks
- Build financial models for banking institutions

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with tickers `JPM` (JPMorgan Chase & Co), `BAC` (Bank of America Corporation), or `WFC` (Wells Fargo & Company).

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticker` | string | Ticker symbol for the bank (e.g. `JPM`, `BAC`, `WFC`) |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key (or `demo` for demo tickers) |

## Response (shape)

JSON object with top-level envelope:

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` if request succeeded |
| `message` | string | Status message (empty on success) |
| `errors` | array | Error objects with `code` and `description` (empty on success) |
| `items` | array | Array of income statement records (annual and quarterly) |

> **Note**: The response uses `items` (plural), not `item` (singular) as in the PRAAMS equity/bond endpoints.

### `items[]` record fields

Each record in the `items` array represents one reporting period. All monetary values are in the bank's reporting currency (typically USD).

#### Period identification

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Period end date in ISO 8601 format (e.g. `"2024-12-31T00:00:00"`) |
| `period` | string | Period identifier: `"FY"` for full year, `"Q1"`–`"Q4"` for quarters |
| `isQuarter` | boolean | `true` for quarterly data, `false` for annual data |

#### Revenue and income metrics

| Field | Type | Description |
|-------|------|-------------|
| `interestIncome` | number | Total interest income |
| `interestExpense` | number | Total interest expense |
| `netInterestIncome` | number | Net interest income (`interestIncome - interestExpense`) |
| `netFeeAndCommission` | number \| null | Net fee and commission income. May be absent in some quarterly records. |
| `coreRevenue` | number \| null | Core revenue (`netInterestIncome + netFeeAndCommission`). May be absent when `netFeeAndCommission` is not broken out. |
| `nonRecurringIncome` | number \| null | Non-recurring/non-operating income. May be absent in some quarterly records. |

#### Profitability metrics

| Field | Type | Description |
|-------|------|-------------|
| `ribpt` | number \| null | Recurring Income Before Provisioning and Taxes. May be absent in some quarterly records. |
| `ibpt` | number | Income Before Provisioning and Taxes |
| `preTaxProfit` | number | Pre-tax profit (income before taxes) |
| `incomeTaxExpense` | number | Income tax expense |
| `netProfit` | number | Net profit (bottom line) |

#### Provisioning and credit losses

| Field | Type | Description |
|-------|------|-------------|
| `creditLossesProvision` | number | Credit loss provisions (negative = provision charge, positive = provision release) |
| `provisioning` | number | Provisioning amount (positive = provision charge, negative = provision release). Inverse sign convention from `creditLossesProvision`. |

#### Expenses

| Field | Type | Description |
|-------|------|-------------|
| `nonInterestExpenses` | number | Total non-interest expenses (operating expenses) |
| `operatingExpenses` | number | Operating expenses (same value as `nonInterestExpenses`) |

#### Special items and dividends

| Field | Type | Description |
|-------|------|-------------|
| `specialIncomeCharges` | number \| null | Special/one-time income or charges (positive = income, negative = charge). Not present in all records. |
| `dps` | number | Dividend per share for the period |

## Example Request

```bash
curl "https://eodhd.com/api/mp/praams/bank/income_statement/ticker/JPM?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/praams/bank/income_statement/ticker/JPM?api_token=demo"
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
      "netFeeAndCommission": 39835000000.0,
      "creditLossesProvision": -10654000000.0,
      "specialIncomeCharges": 5851000000.0,
      "nonInterestExpenses": 89555000000.0,
      "interestIncome": 193933000000.0,
      "interestExpense": 101350000000.0,
      "incomeTaxExpense": 16610000000.0,
      "netProfit": 58471000000.0,
      "dps": 4.60000,
      "provisioning": 4803000000.0,
      "operatingExpenses": 89555000000.0,
      "netInterestIncome": 92583000000.0,
      "coreRevenue": 132418000000.0,
      "ribpt": 42863000000.0,
      "preTaxProfit": 75081000000.0,
      "ibpt": 79884000000.0,
      "nonRecurringIncome": 37021000000.0
    },
    {
      "date": "2024-12-31T00:00:00",
      "period": "Q4",
      "isQuarter": true,
      "netFeeAndCommission": 10669000000.0,
      "creditLossesProvision": -2654000000.0,
      "specialIncomeCharges": -1123000000.0,
      "nonInterestExpenses": 21639000000.0,
      "interestIncome": 47566000000.0,
      "interestExpense": 24216000000.0,
      "incomeTaxExpense": 3370000000.0,
      "netProfit": 14005000000.0,
      "dps": 1.25000,
      "provisioning": 3777000000.0,
      "operatingExpenses": 21639000000.0,
      "netInterestIncome": 23350000000.0,
      "coreRevenue": 34019000000.0,
      "ribpt": 12380000000.0,
      "preTaxProfit": 17375000000.0,
      "ibpt": 21152000000.0,
      "nonRecurringIncome": 8772000000.0
    },
    {
      "date": "2025-03-31T00:00:00",
      "period": "Q1",
      "isQuarter": true,
      "netFeeAndCommission": 10359000000.0,
      "creditLossesProvision": -3322000000.0,
      "specialIncomeCharges": -444000000.0,
      "nonInterestExpenses": 23153000000.0,
      "interestIncome": 46853000000.0,
      "interestExpense": 23580000000.0,
      "incomeTaxExpense": 3765000000.0,
      "netProfit": 14643000000.0,
      "dps": 1.25000,
      "provisioning": 3766000000.0,
      "operatingExpenses": 23153000000.0,
      "netInterestIncome": 23273000000.0,
      "coreRevenue": 33632000000.0,
      "ribpt": 10479000000.0,
      "preTaxProfit": 18408000000.0,
      "ibpt": 22174000000.0,
      "nonRecurringIncome": 11695000000.0
    }
  ]
}
```

## Notes

- **Marketplace product**: Requires a separate PRAAMS Bank Financials marketplace subscription, not included in main EODHD plans.
- **Bank-specific format**: Unlike standard corporate income statements, this endpoint uses a banking-specific methodology that correctly represents bank financials. Key banking metrics include Net Interest Income, Net Fee & Commission Income, RIBPT, IBPT, and Provisioning.
- **Demo tickers**: `JPM` (JPMorgan Chase), `BAC` (Bank of America), and `WFC` (Wells Fargo) are available with `api_token=demo`.
- **Coverage**: All regional and global banks and banking financial institutions, including banking conglomerates from North America, Europe, UK, and Asia.
- **Mixed annual and quarterly data**: The `items` array contains both FY (annual) and Q1–Q4 (quarterly) records. Use `isQuarter` or `period` to filter.
- **Record ordering**: Records are returned with annual (FY) records first, followed by quarterly records. Within each group, records are ordered chronologically by `date`.
- **Incomplete quarterly records**: Some older quarterly records (particularly Q4 and early quarters) may lack certain fields like `netFeeAndCommission`, `coreRevenue`, `ribpt`, and `nonRecurringIncome`. These fields are simply absent from those records, not null.
- **Provisioning sign conventions**: `creditLossesProvision` uses negative for charges and positive for releases. `provisioning` uses the opposite convention (positive for charges, negative for releases). Both represent the same underlying data.
- **Quarterly scaling anomaly**: Some older quarterly records (e.g. Q4 2020, Q4 2021, Q4 2022) may show `nonInterestExpenses`, `operatingExpenses`, `creditLossesProvision`, and `provisioning` scaled by a factor of 100x compared to expected values. This appears to be a data presentation characteristic — use the annual (FY) figures as the authoritative source.
- **specialIncomeCharges**: This field is not present in all records. When present, positive values represent one-time income and negative values represent one-time charges.
- **Key metric definitions**:
  - **Core Revenue** = Net Interest Income + Net Fee & Commission Income
  - **RIBPT** (Recurring Income Before Provisioning and Taxes) = Core Revenue − Operating Expenses
  - **IBPT** (Income Before Provisioning and Taxes) = RIBPT + Non-Recurring Income
  - **Net Interest Income** = Interest Income − Interest Expense
- **Currency**: All monetary values are in the bank's reporting currency (USD for US banks).
- **Related endpoints**: Use the Bank Balance Sheet endpoint for the complementary balance sheet data. Use the Bank Income Statement by ISIN endpoint for ISIN-based lookups.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **415** | Wrong Token | Token format is invalid. |
| **420** | Operation Cancelled | Request was cancelled. |
| **430** | Data Not Found | Ticker not found in PRAAMS bank database. |

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
            print("Error: Ticker not found in PRAAMS bank database.")
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
