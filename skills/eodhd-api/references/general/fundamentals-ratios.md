# Financial Ratios & Calculations Reference

This reference guide provides formulas and explanations for calculating key financial ratios and metrics from the EODHD Fundamentals API data.

## Overview

This document explains how various financial metrics are calculated from the raw fundamental data fields. Use this as a reference when analyzing stocks or building financial models.

**Related Documentation**:
- [Common Stock Fundamentals Guide](fundamentals-common-stock.md) - Complete API reference
- [Fundamentals API Overview](fundamentals-api.md) - All instrument types

---

## Table of Contents

- [Valuation Ratios](#valuation-ratios)
- [Profitability Ratios](#profitability-ratios)
- [Liquidity Ratios](#liquidity-ratios)
- [Efficiency Ratios](#efficiency-ratios)
- [Leverage Ratios](#leverage-ratios)
- [Market Ratios](#market-ratios)
- [Growth Metrics](#growth-metrics)
- [Cash Flow Metrics](#cash-flow-metrics)

---

## Valuation Ratios

### Price-to-Earnings Ratio (P/E)

**Trailing P/E (TTM)**:
```
TrailingPE = Current Stock Price / Diluted EPS (TTM)
```

**Forward P/E**:
```
ForwardPE = Current Stock Price / Estimated Future EPS
```

**Fields Used**:
- `Valuation::TrailingPE` (provided)
- `Valuation::ForwardPE` (provided)
- `Highlights::DilutedEpsTTM`
- `Highlights::EPSEstimateNextYear`

**Interpretation**:
- Higher P/E = market expects higher growth
- Lower P/E = potentially undervalued or lower growth expectations
- Compare to industry peers and historical average

---

### Price-to-Earnings Growth Ratio (PEG)

**Formula**:
```
PEGRatio = PERatio / Expected Earnings Growth Rate (5 year)
```

**Fields Used**:
- `Highlights::PEGRatio` (provided)
- `Highlights::PERatio`

**Interpretation**:
- PEG < 1: Stock may be undervalued relative to growth
- PEG = 1: Stock is fairly valued
- PEG > 1: Stock may be overvalued relative to growth

---

### Price-to-Sales Ratio (P/S)

**Formula (TTM)**:
```
PriceSalesTTM = Market Capitalization / Revenue (TTM)
```

Or per share:
```
Price-to-Sales = Stock Price / Revenue Per Share (TTM)
```

**Fields Used**:
- `Valuation::PriceSalesTTM` (provided)
- `Highlights::MarketCapitalization`
- `Highlights::RevenueTTM`
- `Highlights::RevenuePerShareTTM`

**Interpretation**:
- Useful for companies with negative earnings
- Lower P/S = better value
- Compare to industry peers

---

### Price-to-Book Ratio (P/B)

**Formula (MRQ)**:
```
PriceBookMRQ = Stock Price / Book Value Per Share
```

**Fields Used**:
- `Valuation::PriceBookMRQ` (provided)
- `Highlights::BookValue`

**Calculation of Book Value Per Share**:
```
BookValue = (Total Assets - Total Liabilities) / Shares Outstanding
BookValue = Total Stockholder Equity / Shares Outstanding
```

**Source Fields**:
- `Financials::Balance_Sheet::totalStockholderEquity`
- `SharesStats::SharesOutstanding`

**Interpretation**:
- P/B < 1: Stock trading below book value
- P/B > 1: Market values company above assets
- Industry-dependent (tech typically higher, financials lower)

---

### Enterprise Value Ratios

#### Enterprise Value (EV)

**Formula**:
```
EnterpriseValue = Market Cap + Total Debt + Minority Interest - Cash & Equivalents
```

**Simplified**:
```
EV = MarketCapitalization + shortLongTermDebtTotal + minorityInterest - cashAndEquivalents
```

**Fields Used**:
- `Valuation::EnterpriseValue` (provided)
- `Highlights::MarketCapitalization`
- `Financials::Balance_Sheet::shortLongTermDebtTotal`
- `Financials::Balance_Sheet::cashAndEquivalents`

#### EV/Revenue

**Formula**:
```
EnterpriseValueRevenue = Enterprise Value / Revenue (TTM)
```

**Fields Used**:
- `Valuation::EnterpriseValueRevenue` (provided)
- `Valuation::EnterpriseValue`
- `Highlights::RevenueTTM`

#### EV/EBITDA

**Formula**:
```
EnterpriseValueEbitda = Enterprise Value / EBITDA
```

**Fields Used**:
- `Valuation::EnterpriseValueEbitda` (provided)
- `Valuation::EnterpriseValue`
- `Highlights::EBITDA`

**Interpretation**:
- EV/EBITDA is capital-structure neutral
- Lower ratio = potentially better value
- Typical range: 10-15 (varies by industry)

---

## Profitability Ratios

### Profit Margin

**Net Profit Margin**:
```
ProfitMargin = Net Income / Total Revenue
```

**Fields Used**:
- `Highlights::ProfitMargin` (provided)
- `Financials::Income_Statement::netIncome`
- `Financials::Income_Statement::totalRevenue`

**Interpretation**:
- Higher margin = more profitable
- Industry-dependent (software >20%, retail <5%)

---

### Operating Margin

**Formula (TTM)**:
```
OperatingMarginTTM = (Operating Income / Total Revenue) × 100
```

**Fields Used**:
- `Highlights::OperatingMarginTTM` (provided)
- `Financials::Income_Statement::operatingIncome`
- `Financials::Income_Statement::totalRevenue`

**Interpretation**:
- Measures operational efficiency
- Excludes financing and tax impacts
- Higher = better operational performance

---

### Gross Profit Margin

**Formula**:
```
Gross Profit Margin = (Gross Profit / Total Revenue) × 100
```

**Calculation of Gross Profit**:
```
GrossProfit = Total Revenue - Cost of Revenue
```

**Fields Used**:
- `Highlights::GrossProfitTTM` (provided)
- `Financials::Income_Statement::grossProfit`
- `Financials::Income_Statement::totalRevenue`
- `Financials::Income_Statement::costOfRevenue`

---

### Return on Assets (ROA)

**Formula (TTM)**:
```
ReturnOnAssetsTTM = Net Income / Total Assets
```

**Fields Used**:
- `Highlights::ReturnOnAssetsTTM` (provided)
- `Financials::Income_Statement::netIncome`
- `Financials::Balance_Sheet::totalAssets`

**Interpretation**:
- Measures how efficiently assets generate profit
- Higher ROA = better asset utilization
- Industry-dependent (capital-intensive industries typically lower)

---

### Return on Equity (ROE)

**Formula (TTM)**:
```
ReturnOnEquityTTM = Net Income / Total Stockholder Equity
```

**Fields Used**:
- `Highlights::ReturnOnEquityTTM` (provided)
- `Financials::Income_Statement::netIncome`
- `Financials::Balance_Sheet::totalStockholderEquity`

**Interpretation**:
- Measures return to shareholders
- Higher ROE = better shareholder returns
- Warren Buffett looks for ROE > 15%

---

### EBITDA

**Calculation**:
```
EBITDA = EBIT + Depreciation + Amortization
```

Or from Income Statement:
```
EBITDA = Total Revenue - Cost of Revenue - Total Operating Expenses + D&A
```

**Fields Used**:
- `Highlights::EBITDA` (provided)
- `Financials::Income_Statement::ebitda`
- `Financials::Income_Statement::ebit`
- `Financials::Income_Statement::depreciationAndAmortization`

---

## Liquidity Ratios

### Current Ratio

**Formula**:
```
Current Ratio = Total Current Assets / Total Current Liabilities
```

**Fields Used**:
- `Financials::Balance_Sheet::totalCurrentAssets`
- `Financials::Balance_Sheet::totalCurrentLiabilities`

**Interpretation**:
- Ratio > 2: Good short-term liquidity
- Ratio 1-2: Adequate liquidity
- Ratio < 1: Potential liquidity concerns

---

### Quick Ratio (Acid Test)

**Formula**:
```
Quick Ratio = (Current Assets - Inventory) / Current Liabilities
```

Or:
```
Quick Ratio = (Cash + Short-Term Investments + Receivables) / Current Liabilities
```

**Fields Used**:
- `Financials::Balance_Sheet::totalCurrentAssets`
- `Financials::Balance_Sheet::inventory`
- `Financials::Balance_Sheet::totalCurrentLiabilities`
- `Financials::Balance_Sheet::cash`
- `Financials::Balance_Sheet::shortTermInvestments`
- `Financials::Balance_Sheet::netReceivables`

**Interpretation**:
- More conservative than current ratio
- Ratio > 1: Good liquidity without selling inventory
- Ratio < 1: May need to sell inventory or borrow

---

### Cash Ratio

**Formula**:
```
Cash Ratio = (Cash + Cash Equivalents) / Current Liabilities
```

**Fields Used**:
- `Financials::Balance_Sheet::cashAndEquivalents`
- `Financials::Balance_Sheet::totalCurrentLiabilities`

**Interpretation**:
- Most conservative liquidity measure
- Shows ability to pay debts with cash only

---

### Net Working Capital

**Formula**:
```
NetWorkingCapital = (Total Current Assets - Cash) - (Total Current Liabilities - Short-Long Term Debt)
```

**Fields Used**:
- `Financials::Balance_Sheet::netWorkingCapital` (provided)
- `Financials::Balance_Sheet::totalCurrentAssets`
- `Financials::Balance_Sheet::cash`
- `Financials::Balance_Sheet::totalCurrentLiabilities`
- `Financials::Balance_Sheet::shortLongTermDebtTotal`

**Interpretation**:
- Positive: Company can fund operations
- Negative: Potential liquidity issues

---

## Efficiency Ratios

### Asset Turnover

**Formula**:
```
Asset Turnover = Total Revenue / Average Total Assets
```

**Fields Used**:
- `Financials::Income_Statement::totalRevenue`
- `Financials::Balance_Sheet::totalAssets` (current and prior period)

**Interpretation**:
- Higher ratio = more efficient asset utilization
- Industry-dependent (retail high, utilities low)

---

### Inventory Turnover

**Formula**:
```
Inventory Turnover = Cost of Revenue / Average Inventory
```

**Fields Used**:
- `Financials::Income_Statement::costOfRevenue`
- `Financials::Balance_Sheet::inventory` (current and prior period)

**Interpretation**:
- Higher = faster inventory movement
- Lower = slow-moving or obsolete inventory risk

---

### Receivables Turnover

**Formula**:
```
Receivables Turnover = Total Revenue / Average Net Receivables
```

**Fields Used**:
- `Financials::Income_Statement::totalRevenue`
- `Financials::Balance_Sheet::netReceivables` (current and prior period)

**Days Sales Outstanding (DSO)**:
```
DSO = 365 / Receivables Turnover
```

**Interpretation**:
- Higher turnover = faster collection
- Lower DSO = better cash collection

---

## Leverage Ratios

### Debt-to-Equity Ratio

**Formula**:
```
Debt-to-Equity = Total Debt / Total Stockholder Equity
```

**Fields Used**:
- `Financials::Balance_Sheet::shortLongTermDebtTotal`
- `Financials::Balance_Sheet::totalStockholderEquity`

**Interpretation**:
- Ratio > 2: High leverage
- Ratio 1-2: Moderate leverage
- Ratio < 1: Conservative leverage
- Industry-dependent (utilities higher, tech lower)

---

### Debt-to-Assets Ratio

**Formula**:
```
Debt-to-Assets = Total Debt / Total Assets
```

**Fields Used**:
- `Financials::Balance_Sheet::shortLongTermDebtTotal`
- `Financials::Balance_Sheet::totalAssets`

**Interpretation**:
- Shows percentage of assets financed by debt
- Lower ratio = less risky

---

### Net Debt

**Formula**:
```
NetDebt = Short-Term Debt + Long-Term Debt - Cash
```

**Fields Used**:
- `Financials::Balance_Sheet::netDebt` (provided)
- `Financials::Balance_Sheet::shortTermDebt`
- `Financials::Balance_Sheet::longTermDebtTotal`
- `Financials::Balance_Sheet::cash`

**Interpretation**:
- Negative net debt = more cash than debt (strong position)
- Positive net debt = company is net borrower

---

### Interest Coverage Ratio

**Formula**:
```
Interest Coverage = EBIT / Interest Expense
```

**Fields Used**:
- `Financials::Income_Statement::ebit`
- `Financials::Income_Statement::interestExpense`

**Interpretation**:
- Ratio > 3: Comfortable coverage
- Ratio 1.5-3: Adequate coverage
- Ratio < 1.5: Financial stress potential

---

## Market Ratios

### Earnings Per Share (EPS)

**Diluted EPS (TTM)**:
```
DilutedEpsTTM = Net Income / Weighted Average Diluted Shares Outstanding
```

**Fields Used**:
- `Highlights::DilutedEpsTTM` (provided)
- `Financials::Income_Statement::netIncome`
- `Financials::Balance_Sheet::commonStockSharesOutstanding`

---

### Dividend Yield

**Formula**:
```
DividendYield = Annual Dividend Per Share / Current Stock Price
```

Or:
```
DividendYield = DividendShare / Current Price
```

**Fields Used**:
- `Highlights::DividendYield` (provided)
- `Highlights::DividendShare`
- `SplitsDividends::ForwardAnnualDividendYield`

**Interpretation**:
- Higher yield = more income return
- Compare to industry and historical average
- Extremely high yield may signal distress

---

### Dividend Payout Ratio

**Formula (TTM)**:
```
PayoutRatio = Sum of Last 4 Quarters Dividends Paid / Sum of Last 4 Quarters Net Income
```

Or:
```
Payout Ratio = Dividends Paid / Net Income Applicable to Common Shares
```

**Fields Used**:
- `SplitsDividends::PayoutRatio` (provided)
- `Financials::Cash_Flow::dividendsPaid` (last 4 quarters)
- `Financials::Income_Statement::netIncomeApplicableToCommonShares` (last 4 quarters)

**Interpretation**:
- Ratio 0-30%: Growth company, reinvesting
- Ratio 30-60%: Balanced approach
- Ratio 60-100%: Income-focused, mature company
- Ratio > 100%: Unsustainable, paying more than earning

---

### Book Value Per Share

**Formula**:
```
BookValue = (Total Assets - Total Liabilities) / Shares Outstanding
```

Or:
```
BookValue = Total Stockholder Equity / Shares Outstanding
```

**Fields Used**:
- `Highlights::BookValue` (provided)
- `Financials::Balance_Sheet::totalStockholderEquity`
- `SharesStats::SharesOutstanding`

---

### Market Capitalization

**Formula**:
```
MarketCapitalization = Current Stock Price × Shares Outstanding
```

**Fields Used**:
- `Highlights::MarketCapitalization` (provided)
- `Highlights::MarketCapitalizationMln` (in millions)

---

## Growth Metrics

### Revenue Growth (YoY)

**Quarterly Revenue Growth**:
```
QuarterlyRevenueGrowthYOY = (Q4 Year 2 Revenue - Q4 Year 1 Revenue) / Q4 Year 1 Revenue
```

**Fields Used**:
- `Highlights::QuarterlyRevenueGrowthYOY` (provided)
- `Financials::Income_Statement::totalRevenue` (compare same quarter year-over-year)

**Annual Revenue Growth**:
```
Annual Growth = (Current Year Revenue - Prior Year Revenue) / Prior Year Revenue
```

---

### Earnings Growth (YoY)

**Quarterly Earnings Growth**:
```
QuarterlyEarningsGrowthYOY = (Q4 Year 2 EPS - Q4 Year 1 EPS) / Q4 Year 1 EPS
```

**Fields Used**:
- `Highlights::QuarterlyEarningsGrowthYOY` (provided)
- `Earnings::History` (compare same quarter year-over-year)

---

### Estimated Growth

**Earnings Estimate Growth**:
```
earningsEstimateGrowth = (earningsEstimateAvg - earningsEstimateYearAgoEps) / earningsEstimateYearAgoEps
```

**Revenue Estimate Growth**:
```
revenueEstimateGrowth = (revenueEstimateAvg - revenueEstimateYearAgoEps) / revenueEstimateYearAgoEps
```

**Fields Used**:
- `Earnings::Trend::{period}::earningsEstimateGrowth`
- `Earnings::Trend::{period}::revenueEstimateGrowth`
- `Earnings::Trend::{period}::growth`

---

## Cash Flow Metrics

### Free Cash Flow (FCF)

**Formula**:
```
FreeCashFlow = Operating Cash Flow - Capital Expenditures
```

**Fields Used**:
- `Financials::Cash_Flow::freeCashFlow` (provided)
- `Financials::Cash_Flow::totalCashFromOperatingActivities`
- `Financials::Cash_Flow::capitalExpenditures`

**Interpretation**:
- Positive FCF: Company generates excess cash
- Negative FCF: Company consuming cash
- Growing FCF: Sign of financial health

---

### FCF Yield

**Formula**:
```
FCF Yield = Free Cash Flow / Market Capitalization
```

**Fields Used**:
- `Financials::Cash_Flow::freeCashFlow`
- `Highlights::MarketCapitalization`

**Interpretation**:
- Higher yield = better value
- Compare to dividend yield and earnings yield

---

### Operating Cash Flow Ratio

**Formula**:
```
OCF Ratio = Operating Cash Flow / Current Liabilities
```

**Fields Used**:
- `Financials::Cash_Flow::totalCashFromOperatingActivities`
- `Financials::Balance_Sheet::totalCurrentLiabilities`

**Interpretation**:
- Measures ability to pay short-term obligations with cash from operations
- Ratio > 1: Strong liquidity

---

### Cash Flow to Net Income

**Formula**:
```
CF to NI Ratio = Operating Cash Flow / Net Income
```

**Fields Used**:
- `Financials::Cash_Flow::totalCashFromOperatingActivities`
- `Financials::Income_Statement::netIncome`

**Interpretation**:
- Ratio > 1: High-quality earnings (cash backing)
- Ratio < 1: Earnings not converting to cash
- Ratio consistently > 1.5: Excellent cash generation

---

## Special Calculations

### Working Capital

**Formula**:
```
Working Capital = Current Assets - Current Liabilities
```

**Net Working Capital (Alternative)**:
```
NetWorkingCapital = (Current Assets - Cash) - (Current Liabilities - Short-Long Term Debt)
```

**Fields Used**:
- `Financials::Balance_Sheet::totalCurrentAssets`
- `Financials::Balance_Sheet::totalCurrentLiabilities`
- `Financials::Balance_Sheet::netWorkingCapital` (provided)

---

### Invested Capital

**Formula**:
```
NetInvestedCapital = Total Equity + Total Debt - Cash
```

Or:
```
Invested Capital = Total Assets - Non-Interest Bearing Current Liabilities
```

**Fields Used**:
- `Financials::Balance_Sheet::netInvestedCapital` (provided)

---

### Return on Invested Capital (ROIC)

**Formula**:
```
ROIC = NOPAT / Invested Capital
```

Where NOPAT (Net Operating Profit After Tax):
```
NOPAT = Operating Income × (1 - Tax Rate)
```

**Fields Used**:
- `Financials::Income_Statement::operatingIncome`
- `Financials::Income_Statement::incomeTaxExpense`
- `Financials::Income_Statement::incomeBeforeTax`
- `Financials::Balance_Sheet::netInvestedCapital`

**Tax Rate Calculation**:
```
Tax Rate = Income Tax Expense / Income Before Tax
```

---

## Surprise Metrics

### Earnings Surprise

**Formula**:
```
surprisePercent = (epsActual - epsEstimate) / epsEstimate
```

**Absolute Surprise**:
```
epsDifference = epsActual - epsEstimate
```

**Fields Used**:
- `Earnings::History::{date}::epsActual`
- `Earnings::History::{date}::epsEstimate`
- `Earnings::History::{date}::epsDifference` (provided)
- `Earnings::History::{date}::surprisePercent` (provided)

**Interpretation**:
- Positive surprise: Beat expectations (typically bullish)
- Negative surprise: Missed expectations (typically bearish)
- Consistent beats: High-quality company

---

## Ratios Summary Table

| Ratio | Formula | Ideal Range | Use Case |
|-------|---------|-------------|----------|
| **P/E** | Price / EPS | 15-25 (varies) | Valuation |
| **PEG** | P/E / Growth Rate | < 1 | Growth valuation |
| **P/S** | Market Cap / Revenue | Industry-dependent | Sales efficiency |
| **P/B** | Price / Book Value | < 3 (varies) | Asset value |
| **EV/EBITDA** | EV / EBITDA | 10-15 | Enterprise valuation |
| **ROE** | Net Income / Equity | > 15% | Shareholder returns |
| **ROA** | Net Income / Assets | > 5% | Asset efficiency |
| **Current Ratio** | Current Assets / Current Liab | 1.5-3 | Liquidity |
| **Quick Ratio** | (CA - Inventory) / CL | > 1 | Liquidity (conservative) |
| **Debt/Equity** | Total Debt / Equity | < 2 | Leverage |
| **Profit Margin** | Net Income / Revenue | > 10% | Profitability |
| **Dividend Yield** | Dividend / Price | 2-6% | Income |
| **Payout Ratio** | Dividends / Net Income | 30-60% | Dividend sustainability |
| **FCF Yield** | FCF / Market Cap | > 5% | Cash generation value |

---

## Data Extraction Examples

### Python Example

```python
import requests

def calculate_current_ratio(ticker, api_token):
    """Calculate current ratio from balance sheet data."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "Financials::Balance_Sheet::quarterly",
        "from": "2024-09-30",
        "to": "2024-09-30"
    }

    response = requests.get(url, params=params).json()
    latest_quarter = list(response["quarterly"].values())[0]

    current_assets = float(latest_quarter["totalCurrentAssets"])
    current_liabilities = float(latest_quarter["totalCurrentLiabilities"])

    current_ratio = current_assets / current_liabilities

    return {
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "current_ratio": current_ratio,
        "status": "Healthy" if current_ratio > 1.5 else "Concerning"
    }

# Usage
result = calculate_current_ratio("AAPL.US", "demo")
print(f"Current Ratio: {result['current_ratio']:.2f}")
print(f"Status: {result['status']}")
```

### Comprehensive Valuation Example

```python
def get_valuation_metrics(ticker, api_token):
    """Get comprehensive valuation metrics."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "Highlights,Valuation"
    }

    data = requests.get(url, params=params).json()

    return {
        "pe_ratio": data["Valuation"]["TrailingPE"],
        "forward_pe": data["Valuation"]["ForwardPE"],
        "peg_ratio": data["Highlights"]["PEGRatio"],
        "ps_ratio": data["Valuation"]["PriceSalesTTM"],
        "pb_ratio": data["Valuation"]["PriceBookMRQ"],
        "ev_ebitda": data["Valuation"]["EnterpriseValueEbitda"],
        "market_cap_mln": data["Highlights"]["MarketCapitalizationMln"]
    }

# Usage
metrics = get_valuation_metrics("AAPL.US", "demo")
for metric, value in metrics.items():
    print(f"{metric}: {value}")
```

---

## Notes and Best Practices

### Field Availability

**Important**: Not all companies report all fields. Always check for None/null values:

```python
# Safe access pattern
roe = data.get("Highlights", {}).get("ReturnOnEquityTTM")
if roe is not None:
    print(f"ROE: {roe * 100:.2f}%")
else:
    print("ROE not available")
```

### TTM vs MRQ

- **TTM** (Trailing Twelve Months): Sum of last 4 quarters
- **MRQ** (Most Recent Quarter): Latest quarter only

Use TTM for annual metrics, MRQ for point-in-time balance sheet items.

### Industry Comparisons

Always compare ratios to:
1. Industry peers
2. Company's historical average
3. Market average
4. Industry benchmarks

### Data Quality

- Check `General::UpdatedAt` for last refresh date
- Verify `Financials::{statement}::filing_date` for statement dates
- Cross-reference multiple metrics for consistency

---

**Last Updated**: February 2026
**API Version**: Current
**Maintained By**: EODHD Skills Team
