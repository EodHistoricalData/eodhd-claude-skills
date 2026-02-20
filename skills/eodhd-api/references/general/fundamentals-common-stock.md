# Common Stock Fundamentals API - Complete Guide

This guide covers the Fundamentals API specifically for **Common Stocks (Equities)**.

## Overview

The EODHD API provides extensive fundamental data for stocks from different exchanges and countries. This is the most comprehensive fundamental data type, with 10+ top-level sections and support for both US and non-US companies.

**Key Characteristics**:
- **API calls consumption**: 10 calls per request
- **Format**: JSON only (due to complex data structure)
- **Response size**: Very large (800+ KB for major stocks)
- **Filter support**: **Critical** - Always use filters for production
- **Type field**: `"Type": "Common Stock"` in the General section
- **Date filtering**: ✅ **NEW** - Supported for financial statements

## Data Coverage

### Historical Data Availability

| Company Type | Coverage Period | Details |
|-------------|----------------|---------|
| **Major US companies** | From 1985 | 30+ years of financial data |
| **Non-US companies** | From 2000 | 21+ years of financial data |
| **Major US exchanges** | 20 years | Both yearly and quarterly (NYSE, NASDAQ, ARCA - ~11,000 tickers) |
| **Minor companies** | 6 years + 20 quarters | Last 6 years yearly, previous 20 quarters |

**Note**: Not all companies report complete financial data. Some data points may be unavailable for certain companies.

## API Endpoint

### Base URL Format

```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json
```

**Parameters**:
- `{TICKER}`: Format `{SYMBOL}.{EXCHANGE}` (e.g., `AAPL.US`, `BMW.XETRA`)
- `{API_TOKEN}`: Your API key
- `fmt=json`: Required (JSON only format)
- `filter=`: **Highly recommended** - Retrieve specific sections only
- `from=` / `to=`: **NEW** - Date filtering for financial statements

**Example - Full data**:
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json
```

**Example - Filtered data**:
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Highlights
```

**Example - Date filtered financials** (NEW):
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Cash_Flow::quarterly&from=2024-09-30&to=2024-12-31
```

## Data Structure

Common Stock fundamental data has **12+ top-level sections**:

| Section | Description | Use Filter |
|---------|-------------|------------|
| **General** | Company details, officers, identifiers | `&filter=General` |
| **Highlights** | Key financial metrics and ratios | `&filter=Highlights` |
| **Valuation** | Valuation metrics (P/E, P/S, P/B, EV) | `&filter=Valuation` |
| **SharesStats** | Share statistics and ownership | `&filter=SharesStats` |
| **Technicals** | Technical indicators and metrics | `&filter=Technicals` |
| **SplitsDividends** | Dividend and split history | `&filter=SplitsDividends` |
| **AnalystRatings** | Analyst recommendations | `&filter=AnalystRatings` |
| **Holders** | Institutional and fund holders | `&filter=Holders` |
| **InsiderTransactions** | Insider trading activity | `&filter=InsiderTransactions` |
| **ESGScores** | ESG ratings (if available) | `&filter=ESGScores` |
| **outstandingShares** | Historical shares outstanding | `&filter=outstandingShares` |
| **Earnings** | Earnings history and estimates | `&filter=Earnings` |
| **Financials** | Financial statements | `&filter=Financials` |

## Section 1: General

Returns comprehensive company information including identifiers, officers, and listings.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=General
```

### Response Structure (Partial)

```json
{
  "Code": "AAPL",
  "Type": "Common Stock",
  "Name": "Apple Inc",
  "Exchange": "NASDAQ",
  "CurrencyCode": "USD",
  "CurrencyName": "US Dollar",
  "CurrencySymbol": "$",
  "CountryName": "USA",
  "CountryISO": "US",
  "OpenFigi": "BBG000B9XRY4",
  "ISIN": "US0378331005",
  "LEI": "HWUPKR0MPOU8FGXBT394",
  "PrimaryTicker": "AAPL.US",
  "CUSIP": "037833100",
  "CIK": "320193",
  "EmployerIdNumber": "94-2404110",
  "FiscalYearEnd": "September",
  "IPODate": "1980-12-12",
  "InternationalDomestic": "International/Domestic",
  "Sector": "Technology",
  "Industry": "Consumer Electronics",
  "GicSector": "Information Technology",
  "GicGroup": "Technology Hardware & Equipment",
  "GicIndustry": "Technology Hardware, Storage & Peripherals",
  "GicSubIndustry": "Technology Hardware, Storage & Peripherals",
  "HomeCategory": "Domestic",
  "IsDelisted": false,
  "Description": "Apple Inc. designs, manufactures, and markets smartphones...",
  "Address": "One Apple Park Way, Cupertino, CA, United States, 95014",
  "AddressData": {
    "Street": "One Apple Park Way",
    "City": "Cupertino",
    "State": "CA",
    "Country": "United States",
    "ZIP": "95014"
  },
  "Listings": {
    "0": {
      "Code": "0R2V",
      "Exchange": "LSE",
      "Name": "Apple Inc."
    }
  },
  "Officers": {
    "0": {
      "Name": "Mr. Timothy D. Cook",
      "Title": "CEO & Director",
      "YearBorn": "1961"
    }
  },
  "Phone": "(408) 996-1010",
  "WebURL": "https://www.apple.com",
  "LogoURL": "/img/logos/US/aapl.png",
  "FullTimeEmployees": 164000,
  "UpdatedAt": "2025-01-21"
}
```

### Field Descriptions

#### Basic Information

| Field | Type | Description |
|-------|------|-------------|
| `Code` | string | Stock ticker symbol (without exchange) |
| `Type` | string | Always "Common Stock" for stocks |
| `Name` | string | Full company name |
| `Exchange` | string | Primary exchange listing |
| `CurrencyCode` | string | Trading currency code (ISO 4217) |
| `CurrencyName` | string | Currency full name |
| `CurrencySymbol` | string | Currency symbol |
| `CountryName` | string | Country of domicile |
| `CountryISO` | string | ISO 3166-1 alpha-2 country code |

#### Identifiers

| Field | Type | Description |
|-------|------|-------------|
| `OpenFigi` | string | Financial Instrument Global Identifier |
| `ISIN` | string | International Securities Identification Number |
| `LEI` | string | Legal Entity Identifier |
| `PrimaryTicker` | string | Primary ticker with exchange (e.g., "AAPL.US") |
| `CUSIP` | string | Committee on Uniform Securities Identification Procedures |
| `CIK` | string | Central Index Key (SEC identifier) |
| `EmployerIdNumber` | string | EIN (tax identifier) |

#### Company Details

| Field | Type | Description |
|-------|------|-------------|
| `FiscalYearEnd` | string | Fiscal year end month |
| `IPODate` | string | Initial public offering date (YYYY-MM-DD) |
| `InternationalDomestic` | string | Business scope classification |
| `Sector` | string | Business sector |
| `Industry` | string | Specific industry |
| `GicSector` | string | Global Industry Classification Standard - Sector |
| `GicGroup` | string | GICS Group |
| `GicIndustry` | string | GICS Industry |
| `GicSubIndustry` | string | GICS Sub-Industry |
| `HomeCategory` | string | "Domestic" or "ADR" (American Depositary Receipt) |
| `IsDelisted` | boolean | Whether the stock has been delisted |
| `Description` | string | Detailed company description |

#### Contact Information

| Field | Type | Description |
|-------|------|-------------|
| `Address` | string | Full address as single string |
| `AddressData` | object | Structured address (Street, City, State, Country, ZIP) |
| `Phone` | string | Company phone number |
| `WebURL` | string | Official website URL |
| `LogoURL` | string | Path to company logo (available for major companies) |

#### Additional Fields

| Field | Type | Description |
|-------|------|-------------|
| `FullTimeEmployees` | number | Number of full-time employees |
| `UpdatedAt` | string | Last update date (YYYY-MM-DD) |
| `Listings` | object | Other exchange listings (array-indexed) |
| `Officers` | object | Company executives (array-indexed) |

### Officers Structure

Each officer entry contains:
- `Name` - Full name with title prefix (Mr./Ms.)
- `Title` - Job title/role
- `YearBorn` - Birth year (or "NA" if unavailable)

### Listings Structure

Each listing entry contains:
- `Code` - Ticker symbol on that exchange
- `Exchange` - Exchange code
- `Name` - Company name on that listing

## Section 2: Highlights

Returns key financial metrics and performance indicators.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Highlights
```

### Response Structure

```json
{
  "MarketCapitalization": 3458400518144,
  "MarketCapitalizationMln": 3458400.5181,
  "EBITDA": 134660997120,
  "PERatio": 37.8639,
  "PEGRatio": 2.0958,
  "WallStreetTargetPrice": 246.1405,
  "BookValue": 3.767,
  "DividendShare": 0.98,
  "DividendYield": 0.0043,
  "EarningsShare": 5.88,
  "EPSEstimateCurrentYear": 7.368,
  "EPSEstimateNextYear": 8.2441,
  "EPSEstimateNextQuarter": 2.38,
  "EPSEstimateCurrentQuarter": 1.6,
  "MostRecentQuarter": "2024-09-30",
  "ProfitMargin": 0.2397,
  "OperatingMarginTTM": 0.3117,
  "ReturnOnAssetsTTM": 0.2146,
  "ReturnOnEquityTTM": 1.5741,
  "RevenueTTM": 391034994688,
  "RevenuePerShareTTM": 25.485,
  "QuarterlyRevenueGrowthYOY": 0.061,
  "GrossProfitTTM": 180682997760,
  "DilutedEpsTTM": 5.88,
  "QuarterlyEarningsGrowthYOY": -0.341
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `MarketCapitalization` | number | Total market cap in base currency |
| `MarketCapitalizationMln` | number | Market cap in millions |
| `EBITDA` | number | Earnings before interest, taxes, depreciation, amortization |
| `PERatio` | number | Price-to-earnings ratio |
| `PEGRatio` | number | Price/earnings to growth ratio |
| `WallStreetTargetPrice` | number | Average analyst target price |
| `BookValue` | number | Book value per share |
| `DividendShare` | number | Annual dividend per share |
| `DividendYield` | number | Annual dividend yield (decimal) |
| `EarningsShare` | number | Earnings per share (TTM) |
| `EPSEstimateCurrentYear` | number | EPS estimate for current fiscal year |
| `EPSEstimateNextYear` | number | EPS estimate for next fiscal year |
| `EPSEstimateNextQuarter` | number | EPS estimate for next quarter |
| `EPSEstimateCurrentQuarter` | number | EPS estimate for current quarter |
| `MostRecentQuarter` | string | Most recent quarter date (YYYY-MM-DD) |
| `ProfitMargin` | number | Net profit margin (decimal) |
| `OperatingMarginTTM` | number | Operating margin, trailing twelve months |
| `ReturnOnAssetsTTM` | number | Return on assets TTM (decimal) |
| `ReturnOnEquityTTM` | number | Return on equity TTM (decimal) |
| `RevenueTTM` | number | Total revenue, trailing twelve months |
| `RevenuePerShareTTM` | number | Revenue per share TTM |
| `QuarterlyRevenueGrowthYOY` | number | Quarterly revenue growth YoY (decimal) |
| `GrossProfitTTM` | number | Gross profit TTM |
| `DilutedEpsTTM` | number | Diluted earnings per share TTM |
| `QuarterlyEarningsGrowthYOY` | number | Quarterly earnings growth YoY (decimal) |

**Note**: Decimal fields represent percentages (e.g., 0.2397 = 23.97%).

## Section 3: Valuation

Returns valuation metrics and ratios.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Valuation
```

### Response Structure

```json
{
  "TrailingPE": 37.8639,
  "ForwardPE": 30.7692,
  "PriceSalesTTM": 8.8442,
  "PriceBookMRQ": 60.7271,
  "EnterpriseValue": 3499868262520,
  "EnterpriseValueRevenue": 8.9503,
  "EnterpriseValueEbitda": 25.9902
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `TrailingPE` | number | Trailing price-to-earnings ratio (based on TTM earnings) |
| `ForwardPE` | number | Forward P/E ratio (based on estimated future earnings) |
| `PriceSalesTTM` | number | Price-to-sales ratio (TTM) |
| `PriceBookMRQ` | number | Price-to-book ratio (most recent quarter) |
| `EnterpriseValue` | number | Enterprise value (market cap + debt - cash) |
| `EnterpriseValueRevenue` | number | EV-to-revenue ratio |
| `EnterpriseValueEbitda` | number | EV-to-EBITDA ratio |

## Section 4: SharesStats

Returns share statistics and ownership percentages.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=SharesStats
```

### Response Structure

```json
{
  "SharesOutstanding": 15037899776,
  "SharesFloat": 15091184209,
  "PercentInsiders": 2.066,
  "PercentInstitutions": 62.25,
  "SharesShort": null,
  "SharesShortPriorMonth": null,
  "ShortRatio": null,
  "ShortPercentOutstanding": null,
  "ShortPercentFloat": 0.0104
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `SharesOutstanding` | number | Total shares outstanding |
| `SharesFloat` | number | Shares available for trading (float) |
| `PercentInsiders` | number | Percentage held by insiders |
| `PercentInstitutions` | number | Percentage held by institutions |
| `SharesShort` | number/null | Total shares sold short |
| `SharesShortPriorMonth` | number/null | Shares short previous month |
| `ShortRatio` | number/null | Days to cover short positions |
| `ShortPercentOutstanding` | number/null | Short interest as % of outstanding |
| `ShortPercentFloat` | number | Short interest as % of float |

**Note**: Some short interest fields may be null if data is unavailable.

## Section 5: Technicals

Returns technical indicators and performance metrics.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Technicals
```

### Response Structure

```json
{
  "Beta": 1.24,
  "52WeekHigh": 260.1,
  "52WeekLow": 163.4884,
  "50DayMA": 239.2966,
  "200DayMA": 217.0157,
  "SharesShort": 157008120,
  "SharesShortPriorMonth": 156458273,
  "ShortRatio": 3.37,
  "ShortPercent": 0.0104
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `Beta` | number | Stock volatility vs. market (1.0 = market volatility) |
| `52WeekHigh` | number | Highest price in past 52 weeks |
| `52WeekLow` | number | Lowest price in past 52 weeks |
| `50DayMA` | number | 50-day moving average |
| `200DayMA` | number | 200-day moving average |
| `SharesShort` | number | Current shares sold short |
| `SharesShortPriorMonth` | number | Shares short previous month |
| `ShortRatio` | number | Days to cover (short interest ratio) |
| `ShortPercent` | number | Short interest as percentage (decimal) |

## Section 6: SplitsDividends

Returns dividend and stock split history.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=SplitsDividends
```

### Response Structure

```json
{
  "ForwardAnnualDividendRate": 1,
  "ForwardAnnualDividendYield": 0.0043,
  "PayoutRatio": 0.1467,
  "DividendDate": "2024-11-14",
  "ExDividendDate": "2024-11-08",
  "LastSplitFactor": "4:1",
  "LastSplitDate": "2020-08-31",
  "NumberDividendsByYear": {
    "0": {
      "Year": 1987,
      "Count": 3
    },
    "1": {
      "Year": 1988,
      "Count": 4
    }
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `ForwardAnnualDividendRate` | number | Expected annual dividend per share |
| `ForwardAnnualDividendYield` | number | Expected annual dividend yield (decimal) |
| `PayoutRatio` | number | Dividend payout ratio (decimal) |
| `DividendDate` | string | Payment date for next dividend (YYYY-MM-DD) |
| `ExDividendDate` | string | Ex-dividend date (YYYY-MM-DD) |
| `LastSplitFactor` | string | Most recent stock split ratio (e.g., "4:1") |
| `LastSplitDate` | string | Date of last split (YYYY-MM-DD) |
| `NumberDividendsByYear` | object | Array-indexed dividend counts by year |

### NumberDividendsByYear Structure

Each entry contains:
- `Year` - Calendar year
- `Count` - Number of dividend payments that year

## Section 7: AnalystRatings

Returns analyst recommendations and target prices.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=AnalystRatings
```

### Response Structure

```json
{
  "Rating": 4.1064,
  "TargetPrice": 247.925,
  "StrongBuy": 24,
  "Buy": 8,
  "Hold": 12,
  "Sell": 2,
  "StrongSell": 1
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `Rating` | number | Average rating (1-5 scale, 5=Strong Buy, 1=Strong Sell) |
| `TargetPrice` | number | Average analyst price target |
| `StrongBuy` | number | Number of Strong Buy ratings |
| `Buy` | number | Number of Buy ratings |
| `Hold` | number | Number of Hold ratings |
| `Sell` | number | Number of Sell ratings |
| `StrongSell` | number | Number of Strong Sell ratings |

**Rating Scale**:
- 5.0 - 4.5 = Strong Buy
- 4.5 - 3.5 = Buy
- 3.5 - 2.5 = Hold
- 2.5 - 1.5 = Sell
- 1.5 - 1.0 = Strong Sell

## Section 8: Holders

Returns institutional and fund holders with ownership details.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Holders
```

### Response Structure

The Holders section has two subsections:
- `Institutions` - Institutional holders (investment firms, banks, etc.)
- `Funds` - Mutual funds and ETFs

Both use array-indexed structure.

### 8.1 Institutions

```json
{
  "Institutions": {
    "0": {
      "name": "Vanguard Group Inc",
      "date": "2024-09-30",
      "totalShares": 8.9087,
      "totalAssets": 5.6185,
      "currentShares": 1346616669,
      "change": 21646442,
      "change_p": 1.6337
    }
  }
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Institution name |
| `date` | string | Report date (YYYY-MM-DD) |
| `totalShares` | number | Percentage of total shares held |
| `totalAssets` | number | Percentage of institution's total assets |
| `currentShares` | number | Number of shares held |
| `change` | number | Change in shares from previous report |
| `change_p` | number | Percentage change in holdings |

### 8.2 Funds

```json
{
  "Funds": {
    "0": {
      "name": "Vanguard Total Stock Mkt Idx Inv",
      "date": "2024-12-31",
      "totalShares": 3.1349,
      "totalAssets": 6.6656,
      "currentShares": 473862940,
      "change": 19839097,
      "change_p": 4.3696
    }
  }
}
```

**Field Descriptions**: Same as Institutions

**Notes**:
- Both subsections are array-indexed ("0", "1", "2", etc.)
- Sorted by holdings size (largest first)
- Typically shows top 20 holders
- Changes indicate buying/selling activity

## Section 9: InsiderTransactions

Returns recent insider trading activity (Form 4 filings).

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=InsiderTransactions
```

### Response Structure

```json
{
  "0": {
    "date": "2025-01-02",
    "ownerCik": null,
    "ownerName": "James Comer",
    "transactionDate": "2025-01-02",
    "transactionCode": "P",
    "transactionAmount": 0,
    "transactionPrice": 243.85,
    "transactionAcquiredDisposed": "A",
    "postTransactionAmount": null,
    "secLink": null
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Report date (YYYY-MM-DD) |
| `ownerCik` | string/null | Owner's CIK (Central Index Key) |
| `ownerName` | string | Name of insider |
| `transactionDate` | string | Date of transaction (YYYY-MM-DD) |
| `transactionCode` | string | Transaction type code |
| `transactionAmount` | number | Number of shares |
| `transactionPrice` | number | Price per share |
| `transactionAcquiredDisposed` | string | "A" (Acquired) or "D" (Disposed) |
| `postTransactionAmount` | number/null | Total shares held after transaction |
| `secLink` | string/null | Link to SEC filing |

**Transaction Codes**:
- `P` - Open market purchase
- `S` - Open market sale
- `M` - Exercise of options
- `A` - Grant, award, or other acquisition
- `G` - Gift
- `F` - Payment of exercise price or tax liability

**Note**: Array-indexed structure, sorted by date (most recent first).

## Section 10: outstandingShares

Returns historical shares outstanding data.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=outstandingShares
```

### Response Structure

```json
{
  "0": {
    "dateFormatted": "2024-09-30",
    "shares": 15037.9
  },
  "1": {
    "dateFormatted": "2024-06-30",
    "shares": 15204.2
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `dateFormatted` | string | Date (YYYY-MM-DD) |
| `shares` | number | Outstanding shares in millions |

**Notes**:
- Array-indexed, sorted by date (most recent first)
- Shares are in millions
- Historical data available based on company filings
- Used for calculating diluted metrics over time

## Section 11: Earnings

Returns earnings history, trends, and estimates.

### Request

```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Earnings
```

### Response Structure

The Earnings section has three subsections:
- `History` - Historical quarterly earnings
- `Trend` - Earnings estimates and revenue forecasts
- `Annual` - Annual earnings data

### 11.1 Earnings::History

Historical quarterly earnings with estimates vs. actuals:

```json
{
  "History": {
    "2024-09-30": {
      "date": "2024-09-30",
      "epsActual": 1.64,
      "epsEstimate": 1.6,
      "epsDifference": 0.04,
      "surprisePercent": 2.5
    }
  }
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Quarter end date (YYYY-MM-DD) |
| `epsActual` | number | Actual reported EPS |
| `epsEstimate` | number | Analyst consensus estimate |
| `epsDifference` | number | Difference (actual - estimate) |
| `surprisePercent` | number | Surprise as percentage of estimate |

### 11.2 Earnings::Trend

Earnings and revenue estimates for upcoming periods:

```json
{
  "Trend": {
    "0q": {
      "date": "2024-12-31",
      "period": "0q",
      "growth": "-0.1060",
      "earningsEstimateAvg": "2.1100",
      "earningsEstimateLow": "1.9400",
      "earningsEstimateHigh": "2.3200",
      "earningsEstimateNumberOfAnalysts": "34",
      "earningsEstimateGrowth": "-0.1060",
      "revenueEstimateAvg": "124710000000.00",
      "revenueEstimateLow": "120500000000.00",
      "revenueEstimateHigh": "128000000000.00",
      "revenueEstimateNumberOfAnalysts": "30",
      "revenueEstimateGrowth": "0.0330",
      "epsTrendCurrent": "2.1100",
      "epsTrend7daysAgo": "2.1200",
      "epsTrend30daysAgo": "2.1300",
      "epsTrend60daysAgo": "2.1200",
      "epsTrend90daysAgo": "2.1100",
      "epsRevisionsUpLast7days": "0",
      "epsRevisionsUpLast30days": "1",
      "epsRevisionsDownLast7days": null,
      "epsRevisionsDownLast30days": null
    },
    "+1q": {
      "period": "+1q"
    },
    "0y": {
      "period": "0y"
    },
    "+1y": {
      "period": "+1y"
    }
  }
}
```

**Period Keys**:
- `0q` - Current quarter
- `+1q` - Next quarter
- `0y` - Current fiscal year
- `+1y` - Next fiscal year

**Field Descriptions**: (for each period)

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Period end date |
| `period` | string | Period identifier |
| `growth` | string | Expected earnings growth (decimal) |
| `earningsEstimateAvg` | string | Average EPS estimate |
| `earningsEstimateLow` | string | Low EPS estimate |
| `earningsEstimateHigh` | string | High EPS estimate |
| `earningsEstimateNumberOfAnalysts` | string | Number of analysts |
| `revenueEstimateAvg` | string | Average revenue estimate |
| `revenueEstimateLow` | string | Low revenue estimate |
| `revenueEstimateHigh` | string | High revenue estimate |
| `revenueEstimateNumberOfAnalysts` | string | Number of analysts |
| `epsTrendCurrent` | string | Current consensus |
| `epsTrend7daysAgo` | string | Consensus 7 days ago |
| `epsTrend30daysAgo` | string | Consensus 30 days ago |
| `epsTrend60daysAgo` | string | Consensus 60 days ago |
| `epsTrend90daysAgo` | string | Consensus 90 days ago |
| `epsRevisionsUpLast7days` | string | Upward revisions (last 7 days) |
| `epsRevisionsUpLast30days` | string | Upward revisions (last 30 days) |
| `epsRevisionsDownLast7days` | string/null | Downward revisions (last 7 days) |
| `epsRevisionsDownLast30days` | string/null | Downward revisions (last 30 days) |

### 11.3 Earnings::Annual

Annual earnings data:

```json
{
  "Annual": {
    "2024-09-30": {
      "date": "2024-09-30",
      "epsActual": 6.11
    }
  }
}
```

## Section 12: Financials (NEW Date Filtering Support)

Returns comprehensive financial statements with **NEW date filtering capability**.

### Overview

The Financials section contains three statement types, each with quarterly and yearly data:
- **Balance_Sheet** - Assets, liabilities, equity
- **Cash_Flow** - Operating, investing, financing cash flows
- **Income_Statement** - Revenue, expenses, net income

### NEW Feature: Date Filtering

As of the latest update, you can now filter financial statements by date range using `from` and `to` parameters.

**Supported Filters with Date Filtering**:
- `Financials::Balance_Sheet::quarterly`
- `Financials::Balance_Sheet::yearly`
- `Financials::Cash_Flow::quarterly`
- `Financials::Cash_Flow::yearly`
- `Financials::Income_Statement::quarterly`
- `Financials::Income_Statement::yearly`

### Request Examples

**Without date filtering** (returns all available periods):
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Cash_Flow::quarterly
```

**With date filtering** (NEW - returns only specified period):
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Cash_Flow::quarterly&from=2024-09-30&to=2024-12-31
```

**Get all financials for a specific date**:
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&from=2024-09-30&to=2024-09-30&filter=Financials
```

### 12.1 Balance Sheet

**Request**:
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Balance_Sheet::quarterly&from=2024-09-30&to=2024-09-30
```

**Response Structure** (Partial):
```json
{
  "currency_symbol": "USD",
  "quarterly": {
    "2024-09-30": {
      "date": "2024-09-30",
      "filing_date": "2024-11-01",
      "currency_symbol": "USD",
      "totalAssets": "364980000000.00",
      "totalLiab": "308030000000.00",
      "totalStockholderEquity": "56950000000.00",
      "cash": "29943000000.00",
      "currentDeferredRevenue": "8249000000.00",
      "netDebt": "76686000000.00",
      "shortTermDebt": "22511000000.00",
      "longTermDebt": "85750000000.00",
      "inventory": "7286000000.00",
      "accountsPayable": "68960000000.00",
      "retainedEarnings": "-19154000000.00",
      "commonStock": "83276000000.00",
      "propertyPlantEquipment": "45680000000.00",
      "totalCurrentAssets": "152987000000.00",
      "totalCurrentLiabilities": "176392000000.00",
      "netReceivables": "66243000000.00",
      "longTermInvestments": "91479000000.00",
      "shortTermInvestments": "35228000000.00",
      "commonStockSharesOutstanding": "15408095000.00"
    }
  }
}
```

**Key Fields**:

| Category | Fields |
|----------|--------|
| **Assets** | totalAssets, totalCurrentAssets, cash, shortTermInvestments, longTermInvestments, netReceivables, inventory, propertyPlantEquipment |
| **Liabilities** | totalLiab, totalCurrentLiabilities, accountsPayable, shortTermDebt, longTermDebt, currentDeferredRevenue |
| **Equity** | totalStockholderEquity, commonStock, retainedEarnings, commonStockSharesOutstanding |
| **Derived** | netDebt (totalDebt - cash), netWorkingCapital (currentAssets - currentLiabilities) |

### 12.2 Cash Flow Statement

**Request**:
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Cash_Flow::quarterly&from=2024-09-30&to=2024-12-31
```

**Response Structure** (Partial):
```json
{
  "currency_symbol": "USD",
  "quarterly": {
    "2024-12-31": {
      "date": "2024-12-31",
      "filing_date": "2025-01-31",
      "currency_symbol": "USD",
      "netIncome": "36330000000.00",
      "depreciation": "3080000000.00",
      "changeInCash": "356000000.00",
      "totalCashFromOperatingActivities": "29935000000.00",
      "capitalExpenditures": "2940000000",
      "investments": "9792000000.00",
      "totalCashflowsFromInvestingActivities": "9792000000.00",
      "dividendsPaid": "3856000000.00",
      "netBorrowings": "-8953000000.00",
      "totalCashFromFinancingActivities": "-39371000000.00",
      "changeInWorkingCapital": "-10752000000.00",
      "stockBasedCompensation": "3286000000.00",
      "freeCashFlow": "26995000000.00"
    },
    "2024-09-30": {
      "date": "2024-09-30",
      "netIncome": "14736000000.00",
      "totalCashFromOperatingActivities": "26811000000.00",
      "capitalExpenditures": "2908000000",
      "freeCashFlow": "23903000000.00"
    }
  }
}
```

**Key Fields**:

| Category | Fields |
|----------|--------|
| **Operating** | netIncome, depreciation, totalCashFromOperatingActivities, changeInWorkingCapital, stockBasedCompensation |
| **Investing** | capitalExpenditures, investments, totalCashflowsFromInvestingActivities |
| **Financing** | dividendsPaid, netBorrowings, totalCashFromFinancingActivities |
| **Summary** | changeInCash, freeCashFlow (operating cash flow - capex) |

### 12.3 Income Statement

**Request**:
```
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Income_Statement::quarterly&from=2024-09-30&to=2024-09-30
```

**Response Structure** (Partial):
```json
{
  "currency_symbol": "USD",
  "quarterly": {
    "2024-09-30": {
      "date": "2024-09-30",
      "filing_date": "2024-11-01",
      "currency_symbol": "USD",
      "totalRevenue": "94930000000.00",
      "costOfRevenue": "51051000000.00",
      "grossProfit": "43879000000.00",
      "researchDevelopment": "7765000000.00",
      "sellingGeneralAdministrative": "6523000000.00",
      "totalOperatingExpenses": "14288000000.00",
      "operatingIncome": "29591000000.00",
      "ebit": "29591000000.00",
      "ebitda": "32502000000.00",
      "incomeBeforeTax": "29610000000.00",
      "incomeTaxExpense": "14874000000.00",
      "netIncome": "14736000000.00",
      "netIncomeApplicableToCommonShares": "14736000000.00"
    }
  }
}
```

**Key Fields**:

| Category | Fields |
|----------|--------|
| **Revenue** | totalRevenue, costOfRevenue, grossProfit |
| **Expenses** | researchDevelopment, sellingGeneralAdministrative, totalOperatingExpenses |
| **Profitability** | operatingIncome, ebit, ebitda, incomeBeforeTax, netIncome |
| **Taxes** | incomeTaxExpense |

### Date Filtering Best Practices

**1. Get latest quarter only**:
```bash
# Much faster and smaller response
&filter=Financials::Cash_Flow::quarterly&from=2024-09-30&to=2024-09-30
```

**2. Get specific date range**:
```bash
# Get Q3 and Q4 2024
&filter=Financials::Cash_Flow::quarterly&from=2024-07-01&to=2024-12-31
```

**3. Get all financials for one period**:
```bash
# Balance Sheet, Cash Flow, Income Statement for one date
&from=2024-09-30&to=2024-09-30&filter=Financials
```

**4. Combine with other sections**:
```bash
# Get financials and highlights
&filter=Highlights,Financials::Balance_Sheet::quarterly&from=2024-09-30&to=2024-09-30
```

## Filter Parameter Reference

### Single Section Filters

```bash
# Top-level sections
&filter=General
&filter=Highlights
&filter=Valuation
&filter=SharesStats
&filter=Technicals
&filter=SplitsDividends
&filter=AnalystRatings
&filter=Holders
&filter=InsiderTransactions
&filter=outstandingShares
&filter=Earnings
&filter=Financials
```

### Nested Filters

```bash
# Specific subsections
&filter=General::Code
&filter=General::Officers
&filter=Holders::Institutions
&filter=Holders::Funds
&filter=Earnings::History
&filter=Earnings::Trend
&filter=Earnings::Annual

# Financial statements
&filter=Financials::Balance_Sheet::quarterly
&filter=Financials::Balance_Sheet::yearly
&filter=Financials::Cash_Flow::quarterly
&filter=Financials::Cash_Flow::yearly
&filter=Financials::Income_Statement::quarterly
&filter=Financials::Income_Statement::yearly
```

### Multiple Filters (Comma-Separated)

```bash
# Get multiple sections in one request
&filter=General,Highlights,Valuation

# Get specific fields
&filter=General::Code,General::Name,Highlights::MarketCapitalization
```

### Filters with Date Range (NEW)

```bash
# Single statement type
&filter=Financials::Cash_Flow::quarterly&from=2024-09-30&to=2024-12-31

# All financials for specific date
&filter=Financials&from=2024-09-30&to=2024-09-30

# Specific field for date range
&filter=Financials::Balance_Sheet::quarterly::2024-09-30
```

## Common Use Cases

### 1. Quick Company Overview

Get essential company information:

```bash
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter "General,Highlights"
```

**Use case**: Building company profile pages, initial research.

### 2. Valuation Analysis

Get valuation metrics and compare to peers:

```bash
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Valuation,Highlights" | jq '{PE: .Valuation.TrailingPE, PS: .Valuation.PriceSalesTTM, PB: .Valuation.PriceBookMRQ}'
```

**Use case**: Value investing, peer comparison.

### 3. Latest Quarterly Financials

Get most recent quarter's financial statements:

```bash
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter "Financials::Income_Statement::quarterly" --from-date 2024-09-30 --to-date 2024-09-30
```

**Use case**: Earnings analysis, quarter-over-quarter comparison.

### 4. Ownership Analysis

Check institutional and insider ownership:

```bash
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=SharesStats,Holders::Institutions"
```

**Use case**: Understanding ownership structure, identifying major holders.

### 5. Insider Activity Monitoring

Track recent insider transactions:

```bash
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter InsiderTransactions
```

**Use case**: Detecting insider buying/selling signals.

### 6. Analyst Consensus

Get analyst ratings and target prices:

```bash
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=AnalystRatings" | jq '{Rating, TargetPrice, StrongBuy, Buy, Hold, Sell}'
```

**Use case**: Sentiment analysis, price target comparison.

### 7. Historical Financial Trends

Get 5 years of annual financial statements:

```bash
# Without date filter (gets all available years)
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter "Financials::Income_Statement::yearly"

# Or filter to specific range
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter "Financials::Income_Statement::yearly" --from-date 2020-01-01 --to-date 2024-12-31
```

**Use case**: Trend analysis, financial modeling.

### 8. Dividend Analysis

Get dividend history and metrics:

```bash
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=SplitsDividends,Highlights" | jq '{DividendYield: .Highlights.DividendYield, PayoutRatio: .SplitsDividends.PayoutRatio, History: .SplitsDividends.NumberDividendsByYear}'
```

**Use case**: Income investing, dividend growth analysis.

## Best Practices

### 1. Always Use Filters

**Problem**: Full response can be 800+ KB
**Solution**: Use specific filters

```bash
# Bad - gets everything (800+ KB)
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json"

# Good - gets only needed section (5-50 KB)
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Highlights"
```

### 2. Use Date Filtering for Financials

**Problem**: Getting all historical quarters when you only need latest
**Solution**: Use `from` and `to` parameters

```bash
# Gets all quarters (large response)
&filter=Financials::Cash_Flow::quarterly

# Gets only latest quarter (small response)
&filter=Financials::Cash_Flow::quarterly&from=2024-09-30&to=2024-09-30
```

### 3. Cache Aggressively

**Recommendation**: Different cache durations for different sections

| Section | Update Frequency | Recommended Cache |
|---------|-----------------|-------------------|
| General | Rarely | 7+ days |
| Highlights, Technicals | Daily | 24 hours |
| Financials (quarterly) | Quarterly | Until next earnings |
| Financials (yearly) | Yearly | Until fiscal year end |
| AnalystRatings | Weekly | 7 days |
| InsiderTransactions | As filed | 24 hours |
| Holders | Quarterly | 90 days |

### 4. Handle Missing Fields

Not all companies report all fields:

```python
# Use .get() with defaults
ebitda = data.get("Highlights", {}).get("EBITDA")
if ebitda is None:
    print("EBITDA not reported")

# Check before accessing nested data
if "Financials" in data and "Balance_Sheet" in data["Financials"]:
    balance_sheet = data["Financials"]["Balance_Sheet"]
```

### 5. Validate Data Types

Some fields may be null:

```python
# SharesStats
shares_short = data["SharesStats"].get("SharesShort")
if shares_short is not None:
    short_ratio = data["SharesStats"]["ShortRatio"]
    print(f"Short interest: {shares_short:,.0f} shares ({short_ratio:.2f} days to cover)")
```

### 6. Parse Array-Indexed Structures

Many sections use numeric indices:

```python
# Officers
officers = data["General"]["Officers"]
for idx, officer in officers.items():
    print(f"{officer['Name']} - {officer['Title']}")

# Insider Transactions
transactions = data["InsiderTransactions"]
for idx, txn in transactions.items():
    print(f"{txn['transactionDate']}: {txn['ownerName']} {txn['transactionCode']} {txn['transactionAmount']} shares")
```

## Error Handling

### Common Issues

**1. Wrong Type**

**Problem**: Requesting stock filters for ETF/Fund
```python
if data.get("General", {}).get("Type") != "Common Stock":
    raise ValueError("Not a stock")
```

**2. Missing Financial Data**

**Problem**: Company doesn't report certain fields
```python
# Check if financials exist
if "Financials" not in data:
    raise ValueError("No financial data available")

# Check for specific statement
if "Cash_Flow" not in data["Financials"]:
    print("Cash flow statement not available")
```

**3. Invalid Date Range**

**Problem**: Requesting dates outside available range
**Solution**: Query without date filter first to see available dates

```python
# Get all available dates
response = requests.get(url, params={"filter": "Financials::Cash_Flow::quarterly"})
dates = response.json()["quarterly"].keys()
print(f"Available dates: {list(dates)}")
```

**4. Delisted Stock**

**Problem**: Stock no longer trades
```python
if data["General"]["IsDelisted"]:
    delisted_date = data["General"].get("DelistedDate")
    print(f"Stock delisted on {delisted_date}")
```

## Rate Limits & API Costs

- **API calls per request**: 10 calls
- **Recommended cache duration**: 24+ hours (varies by section)
- **Update frequency**: Daily to quarterly (varies by section)
- **Required subscription**: All-In-One or Fundamentals Data Feed

See [rate-limits.md](rate-limits.md) for optimization strategies.

## Related Documentation

- **[Fundamentals API Overview](fundamentals-api.md)** - Compare all instrument types
- **[Symbol Format](symbol-format.md)** - How to format stock tickers
- **[Exchanges](exchanges.md)** - List of supported exchanges
- **[Update Times](update-times.md)** - When fundamentals are refreshed
- **[Rate Limits](rate-limits.md)** - API quotas and optimization

## Quick Reference

### Common Stock Structure

```
Common Stock Fundamentals
├── General
│   ├── Code, Name, Exchange, Type
│   ├── Identifiers (ISIN, CUSIP, CIK, LEI, etc.)
│   ├── Sector, Industry, GIC classifications
│   ├── Address, Contact, Logo
│   ├── Officers (array-indexed)
│   └── Listings (array-indexed)
├── Highlights
│   ├── Market Cap, EBITDA
│   ├── P/E, PEG ratios
│   ├── EPS (actual and estimates)
│   ├── Margins, Returns
│   └── Revenue, Growth
├── Valuation
│   ├── P/E (trailing, forward)
│   ├── P/S, P/B ratios
│   └── EV ratios
├── SharesStats
│   ├── Outstanding, Float
│   ├── Insider/Institutional %
│   └── Short interest
├── Technicals
│   ├── Beta
│   ├── 52-week high/low
│   ├── Moving averages
│   └── Short data
├── SplitsDividends
│   ├── Dividend rates, yields
│   ├── Payout ratio
│   ├── Split history
│   └── Dividend history by year
├── AnalystRatings
│   ├── Average rating
│   ├── Target price
│   └── Buy/Hold/Sell counts
├── Holders
│   ├── Institutions (array-indexed)
│   └── Funds (array-indexed)
├── InsiderTransactions (array-indexed)
│   └── Recent Form 4 filings
├── outstandingShares (array-indexed)
│   └── Historical shares outstanding
├── Earnings
│   ├── History (quarterly actuals vs. estimates)
│   ├── Trend (estimates for upcoming periods)
│   └── Annual (yearly earnings)
└── Financials
    ├── Balance_Sheet
    │   ├── quarterly (date-indexed)
    │   └── yearly (date-indexed)
    ├── Cash_Flow
    │   ├── quarterly (date-indexed)
    │   └── yearly (date-indexed)
    └── Income_Statement
        ├── quarterly (date-indexed)
        └── yearly (date-indexed)
```

### Python Client Examples

```bash
# Get all fundamentals
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US

# Get specific section
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter Highlights

# Get latest quarterly financials (NEW - with date filtering)
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter Financials::Cash_Flow::quarterly --from-date 2024-09-30 --to-date 2024-09-30

# Get multiple sections
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter "General,Highlights,Valuation"
```

### curl Examples

```bash
# Company overview
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=General"

# Key metrics
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Highlights"

# Latest quarter financials (NEW)
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Income_Statement::quarterly&from=2024-09-30&to=2024-09-30"

# Extract specific fields
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Highlights" | jq '{MarketCap: .MarketCapitalizationMln, PE: .PERatio, EPS: .EarningsShare}'
```

### Popular Stock Symbols for Testing

**Demo Token Access**:
- `AAPL.US` - Apple Inc. (full access with demo token)
- `TSLA.US` - Tesla Inc. (full access with demo token)
- `AMZN.US` - Amazon.com Inc. (full access with demo token)

**Other Major Stocks**:
- `MSFT.US` - Microsoft Corporation
- `GOOGL.US` - Alphabet Inc. Class A
- `NVDA.US` - NVIDIA Corporation
- `META.US` - Meta Platforms Inc.
- `BRK-B.US` - Berkshire Hathaway Inc. Class B

## Summary: Common Stock vs. Other Types

| Feature | Common Stock | ETF | Fund | Crypto |
|---------|-------------|-----|------|--------|
| **Sections** | 12+ | 3 | 2 | 4 |
| **Response size** | Very Large (800+ KB) | Large (100+ KB) | Large (100+ KB) | Small (5-20 KB) |
| **Financial statements** | ✅ Yes (3 types, quarterly/yearly) | ❌ No | ❌ No | ❌ No |
| **Date filtering** | ✅ Yes (NEW for financials) | ❌ No | ❌ No | ❌ No |
| **Holders** | ✅ Yes (Institutions, Funds) | ❌ No | ❌ No | ❌ No |
| **Insider transactions** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Earnings data** | ✅ Yes (History, Trend, Annual) | ❌ No | ❌ No | ❌ No |
| **Analyst ratings** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Historical depth** | 1985 (US), 2000 (non-US) | Current | Current | Varies |
| **Filter necessity** | **Critical** | Recommended | Recommended | Optional |

---

**Last Updated**: February 2026
**API Version**: Current
**Maintained By**: EODHD Skills Team
