# ETF Fundamentals API - Complete Guide

This guide covers the Fundamentals API specifically for **Exchange-Traded Funds (ETFs)**.

## Overview

The EODHD API supports fundamental data for **more than 10,000 ETFs** from different exchanges and countries. ETF fundamental data includes holdings, allocations, performance metrics, and valuation ratios.

**Key Characteristics**:
- **API calls consumption**: 10 calls per request
- **Format**: JSON only
- **Response size**: Can be large (100+ KB for major ETFs)
- **Filter support**: Highly recommended to retrieve specific sections
- **Type field**: `"Type": "ETF"` in the General section

## API Endpoint

### Base URL Format

```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json
```

**Parameters**:
- `{TICKER}`: Format `{SYMBOL}.{EXCHANGE}` (e.g., `VTI.US`, `SPY.US`)
- `{API_TOKEN}`: Your API key
- `fmt=json`: Required (JSON only format)
- `filter=`: Optional parameter to limit data returned

**Example - Full data**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json
```

**Example - Filtered data**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Top_10_Holdings
```

## Data Structure

ETF fundamental data has **three top-level sections**:

| Section | Description | Use Filter |
|---------|-------------|------------|
| **General** | Basic ETF information, name, category | `&filter=General` |
| **Technicals** | Technical metrics, ratios, estimates | `&filter=Technicals` |
| **ETF_Data** | ETF-specific data (holdings, allocations, etc.) | `&filter=ETF_Data` |

## Available Data Fields

For ETFs, the following fields are provided:

### ETF General Data
- Company Name and URL
- Current Yield and Dividend Payment information
- Ongoing charge
- Average Market Capitalization (in Millions)
- Net expense ratio
- Annual holdings turnover
- Total Net Assets

### Technicals
- Beta
- 52-week high/low
- 50/200-day moving average

### Breakdowns
- Market Capitalization distribution
- Asset Allocation
- World Regions
- Sector Weights
- Top 10 Holdings
- All Holdings
- Fixed Income characteristics

### Valuations and Growth
- Valuation rates for portfolio
- Comparison to ETF category
- Growth rates (earnings, sales, cash flow, book value)

### Performance Metrics
- Volatility (1-year, 3-year)
- Expected Returns
- Sharpe Ratio
- Returns: YTD, 1Y, 3Y, 5Y, 10Y

## Section 1: General

Returns basic ETF information including name, category, and description.

### Request

```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=General
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=General
```

### Response Structure

```json
{
  "Code": "VTI",
  "Type": "ETF",
  "Name": "Vanguard Total Stock Market Index Fund ETF Shares",
  "Exchange": "NYSE ARCA",
  "CurrencyCode": "USD",
  "CurrencyName": "US Dollar",
  "CurrencySymbol": "$",
  "CountryName": "USA",
  "CountryISO": "US",
  "OpenFigi": "BBG000HR9779",
  "Description": "The fund employs an indexing investment approach designed to track the performance of the index, which represents approximately 100% of the investable U.S. stock market and includes large-, mid-, small-, and micro-cap stocks. It invests by sampling the index, meaning that it holds a broadly diversified collection of securities that, in the aggregate, approximates the full index in terms of key characteristics. The fund is non-diversified.",
  "Category": "Large Blend",
  "UpdatedAt": "2024-11-26"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `Code` | string | ETF ticker symbol (without exchange) |
| `Type` | string | Always "ETF" for ETFs |
| `Name` | string | Full name of the ETF |
| `Exchange` | string | Exchange where ETF is listed |
| `CurrencyCode` | string | Currency code (ISO 4217) |
| `CurrencyName` | string | Full currency name |
| `CurrencySymbol` | string | Currency symbol |
| `CountryName` | string | Country name |
| `CountryISO` | string | ISO 3166-1 alpha-2 country code |
| `OpenFigi` | string | OpenFIGI identifier |
| `Description` | string | Detailed description of ETF strategy |
| `Category` | string | Morningstar category |
| `UpdatedAt` | string | Last update date (YYYY-MM-DD) |

## Section 2: Technicals

Returns technical metrics and financial estimates for the ETF.

### Request

```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=Technicals
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=Technicals
```

### Response Structure

```json
{
  "MarketCapitalization": 3552741949440,
  "MarketCapitalizationMln": 3552741.9494,
  "EBITDA": 131781001216,
  "PERatio": 35.5662,
  "PEGRatio": 2.4295,
  "WallStreetTargetPrice": 239.76,
  "BookValue": 4.382,
  "DividendShare": 0.97,
  "DividendYield": 0.0043,
  "EarningsShare": 6.57,
  "EPSEstimateCurrentYear": 6.65,
  "EPSEstimateNextYear": 7.46,
  "EPSEstimateNextQuarter": 1.56,
  "EPSEstimateCurrentQuarter": 1.35,
  "MostRecentQuarter": "2024-06-30",
  "ProfitMargin": 0.2644,
  "OperatingMarginTTM": 0.2956,
  "ReturnOnAssetsTTM": 0.2261,
  "ReturnOnEquityTTM": 1.6058,
  "RevenueTTM": 385603010560,
  "RevenuePerShareTTM": 24.957,
  "QuarterlyRevenueGrowthYOY": 0.049,
  "GrossProfitTTM": 170782000000,
  "DilutedEpsTTM": 6.57,
  "QuarterlyEarningsGrowthYOY": 0.111
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
| `WallStreetTargetPrice` | number | Analyst target price |
| `BookValue` | number | Book value per share |
| `DividendShare` | number | Dividend per share (annual) |
| `DividendYield` | number | Annual dividend yield (decimal) |
| `EarningsShare` | number | Earnings per share |
| `EPSEstimateCurrentYear` | number | EPS estimate for current year |
| `EPSEstimateNextYear` | number | EPS estimate for next year |
| `EPSEstimateNextQuarter` | number | EPS estimate for next quarter |
| `EPSEstimateCurrentQuarter` | number | EPS estimate for current quarter |
| `MostRecentQuarter` | string | Date of most recent quarter (YYYY-MM-DD) |
| `ProfitMargin` | number | Net profit margin (decimal) |
| `OperatingMarginTTM` | number | Operating margin, trailing twelve months |
| `ReturnOnAssetsTTM` | number | Return on assets TTM (decimal) |
| `ReturnOnEquityTTM` | number | Return on equity TTM (decimal) |
| `RevenueTTM` | number | Total revenue, trailing twelve months |
| `RevenuePerShareTTM` | number | Revenue per share TTM |
| `QuarterlyRevenueGrowthYOY` | number | Quarterly revenue growth year-over-year (decimal) |
| `GrossProfitTTM` | number | Gross profit TTM |
| `DilutedEpsTTM` | number | Diluted earnings per share TTM |
| `QuarterlyEarningsGrowthYOY` | number | Quarterly earnings growth YoY (decimal) |

**Note**: These metrics represent aggregate statistics for the underlying holdings.

## Section 3: ETF_Data

The `ETF_Data` section contains ETF-specific information including holdings, allocations, and performance. This section is large and has multiple subsections.

### Request

```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data
```

**Warning**: This returns a very large response. Use nested filters to get specific subsections.

### ETF_Data Subsections

The `ETF_Data` section contains the following subsections:

1. **Top-level fields** - Basic ETF information
2. **Market_Capitalisation** - Market cap distribution
3. **Asset_Allocation** - Asset class breakdown
4. **World_Regions** - Geographic allocation
5. **Sector_Weights** - Sector exposure
6. **Fixed_Income** - Fixed income characteristics
7. **Top_10_Holdings** - Top 10 holdings
8. **Holdings** - All holdings (can be very large)
9. **Valuations_Growth** - Valuation and growth metrics
10. **MorningStar** - Morningstar ratings
11. **Performance** - Performance metrics

### 3.1 ETF_Data Top-Level Fields

These fields are returned with `&filter=ETF_Data`:

```json
{
  "ISIN": "US9229087690",
  "Company_Name": "Vanguard",
  "Company_URL": "http://www.vanguard.com",
  "ETF_URL": "https://personal.vanguard.com/us/funds/snapshot?FundIntExt=INT&FundId=0970",
  "Domicile": "United States",
  "Index_Name": null,
  "Yield": "1.330000",
  "Dividend_Paying_Frequency": "Quarterly",
  "Inception_Date": "2001-05-24",
  "Max_Annual_Mgmt_Charge": "0.00",
  "Ongoing_Charge": "0.0000",
  "Date_Ongoing_Charge": "0000-00-00",
  "NetExpenseRatio": "0.00030",
  "AnnualHoldingsTurnover": "0.02000",
  "TotalAssets": "462571412072.00",
  "Average_Mkt_Cap_Mil": "200695.42031",
  "Holdings_Count": 3268,
  "Market_Capitalisation": {...},
  "Asset_Allocation": {...},
  "World_Regions": {...},
  "Sector_Weights": {...},
  "Fixed_Income": {...},
  "Top_10_Holdings": {...},
  "Holdings": {...},
  "Valuations_Growth": {...},
  "MorningStar": {...},
  "Performance": {...}
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `ISIN` | string | International Securities Identification Number |
| `Company_Name` | string | ETF provider/company name |
| `Company_URL` | string | ETF provider website |
| `ETF_URL` | string | Direct link to ETF page |
| `Domicile` | string | Country of domicile |
| `Index_Name` | string | Name of tracked index (null if not index-based) |
| `Yield` | string | Current yield (percentage as string) |
| `Dividend_Paying_Frequency` | string | Dividend frequency (e.g., "Quarterly") |
| `Inception_Date` | string | ETF inception date (YYYY-MM-DD) |
| `Max_Annual_Mgmt_Charge` | string | Maximum annual management charge |
| `Ongoing_Charge` | string | Ongoing charge (expense ratio) |
| `Date_Ongoing_Charge` | string | Date of ongoing charge data |
| `NetExpenseRatio` | string | Net expense ratio (decimal as string) |
| `AnnualHoldingsTurnover` | string | Annual portfolio turnover rate |
| `TotalAssets` | string | Total net assets (AUM) |
| `Average_Mkt_Cap_Mil` | string | Average market cap of holdings (millions) |
| `Holdings_Count` | number | Total number of holdings |

### 3.2 Market Capitalisation

Distribution of holdings by market cap size.

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Market_Capitalisation
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::Market_Capitalisation
```

**Response**:
```json
{
  "Mega": "40.90849",
  "Big": "30.64542",
  "Medium": "19.68254",
  "Small": "6.39806",
  "Micro": "2.14857"
}
```

**Field Descriptions**:

| Field | Description | Typical Range |
|-------|-------------|---------------|
| `Mega` | Mega-cap stocks (>$200B) | Percentage as string |
| `Big` | Large-cap stocks ($10B-$200B) | Percentage as string |
| `Medium` | Mid-cap stocks ($2B-$10B) | Percentage as string |
| `Small` | Small-cap stocks ($300M-$2B) | Percentage as string |
| `Micro` | Micro-cap stocks (<$300M) | Percentage as string |

**Note**: Values are percentages represented as strings.

### 3.3 Asset Allocation

Breakdown by asset class (stocks, bonds, cash, etc.).

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Asset_Allocation
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::Asset_Allocation
```

**Response**:
```json
{
  "Cash": {
    "Long_%": "0.23903",
    "Short_%": "0.02578",
    "Net_Assets_%": "0.21325"
  },
  "NotClassified": {
    "Long_%": "0",
    "Short_%": "0",
    "Net_Assets_%": "0"
  },
  "Stock non-US": {
    "Long_%": "0.59753",
    "Short_%": "0",
    "Net_Assets_%": "0.59753"
  },
  "Other": {
    "Long_%": "0",
    "Short_%": "0",
    "Net_Assets_%": "0"
  },
  "Stock US": {
    "Long_%": "99.18922",
    "Short_%": "0",
    "Net_Assets_%": "99.18922"
  },
  "Bond": {
    "Long_%": "0",
    "Short_%": "0",
    "Net_Assets_%": "0"
  }
}
```

**Field Descriptions**:

Each asset class has three metrics:

| Field | Description |
|-------|-------------|
| `Long_%` | Long positions as percentage of assets |
| `Short_%` | Short positions as percentage of assets |
| `Net_Assets_%` | Net allocation (Long - Short) as percentage |

**Asset Classes**:
- `Cash` - Cash and cash equivalents
- `NotClassified` - Assets not classified
- `Stock non-US` - Non-US equities
- `Stock US` - US equities
- `Bond` - Fixed income securities
- `Other` - Other asset types

### 3.4 World Regions

Geographic allocation of holdings.

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::World_Regions
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::World_Regions
```

**Response**:
```json
{
  "North America": {
    "Equity_%": "99.521",
    "Relative_to_Category": "98.023"
  },
  "United Kingdom": {
    "Equity_%": "0.08822",
    "Relative_to_Category": "0.46516"
  },
  "Europe Developed": {
    "Equity_%": "0.305",
    "Relative_to_Category": "1.105"
  },
  "Europe Emerging": {
    "Equity_%": "0",
    "Relative_to_Category": "0"
  },
  "Africa/Middle East": {
    "Equity_%": "0.005",
    "Relative_to_Category": "0.019"
  },
  "Japan": {
    "Equity_%": "0",
    "Relative_to_Category": "0.061"
  },
  "Australasia": {
    "Equity_%": "0",
    "Relative_to_Category": "0.002"
  },
  "Asia Developed": {
    "Equity_%": "0.044",
    "Relative_to_Category": "0.235"
  },
  "Asia Emerging": {
    "Equity_%": "0.012",
    "Relative_to_Category": "0.036"
  },
  "Latin America": {
    "Equity_%": "0.025",
    "Relative_to_Category": "0.052"
  }
}
```

**Field Descriptions**:

| Field | Description |
|-------|-------------|
| `Equity_%` | Percentage of equity allocated to this region |
| `Relative_to_Category` | ETF's allocation relative to category average |

**Regions**:
- North America
- United Kingdom
- Europe Developed
- Europe Emerging
- Africa/Middle East
- Japan
- Australasia
- Asia Developed
- Asia Emerging
- Latin America

### 3.5 Sector Weights

Sector allocation breakdown.

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Sector_Weights
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::Sector_Weights
```

**Response**:
```json
{
  "Basic Materials": {
    "Equity_%": "2.13447",
    "Relative_to_Category": "2.51562"
  },
  "Consumer Cyclicals": {
    "Equity_%": "10.32982",
    "Relative_to_Category": "9.97737"
  },
  "Financial Services": {
    "Equity_%": "13.39844",
    "Relative_to_Category": "13.5007"
  },
  "Real Estate": {
    "Equity_%": "2.87257",
    "Relative_to_Category": "2.04371"
  },
  "Communication Services": {
    "Equity_%": "8.48693",
    "Relative_to_Category": "8.40353"
  },
  "Energy": {
    "Equity_%": "3.52266",
    "Relative_to_Category": "3.4342"
  },
  "Industrials": {
    "Equity_%": "8.90539",
    "Relative_to_Category": "9.78099"
  },
  "Technology": {
    "Equity_%": "30.77272",
    "Relative_to_Category": "29.6431"
  },
  "Consumer Defensive": {
    "Equity_%": "5.47789",
    "Relative_to_Category": "5.90142"
  },
  "Healthcare": {
    "Equity_%": "11.51794",
    "Relative_to_Category": "12.25982"
  },
  "Utilities": {
    "Equity_%": "2.58117",
    "Relative_to_Category": "2.53955"
  }
}
```

**Field Descriptions**:

| Field | Description |
|-------|-------------|
| `Equity_%` | Percentage of equity allocated to this sector |
| `Relative_to_Category` | ETF's allocation relative to category average |

**Sectors** (following Morningstar classification):
- Basic Materials
- Consumer Cyclicals
- Consumer Defensive
- Communication Services
- Energy
- Financial Services
- Healthcare
- Industrials
- Real Estate
- Technology
- Utilities

### 3.6 Fixed Income

Fixed income characteristics for ETFs with bond holdings.

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Fixed_Income
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::Fixed_Income
```

**Response**:
```json
{
  "EffectiveDuration": {
    "Fund_%": "0",
    "Relative_to_Category": "-0.41644"
  },
  "ModifiedDuration": {
    "Fund_%": "0",
    "Relative_to_Category": "-0.986"
  },
  "EffectiveMaturity": {
    "Fund_%": "0",
    "Relative_to_Category": "2.47738"
  },
  "CreditQuality": {
    "Fund_%": "0",
    "Relative_to_Category": "0"
  },
  "Coupon": {
    "Fund_%": "0",
    "Relative_to_Category": "0"
  },
  "Price": {
    "Fund_%": "0",
    "Relative_to_Category": "0"
  },
  "YieldToMaturity": {
    "Fund_%": "0",
    "Relative_to_Category": "2.93132"
  }
}
```

**Field Descriptions**:

| Field | Description |
|-------|-------------|
| `EffectiveDuration` | Effective duration (interest rate sensitivity) |
| `ModifiedDuration` | Modified duration |
| `EffectiveMaturity` | Weighted average maturity in years |
| `CreditQuality` | Average credit quality rating |
| `Coupon` | Weighted average coupon rate |
| `Price` | Weighted average bond price |
| `YieldToMaturity` | Weighted average yield to maturity |

Each metric includes:
- `Fund_%` - Value for the ETF
- `Relative_to_Category` - Comparison to category average

**Note**: For equity-only ETFs (like VTI), these values will be 0.

### 3.7 Top 10 Holdings

Top 10 holdings by asset percentage.

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Top_10_Holdings
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::Top_10_Holdings
```

**Response**:
```json
{
  "AAPL.US": {
    "Code": "AAPL",
    "Exchange": "US",
    "Name": "Apple Inc",
    "Sector": "Technology",
    "Industry": "Consumer Electronics",
    "Country": "United States",
    "Region": "North America",
    "Assets_%": 5.94
  },
  "NVDA.US": {
    "Code": "NVDA",
    "Exchange": "US",
    "Name": "NVIDIA Corporation",
    "Sector": "Technology",
    "Industry": "Semiconductors",
    "Country": "United States",
    "Region": "North America",
    "Assets_%": 5.65
  }
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| Key | string | Ticker in format `{CODE}.{EXCHANGE}` |
| `Code` | string | Ticker symbol |
| `Exchange` | string | Exchange code |
| `Name` | string | Company/security name |
| `Sector` | string | Sector classification |
| `Industry` | string | Industry classification |
| `Country` | string | Country of domicile |
| `Region` | string | Geographic region |
| `Assets_%` | number | Percentage of ETF assets |

**Note**: Returns up to 10 holdings sorted by `Assets_%` descending.

### 3.8 Holdings

All ETF holdings (can be very large for diversified ETFs).

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Holdings
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::Holdings
```

**Response**:
```json
{
  "AAPL.US": {
    "Code": "AAPL",
    "Exchange": "US",
    "Name": "Apple Inc",
    "Sector": "Technology",
    "Industry": "Consumer Electronics",
    "Country": "United States",
    "Region": "North America",
    "Assets_%": 5.94
  },
  "NVDA.US": {
    "Code": "NVDA",
    "Exchange": "US",
    "Name": "NVIDIA Corporation",
    "Sector": "Technology",
    "Industry": "Semiconductors",
    "Country": "United States",
    "Region": "North America",
    "Assets_%": 5.65
  },
  "MSFT.US": {
    "Code": "MSFT",
    "Exchange": "US",
    "Name": "Microsoft Corporation",
    "Sector": "Technology",
    "Industry": "Software - Infrastructure",
    "Country": "United States",
    "Region": "North America",
    "Assets_%": 5.5
  }
}
```

**Structure**: Same as Top_10_Holdings but includes all holdings.

**Warning**:
- For ETFs with 1000+ holdings (like VTI with 3268 holdings), this response is very large
- Each holding includes 8 fields
- Total response can exceed 100 KB
- Consider using `Top_10_Holdings` for most use cases

**Field Descriptions**: Same as Top_10_Holdings section.

### 3.9 Valuations and Growth

Valuation ratios and growth rates for the portfolio.

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Valuations_Growth
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::Valuations_Growth
```

**Response**:
```json
{
  "Valuations_Rates_Portfolio": {
    "Price/Prospective Earnings": "20.6485",
    "Price/Book": "3.846",
    "Price/Sales": "2.52127",
    "Price/Cash Flow": "14.40407",
    "Dividend-Yield Factor": "1.43128"
  },
  "Valuations_Rates_To_Category": {
    "Price/Prospective Earnings": "21.06387",
    "Price/Book": "4.57773",
    "Price/Sales": "2.64899",
    "Price/Cash Flow": "14.99994",
    "Dividend-Yield Factor": "1.42725"
  },
  "Growth_Rates_Portfolio": {
    "Long-Term Projected Earnings Growth": "11.5817",
    "Historical Earnings Growth": "5.95988",
    "Sales Growth": "7.7793",
    "Cash-Flow Growth": "8.75405",
    "Book-Value Growth": "5.95312"
  },
  "Growth_Rates_To_Category": {
    "Long-Term Projected Earnings Growth": "11.51378",
    "Historical Earnings Growth": "10.85208",
    "Sales Growth": "10.74037",
    "Cash-Flow Growth": "15.9931",
    "Book-Value Growth": "8.60095"
  }
}
```

**Structure**:

The response has four subsections:

#### Valuations_Rates_Portfolio

Valuation metrics for the ETF's portfolio (weighted average of holdings):

| Metric | Description |
|--------|-------------|
| `Price/Prospective Earnings` | Forward P/E ratio |
| `Price/Book` | Price to book value ratio |
| `Price/Sales` | Price to sales ratio |
| `Price/Cash Flow` | Price to cash flow ratio |
| `Dividend-Yield Factor` | Dividend yield metric |

#### Valuations_Rates_To_Category

Same valuation metrics, but showing the category average for comparison.

#### Growth_Rates_Portfolio

Growth metrics for the ETF's portfolio:

| Metric | Description |
|--------|-------------|
| `Long-Term Projected Earnings Growth` | Expected long-term earnings growth rate (%) |
| `Historical Earnings Growth` | Historical earnings growth rate (%) |
| `Sales Growth` | Revenue growth rate (%) |
| `Cash-Flow Growth` | Cash flow growth rate (%) |
| `Book-Value Growth` | Book value growth rate (%) |

#### Growth_Rates_To_Category

Same growth metrics, but showing the category average for comparison.

**All values are percentages represented as strings**.

### 3.10 MorningStar

Morningstar ratings and benchmark information.

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::MorningStar
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::MorningStar
```

**Response**:
```json
{
  "Ratio": "3",
  "Category_Benchmark": "S&P 500 TR USD",
  "Sustainability_Ratio": "2"
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Ratio` | string | Morningstar star rating (1-5 stars) |
| `Category_Benchmark` | string | Benchmark index for category |
| `Sustainability_Ratio` | string | Morningstar sustainability rating (1-5 globes) |

**Morningstar Star Ratings**:
- `5` - Excellent (top 10%)
- `4` - Above average (next 22.5%)
- `3` - Average (middle 35%)
- `2` - Below average (next 22.5%)
- `1` - Poor (bottom 10%)

**Sustainability Ratings**:
- `5` - Leader (top 10%)
- `4` - Above average (next 25%)
- `3` - Average (middle 30%)
- `2` - Below average (next 25%)
- `1` - Laggard (bottom 10%)

### 3.11 Performance

Historical performance metrics and risk statistics.

**Request**:
```
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Performance
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=ETF_Data::Performance
```

**Response**:
```json
{
  "1y_Volatility": "11.89",
  "3y_Volatility": "17.52",
  "3y_ExpReturn": "0.00",
  "3y_SharpRatio": "0.28",
  "Returns_YTD": "26.27",
  "Returns_1Y": "33.61",
  "Returns_3Y": "8.90",
  "Returns_5Y": "15.18",
  "Returns_10Y": "12.74"
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `1y_Volatility` | string | 1-year volatility (standard deviation %) |
| `3y_Volatility` | string | 3-year annualized volatility (%) |
| `3y_ExpReturn` | string | 3-year expected return (%) |
| `3y_SharpRatio` | string | 3-year Sharpe ratio |
| `Returns_YTD` | string | Year-to-date return (%) |
| `Returns_1Y` | string | 1-year total return (%) |
| `Returns_3Y` | string | 3-year annualized return (%) |
| `Returns_5Y` | string | 5-year annualized return (%) |
| `Returns_10Y` | string | 10-year annualized return (%) |

**Notes**:
- All values are percentages represented as strings
- Returns include dividends and capital gains
- Volatility is annualized standard deviation
- Sharpe ratio measures risk-adjusted return
- Not all ETFs have 10-year history

## Filter Parameter Reference

### Single Filter Examples

```bash
# General information
&filter=General

# Technical metrics
&filter=Technicals

# All ETF-specific data (large response)
&filter=ETF_Data
```

### Nested Filter Examples

```bash
# Market cap breakdown
&filter=ETF_Data::Market_Capitalisation

# Asset allocation
&filter=ETF_Data::Asset_Allocation

# Geographic exposure
&filter=ETF_Data::World_Regions

# Sector weights
&filter=ETF_Data::Sector_Weights

# Fixed income metrics
&filter=ETF_Data::Fixed_Income

# Top 10 holdings only
&filter=ETF_Data::Top_10_Holdings

# All holdings (warning: large)
&filter=ETF_Data::Holdings

# Valuation and growth metrics
&filter=ETF_Data::Valuations_Growth

# Morningstar ratings
&filter=ETF_Data::MorningStar

# Performance statistics
&filter=ETF_Data::Performance
```

### Multiple Filter Examples

To get multiple sections in one request, make separate API calls. The filter parameter does not support comma-separated values.

## Common Use Cases

### 1. ETF Screening by Holdings

Get top holdings to identify concentration risk:

```bash
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter ETF_Data::Top_10_Holdings
```

**Use case**: Check if ETF is overweight in specific stocks.

### 2. Sector Allocation Analysis

Compare sector exposure across multiple ETFs:

```bash
# Technology ETF
python eodhd_client.py --endpoint fundamentals --symbol XLK.US --filter ETF_Data::Sector_Weights

# Broad market ETF
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter ETF_Data::Sector_Weights
```

**Use case**: Portfolio diversification and sector rotation strategies.

### 3. Geographic Diversification

Analyze international exposure:

```bash
python eodhd_client.py --endpoint fundamentals --symbol VXUS.US --filter ETF_Data::World_Regions
```

**Use case**: Assess geographic risk and diversification.

### 4. Cost Analysis

Compare expense ratios and turnover:

```bash
# Get basic ETF data including expenses
curl "https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data" | jq '{NetExpenseRatio, AnnualHoldingsTurnover, TotalAssets}'
```

**Use case**: Cost-conscious ETF selection.

### 5. Performance Comparison

Compare risk-adjusted returns:

```bash
# ETF 1
python eodhd_client.py --endpoint fundamentals --symbol SPY.US --filter ETF_Data::Performance

# ETF 2
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter ETF_Data::Performance
```

**Use case**: Historical performance and volatility analysis.

### 6. Valuation Analysis

Assess if ETF holdings are over/undervalued:

```bash
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter ETF_Data::Valuations_Growth
```

**Use case**: Market timing and value investing strategies.

### 7. Complete ETF Profile

Get all data for in-depth analysis:

```bash
# Get all sections (large response)
python eodhd_client.py --endpoint fundamentals --symbol VTI.US
```

**Use case**: Comprehensive due diligence.

## Best Practices

### 1. Always Use Filters

**Problem**: Full ETF fundamental data can be 100+ KB
**Solution**: Use specific filters to get only needed data

```bash
# Bad - gets everything
curl "https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json"

# Good - gets only holdings
curl "https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Top_10_Holdings"
```

### 2. Cache Fundamental Data

**Recommendation**: Cache for 24 hours minimum
- Fundamentals update daily at most
- Saves API calls (10 calls per request)
- Improves application performance

### 3. Use Top_10_Holdings Instead of Holdings

**Problem**: Full holdings list for VTI = 3268 holdings
**Solution**: Use Top_10_Holdings for most analyses

```bash
# Good for most cases - top 10 holdings
&filter=ETF_Data::Top_10_Holdings

# Only when you need complete holdings
&filter=ETF_Data::Holdings
```

### 4. Check the Type Field

**Always verify** you're getting ETF data:

```python
import requests

response = requests.get(
    "https://eodhd.com/api/fundamentals/VTI.US",
    params={"api_token": "demo", "fmt": "json", "filter": "General"}
).json()

if response.get("Type") != "ETF":
    raise ValueError(f"Expected ETF, got {response.get('Type')}")
```

### 5. Handle Missing Fields Gracefully

Not all ETFs have all fields:

```python
holdings_count = data.get("ETF_Data", {}).get("Holdings_Count", 0)
if holdings_count == 0:
    print("Holdings data not available")
```

### 6. Compare to Category Benchmarks

Use `Relative_to_Category` fields for context:

```python
sector_weights = data["ETF_Data"]["Sector_Weights"]
for sector, metrics in sector_weights.items():
    etf_weight = float(metrics["Equity_%"])
    category_weight = float(metrics["Relative_to_Category"])

    if etf_weight > category_weight * 1.2:
        print(f"{sector} is overweight")
```

## Error Handling

### Common Issues

**1. Wrong Type**

**Problem**: Requesting ETF filters for a stock
```json
{
  "General": {
    "Type": "Common Stock"
  }
}
```

**Solution**: Check Type field first:
```python
if data["General"]["Type"] != "ETF":
    raise ValueError("Not an ETF")
```

**2. Missing Data**

**Problem**: Some ETFs lack certain fields
**Solution**: Use `.get()` with defaults:
```python
expense_ratio = data.get("ETF_Data", {}).get("NetExpenseRatio", "N/A")
```

**3. Invalid Ticker**

**Problem**: ETF doesn't exist or wrong exchange
```json
{
  "error": "Not found"
}
```

**Solution**: Verify ticker using search endpoint first

**4. Large Response Timeout**

**Problem**: Full Holdings for large ETF times out
**Solution**: Use filters to reduce response size

## Rate Limits & API Costs

- **API calls per request**: 10 calls
- **Recommended cache duration**: 24 hours
- **Update frequency**: Daily
- **Subscription required**: All-In-One or Fundamentals Data Feed

See [rate-limits.md](rate-limits.md) for optimization strategies.

## Related Documentation

- **[Fundamentals API Overview](fundamentals-api.md)** - Compare all instrument types
- **[Symbol Format](symbol-format.md)** - How to format ETF tickers
- **[Exchanges](exchanges.md)** - List of supported exchanges
- **[Update Times](update-times.md)** - When fundamentals are refreshed
- **[Rate Limits](rate-limits.md)** - API quotas and optimization

## Quick Reference

### ETF_Data Filter Hierarchy

```
ETF_Data
├── [Top-level fields]
│   ├── ISIN
│   ├── Company_Name
│   ├── NetExpenseRatio
│   ├── TotalAssets
│   └── Holdings_Count
├── Market_Capitalisation
│   ├── Mega
│   ├── Big
│   ├── Medium
│   ├── Small
│   └── Micro
├── Asset_Allocation
│   ├── Cash
│   ├── Stock US
│   ├── Stock non-US
│   └── Bond
├── World_Regions
│   ├── North America
│   ├── Europe Developed
│   ├── Asia Developed
│   └── [others]
├── Sector_Weights
│   ├── Technology
│   ├── Healthcare
│   ├── Financial Services
│   └── [others]
├── Fixed_Income
│   ├── EffectiveDuration
│   ├── YieldToMaturity
│   └── [others]
├── Top_10_Holdings
│   └── {TICKER.EXCHANGE}
├── Holdings
│   └── {TICKER.EXCHANGE}
├── Valuations_Growth
│   ├── Valuations_Rates_Portfolio
│   ├── Valuations_Rates_To_Category
│   ├── Growth_Rates_Portfolio
│   └── Growth_Rates_To_Category
├── MorningStar
│   ├── Ratio
│   └── Sustainability_Ratio
└── Performance
    ├── Returns_YTD
    ├── Returns_1Y
    ├── 3y_Volatility
    └── 3y_SharpRatio
```

### Python Client Examples

```python
# Get ETF general info
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter General

# Get top holdings
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter ETF_Data::Top_10_Holdings

# Get sector allocation
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter ETF_Data::Sector_Weights

# Get performance metrics
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter ETF_Data::Performance
```

### Popular ETF Symbols for Testing

- `VTI.US` - Vanguard Total Stock Market (3268 holdings)
- `SPY.US` - SPDR S&P 500 (503 holdings)
- `QQQ.US` - Invesco QQQ (Nasdaq 100)
- `AGG.US` - iShares Core US Aggregate Bond
- `VEA.US` - Vanguard FTSE Developed Markets
- `XLK.US` - Technology Select Sector SPDR

---

**Last Updated**: February 2026
**API Version**: Current
**Maintained By**: EODHD Skills Team
