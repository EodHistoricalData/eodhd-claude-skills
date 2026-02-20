# Historical Financial Ratios Calculation Guide

**Purpose**: Calculate financial ratios using EODHD Fundamentals API
**Last Updated**: 2024-11-27
**Data Source**: EODHD Fundamentals API, End-of-Day API

---

## Table of Contents

1. [Overview](#overview)
2. [Discovering Available Fields](#discovering-available-fields)
3. [Data Requirements](#data-requirements)
4. [Valuation Ratios](#valuation-ratios)
5. [Profitability Ratios](#profitability-ratios)
6. [Liquidity Ratios](#liquidity-ratios)
7. [Leverage Ratios](#leverage-ratios)
8. [Efficiency Ratios](#efficiency-ratios)
9. [Return Ratios](#return-ratios)
10. [Per-Share Metrics](#per-share-metrics)
11. [Complete Ratio List](#complete-ratio-list)
12. [Python Implementation](#python-implementation)
13. [Best Practices](#best-practices)

---

## Overview

### What This Guide Covers

This guide provides **step-by-step calculations** for 33+ financial ratios using EODHD API data. Each ratio includes:

- **Formula** - Mathematical definition
- **API Endpoints** - Exact queries to retrieve data
- **Python Code** - Working implementation
- **Examples** - Real calculations with AAPL data
- **Interpretation** - What the ratio means

### Key Capabilities

**Calculate Any Ratio**: Not limited to the 33 ratios listed - any ratio calculable from EODHD data can be computed using the same methodology.

**Historical Analysis**: Calculate ratios for any historical period (quarterly or yearly).

**Third-Party Integration**: Can combine with third-party data sources for additional metrics.

**Flexible Periods**: Support for quarterly, yearly, and trailing-twelve-month (TTM) calculations.

### Data Sources

**Primary Source**: EODHD Fundamentals API
- Balance Sheet data
- Income Statement data
- Cash Flow Statement data
- Earnings history

**Secondary Source**: EODHD End-of-Day API
- Historical stock prices
- Adjusted close prices

---

## Discovering Available Fields

### Get Data Schema

To discover all available fields in financial statements, request **data for a single period** across all statements:

**API Query**:
```bash
https://eodhd.com/api/fundamentals/AMZN.US?api_token=demo&fmt=json&filter=Financials::Income_Statement::quarterly::2020-12-31,Financials::Balance_Sheet::quarterly::2020-12-31,Financials::Cash_Flow::quarterly::2020-12-31
```

This returns field names for:
- Income Statement
- Balance Sheet
- Cash Flow Statement

**Response Structure**:
```json
{
  "Financials": {
    "Income_Statement": {
      "quarterly": {
        "2020-12-31": {
          "date": "2020-12-31",
          "totalRevenue": 125555000000,
          "costOfRevenue": 84732000000,
          "grossProfit": 40823000000,
          "operatingIncome": 6873000000,
          "netIncome": 7222000000,
          ...
        }
      }
    },
    "Balance_Sheet": {
      "quarterly": {
        "2020-12-31": {
          "date": "2020-12-31",
          "totalAssets": 321195000000,
          "totalCurrentAssets": 132733000000,
          "totalLiab": 227791000000,
          "totalStockholderEquity": 93404000000,
          ...
        }
      }
    },
    "Cash_Flow": {
      "quarterly": {
        "2020-12-31": {
          "date": "2020-12-31",
          "totalCashFromOperatingActivities": 38514000000,
          "freeCashFlow": 30905000000,
          "capitalExpenditures": -7609000000,
          ...
        }
      }
    }
  }
}
```

### Python Example

```python
import requests

def discover_available_fields(ticker, period_date, api_token):
    """
    Discover all available fields for a company's financial statements.

    Args:
        ticker: Stock ticker (e.g., 'AMZN.US')
        period_date: Period end date (e.g., '2020-12-31')
        api_token: Your API token

    Returns:
        Dict with all available fields
    """
    url = f"https://eodhd.com/api/fundamentals/{ticker}"

    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}",
        f"Financials::Balance_Sheet::quarterly::{period_date}",
        f"Financials::Cash_Flow::quarterly::{period_date}"
    ]

    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extract field names
    fields = {
        "income_statement": list(data["Financials"]["Income_Statement"]["quarterly"][period_date].keys()),
        "balance_sheet": list(data["Financials"]["Balance_Sheet"]["quarterly"][period_date].keys()),
        "cash_flow": list(data["Financials"]["Cash_Flow"]["quarterly"][period_date].keys())
    }

    return fields

# Usage
fields = discover_available_fields('AMZN.US', '2020-12-31', 'demo')
print("Income Statement Fields:", fields['income_statement'])
print("Balance Sheet Fields:", fields['balance_sheet'])
print("Cash Flow Fields:", fields['cash_flow'])
```

---

## Data Requirements

### Common Data Points

Most ratio calculations require these data points:

**From Balance Sheet**:
- `totalAssets`
- `totalCurrentAssets`
- `totalLiab` (Total Liabilities)
- `totalCurrentLiabilities`
- `totalStockholderEquity`
- `commonStockSharesOutstanding`
- `longTermDebt`
- `shortTermDebt`
- `cashAndEquivalents`
- `intangibleAssets`

**From Income Statement**:
- `totalRevenue`
- `grossProfit`
- `operatingIncome`
- `ebit` (Earnings Before Interest and Taxes)
- `ebitda`
- `netIncome`
- `costOfRevenue`
- `totalOperatingExpenses`
- `interestExpense`

**From Cash Flow Statement**:
- `totalCashFromOperatingActivities`
- `freeCashFlow`
- `capitalExpenditures`
- `dividendsPaid`

**From End-of-Day API**:
- `close` (closing price)
- `adjusted_close` (adjusted for splits & dividends)

**From Earnings**:
- `epsActual` (Earnings Per Share)

### Period Types

**Quarterly**: Most recent quarter data
```
filter=Financials::Balance_Sheet::quarterly::2020-12-31
```

**Yearly**: Annual data
```
filter=Financials::Balance_Sheet::yearly::2020-12-31
```

**Trailing Twelve Months (TTM)**: Sum of last 4 quarters (calculate manually)

---

## Valuation Ratios

Valuation ratios help determine if a stock is over or undervalued.

### 1. Market Capitalization

**Formula**:
```
Market Cap = Outstanding Shares × Price
```

**API Endpoints**:
```bash
# Outstanding Shares
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=Financials::Balance_Sheet::quarterly::{PERIOD_END_DATE}::commonStockSharesOutstanding

# Price
https://eodhd.com/api/eod/{TICKER}?api_token={API_TOKEN}&fmt=json&from={DATE}&to={DATE}&filter=close
```

**Python Implementation**:
```python
def calculate_market_cap(ticker, period_date, api_token):
    """Calculate Market Capitalization."""
    # Get shares outstanding
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding"
    }
    response = requests.get(url, params=params).json()
    shares = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["commonStockSharesOutstanding"]

    # Get price (use same date or closest trading day)
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    eod_params = {
        "api_token": api_token,
        "fmt": "json",
        "from": period_date,
        "to": period_date,
        "filter": "close"
    }
    price_data = requests.get(eod_url, params=eod_params).json()
    price = price_data[0]["close"]

    # Calculate
    market_cap = shares * price

    return {
        "market_cap": market_cap,
        "shares": shares,
        "price": price,
        "market_cap_billions": market_cap / 1e9
    }

# Example: AAPL on 2020-12-30
result = calculate_market_cap('AAPL.US', '2020-12-31', 'demo')
print(f"Market Cap: ${result['market_cap_billions']:.2f}B")
# Output: Market Cap: $2,288.48B
```

**Example (AAPL Q4 2020)**:
```
Outstanding Shares: 17,114,000,000
Close Price: $133.72
Market Cap = 17,114,000,000 × 133.72 = $2,288,484,080,000
```

**Interpretation**:
- **Large Cap**: > $10B
- **Mid Cap**: $2B - $10B
- **Small Cap**: $300M - $2B
- **Micro Cap**: < $300M

---

### 2. Price-to-Earnings Ratio (P/E)

**Formula**:
```
P/E Ratio = Market Price per Share / Earnings per Share
```

**API Endpoints**:
```bash
# EPS
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=Earnings::History::{PERIOD_END_DATE}::epsActual

# Adjusted Close
https://eodhd.com/api/eod/{TICKER}?api_token={API_TOKEN}&fmt=json&from={DATE}&to={DATE}&filter=adjusted_close
```

**Python Implementation**:
```python
def calculate_pe_ratio(ticker, period_date, price_date, api_token):
    """Calculate P/E Ratio."""
    # Get EPS
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": f"Earnings::History::{period_date}::epsActual"
    }
    response = requests.get(url, params=params).json()
    eps = response["Earnings"]["History"][period_date]["epsActual"]

    # Get adjusted close
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    eod_params = {
        "api_token": api_token,
        "fmt": "json",
        "from": price_date,
        "to": price_date,
        "filter": "adjusted_close"
    }
    price_data = requests.get(eod_url, params=eod_params).json()
    adjusted_close = price_data[0]["adjusted_close"]

    # Calculate
    pe_ratio = adjusted_close / eps

    return {
        "pe_ratio": pe_ratio,
        "eps": eps,
        "price": adjusted_close
    }

# Example: AAPL on 2020-12-30
result = calculate_pe_ratio('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"P/E Ratio: {result['pe_ratio']:.2f}")
# Output: P/E Ratio: 77.92
```

**Example (AAPL Q4 2020)**:
```
EPS: $1.68
Adjusted Close: $130.90
P/E = 130.90 / 1.68 = 77.92
```

**Interpretation**:
- **< 15**: Undervalued or slow growth
- **15-25**: Fair value for mature companies
- **> 25**: Growth stock or overvalued
- **Negative**: Company losing money

---

### 3. Price-to-Book Ratio (P/B)

**Formula**:
```
P/B Ratio = Market Price per Share / Book Value per Share

Where:
Book Value = Total Assets - Total Liabilities
BVPS = Book Value / Shares Outstanding
```

**API Endpoints**:
```bash
# Total Assets
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=Financials::Balance_Sheet::quarterly::{PERIOD_END_DATE}::totalAssets

# Total Liabilities
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=Financials::Balance_Sheet::quarterly::{PERIOD_END_DATE}::totalLiab

# Shares Outstanding
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=Financials::Balance_Sheet::quarterly::{PERIOD_END_DATE}::commonStockSharesOutstanding

# Adjusted Close
https://eodhd.com/api/eod/{TICKER}?api_token={API_TOKEN}&fmt=json&from={DATE}&to={DATE}&filter=adjusted_close
```

**Python Implementation**:
```python
def calculate_pb_ratio(ticker, period_date, price_date, api_token):
    """Calculate P/B Ratio."""
    # Get balance sheet data
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalLiab",
        f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    bs_data = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]

    total_assets = bs_data["totalAssets"]
    total_liab = bs_data["totalLiab"]
    shares = bs_data["commonStockSharesOutstanding"]

    # Calculate Book Value per Share
    book_value = total_assets - total_liab
    bvps = book_value / shares

    # Get price
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    eod_params = {
        "api_token": api_token,
        "fmt": "json",
        "from": price_date,
        "to": price_date,
        "filter": "adjusted_close"
    }
    price_data = requests.get(eod_url, params=eod_params).json()
    adjusted_close = price_data[0]["adjusted_close"]

    # Calculate P/B Ratio
    pb_ratio = adjusted_close / bvps

    return {
        "pb_ratio": pb_ratio,
        "book_value": book_value,
        "bvps": bvps,
        "price": adjusted_close
    }

# Example: AAPL on 2020-12-30
result = calculate_pb_ratio('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"P/B Ratio: {result['pb_ratio']:.2f}")
# Output: P/B Ratio: 33.83
```

**Example (AAPL Q4 2020)**:
```
Total Assets: $354,054,000,000
Total Liabilities: $287,830,000,000
Shares Outstanding: 17,114,000,000
Price: $130.90

Book Value = $354,054M - $287,830M = $66,224M
BVPS = $66,224M / 17,114M shares = $3.87
P/B = $130.90 / $3.87 = 33.83
```

**Interpretation**:
- **< 1**: Trading below book value (potential value)
- **1-3**: Reasonable for most companies
- **> 3**: Growth premium or overvalued

---

### 4. Price-to-Sales Ratio (P/S)

**Formula**:
```
P/S = Adjusted Close / (Total Revenue / Shares)
```

**Python Implementation**:
```python
def calculate_ps_ratio(ticker, period_date, price_date, api_token):
    """Calculate P/S Ratio."""
    # Get revenue and shares
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::totalRevenue",
        f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    total_revenue = response["Financials"]["Income_Statement"]["quarterly"][period_date]["totalRevenue"]
    shares = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["commonStockSharesOutstanding"]

    # Get price
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    price_data = requests.get(eod_url, params={
        "api_token": api_token,
        "from": price_date,
        "to": price_date,
        "filter": "adjusted_close",
        "fmt": "json"
    }).json()
    adjusted_close = price_data[0]["adjusted_close"]

    # Calculate
    revenue_per_share = total_revenue / shares
    ps_ratio = adjusted_close / revenue_per_share

    return {
        "ps_ratio": ps_ratio,
        "revenue_per_share": revenue_per_share,
        "price": adjusted_close
    }

# Example: AAPL Q4 2020
result = calculate_ps_ratio('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"P/S Ratio: {result['ps_ratio']:.2f}")
# Output: P/S Ratio: 20.10
```

**Example (AAPL Q4 2020)**:
```
Adjusted Close: $130.90
Total Revenue: $111,439,000,000
Shares: 17,114,000,000

Revenue per Share = $111,439M / 17,114M = $6.51
P/S = $130.90 / $6.51 = 20.10
```

**Interpretation**:
- **< 1**: Undervalued or distressed
- **1-2**: Fair value
- **> 2**: Growth stock or overvalued

---

### 5. Enterprise Value (EV)

**Formula**:
```
EV = Market Cap + (Long-Term Debt + Short-Term Debt) - Cash and Equivalents
```

**Python Implementation**:
```python
def calculate_enterprise_value(ticker, period_date, price_date, api_token):
    """Calculate Enterprise Value."""
    # Get balance sheet data
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding",
        f"Financials::Balance_Sheet::quarterly::{period_date}::longTermDebt",
        f"Financials::Balance_Sheet::quarterly::{period_date}::shortTermDebt",
        f"Financials::Balance_Sheet::quarterly::{period_date}::cashAndEquivalents"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    bs_data = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]

    shares = bs_data["commonStockSharesOutstanding"]
    long_term_debt = bs_data["longTermDebt"]
    short_term_debt = bs_data["shortTermDebt"]
    cash = bs_data["cashAndEquivalents"]

    # Get price
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    price_data = requests.get(eod_url, params={
        "api_token": api_token,
        "from": price_date,
        "to": price_date,
        "filter": "close",
        "fmt": "json"
    }).json()
    close = price_data[0]["close"]

    # Calculate
    market_cap = shares * close
    total_debt = long_term_debt + short_term_debt
    ev = market_cap + total_debt - cash

    return {
        "enterprise_value": ev,
        "market_cap": market_cap,
        "total_debt": total_debt,
        "cash": cash,
        "ev_billions": ev / 1e9
    }

# Example: AAPL Q4 2020
result = calculate_enterprise_value('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"Enterprise Value: ${result['ev_billions']:.2f}B")
# Output: Enterprise Value: $2,364.52B
```

**Example (AAPL Q4 2020)**:
```
Shares: 17,114,000,000
Close: $133.72
Long-Term Debt: $99,281,000,000
Short-Term Debt: $12,762,000,000
Cash: $36,010,000,000

Market Cap = 17,114M × $133.72 = $2,288,484M
Total Debt = $99,281M + $12,762M = $112,043M
EV = $2,288,484M + $112,043M - $36,010M = $2,364,517M
```

**Use Cases**:
- M&A valuations
- More accurate than market cap (includes debt)
- Basis for EV/EBITDA, EV/Sales ratios

---

### 6. EV/EBITDA Ratio

**Formula**:
```
EV/EBITDA = Enterprise Value / EBITDA
```

**Python Implementation**:
```python
def calculate_ev_ebitda(ticker, period_date, price_date, api_token):
    """Calculate EV/EBITDA Ratio."""
    # Get EV (from previous function)
    ev_data = calculate_enterprise_value(ticker, period_date, price_date, api_token)
    ev = ev_data["enterprise_value"]

    # Get EBITDA
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": f"Financials::Income_Statement::quarterly::{period_date}::ebitda"
    }
    response = requests.get(url, params=params).json()
    ebitda = response["Financials"]["Income_Statement"]["quarterly"][period_date]["ebitda"]

    # Calculate
    ev_ebitda = ev / ebitda

    return {
        "ev_ebitda": ev_ebitda,
        "ev": ev,
        "ebitda": ebitda
    }

# Example
result = calculate_ev_ebitda('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"EV/EBITDA: {result['ev_ebitda']:.2f}")
# Output: EV/EBITDA: 65.32
```

**Example (AAPL Q4 2020)**:
```
EV: $2,364,517,080,000
EBITDA: $36,200,000,000

EV/EBITDA = $2,364,517M / $36,200M = 65.32
```

**Interpretation**:
- **< 10**: Potentially undervalued
- **10-15**: Fair value
- **> 15**: Potentially overvalued or high growth

---

### 7. EV/Sales Ratio

**Formula**:
```
EV/Sales = Enterprise Value / Total Revenue
```

**Python Implementation**:
```python
def calculate_ev_sales(ticker, period_date, price_date, api_token):
    """Calculate EV/Sales Ratio."""
    # Get EV
    ev_data = calculate_enterprise_value(ticker, period_date, price_date, api_token)
    ev = ev_data["enterprise_value"]

    # Get Total Revenue
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": f"Financials::Income_Statement::quarterly::{period_date}::totalRevenue"
    }
    response = requests.get(url, params=params).json()
    total_revenue = response["Financials"]["Income_Statement"]["quarterly"][period_date]["totalRevenue"]

    # Calculate
    ev_sales = ev / total_revenue

    return {
        "ev_sales": ev_sales,
        "ev": ev,
        "total_revenue": total_revenue
    }

# Example
result = calculate_ev_sales('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"EV/Sales: {result['ev_sales']:.2f}")
# Output: EV/Sales: 21.22
```

**Example (AAPL Q4 2020)**:
```
EV: $2,364,517,080,000
Total Revenue: $111,439,000,000

EV/Sales = $2,364,517M / $111,439M = 21.22
```

---

### 8. EV/CFO Ratio

**Formula**:
```
EV/CFO = Enterprise Value / Total Cash from Operating Activities
```

**Python Implementation**:
```python
def calculate_ev_cfo(ticker, period_date, price_date, api_token):
    """Calculate EV/CFO Ratio."""
    # Get EV
    ev_data = calculate_enterprise_value(ticker, period_date, price_date, api_token)
    ev = ev_data["enterprise_value"]

    # Get Operating Cash Flow
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": f"Financials::Cash_Flow::quarterly::{period_date}::totalCashFromOperatingActivities"
    }
    response = requests.get(url, params=params).json()
    cfo = response["Financials"]["Cash_Flow"]["quarterly"][period_date]["totalCashFromOperatingActivities"]

    # Calculate
    ev_cfo = ev / cfo

    return {
        "ev_cfo": ev_cfo,
        "ev": ev,
        "operating_cash_flow": cfo
    }

# Example
result = calculate_ev_cfo('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"EV/CFO: {result['ev_cfo']:.2f}")
# Output: EV/CFO: 61.00
```

**Interpretation**: How many years of operating cash flow needed to cover enterprise value.

---

## Profitability Ratios

### 9. Gross Profit Margin

**Formula**:
```
Gross Profit Margin = Gross Profit / Total Revenue
```

**Python Implementation**:
```python
def calculate_gross_profit_margin(ticker, period_date, api_token):
    """Calculate Gross Profit Margin."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::grossProfit",
        f"Financials::Income_Statement::quarterly::{period_date}::totalRevenue"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    is_data = response["Financials"]["Income_Statement"]["quarterly"][period_date]

    gross_profit = is_data["grossProfit"]
    total_revenue = is_data["totalRevenue"]

    gp_margin = gross_profit / total_revenue

    return {
        "gross_profit_margin": gp_margin,
        "gross_profit_margin_pct": gp_margin * 100,
        "gross_profit": gross_profit,
        "total_revenue": total_revenue
    }

# Example
result = calculate_gross_profit_margin('AAPL.US', '2020-12-31', 'demo')
print(f"Gross Profit Margin: {result['gross_profit_margin_pct']:.2f}%")
# Output: Gross Profit Margin: 39.78%
```

**Example (AAPL Q4 2020)**:
```
Gross Profit: $44,328,000,000
Total Revenue: $111,439,000,000

GP Margin = $44,328M / $111,439M = 0.398 (39.8%)
```

**Interpretation**:
- **< 20%**: Low margin business (retail, grocery)
- **20-40%**: Moderate margin
- **> 40%**: High margin business (software, pharma)

---

### 10. Operating Profit Margin

**Formula**:
```
Operating Profit Margin = Operating Income / Total Revenue
```

**Python Implementation**:
```python
def calculate_operating_profit_margin(ticker, period_date, api_token):
    """Calculate Operating Profit Margin."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::operatingIncome",
        f"Financials::Income_Statement::quarterly::{period_date}::totalRevenue"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    is_data = response["Financials"]["Income_Statement"]["quarterly"][period_date]

    operating_income = is_data["operatingIncome"]
    total_revenue = is_data["totalRevenue"]

    op_margin = operating_income / total_revenue

    return {
        "operating_profit_margin": op_margin,
        "operating_profit_margin_pct": op_margin * 100,
        "operating_income": operating_income,
        "total_revenue": total_revenue
    }

# Example
result = calculate_operating_profit_margin('AAPL.US', '2020-12-31', 'demo')
print(f"Operating Profit Margin: {result['operating_profit_margin_pct']:.2f}%")
# Output: Operating Profit Margin: 30.10%
```

**Example (AAPL Q4 2020)**:
```
Operating Income: $33,534,000,000
Total Revenue: $111,439,000,000

Op Margin = $33,534M / $111,439M = 0.301 (30.1%)
```

---

## Liquidity Ratios

### 11. Current Ratio

**Formula**:
```
Current Ratio = Total Current Assets / Total Current Liabilities
```

**Python Implementation**:
```python
def calculate_current_ratio(ticker, period_date, api_token):
    """Calculate Current Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalCurrentAssets",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalCurrentLiabilities"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    bs_data = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]

    current_assets = bs_data["totalCurrentAssets"]
    current_liabilities = bs_data["totalCurrentLiabilities"]

    current_ratio = current_assets / current_liabilities

    return {
        "current_ratio": current_ratio,
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "status": "Healthy" if current_ratio > 1.5 else "Concerning" if current_ratio < 1 else "Acceptable"
    }

# Example
result = calculate_current_ratio('AAPL.US', '2020-12-31', 'demo')
print(f"Current Ratio: {result['current_ratio']:.2f} ({result['status']})")
# Output: Current Ratio: 1.16 (Acceptable)
```

**Example (AAPL Q4 2020)**:
```
Total Current Assets: $154,106,000,000
Total Current Liabilities: $132,507,000,000

Current Ratio = $154,106M / $132,507M = 1.16
```

**Interpretation**:
- **< 1.0**: Cannot cover short-term obligations
- **1.0-1.5**: Acceptable but tight
- **> 1.5**: Healthy liquidity

---

### 12. Quick Ratio (Acid-Test)

**Formula**:
```
Quick Ratio = (Cash + Short-Term Investments + Net Receivables) / Total Current Liabilities
```

**Python Implementation**:
```python
def calculate_quick_ratio(ticker, period_date, api_token):
    """Calculate Quick Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::cashAndEquivalents",
        f"Financials::Balance_Sheet::quarterly::{period_date}::shortTermInvestments",
        f"Financials::Balance_Sheet::quarterly::{period_date}::netReceivables",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalCurrentLiabilities"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    bs_data = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]

    cash = bs_data["cashAndEquivalents"]
    short_term_investments = bs_data["shortTermInvestments"]
    net_receivables = bs_data["netReceivables"]
    current_liabilities = bs_data["totalCurrentLiabilities"]

    quick_assets = cash + short_term_investments + net_receivables
    quick_ratio = quick_assets / current_liabilities

    return {
        "quick_ratio": quick_ratio,
        "quick_assets": quick_assets,
        "current_liabilities": current_liabilities
    }

# Example
result = calculate_quick_ratio('AAPL.US', '2020-12-31', 'demo')
print(f"Quick Ratio: {result['quick_ratio']:.2f}")
# Output: Quick Ratio: 1.02
```

**Example (AAPL Q4 2020)**:
```
Cash: $36,010,000,000
Short-Term Investments: $40,816,000,000
Net Receivables: $58,620,000,000
Current Liabilities: $132,507,000,000

Quick Assets = $36,010M + $40,816M + $58,620M = $135,446M
Quick Ratio = $135,446M / $132,507M = 1.02
```

**Interpretation**:
- **< 0.5**: Severe liquidity issues
- **0.5-1.0**: Potential liquidity concerns
- **> 1.0**: Good liquidity

---

### 13. Cash Ratio

**Formula**:
```
Cash Ratio = Cash and Equivalents / Total Current Liabilities
```

**Python Implementation**:
```python
def calculate_cash_ratio(ticker, period_date, api_token):
    """Calculate Cash Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::cashAndEquivalents",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalCurrentLiabilities"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    bs_data = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]

    cash = bs_data["cashAndEquivalents"]
    current_liabilities = bs_data["totalCurrentLiabilities"]

    cash_ratio = cash / current_liabilities

    return {
        "cash_ratio": cash_ratio,
        "cash": cash,
        "current_liabilities": current_liabilities
    }

# Example
result = calculate_cash_ratio('AAPL.US', '2020-12-31', 'demo')
print(f"Cash Ratio: {result['cash_ratio']:.2f}")
# Output: Cash Ratio: 0.28
```

**Example (AAPL Q4 2020)**:
```
Cash: $36,010,000,000
Current Liabilities: $132,507,000,000

Cash Ratio = $36,010M / $132,507M = 0.28
```

---

## Leverage Ratios

### 14. Debt-to-Equity Ratio (D/E)

**Formula**:
```
D/E = (Long-Term Debt + Short-Term Debt) / Total Stockholder Equity
```

**Python Implementation**:
```python
def calculate_debt_to_equity(ticker, period_date, api_token):
    """Calculate Debt-to-Equity Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::longTermDebt",
        f"Financials::Balance_Sheet::quarterly::{period_date}::shortTermDebt",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalStockholderEquity"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    bs_data = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]

    long_term_debt = bs_data["longTermDebt"]
    short_term_debt = bs_data["shortTermDebt"]
    equity = bs_data["totalStockholderEquity"]

    total_debt = long_term_debt + short_term_debt
    de_ratio = total_debt / equity

    return {
        "debt_to_equity": de_ratio,
        "total_debt": total_debt,
        "equity": equity
    }

# Example
result = calculate_debt_to_equity('AAPL.US', '2020-12-31', 'demo')
print(f"Debt-to-Equity: {result['debt_to_equity']:.2f}")
# Output: Debt-to-Equity: 1.69
```

**Example (AAPL Q4 2020)**:
```
Long-Term Debt: $99,281,000,000
Short-Term Debt: $12,762,000,000
Total Stockholder Equity: $66,224,000,000

Total Debt = $99,281M + $12,762M = $112,043M
D/E = $112,043M / $66,224M = 1.69
```

**Interpretation**:
- **< 0.5**: Conservative, low leverage
- **0.5-1.5**: Moderate leverage
- **> 2.0**: High leverage, risky

---

### 15. Debt-to-Assets Ratio

**Formula**:
```
Debt-to-Assets = (Long-Term Debt + Short-Term Debt) / Total Assets
```

**Python Implementation**:
```python
def calculate_debt_to_assets(ticker, period_date, api_token):
    """Calculate Debt-to-Assets Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::longTermDebt",
        f"Financials::Balance_Sheet::quarterly::{period_date}::shortTermDebt",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    bs_data = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]

    long_term_debt = bs_data["longTermDebt"]
    short_term_debt = bs_data["shortTermDebt"]
    total_assets = bs_data["totalAssets"]

    total_debt = long_term_debt + short_term_debt
    da_ratio = total_debt / total_assets

    return {
        "debt_to_assets": da_ratio,
        "debt_to_assets_pct": da_ratio * 100,
        "total_debt": total_debt,
        "total_assets": total_assets
    }

# Example
result = calculate_debt_to_assets('AAPL.US', '2020-12-31', 'demo')
print(f"Debt-to-Assets: {result['debt_to_assets']:.2f} ({result['debt_to_assets_pct']:.1f}%)")
# Output: Debt-to-Assets: 0.32 (31.6%)
```

**Example (AAPL Q4 2020)**:
```
Total Debt: $112,043,000,000
Total Assets: $354,054,000,000

Debt-to-Assets = $112,043M / $354,054M = 0.32 (31.6%)
```

---

### 16. Debt Ratio

**Formula**:
```
Debt Ratio = Total Liabilities / Total Assets
```

**Python Implementation**:
```python
def calculate_debt_ratio(ticker, period_date, api_token):
    """Calculate Debt Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalLiab",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    bs_data = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]

    total_liab = bs_data["totalLiab"]
    total_assets = bs_data["totalAssets"]

    debt_ratio = total_liab / total_assets

    return {
        "debt_ratio": debt_ratio,
        "debt_ratio_pct": debt_ratio * 100,
        "total_liabilities": total_liab,
        "total_assets": total_assets
    }

# Example
result = calculate_debt_ratio('AAPL.US', '2020-12-31', 'demo')
print(f"Debt Ratio: {result['debt_ratio_pct']:.1f}%")
# Output: Debt Ratio: 81.3%
```

**Example (AAPL Q4 2020)**:
```
Total Liabilities: $287,830,000,000
Total Assets: $354,054,000,000

Debt Ratio = $287,830M / $354,054M = 0.813 (81.3%)
```

---

### 17. Interest Coverage Ratio

**Formula**:
```
Interest Coverage = EBIT / Interest Expense
```

**Python Implementation**:
```python
def calculate_interest_coverage(ticker, period_date, api_token):
    """Calculate Interest Coverage Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::ebit",
        f"Financials::Income_Statement::quarterly::{period_date}::interestExpense"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    is_data = response["Financials"]["Income_Statement"]["quarterly"][period_date]

    ebit = is_data["ebit"]
    interest_expense = is_data["interestExpense"]

    interest_coverage = ebit / interest_expense

    return {
        "interest_coverage": interest_coverage,
        "ebit": ebit,
        "interest_expense": interest_expense,
        "status": "Excellent" if interest_coverage > 5 else "Good" if interest_coverage > 2.5 else "Risky"
    }

# Example
result = calculate_interest_coverage('AAPL.US', '2020-12-31', 'demo')
print(f"Interest Coverage: {result['interest_coverage']:.2f}x ({result['status']})")
# Output: Interest Coverage: 52.56x (Excellent)
```

**Example (AAPL Q4 2020)**:
```
EBIT: $33,534,000,000
Interest Expense: $638,000,000

Interest Coverage = $33,534M / $638M = 52.56x
```

**Interpretation**:
- **< 1.5**: Cannot cover interest (distress)
- **1.5-2.5**: Risky
- **2.5-5.0**: Acceptable
- **> 5.0**: Very safe

---

### 18. Net Debt-to-EBITDA Ratio

**Formula**:
```
Net Debt-to-EBITDA = Net Debt / EBITDA
```

**Python Implementation**:
```python
def calculate_net_debt_to_ebitda(ticker, period_date, api_token):
    """Calculate Net Debt-to-EBITDA Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Balance_Sheet::quarterly::{period_date}::netDebt",
        f"Financials::Income_Statement::quarterly::{period_date}::ebitda"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    net_debt = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["netDebt"]
    ebitda = response["Financials"]["Income_Statement"]["quarterly"][period_date]["ebitda"]

    ratio = net_debt / ebitda

    return {
        "net_debt_to_ebitda": ratio,
        "net_debt": net_debt,
        "ebitda": ebitda,
        "interpretation": "Years to pay off net debt with EBITDA"
    }

# Example
result = calculate_net_debt_to_ebitda('AAPL.US', '2020-12-31', 'demo')
print(f"Net Debt/EBITDA: {result['net_debt_to_ebitda']:.2f}x")
# Output: Net Debt/EBITDA: 2.10x
```

**Interpretation**: Negative ratio means company has more cash than debt (excellent).

---

## Return Ratios

### 19. Return on Equity (ROE)

**Formula**:
```
ROE = Net Income / Total Stockholder Equity
```

**Python Implementation**:
```python
def calculate_roe(ticker, period_date, api_token):
    """Calculate Return on Equity."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::netIncome",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalStockholderEquity"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    net_income = response["Financials"]["Income_Statement"]["quarterly"][period_date]["netIncome"]
    equity = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["totalStockholderEquity"]

    roe = net_income / equity

    return {
        "roe": roe,
        "roe_pct": roe * 100,
        "net_income": net_income,
        "equity": equity
    }

# Example
result = calculate_roe('AAPL.US', '2020-12-31', 'demo')
print(f"ROE: {result['roe_pct']:.2f}%")
# Output: ROE: 43.42%
```

**Example (AAPL Q4 2020)**:
```
Net Income: $28,755,000,000
Total Stockholder Equity: $66,224,000,000

ROE = $28,755M / $66,224M = 0.434 (43.4%)
```

**Interpretation**:
- **< 10%**: Poor returns to shareholders
- **10-15%**: Average
- **15-20%**: Good
- **> 20%**: Excellent (Warren Buffett looks for >15%)

---

### 20. Return on Assets (ROA)

**Formula**:
```
ROA = Net Income / Total Assets
```

**Python Implementation**:
```python
def calculate_roa(ticker, period_date, api_token):
    """Calculate Return on Assets."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::netIncome",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    net_income = response["Financials"]["Income_Statement"]["quarterly"][period_date]["netIncome"]
    total_assets = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["totalAssets"]

    roa = net_income / total_assets

    return {
        "roa": roa,
        "roa_pct": roa * 100,
        "net_income": net_income,
        "total_assets": total_assets
    }

# Example
result = calculate_roa('AAPL.US', '2020-12-31', 'demo')
print(f"ROA: {result['roa_pct']:.2f}%")
# Output: ROA: 8.12%
```

**Example (AAPL Q4 2020)**:
```
Net Income: $28,755,000,000
Total Assets: $354,054,000,000

ROA = $28,755M / $354,054M = 0.081 (8.1%)
```

---

### 21. Return on Invested Capital (ROIC)

**Formula**:
```
ROIC = EBIT / (Total Assets - Total Current Assets)
```

**Python Implementation**:
```python
def calculate_roic(ticker, period_date, api_token):
    """Calculate Return on Invested Capital."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::ebit",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalCurrentAssets"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    ebit = response["Financials"]["Income_Statement"]["quarterly"][period_date]["ebit"]
    total_assets = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["totalAssets"]
    current_assets = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["totalCurrentAssets"]

    invested_capital = total_assets - current_assets
    roic = ebit / invested_capital

    return {
        "roic": roic,
        "roic_pct": roic * 100,
        "ebit": ebit,
        "invested_capital": invested_capital
    }

# Example
result = calculate_roic('AAPL.US', '2020-12-31', 'demo')
print(f"ROIC: {result['roic_pct']:.2f}%")
# Output: ROIC: 16.77%
```

**Example (AAPL Q4 2020)**:
```
EBIT: $33,534,000,000
Total Assets: $354,054,000,000
Total Current Assets: $154,106,000,000

Invested Capital = $354,054M - $154,106M = $199,948M
ROIC = $33,534M / $199,948M = 0.168 (16.8%)
```

---

### 22. Return on Capital Employed (ROCE)

**Formula**:
```
ROCE = EBIT / (Total Assets - Total Current Liabilities)
```

**Python Implementation**:
```python
def calculate_roce(ticker, period_date, api_token):
    """Calculate Return on Capital Employed."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::ebit",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalCurrentLiabilities"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    ebit = response["Financials"]["Income_Statement"]["quarterly"][period_date]["ebit"]
    total_assets = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["totalAssets"]
    current_liabilities = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["totalCurrentLiabilities"]

    capital_employed = total_assets - current_liabilities
    roce = ebit / capital_employed

    return {
        "roce": roce,
        "roce_pct": roce * 100,
        "ebit": ebit,
        "capital_employed": capital_employed
    }

# Example
result = calculate_roce('AAPL.US', '2020-12-31', 'demo')
print(f"ROCE: {result['roce_pct']:.2f}%")
# Output: ROCE: 15.14%
```

**Example (AAPL Q4 2020)**:
```
EBIT: $33,534,000,000
Total Assets: $354,054,000,000
Total Current Liabilities: $132,507,000,000

Capital Employed = $354,054M - $132,507M = $221,547M
ROCE = $33,534M / $221,547M = 0.151 (15.1%)
```

---

### 23. Return on Tangible Assets (RoTE)

**Formula**:
```
RoTE = Net Income / (Total Assets - Intangible Assets)
```

**Python Implementation**:
```python
def calculate_rote(ticker, period_date, api_token):
    """Calculate Return on Tangible Assets."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::netIncome",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets",
        f"Financials::Balance_Sheet::quarterly::{period_date}::intangibleAssets"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    net_income = response["Financials"]["Income_Statement"]["quarterly"][period_date]["netIncome"]
    total_assets = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["totalAssets"]
    intangible_assets = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["intangibleAssets"]

    tangible_assets = total_assets - intangible_assets
    rote = net_income / tangible_assets

    return {
        "rote": rote,
        "rote_pct": rote * 100,
        "net_income": net_income,
        "tangible_assets": tangible_assets
    }

# Example (for a company with significant intangibles)
result = calculate_rote('COMPANY.US', '2020-12-31', 'demo')
print(f"RoTE: {result['rote_pct']:.2f}%")
```

**Use Case**: Particularly useful for banks and insurance companies.

---

## Efficiency Ratios

### 24. Assets Turnover Ratio

**Formula**:
```
Assets Turnover = Total Revenue / Total Assets
```

**Python Implementation**:
```python
def calculate_asset_turnover(ticker, period_date, api_token):
    """Calculate Assets Turnover Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::totalRevenue",
        f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    total_revenue = response["Financials"]["Income_Statement"]["quarterly"][period_date]["totalRevenue"]
    total_assets = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["totalAssets"]

    asset_turnover = total_revenue / total_assets

    return {
        "asset_turnover": asset_turnover,
        "total_revenue": total_revenue,
        "total_assets": total_assets,
        "interpretation": f"Generates ${asset_turnover:.2f} in revenue per $1 of assets"
    }

# Example
result = calculate_asset_turnover('AAPL.US', '2020-12-31', 'demo')
print(f"Asset Turnover: {result['asset_turnover']:.2f}x")
print(result['interpretation'])
# Output: Asset Turnover: 0.31x
# Generates $0.31 in revenue per $1 of assets
```

**Example (AAPL Q4 2020)**:
```
Total Revenue: $111,439,000,000
Total Assets: $354,054,000,000

Asset Turnover = $111,439M / $354,054M = 0.31
```

**Interpretation**:
- **< 0.5**: Capital-intensive business (utilities, real estate)
- **0.5-1.0**: Moderate efficiency
- **> 1.0**: High efficiency (retail, services)

---

### 25. Berry Ratio

**Formula**:
```
Berry Ratio = (Gross Profit - Total Operating Expenses) / Total Operating Expenses
```

**Python Implementation**:
```python
def calculate_berry_ratio(ticker, period_date, api_token):
    """Calculate Berry Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::grossProfit",
        f"Financials::Income_Statement::quarterly::{period_date}::totalOperatingExpenses"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()
    is_data = response["Financials"]["Income_Statement"]["quarterly"][period_date]

    gross_profit = is_data["grossProfit"]
    total_op_expenses = is_data["totalOperatingExpenses"]

    berry_ratio = (gross_profit - total_op_expenses) / total_op_expenses

    return {
        "berry_ratio": berry_ratio,
        "gross_profit": gross_profit,
        "operating_expenses": total_op_expenses,
        "status": "Profitable" if berry_ratio > 1 else "Unprofitable"
    }

# Example
result = calculate_berry_ratio('AAPL.US', '2020-12-31', 'demo')
print(f"Berry Ratio: {result['berry_ratio']:.2f} ({result['status']})")
# Output: Berry Ratio: 3.08 (Profitable)
```

**Example (AAPL Q4 2020)**:
```
Gross Profit: $44,328,000,000
Total Operating Expenses: $10,858,000,000

Berry Ratio = ($44,328M - $10,858M) / $10,858M = 3.08
```

**Interpretation**:
- **< 1**: Operating at a loss
- **= 1**: Break-even
- **> 1**: Profitable operation

---

## Per-Share Metrics

### 26. Earnings Per Share (EPS)

**Note**: EPS is typically provided directly by the API, but can be calculated:

**Formula**:
```
EPS = Net Income / Shares Outstanding
```

**Python Implementation**:
```python
def calculate_eps(ticker, period_date, api_token):
    """Calculate Earnings Per Share."""
    # Method 1: Get from Earnings API (preferred)
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": f"Earnings::History::{period_date}::epsActual"
    }
    response = requests.get(url, params=params).json()
    eps_actual = response["Earnings"]["History"][period_date]["epsActual"]

    return {
        "eps": eps_actual,
        "source": "Earnings API (reported)"
    }

# Example
result = calculate_eps('AAPL.US', '2020-12-31', 'demo')
print(f"EPS: ${result['eps']:.2f}")
# Output: EPS: $1.68
```

---

### 27. Sales Per Share

**Formula**:
```
Sales Per Share = Total Revenue / Shares Outstanding
```

**Python Implementation**:
```python
def calculate_sales_per_share(ticker, period_date, api_token):
    """Calculate Sales Per Share."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Income_Statement::quarterly::{period_date}::totalRevenue",
        f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    total_revenue = response["Financials"]["Income_Statement"]["quarterly"][period_date]["totalRevenue"]
    shares = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["commonStockSharesOutstanding"]

    sales_per_share = total_revenue / shares

    return {
        "sales_per_share": sales_per_share,
        "total_revenue": total_revenue,
        "shares": shares
    }

# Example
result = calculate_sales_per_share('AAPL.US', '2020-12-31', 'demo')
print(f"Sales Per Share: ${result['sales_per_share']:.2f}")
# Output: Sales Per Share: $6.51
```

**Example (AAPL Q4 2020)**:
```
Total Revenue: $111,439,000,000
Shares Outstanding: 17,114,000,000

Sales Per Share = $111,439M / 17,114M = $6.51
```

---

### 28. Capex Per Share

**Formula**:
```
Capex Per Share = Capital Expenditures / Shares Outstanding
```

**Python Implementation**:
```python
def calculate_capex_per_share(ticker, period_date, api_token):
    """Calculate Capex Per Share."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Cash_Flow::quarterly::{period_date}::capitalExpenditures",
        f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    capex = response["Financials"]["Cash_Flow"]["quarterly"][period_date]["capitalExpenditures"]
    shares = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["commonStockSharesOutstanding"]

    capex_per_share = abs(capex) / shares  # abs() because capex is negative

    return {
        "capex_per_share": capex_per_share,
        "capital_expenditures": capex,
        "shares": shares
    }

# Example
result = calculate_capex_per_share('AAPL.US', '2020-12-31', 'demo')
print(f"Capex Per Share: ${result['capex_per_share']:.2f}")
# Output: Capex Per Share: $0.20
```

---

## Additional Metrics

### 29. Earnings Yield

**Formula**:
```
Earnings Yield = EPS / Adjusted Close
```

(Inverse of P/E Ratio)

**Python Implementation**:
```python
def calculate_earnings_yield(ticker, period_date, price_date, api_token):
    """Calculate Earnings Yield."""
    # Get EPS
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": f"Earnings::History::{period_date}::epsActual"
    }
    response = requests.get(url, params=params).json()
    eps = response["Earnings"]["History"][period_date]["epsActual"]

    # Get price
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    price_data = requests.get(eod_url, params={
        "api_token": api_token,
        "from": price_date,
        "to": price_date,
        "filter": "adjusted_close",
        "fmt": "json"
    }).json()
    adjusted_close = price_data[0]["adjusted_close"]

    earnings_yield = eps / adjusted_close

    return {
        "earnings_yield": earnings_yield,
        "earnings_yield_pct": earnings_yield * 100,
        "eps": eps,
        "price": adjusted_close
    }

# Example
result = calculate_earnings_yield('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"Earnings Yield: {result['earnings_yield_pct']:.2f}%")
# Output: Earnings Yield: 1.28%
```

**Example (AAPL Q4 2020)**:
```
EPS: $1.68
Adjusted Close: $130.90

Earnings Yield = $1.68 / $130.90 = 0.0128 (1.28%)
```

---

### 30. Dividend Payout Ratio

**Formula**:
```
Payout Ratio = Dividends Paid / Net Income
```

**Python Implementation**:
```python
def calculate_payout_ratio(ticker, period_date, api_token):
    """Calculate Dividend Payout Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Cash_Flow::quarterly::{period_date}::dividendsPaid",
        f"Financials::Income_Statement::quarterly::{period_date}::netIncome"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    dividends_paid = abs(response["Financials"]["Cash_Flow"]["quarterly"][period_date]["dividendsPaid"])
    net_income = response["Financials"]["Income_Statement"]["quarterly"][period_date]["netIncome"]

    payout_ratio = dividends_paid / net_income

    return {
        "payout_ratio": payout_ratio,
        "payout_ratio_pct": payout_ratio * 100,
        "dividends_paid": dividends_paid,
        "net_income": net_income,
        "interpretation": "Sustainable" if payout_ratio < 0.6 else "High" if payout_ratio < 0.8 else "Unsustainable"
    }

# Example
result = calculate_payout_ratio('AAPL.US', '2020-12-31', 'demo')
print(f"Payout Ratio: {result['payout_ratio_pct']:.1f}% ({result['interpretation']})")
# Output: Payout Ratio: 12.6% (Sustainable)
```

**Example (AAPL Q4 2020)**:
```
Dividends Paid: $3,613,000,000
Net Income: $28,755,000,000

Payout Ratio = $3,613M / $28,755M = 0.126 (12.6%)
```

**Interpretation**:
- **< 40%**: Conservative, room to grow dividends
- **40-60%**: Sustainable
- **60-80%**: High, little room for growth
- **> 80%**: Potentially unsustainable

---

### 31. Historical Dividend Yield

**Formula**:
```
Dividend Yield = (Dividends Paid / Shares) / Adjusted Close
```

**Python Implementation**:
```python
def calculate_dividend_yield(ticker, period_date, price_date, api_token):
    """Calculate Historical Dividend Yield."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Cash_Flow::quarterly::{period_date}::dividendsPaid",
        f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    dividends_paid = abs(response["Financials"]["Cash_Flow"]["quarterly"][period_date]["dividendsPaid"])
    shares = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["commonStockSharesOutstanding"]

    # Get price
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    price_data = requests.get(eod_url, params={
        "api_token": api_token,
        "from": price_date,
        "to": price_date,
        "filter": "adjusted_close",
        "fmt": "json"
    }).json()
    adjusted_close = price_data[0]["adjusted_close"]

    dividend_per_share = dividends_paid / shares
    dividend_yield = dividend_per_share / adjusted_close

    return {
        "dividend_yield": dividend_yield,
        "dividend_yield_pct": dividend_yield * 100,
        "dividend_per_share": dividend_per_share,
        "price": adjusted_close
    }

# Example
result = calculate_dividend_yield('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"Dividend Yield: {result['dividend_yield_pct']:.2f}%")
# Output: Dividend Yield: 0.16%
```

**Example (AAPL Q4 2020)**:
```
Dividends Paid: $3,613,000,000
Shares: 17,114,000,000
Adjusted Close: $130.90

Dividend Per Share = $3,613M / 17,114M = $0.21
Dividend Yield = $0.21 / $130.90 = 0.0016 (0.16%)
```

---

### 32. Free Cash Flow Yield (FCFY)

**Formula**:
```
FCFY = Free Cash Flow / (Adjusted Close × Shares)
```

**Python Implementation**:
```python
def calculate_fcf_yield(ticker, period_date, price_date, api_token):
    """Calculate Free Cash Flow Yield."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    filters = [
        f"Financials::Cash_Flow::quarterly::{period_date}::freeCashFlow",
        f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding"
    ]
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": ",".join(filters)
    }
    response = requests.get(url, params=params).json()

    free_cash_flow = response["Financials"]["Cash_Flow"]["quarterly"][period_date]["freeCashFlow"]
    shares = response["Financials"]["Balance_Sheet"]["quarterly"][period_date]["commonStockSharesOutstanding"]

    # Get price
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    price_data = requests.get(eod_url, params={
        "api_token": api_token,
        "from": price_date,
        "to": price_date,
        "filter": "adjusted_close",
        "fmt": "json"
    }).json()
    adjusted_close = price_data[0]["adjusted_close"]

    market_cap = adjusted_close * shares
    fcf_yield = free_cash_flow / market_cap

    return {
        "fcf_yield": fcf_yield,
        "fcf_yield_pct": fcf_yield * 100,
        "free_cash_flow": free_cash_flow,
        "market_cap": market_cap
    }

# Example
result = calculate_fcf_yield('AAPL.US', '2020-12-31', '2020-12-30', 'demo')
print(f"FCF Yield: {result['fcf_yield_pct']:.2f}%")
# Output: FCF Yield: 1.57%
```

**Example (AAPL Q4 2020)**:
```
Free Cash Flow: $35,263,000,000
Adjusted Close: $130.90
Shares: 17,114,000,000

Market Cap = $130.90 × 17,114M = $2,240,222M
FCF Yield = $35,263M / $2,240,222M = 0.0157 (1.57%)
```

---

### 33. Total Return

**Formula**:
```
Total Return = ((End Price - Start Price) / Start Price) × 100
```

**Python Implementation**:
```python
def calculate_total_return(ticker, start_date, end_date, api_token):
    """
    Calculate Total Return between two dates.

    Uses adjusted close prices to account for dividends and splits.
    """
    # Get price range (±2 days to handle weekends/holidays)
    from datetime import datetime, timedelta

    def get_closest_price(target_date, api_token):
        """Get closest available price to target date."""
        target = datetime.strptime(target_date, '%Y-%m-%d')
        start = (target - timedelta(days=2)).strftime('%Y-%m-%d')
        end = (target + timedelta(days=2)).strftime('%Y-%m-%d')

        url = f"https://eodhd.com/api/eod/{ticker}"
        params = {
            "api_token": api_token,
            "from": start,
            "to": end,
            "filter": "adjusted_close",
            "fmt": "json"
        }
        data = requests.get(url, params=params).json()

        # Find closest date
        closest = min(data, key=lambda x: abs(
            datetime.strptime(x['date'], '%Y-%m-%d') - target
        ).days)

        return closest['adjusted_close'], closest['date']

    start_price, actual_start_date = get_closest_price(start_date, api_token)
    end_price, actual_end_date = get_closest_price(end_date, api_token)

    total_return = ((end_price - start_price) / start_price) * 100

    return {
        "total_return_pct": total_return,
        "start_price": start_price,
        "end_price": end_price,
        "actual_start_date": actual_start_date,
        "actual_end_date": actual_end_date,
        "price_change": end_price - start_price
    }

# Example: AAPL 1-year return
result = calculate_total_return('AAPL.US', '2020-01-01', '2021-01-01', 'demo')
print(f"Total Return: {result['total_return_pct']:.2f}%")
print(f"Price: ${result['start_price']:.2f} → ${result['end_price']:.2f}")
# Output: Total Return: XX.XX%
```

**Use Cases**:
- YTD return: Jan 1 to today
- 1-year return: 365 days ago to today
- Custom period returns

---

## Complete Ratio List

### Quick Reference Table

| # | Ratio | Category | Formula | Key Use |
|---|-------|----------|---------|---------|
| 1 | Market Cap | Valuation | Shares × Price | Company size |
| 2 | P/E Ratio | Valuation | Price / EPS | Valuation multiple |
| 3 | P/B Ratio | Valuation | Price / Book Value per Share | Asset valuation |
| 4 | P/S Ratio | Valuation | Price / Sales per Share | Revenue multiple |
| 5 | Enterprise Value | Valuation | Market Cap + Debt - Cash | M&A valuation |
| 6 | EV/EBITDA | Valuation | EV / EBITDA | Cash earnings multiple |
| 7 | EV/Sales | Valuation | EV / Revenue | Revenue multiple (debt-adjusted) |
| 8 | EV/CFO | Valuation | EV / Operating Cash Flow | Cash flow multiple |
| 9 | Gross Profit Margin | Profitability | Gross Profit / Revenue | Pricing power |
| 10 | Operating Profit Margin | Profitability | Operating Income / Revenue | Operating efficiency |
| 11 | Current Ratio | Liquidity | Current Assets / Current Liabilities | Short-term solvency |
| 12 | Quick Ratio | Liquidity | (Cash + ST Investments + Receivables) / Current Liabilities | Immediate liquidity |
| 13 | Cash Ratio | Liquidity | Cash / Current Liabilities | Most conservative liquidity |
| 14 | Debt-to-Equity | Leverage | Total Debt / Equity | Financial leverage |
| 15 | Debt-to-Assets | Leverage | Total Debt / Assets | Asset financing |
| 16 | Debt Ratio | Leverage | Total Liabilities / Assets | Overall leverage |
| 17 | Interest Coverage | Leverage | EBIT / Interest Expense | Debt service ability |
| 18 | Net Debt/EBITDA | Leverage | Net Debt / EBITDA | Debt payback period |
| 19 | ROE | Return | Net Income / Equity | Return to shareholders |
| 20 | ROA | Return | Net Income / Assets | Asset efficiency |
| 21 | ROIC | Return | EBIT / Invested Capital | Capital efficiency |
| 22 | ROCE | Return | EBIT / Capital Employed | Capital returns |
| 23 | RoTE | Return | Net Income / Tangible Assets | Return on tangible equity |
| 24 | Asset Turnover | Efficiency | Revenue / Assets | Asset utilization |
| 25 | Berry Ratio | Efficiency | (GP - OpEx) / OpEx | Operating efficiency |
| 26 | EPS | Per-Share | Net Income / Shares | Earnings per share |
| 27 | Sales Per Share | Per-Share | Revenue / Shares | Revenue per share |
| 28 | Capex Per Share | Per-Share | Capex / Shares | Investment per share |
| 29 | Earnings Yield | Other | EPS / Price | Inverse P/E |
| 30 | Payout Ratio | Other | Dividends / Net Income | Dividend sustainability |
| 31 | Dividend Yield | Other | (Dividends/Shares) / Price | Dividend return |
| 32 | FCF Yield | Other | FCF / Market Cap | Cash generation |
| 33 | Total Return | Other | (End Price - Start Price) / Start Price | Investment return |

---

## Python Implementation

### Complete Financial Analysis Class

```python
import requests
from datetime import datetime, timedelta
import pandas as pd

class FinancialRatioCalculator:
    """
    Complete financial ratio calculator using EODHD API.

    Usage:
        calc = FinancialRatioCalculator(api_token="your_api_token")
        ratios = calc.calculate_all_ratios("AAPL.US", "2020-12-31", "2020-12-30")
    """

    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://eodhd.com/api"

    def _get_fundamentals(self, ticker, period_date, filters):
        """Helper to fetch fundamental data."""
        url = f"{self.base_url}/fundamentals/{ticker}"
        params = {
            "api_token": self.api_token,
            "fmt": "json",
            "filter": ",".join(filters)
        }
        return requests.get(url, params=params).json()

    def _get_price(self, ticker, date, price_type="adjusted_close"):
        """Helper to fetch price data."""
        url = f"{self.base_url}/eod/{ticker}"
        params = {
            "api_token": self.api_token,
            "from": date,
            "to": date,
            "filter": price_type,
            "fmt": "json"
        }
        data = requests.get(url, params=params).json()
        return data[0][price_type] if data else None

    def calculate_all_ratios(self, ticker, period_date, price_date=None):
        """
        Calculate all financial ratios for a given period.

        Args:
            ticker: Stock ticker (e.g., "AAPL.US")
            period_date: Period end date (e.g., "2020-12-31")
            price_date: Price date (defaults to period_date if not provided)

        Returns:
            Dictionary with all calculated ratios
        """
        if price_date is None:
            price_date = period_date

        # Fetch all required data in one API call
        filters = [
            # Balance Sheet
            f"Financials::Balance_Sheet::quarterly::{period_date}::totalAssets",
            f"Financials::Balance_Sheet::quarterly::{period_date}::totalCurrentAssets",
            f"Financials::Balance_Sheet::quarterly::{period_date}::totalLiab",
            f"Financials::Balance_Sheet::quarterly::{period_date}::totalCurrentLiabilities",
            f"Financials::Balance_Sheet::quarterly::{period_date}::totalStockholderEquity",
            f"Financials::Balance_Sheet::quarterly::{period_date}::commonStockSharesOutstanding",
            f"Financials::Balance_Sheet::quarterly::{period_date}::longTermDebt",
            f"Financials::Balance_Sheet::quarterly::{period_date}::shortTermDebt",
            f"Financials::Balance_Sheet::quarterly::{period_date}::cashAndEquivalents",
            f"Financials::Balance_Sheet::quarterly::{period_date}::shortTermInvestments",
            f"Financials::Balance_Sheet::quarterly::{period_date}::netReceivables",
            f"Financials::Balance_Sheet::quarterly::{period_date}::intangibleAssets",
            # Income Statement
            f"Financials::Income_Statement::quarterly::{period_date}::totalRevenue",
            f"Financials::Income_Statement::quarterly::{period_date}::grossProfit",
            f"Financials::Income_Statement::quarterly::{period_date}::operatingIncome",
            f"Financials::Income_Statement::quarterly::{period_date}::ebit",
            f"Financials::Income_Statement::quarterly::{period_date}::ebitda",
            f"Financials::Income_Statement::quarterly::{period_date}::netIncome",
            f"Financials::Income_Statement::quarterly::{period_date}::interestExpense",
            f"Financials::Income_Statement::quarterly::{period_date}::totalOperatingExpenses",
            # Cash Flow
            f"Financials::Cash_Flow::quarterly::{period_date}::totalCashFromOperatingActivities",
            f"Financials::Cash_Flow::quarterly::{period_date}::freeCashFlow",
            f"Financials::Cash_Flow::quarterly::{period_date}::dividendsPaid",
            f"Financials::Cash_Flow::quarterly::{period_date}::capitalExpenditures",
            # Earnings
            f"Earnings::History::{period_date}::epsActual"
        ]

        data = self._get_fundamentals(ticker, period_date, filters)

        # Extract data
        bs = data["Financials"]["Balance_Sheet"]["quarterly"][period_date]
        is_data = data["Financials"]["Income_Statement"]["quarterly"][period_date]
        cf = data["Financials"]["Cash_Flow"]["quarterly"][period_date]
        eps = data["Earnings"]["History"][period_date]["epsActual"]

        # Get prices
        close = self._get_price(ticker, price_date, "close")
        adjusted_close = self._get_price(ticker, price_date, "adjusted_close")

        # Calculate all ratios
        shares = bs["commonStockSharesOutstanding"]
        market_cap = shares * close

        ratios = {
            # Valuation
            "market_cap": market_cap,
            "pe_ratio": adjusted_close / eps,
            "pb_ratio": adjusted_close / ((bs["totalAssets"] - bs["totalLiab"]) / shares),
            "ps_ratio": adjusted_close / (is_data["totalRevenue"] / shares),

            # Profitability
            "gross_margin": is_data["grossProfit"] / is_data["totalRevenue"],
            "operating_margin": is_data["operatingIncome"] / is_data["totalRevenue"],

            # Liquidity
            "current_ratio": bs["totalCurrentAssets"] / bs["totalCurrentLiabilities"],
            "quick_ratio": (bs["cashAndEquivalents"] + bs["shortTermInvestments"] + bs["netReceivables"]) / bs["totalCurrentLiabilities"],
            "cash_ratio": bs["cashAndEquivalents"] / bs["totalCurrentLiabilities"],

            # Leverage
            "debt_to_equity": (bs["longTermDebt"] + bs["shortTermDebt"]) / bs["totalStockholderEquity"],
            "debt_to_assets": (bs["longTermDebt"] + bs["shortTermDebt"]) / bs["totalAssets"],
            "interest_coverage": is_data["ebit"] / is_data["interestExpense"],

            # Returns
            "roe": is_data["netIncome"] / bs["totalStockholderEquity"],
            "roa": is_data["netIncome"] / bs["totalAssets"],
            "roic": is_data["ebit"] / (bs["totalAssets"] - bs["totalCurrentAssets"]),

            # Efficiency
            "asset_turnover": is_data["totalRevenue"] / bs["totalAssets"],

            # Per-Share
            "eps": eps,
            "sales_per_share": is_data["totalRevenue"] / shares,
            "dividend_per_share": abs(cf["dividendsPaid"]) / shares,

            # Other
            "payout_ratio": abs(cf["dividendsPaid"]) / is_data["netIncome"],
            "fcf_yield": cf["freeCashFlow"] / market_cap
        }

        # Convert to percentages where appropriate
        ratios["gross_margin_pct"] = ratios["gross_margin"] * 100
        ratios["operating_margin_pct"] = ratios["operating_margin"] * 100
        ratios["roe_pct"] = ratios["roe"] * 100
        ratios["roa_pct"] = ratios["roa"] * 100
        ratios["payout_ratio_pct"] = ratios["payout_ratio"] * 100
        ratios["fcf_yield_pct"] = ratios["fcf_yield"] * 100

        return ratios

# Usage Example
calc = FinancialRatioCalculator(api_token="your_api_token")
ratios = calc.calculate_all_ratios("AAPL.US", "2020-12-31", "2020-12-30")

print("Valuation Ratios:")
print(f"  P/E: {ratios['pe_ratio']:.2f}")
print(f"  P/B: {ratios['pb_ratio']:.2f}")
print(f"  P/S: {ratios['ps_ratio']:.2f}")

print("\nProfitability:")
print(f"  Gross Margin: {ratios['gross_margin_pct']:.2f}%")
print(f"  Operating Margin: {ratios['operating_margin_pct']:.2f}%")

print("\nReturns:")
print(f"  ROE: {ratios['roe_pct']:.2f}%")
print(f"  ROA: {ratios['roa_pct']:.2f}%")
```

---

## Best Practices

### 1. Use Adjusted Close for Ratios

**Always use `adjusted_close`** (not `close`) for price-based ratios:
- P/E Ratio
- P/B Ratio
- P/S Ratio
- Dividend Yield
- Total Return

**Reason**: Adjusted close accounts for splits and dividends, making historical comparisons accurate.

---

### 2. Calculate Daily Adjustment Factor

When combining financial statement data with price data, calculate adjustment factor **for each day**:

```python
k = adjusted_close / close
```

Don't assume `k` is constant across dates.

---

### 3. Handle Weekend/Holiday Dates

Financial period end dates may fall on weekends/holidays when markets are closed. Fetch price data with ±2 day buffer:

```python
from_date = period_date - timedelta(days=2)
to_date = period_date + timedelta(days=2)
```

Then select the closest available date.

---

### 4. Validate Data Before Calculation

Always check for:
- Division by zero
- Null/None values
- Negative numbers where unexpected

```python
if denominator == 0 or denominator is None:
    return None  # or raise exception
```

---

### 5. Use Consistent Period Types

Don't mix quarterly and yearly data in the same calculation:

```python
# GOOD
quarterly_data = get_data("quarterly::2020-12-31")

# BAD
quarterly_revenue = get_data("quarterly::2020-12-31::totalRevenue")
yearly_assets = get_data("yearly::2020-12-31::totalAssets")  # ❌ Mixed periods
```

---

### 6. Cache Financial Data

Financial statement data doesn't change, so cache it:

```python
import functools

@functools.lru_cache(maxsize=128)
def get_fundamentals(ticker, period_date):
    # Fetch data
    return data
```

---

### 7. Fetch Multiple Fields in One Request

Use filter parameter to get multiple fields in a single API call:

```python
filters = [
    "Financials::Income_Statement::quarterly::2020-12-31::totalRevenue",
    "Financials::Income_Statement::quarterly::2020-12-31::netIncome",
    "Financials::Balance_Sheet::quarterly::2020-12-31::totalAssets"
]
filter_param = ",".join(filters)
```

Reduces API calls from 3 to 1.

---

### 8. Document Calculation Methodology

Always document:
- Formula used
- Data source
- Period type (quarterly vs yearly)
- Any adjustments made

```python
def calculate_roe(ticker, period_date, api_token):
    """
    Calculate Return on Equity (ROE).

    Formula: ROE = Net Income / Total Stockholder Equity
    Source: EODHD Fundamentals API
    Period: Quarterly

    Args:
        ticker: Stock ticker (e.g., "AAPL.US")
        period_date: Quarter end date (e.g., "2020-12-31")
        api_token: Your API token

    Returns:
        Dictionary with ROE and components
    """
    # ... implementation
```

---

### 9. Compare Ratios to Industry Benchmarks

Ratios are most useful when compared:
- To company's historical ratios (trend)
- To peers in same industry
- To industry averages

---

### 10. Handle Negative Values Appropriately

Some values may be negative:
- **Negative EPS**: Company losing money (P/E undefined)
- **Negative Equity**: Liabilities > Assets (ROE undefined)
- **Negative Cash Flow**: Cash outflow

Handle these cases explicitly:

```python
if net_income < 0:
    return {"roe": None, "note": "Negative net income"}
```

---

## Summary

This guide provides:

✅ **33+ Financial Ratios** with formulas and examples
✅ **Complete Python Implementation** ready to use
✅ **API Endpoint Documentation** for each data point
✅ **Real Examples** using AAPL Q4 2020 data
✅ **Interpretation Guidelines** for each ratio
✅ **Best Practices** for accurate calculations

### Key Takeaways

1. **Use Filter Parameter**: Fetch multiple fields in one API call
2. **Adjusted Close**: Always use for price-based ratios
3. **Validation**: Check for null, zero, negative values
4. **Caching**: Financial data doesn't change - cache it
5. **Documentation**: Document formulas and data sources
6. **Comparison**: Ratios are most useful when compared to peers and history

### Additional Resources

- **Fundamentals API**: https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds
- **End-of-Day API**: https://eodhd.com/financial-apis/api-for-historical-data-and-volumes
- **Common Stock Ratios Reference**: fundamentals-ratios.md
- **Data Adjustment Guide**: data-adjustment-guide.md

---

**Document Version**: 1.0
**Last Updated**: 2024-11-27
**Maintained by**: EODHD Skills Project
