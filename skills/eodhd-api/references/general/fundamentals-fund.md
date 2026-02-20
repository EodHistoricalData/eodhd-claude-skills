# Mutual Fund Fundamentals API - Complete Guide

This guide covers the Fundamentals API specifically for **Mutual Funds**.

## Overview

The EODHD API supports fundamental data for **more than 20,000 US Mutual Funds**. The database includes equity funds, balanced funds, and bond-based mutual funds, covering all major information about almost all mutual funds on the market.

**Key Characteristics**:
- **API calls consumption**: 10 calls per request
- **Format**: JSON only
- **Response size**: Can be large (100+ KB for major funds)
- **Filter support**: Highly recommended to retrieve specific sections
- **Type field**: `"Type": "FUND"` in the General section

## API Endpoint

### Base URL Format

```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json
```

**Parameters**:
- `{TICKER}`: Format `{SYMBOL}.{EXCHANGE}` (e.g., `SWPPX.US`, `VFIAX.US`)
- `{API_TOKEN}`: Your API key
- `fmt=json`: Required (JSON only format)
- `filter=`: Optional parameter to limit data returned

**Example - Full data**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json
```

**Example - Filtered data**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Top_Holdings
```

## Data Structure

Mutual Fund fundamental data has **two top-level sections**:

| Section | Description | Use Filter |
|---------|-------------|------------|
| **General** | Basic fund information, family, category | `&filter=General` |
| **MutualFund_Data** | Fund-specific data (holdings, allocations, etc.) | `&filter=MutualFund_Data` |

## Available Data Fields

For Mutual Funds, the following data categories are provided:

### 1. General Information
- Fund Summary (description)
- Fund Family (provider)
- Inception date
- Fund Category and Style
- Fiscal Year End
- ISIN, CUSIP identifiers

### 2. Asset Allocation
- Cash
- US Stocks
- Non-US stocks
- Bonds
- Other assets

### 3. Value Growth Measures
- Price/Prospective Earnings
- Price/Book
- Price/Sales
- Price/Cash Flow
- Many other valuation metrics

### 4. Sector Weightings
- **Cyclical** (Basic Materials, Consumer Cyclical, Financial Services, Real Estate)
- **Sensitive** (Communication Services, Energy, Industrials, Technology)
- **Defensive** (Consumer Defensive, Healthcare, Utilities)
- **Bond Sector** (Government, Municipal, Corporate, etc.)

### 5. World Regions
For equity and balanced funds:
- **Americas** (North America, Latin America)
- **Greater Europe** (UK, Europe Developed, Europe Emerging, Africa/Middle East)
- **Greater Asia** (Japan, Australasia, Asia Developed, Asia Emerging)

### 6. Market Classification
- Developed and emerging markets
- Top Countries (especially for bond-based mutual funds)

### 7. Performance Metrics
- NAV (Net Asset Value)
- Yield metrics (current, YTD, 1-year, 3-year, 5-year)
- Expense Ratio

## Section 1: General

Returns basic mutual fund information including name, category, summary, and identifiers.

### Request

```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=General
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=General
```

### Response Structure

```json
{
  "Code": "SWPPX",
  "Type": "FUND",
  "Name": "Schwab® S&P 500 Index Fund",
  "Exchange": "NMFQS",
  "CurrencyCode": "USD",
  "CurrencyName": "US Dollar",
  "CurrencySymbol": "$",
  "CountryName": "USA",
  "CountryISO": "US",
  "OpenFigi": "BBG000J9ZH30",
  "ISIN": "US8085098551",
  "CUSIP": "808509855",
  "Fund_Summary": "The fund generally invests at least 80% of its net assets (including, for this purpose, any borrowings for investment purposes) in these stocks; typically, the actual percentage is considerably higher. It generally will seek to replicate the performance of the index by giving the same weight to a given stock as the index does. The index includes the stocks of 500 leading U.S. publicly traded companies from a broad range of industries. The fund is non-diversified.",
  "Fund_Family": "Schwab Funds",
  "Fund_Category": "Large Blend",
  "Fund_Style": "Large Blend",
  "Fiscal_Year_End": "October",
  "MarketCapitalization": 0
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `Code` | string | Fund ticker symbol (without exchange) |
| `Type` | string | Always "FUND" for mutual funds |
| `Name` | string | Full name of the mutual fund |
| `Exchange` | string | Exchange where fund is listed (typically NMFQS for US mutual funds) |
| `CurrencyCode` | string | Currency code (ISO 4217) |
| `CurrencyName` | string | Full currency name |
| `CurrencySymbol` | string | Currency symbol |
| `CountryName` | string | Country name |
| `CountryISO` | string | ISO 3166-1 alpha-2 country code |
| `OpenFigi` | string | OpenFIGI identifier |
| `ISIN` | string | International Securities Identification Number |
| `CUSIP` | string | CUSIP identifier (US securities) |
| `Fund_Summary` | string | Detailed description of fund strategy and objectives |
| `Fund_Family` | string | Fund provider/family name |
| `Fund_Category` | string | Morningstar category (e.g., "Large Blend") |
| `Fund_Style` | string | Investment style classification |
| `Fiscal_Year_End` | string | Fiscal year end month |
| `MarketCapitalization` | number | Market capitalization (typically 0 for funds) |

## Section 2: MutualFund_Data

The `MutualFund_Data` section contains fund-specific information including holdings, allocations, and performance. This section has multiple subsections.

### Request

```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data
```

**Warning**: This returns a very large response. Use nested filters to get specific subsections.

### MutualFund_Data Subsections

The `MutualFund_Data` section contains the following subsections:

1. **Top-level fields** - Basic fund metrics (NAV, yields, expense ratio)
2. **Asset_Allocation** - Asset class breakdown
3. **Value_Growth** - Valuation metrics
4. **Top_Holdings** - Top holdings
5. **Market_Capitalization** - Market cap distribution
6. **Sector_Weights** - Sector exposure (Cyclical, Defensive, Sensitive, Bond Sector)
7. **World_Regions** - Geographic allocation
8. **Top_Countries** - Country exposure

### 2.1 MutualFund_Data Top-Level Fields

These fields are returned with `&filter=MutualFund_Data`:

```json
{
  "Fund_Category": "Large Blend",
  "Fund_Style": "Large Blend",
  "Nav": "92.59",
  "Prev_Close_Price": "92.26",
  "Update_Date": "2024-09-30",
  "Portfolio_Net_Assets": "72273490000",
  "Share_Class_Net_Assets": "0",
  "Morning_Star_Rating": null,
  "Morning_Star_Risk_Rating": null,
  "Morning_Star_Category": null,
  "Inception_Date": "1997-05-19",
  "Currency": "USD",
  "Domicile": "United States",
  "Yield": "0.0118",
  "Yield_YTD": "26.6621",
  "Yield_1Year_YTD": "32.8114",
  "Yield_3Year_YTD": "10.0894",
  "Yield_5Year_YTD": "15.7262",
  "Expense_Ratio": "0.0200",
  "Expense_Ratio_Date": "2023-02-27",
  "Asset_Allocation": {...},
  "Value_Growth": {...},
  "Top_Holdings": {...},
  "Market_Capitalization": {...},
  "Sector_Weights": {...},
  "World_Regions": {...},
  "Top_Countries": {...},
  "market_capitalization": null,
  "world_regions": null,
  "sector_weights": null,
  "asset_allocation": null
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Fund_Category` | string | Morningstar category |
| `Fund_Style` | string | Investment style |
| `Nav` | string | Net Asset Value (price per share) |
| `Prev_Close_Price` | string | Previous closing price |
| `Update_Date` | string | Last update date (YYYY-MM-DD) |
| `Portfolio_Net_Assets` | string | Total net assets under management |
| `Share_Class_Net_Assets` | string | Net assets for this share class |
| `Morning_Star_Rating` | number/null | Morningstar star rating (1-5) |
| `Morning_Star_Risk_Rating` | number/null | Morningstar risk rating |
| `Morning_Star_Category` | string/null | Morningstar category |
| `Inception_Date` | string | Fund inception date (YYYY-MM-DD) |
| `Currency` | string | Currency code |
| `Domicile` | string | Country of domicile |
| `Yield` | string | Current yield (decimal) |
| `Yield_YTD` | string | Year-to-date return (percentage) |
| `Yield_1Year_YTD` | string | 1-year return (percentage) |
| `Yield_3Year_YTD` | string | 3-year annualized return (percentage) |
| `Yield_5Year_YTD` | string | 5-year annualized return (percentage) |
| `Expense_Ratio` | string | Annual expense ratio (decimal) |
| `Expense_Ratio_Date` | string | Date of expense ratio data |

**Note**: Lowercase fields (`market_capitalization`, `world_regions`, etc.) at the end are typically null and represent deprecated fields.

### 2.2 Asset Allocation

Breakdown by asset class (cash, stocks, bonds, etc.).

**Request**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Asset_Allocation
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=MutualFund_Data::Asset_Allocation
```

**Response**:
```json
{
  "0": {
    "Net_%": "0.34539",
    "Long_%": "0.34539",
    "Type": "Cash",
    "Short_%": null,
    "Category_Average": "1.39629",
    "Benchmark": "0.00000"
  },
  "1": {
    "Net_%": "0.0",
    "Long_%": "0.0",
    "Type": "Not Classified",
    "Short_%": null,
    "Category_Average": "0.02486",
    "Benchmark": "0.0"
  }
}
```

**Structure**: Array of asset allocation objects indexed by position.

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Type` | string | Asset class type (Cash, Stock US, Stock non-US, Bond, Not Classified, Other) |
| `Net_%` | string | Net allocation percentage |
| `Long_%` | string | Long positions percentage |
| `Short_%` | string/null | Short positions percentage (if applicable) |
| `Category_Average` | string | Average allocation for this category |
| `Benchmark` | string | Benchmark allocation for comparison |

**Common Asset Types**:
- `Cash` - Cash and cash equivalents
- `Stock US` - US equities
- `Stock non-US` - Non-US equities
- `Bond` - Fixed income securities
- `Other` - Alternative investments
- `Not Classified` - Unclassified assets

### 2.3 Value Growth Measures

Valuation metrics comparing the fund's portfolio to category average and benchmark.

**Request**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Value_Growth
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=MutualFund_Data::Value_Growth
```

**Response**:
```json
{
  "0": {
    "Name": "Price/Prospective Earnings",
    "Category_Average": 21.06387,
    "Benchmark": 21.21499,
    "Stock_Portfolio": 21.18843
  },
  "1": {
    "Name": "Price/Book",
    "Category_Average": 4.57773,
    "Benchmark": 4.24585,
    "Stock_Portfolio": 4.26978
  }
}
```

**Structure**: Array of valuation metrics indexed by position.

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | Name of the valuation metric |
| `Stock_Portfolio` | number | Value for the fund's portfolio |
| `Category_Average` | number | Average value for the fund category |
| `Benchmark` | number | Benchmark value for comparison |

**Common Valuation Metrics**:
- `Price/Prospective Earnings` - Forward P/E ratio
- `Price/Book` - Price to book value ratio
- `Price/Sales` - Price to sales ratio
- `Price/Cash Flow` - Price to cash flow ratio
- `Dividend-Yield Factor` - Dividend yield metric
- `Long-Term Projected Earnings Growth` - Expected earnings growth
- `Historical Earnings Growth` - Past earnings growth
- `Sales Growth` - Revenue growth rate
- `Cash-Flow Growth` - Cash flow growth rate
- `Book-Value Growth` - Book value growth rate

**Interpretation**:
- Compare `Stock_Portfolio` to `Category_Average` and `Benchmark`
- Higher P/E, P/B, P/S, P/CF suggests growth orientation
- Lower values suggest value orientation
- Growth metrics show expected/historical growth rates

### 2.4 Top Holdings

Top holdings by weight.

**Request**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Top_Holdings
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=MutualFund_Data::Top_Holdings
```

**Response**:
```json
{
  "0": {
    "Name": "Apple Inc",
    "Weight": "6.88%"
  },
  "1": {
    "Name": "Microsoft Corp",
    "Weight": "6.68%"
  }
}
```

**Structure**: Array of holdings indexed by position (sorted by weight descending).

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | Company/security name |
| `Weight` | string | Percentage of portfolio (includes % sign) |

**Notes**:
- Typically shows top 10 holdings
- Weight is a string with percentage sign (e.g., "6.88%")
- Holdings are sorted by weight (largest first)
- Useful for identifying concentration risk

### 2.5 Market Capitalization

Market cap distribution of fund holdings.

**Request**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Market_Capitalization
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=MutualFund_Data::Market_Capitalization
```

**Response**:
```json
{
  "0": {
    "Size": "AverageMarketCap",
    "Category_Average": 365268.10945,
    "Benchmark": 292063.35139,
    "Portfolio_%": 328535.75957
  },
  "1": {
    "Size": "Giant",
    "Category_Average": 56.16412,
    "Benchmark": 45.02014,
    "Portfolio_%": 46.91601
  }
}
```

**Structure**: Array of market cap metrics indexed by position.

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Size` | string | Market cap category or metric |
| `Portfolio_%` | number | Value for the fund's portfolio |
| `Category_Average` | number | Average for the fund category |
| `Benchmark` | number | Benchmark value for comparison |

**Market Cap Categories**:
- `AverageMarketCap` - Average market cap in millions
- `Giant` - Mega-cap stocks (typically >$200B)
- `Large` - Large-cap stocks ($10B-$200B)
- `Medium` - Mid-cap stocks ($2B-$10B)
- `Small` - Small-cap stocks ($300M-$2B)
- `Micro` - Micro-cap stocks (<$300M)

**Interpretation**:
- `AverageMarketCap`: Dollar value in millions
- Size categories: Percentage of portfolio
- Compare to `Category_Average` and `Benchmark` to understand style tilt

### 2.6 Sector Weights

Sector allocation breakdown organized by super-sectors.

**Request**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Sector_Weights
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=MutualFund_Data::Sector_Weights
```

**Response**:
```json
{
  "Cyclical": {
    "0": {
      "Name": "Basic Materials",
      "Category_Average": 2.51562,
      "Amount_%": 1.93346,
      "Benchmark": 2.0688
    },
    "1": {
      "Name": "Consumer Cyclical",
      "Category_Average": 9.97737,
      "Amount_%": 10.20911,
      "Benchmark": 10.28619
    }
  },
  "Defensive": {
    "0": {
      "Name": "Consumer Defensive",
      "Category_Average": 5.90142,
      "Amount_%": 5.7586,
      "Benchmark": 5.64783
    },
    "1": {
      "Name": "Healthcare",
      "Category_Average": 12.25982,
      "Amount_%": 11.17687,
      "Benchmark": 11.22479
    }
  },
  "Sensitive": {
    "0": {
      "Name": "Communication Services",
      "Category_Average": 8.40353,
      "Amount_%": 9.10839,
      "Benchmark": 9.12729
    },
    "1": {
      "Name": "Energy",
      "Category_Average": 3.4342,
      "Amount_%": 3.36916,
      "Benchmark": 3.44415
    }
  },
  "Bond Sector": {
    "0": {
      "Name": "Government",
      "Category_Average": 17.8382,
      "Amount_%": 2.69783,
      "Stocks_%": 0,
      "Benchmark": null
    },
    "1": {
      "Name": "Municipal",
      "Category_Average": 0.00243,
      "Amount_%": 2.69783,
      "Stocks_%": 0,
      "Benchmark": null
    }
  }
}
```

**Structure**: Object with four super-sector categories, each containing arrays of sectors.

### Super-Sector Categories

#### Cyclical
Sectors sensitive to economic cycles:

| Sector | Description |
|--------|-------------|
| **Basic Materials** | Mining, chemicals, forestry products |
| **Consumer Cyclical** | Retail, automotive, housing-related |
| **Financial Services** | Banks, insurance, capital markets |
| **Real Estate** | REITs and real estate companies |

#### Defensive
Sectors less sensitive to economic cycles:

| Sector | Description |
|--------|-------------|
| **Consumer Defensive** | Food, beverages, household products |
| **Healthcare** | Pharmaceuticals, biotech, healthcare services |
| **Utilities** | Electric, gas, water utilities |

#### Sensitive
Sectors moderately sensitive to economic changes:

| Sector | Description |
|--------|-------------|
| **Communication Services** | Telecom, media, entertainment |
| **Energy** | Oil, gas, coal, renewable energy |
| **Industrials** | Manufacturing, aerospace, construction |
| **Technology** | Software, hardware, semiconductors |

#### Bond Sector
For bond-based or balanced funds:

| Sector | Description |
|--------|-------------|
| **Government** | Government bonds (Treasury, agency) |
| **Municipal** | Municipal bonds |
| **Corporate** | Corporate bonds |
| **Securitized** | MBS, ABS, CMBS |
| **Cash & Equivalents** | Cash, money market |

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | Sector name |
| `Amount_%` | number | Fund's allocation to this sector (percentage) |
| `Category_Average` | number | Average allocation for category |
| `Benchmark` | number/null | Benchmark allocation |
| `Stocks_%` | number | Stock allocation (for bond sectors) |

**Notes**:
- `Amount_%` is the fund's actual allocation
- Compare to `Category_Average` to identify over/underweight positions
- Bond sectors may appear in balanced funds
- `Stocks_%` in Bond Sector shows equity portion (typically 0)

### 2.7 World Regions

Geographic allocation organized by major regions.

**Request**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::World_Regions
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=MutualFund_Data::World_Regions
```

**Response**:
```json
{
  "Americas": {
    "0": {
      "Name": "North America",
      "Category_Average": 98.023,
      "Stocks_%": 99.399,
      "Benchmark": 99.172
    },
    "1": {
      "Name": "Latin America",
      "Category_Average": 0.052,
      "Stocks_%": 0,
      "Benchmark": 0.226
    }
  },
  "Greater Asia": {
    "0": {
      "Name": "Japan",
      "Category_Average": 0.061,
      "Stocks_%": 0,
      "Benchmark": 0
    },
    "1": {
      "Name": "Australasia",
      "Category_Average": 0.002,
      "Stocks_%": 0,
      "Benchmark": 0
    }
  },
  "Greater Europe": {
    "0": {
      "Name": "United Kingdom",
      "Category_Average": 0.46516,
      "Stocks_%": 0.09689,
      "Benchmark": 0.11856
    },
    "1": {
      "Name": "Europe Developed",
      "Category_Average": 1.105,
      "Stocks_%": 0.46,
      "Benchmark": 0.443
    }
  }
}
```

**Structure**: Object with three major regions, each containing arrays of sub-regions.

### Regional Structure

#### Americas
| Region | Description |
|--------|-------------|
| **North America** | US, Canada |
| **Latin America** | Mexico, Central America, South America |

#### Greater Europe
| Region | Description |
|--------|-------------|
| **United Kingdom** | UK |
| **Europe Developed** | Western Europe (ex-UK) |
| **Europe Emerging** | Eastern Europe |
| **Africa/Middle East** | Africa and Middle East |

#### Greater Asia
| Region | Description |
|--------|-------------|
| **Japan** | Japan |
| **Australasia** | Australia, New Zealand |
| **Asia Developed** | Hong Kong, Singapore, South Korea |
| **Asia Emerging** | China, India, Southeast Asia |

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | Region/country name |
| `Stocks_%` | number | Fund's equity allocation to this region (percentage) |
| `Category_Average` | number | Average allocation for category |
| `Benchmark` | number | Benchmark allocation |

**Notes**:
- Only applicable for equity and balanced funds
- `Stocks_%` shows percentage of equity portfolio (not total portfolio)
- Compare to `Category_Average` to identify geographic tilts
- Developed vs. emerging market exposure visible through regions

### 2.8 Top Countries

Country-level exposure (especially relevant for bond-based mutual funds).

**Request**:
```
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Top_Countries
```

Or generally:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter=MutualFund_Data::Top_Countries
```

**Response**:
```json
{
  "0": {
    "Name": "United Kingdom",
    "Category_Average": 0.46516,
    "Stocks_%": 0.09689,
    "Benchmark": 0.11856
  }
}
```

**Structure**: Array of country exposures indexed by position.

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | Country name |
| `Stocks_%` | number | Fund's allocation to this country (percentage) |
| `Category_Average` | number | Average allocation for category |
| `Benchmark` | number | Benchmark allocation |

**Notes**:
- Typically shows top countries by exposure
- Particularly useful for international and bond funds
- For US equity funds, US will dominate (often >95%)
- For bond funds, shows sovereign bond exposure by country

## Filter Parameter Reference

### Single Filter Examples

```bash
# General information
&filter=General

# All fund-specific data (large response)
&filter=MutualFund_Data
```

### Nested Filter Examples

```bash
# Asset allocation breakdown
&filter=MutualFund_Data::Asset_Allocation

# Valuation metrics
&filter=MutualFund_Data::Value_Growth

# Top holdings
&filter=MutualFund_Data::Top_Holdings

# Market cap distribution
&filter=MutualFund_Data::Market_Capitalization

# Sector weights
&filter=MutualFund_Data::Sector_Weights

# Geographic exposure
&filter=MutualFund_Data::World_Regions

# Country exposure
&filter=MutualFund_Data::Top_Countries
```

### Multiple Filter Examples

To get multiple sections in one request, make separate API calls. The filter parameter does not support comma-separated values for nested filters.

## Common Use Cases

### 1. Fund Screening by Expense Ratio

Get expense ratio and yields for cost comparison:

```bash
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data
```

**Then extract**:
```python
expense_ratio = data["MutualFund_Data"]["Expense_Ratio"]
yield_5year = data["MutualFund_Data"]["Yield_5Year_YTD"]
```

**Use case**: Compare costs across similar funds.

### 2. Asset Allocation Analysis

Compare asset allocation across funds:

```bash
# Equity fund
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data::Asset_Allocation

# Balanced fund
python eodhd_client.py --endpoint fundamentals --symbol VBIAX.US --filter MutualFund_Data::Asset_Allocation
```

**Use case**: Portfolio construction and asset class exposure.

### 3. Sector Rotation Strategy

Analyze sector weights to identify tilts:

```bash
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data::Sector_Weights
```

**Use case**: Understand sector exposure and rotation opportunities.

### 4. Geographic Diversification

Assess international exposure:

```bash
python eodhd_client.py --endpoint fundamentals --symbol VGTSX.US --filter MutualFund_Data::World_Regions
```

**Use case**: Evaluate geographic risk and diversification.

### 5. Holdings Concentration Analysis

Check top holdings for concentration risk:

```bash
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data::Top_Holdings
```

**Use case**: Assess concentration risk in top positions.

### 6. Style Analysis

Compare valuation metrics to determine fund style (value vs. growth):

```bash
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data::Value_Growth
```

**Use case**: Verify fund style matches investment objectives.

### 7. Performance Comparison

Compare yields and performance across time periods:

```bash
# Get MutualFund_Data for multiple funds
curl "https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data" | jq '{Yield_1Year_YTD, Yield_3Year_YTD, Yield_5Year_YTD, Expense_Ratio}'
```

**Use case**: Historical performance and cost analysis.

## Best Practices

### 1. Always Use Filters

**Problem**: Full mutual fund fundamental data can be 100+ KB
**Solution**: Use specific filters to get only needed data

```bash
# Bad - gets everything
curl "https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json"

# Good - gets only holdings
curl "https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Top_Holdings"
```

### 2. Cache Fundamental Data

**Recommendation**: Cache for 24 hours minimum
- Fundamentals update daily at most
- Saves API calls (10 calls per request)
- Improves application performance

### 3. Check the Type Field

**Always verify** you're getting fund data:

```python
import requests

response = requests.get(
    "https://eodhd.com/api/fundamentals/SWPPX.US",
    params={"api_token": "demo", "fmt": "json", "filter": "General"}
).json()

if response.get("Type") != "FUND":
    raise ValueError(f"Expected FUND, got {response.get('Type')}")
```

### 4. Handle Array-Indexed Responses

Many fund data sections use numeric indices:

```python
asset_allocation = data["MutualFund_Data"]["Asset_Allocation"]

# Iterate through array
for idx, asset in asset_allocation.items():
    asset_type = asset["Type"]
    net_pct = float(asset["Net_%"])
    print(f"{asset_type}: {net_pct}%")
```

### 5. Parse Percentage Strings

Some fields use percentage strings with % sign:

```python
top_holdings = data["MutualFund_Data"]["Top_Holdings"]

for idx, holding in top_holdings.items():
    name = holding["Name"]
    weight_str = holding["Weight"]  # "6.88%"
    weight_float = float(weight_str.rstrip('%'))  # 6.88
    print(f"{name}: {weight_float}%")
```

### 6. Compare to Category Average

Use category comparisons for context:

```python
sector_weights = data["MutualFund_Data"]["Sector_Weights"]["Cyclical"]

for idx, sector in sector_weights.items():
    name = sector["Name"]
    fund_weight = sector["Amount_%"]
    category_avg = sector["Category_Average"]

    if fund_weight > category_avg * 1.2:
        print(f"{name} is overweight ({fund_weight}% vs {category_avg}%)")
```

### 7. Handle Missing/Null Fields

Not all funds have all fields:

```python
morningstar_rating = data.get("MutualFund_Data", {}).get("Morning_Star_Rating")
if morningstar_rating is None:
    print("Morningstar rating not available")
else:
    print(f"Rating: {morningstar_rating} stars")
```

## Error Handling

### Common Issues

**1. Wrong Type**

**Problem**: Requesting fund filters for a stock or ETF
```json
{
  "General": {
    "Type": "Common Stock"
  }
}
```

**Solution**: Check Type field first:
```python
if data["General"]["Type"] != "FUND":
    raise ValueError("Not a mutual fund")
```

**2. Missing Data**

**Problem**: Some funds lack certain fields
**Solution**: Use `.get()` with defaults:
```python
expense_ratio = data.get("MutualFund_Data", {}).get("Expense_Ratio", "N/A")
```

**3. Invalid Ticker**

**Problem**: Fund doesn't exist or wrong exchange
```json
{
  "error": "Not found"
}
```

**Solution**: Verify ticker using search endpoint first

**4. Parsing Array Indices**

**Problem**: Expecting named keys but getting numeric indices
**Solution**: Iterate properly:
```python
# Correct way
for idx, item in data["MutualFund_Data"]["Asset_Allocation"].items():
    print(f"{idx}: {item['Type']}")
```

**5. Percentage String Parsing**

**Problem**: "6.88%" is a string, not a number
**Solution**: Strip % and convert:
```python
weight = holding["Weight"]  # "6.88%"
weight_num = float(weight.rstrip('%'))  # 6.88
```

## Rate Limits & API Costs

- **API calls per request**: 10 calls
- **Recommended cache duration**: 24 hours
- **Update frequency**: Daily
- **Subscription required**: All-In-One or Fundamentals Data Feed

See [rate-limits.md](rate-limits.md) for optimization strategies.

## Related Documentation

- **[Fundamentals API Overview](fundamentals-api.md)** - Compare all instrument types
- **[Fundamentals ETF Guide](fundamentals-etf.md)** - Similar guide for ETFs
- **[Symbol Format](symbol-format.md)** - How to format fund tickers
- **[Exchanges](exchanges.md)** - List of supported exchanges
- **[Update Times](update-times.md)** - When fundamentals are refreshed
- **[Rate Limits](rate-limits.md)** - API quotas and optimization

## Quick Reference

### MutualFund_Data Filter Hierarchy

```
MutualFund_Data
├── [Top-level fields]
│   ├── Nav
│   ├── Yield (current, YTD, 1Y, 3Y, 5Y)
│   ├── Expense_Ratio
│   ├── Portfolio_Net_Assets
│   └── Inception_Date
├── Asset_Allocation
│   └── [Array of asset types]
│       ├── Type (Cash, Stock US, Stock non-US, Bond, etc.)
│       ├── Net_%
│       ├── Long_%
│       ├── Short_%
│       ├── Category_Average
│       └── Benchmark
├── Value_Growth
│   └── [Array of metrics]
│       ├── Name
│       ├── Stock_Portfolio
│       ├── Category_Average
│       └── Benchmark
├── Top_Holdings
│   └── [Array of holdings]
│       ├── Name
│       └── Weight
├── Market_Capitalization
│   └── [Array of size categories]
│       ├── Size
│       ├── Portfolio_%
│       ├── Category_Average
│       └── Benchmark
├── Sector_Weights
│   ├── Cyclical
│   │   └── [Basic Materials, Consumer Cyclical, Financial Services, Real Estate]
│   ├── Defensive
│   │   └── [Consumer Defensive, Healthcare, Utilities]
│   ├── Sensitive
│   │   └── [Communication Services, Energy, Industrials, Technology]
│   └── Bond Sector
│       └── [Government, Municipal, Corporate, Securitized, etc.]
├── World_Regions
│   ├── Americas
│   │   └── [North America, Latin America]
│   ├── Greater Europe
│   │   └── [United Kingdom, Europe Developed, Europe Emerging, Africa/Middle East]
│   └── Greater Asia
│       └── [Japan, Australasia, Asia Developed, Asia Emerging]
└── Top_Countries
    └── [Array of countries]
        ├── Name
        ├── Stocks_%
        ├── Category_Average
        └── Benchmark
```

### Python Client Examples

```python
# Get fund general info
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter General

# Get top holdings
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data::Top_Holdings

# Get sector allocation
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data::Sector_Weights

# Get asset allocation
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data::Asset_Allocation

# Get performance metrics
python eodhd_client.py --endpoint fundamentals --symbol SWPPX.US --filter MutualFund_Data
```

### curl Examples

```bash
# Check fund type
curl "https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=General"

# Get expense ratio and yields
curl "https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data" | jq '{Expense_Ratio, Yield_1Year_YTD, Yield_5Year_YTD}'

# Get top holdings
curl "https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Top_Holdings"

# Get sector weights
curl "https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Sector_Weights"
```

### Popular Fund Symbols for Testing

**Index Funds**:
- `SWPPX.US` - Schwab S&P 500 Index Fund
- `VFIAX.US` - Vanguard 500 Index Fund Admiral Shares
- `FXAIX.US` - Fidelity 500 Index Fund

**Balanced Funds**:
- `VBIAX.US` - Vanguard Balanced Index Fund Admiral Shares
- `VWINX.US` - Vanguard Wellesley Income Fund

**International Funds**:
- `VGTSX.US` - Vanguard Total International Stock Index Fund
- `VTSNX.US` - Vanguard Total International Stock Index Fund

**Bond Funds**:
- `VBTLX.US` - Vanguard Total Bond Market Index Fund Admiral Shares
- `VBMFX.US` - Vanguard Total Bond Market Index Fund

## Data Structure Notes

### Array-Indexed Fields

Unlike ETFs (which use ticker keys), mutual fund subsections use **numeric indices**:

```python
# ETF: Uses ticker as key
etf_holdings = {"AAPL.US": {...}, "MSFT.US": {...}}

# Fund: Uses numeric index
fund_holdings = {"0": {...}, "1": {...}, "2": {...}}
```

**Iteration pattern**:
```python
for idx, item in fund_data.items():
    # idx is "0", "1", "2", etc.
    # item is the data object
    process(item)
```

### Percentage Formats

The API uses **two different percentage formats**:

1. **Decimal strings**: `"0.0200"` = 2%
   - Used for: `Expense_Ratio`, `Yield`, `Net_%`, `Long_%`
   - Convert: `float(value) * 100` for percentage

2. **Percentage strings**: `"6.88%"` = 6.88%
   - Used for: `Weight` in Top_Holdings, `Amount_%` in some contexts
   - Convert: `float(value.rstrip('%'))` for numeric

**Example**:
```python
# Decimal format
expense_ratio = "0.0200"  # This is 2%
pct = float(expense_ratio) * 100  # 2.0

# Percentage format
weight = "6.88%"  # This is already 6.88%
pct = float(weight.rstrip('%'))  # 6.88
```

### Comparison Fields

Most subsections include comparison fields:

- **Category_Average**: Average for Morningstar category
- **Benchmark**: Benchmark index value
- **Stock_Portfolio** / **Portfolio_%** / **Amount_%**: Fund's actual value

**Use these to identify**:
- Overweight positions (fund > average)
- Underweight positions (fund < average)
- Style tilts (value vs. growth, large vs. small cap)

---

**Last Updated**: February 2026
**API Version**: Current
**Maintained By**: EODHD Skills Team
