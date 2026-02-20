# EODHD Fundamentals API - Overview

The Fundamentals API provides extensive fundamental data for stocks, ETFs, mutual funds, indices, and cryptocurrencies from different exchanges and countries.

## Important: Multiple Data Types

**The same API endpoint returns completely different data structures** depending on the instrument type:

| Type | Description | Detailed Guide |
|------|-------------|----------------|
| **Common Stock** | Company fundamentals, financial statements, earnings | **[fundamentals-common-stock.md](fundamentals-common-stock.md)** ✅ |
| **ETF** | Holdings, allocations, sector weights, performance | **[fundamentals-etf.md](fundamentals-etf.md)** ✅ |
| **FUND** | Mutual fund composition, allocations, performance | **[fundamentals-fund.md](fundamentals-fund.md)** ✅ |
| **Index** | Constituents, historical components | [fundamentals-index.md](fundamentals-index.md) *(coming soon)* |
| **Crypto / Currency** | Crypto statistics, forex pairs | **[fundamentals-crypto-currency.md](fundamentals-crypto-currency.md)** ✅ |

The data type is indicated in the `"Type"` field within the `"General"` section of the response.

## Quick Start

### 1. Make API Request

```bash
curl "https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json"
```

**Example**:
```bash
# Stock
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=General"

# ETF
curl "https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=General"

# Mutual Fund
curl "https://eodhd.com/api/fundamentals/VFIAX.US?api_token=demo&fmt=json&filter=General"

# Index
curl "https://eodhd.com/api/fundamentals/GSPC.INDX?api_token=demo&fmt=json&filter=General"
```

### 2. Check the Type Field

```json
{
  "General": {
    "Code": "AAPL",
    "Type": "Common Stock",  // Could be: "Common Stock", "ETF", "FUND", "INDX"
    "Name": "Apple Inc",
    ...
  }
}
```

### 3. Consult Type-Specific Guide

Based on the `Type` value, refer to the appropriate detailed guide:

- **"Common Stock"** → **[fundamentals-common-stock.md](fundamentals-common-stock.md)** ✅
- **"ETF"** → **[fundamentals-etf.md](fundamentals-etf.md)** ✅
- **"FUND"** → **[fundamentals-fund.md](fundamentals-fund.md)** ✅
- **"INDX"** → [fundamentals-index.md](fundamentals-index.md)
- **"Crypto"** or **"Currency"** → **[fundamentals-crypto-currency.md](fundamentals-crypto-currency.md)** ✅

## API Basics

### Endpoint Format

```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json
```

**Parameters**:
- `{TICKER}`: Format `{SYMBOL}.{EXCHANGE}` (e.g., `AAPL.US`, `VTI.US`)
- `{API_TOKEN}`: Your API key
- `fmt=json`: Required (JSON only format)
- `filter=`: **Highly recommended** - Retrieve specific sections only
- `from=` / `to=`: Date filtering (supported for Common Stocks and Indices)

### Key Characteristics

| Characteristic | Value |
|---------------|-------|
| **API calls consumption** | 10 calls per request |
| **Format** | JSON only |
| **Response size** | Very large (100+ KB to 800+ KB) |
| **Filter support** | ✅ Required for production use |
| **Update frequency** | Varies by component (daily to quarterly) |
| **Caching recommendation** | 24 hours minimum |

See [update-times.md](update-times.md) for detailed refresh schedules.

## Filter Parameter (Critical for Performance)

The `filter` parameter is **essential** for working with the Fundamentals API efficiently.

### Why Use Filters?

- **Without filter**: Response can be 800+ KB with all data
- **With filter**: Response reduced to only needed sections (5-50 KB)
- **API cost**: Same (10 calls) regardless of filter usage
- **Performance**: Faster response times, less bandwidth

### Filter Syntax

**Single section**:
```
&filter=General
```

**Nested section** (use `::` separator):
```
&filter=Financials::Balance_Sheet::yearly
&filter=ETF_Data::Top_10_Holdings
```

**Multiple filters** (comma-separated):
```
&filter=General,Highlights,Valuation
```

**Specific field**:
```
&filter=General::Code
```

### Common Filter Examples by Type

#### Common Stock Filters
```bash
# Company overview
&filter=General

# Key metrics
&filter=Highlights

# Latest quarterly balance sheet
&filter=Financials::Balance_Sheet::quarterly

# Annual income statement
&filter=Financials::Income_Statement::yearly

# Earnings history
&filter=Earnings::History

# Analyst estimates
&filter=AnalystRatings
```

#### ETF Filters
```bash
# ETF overview
&filter=General

# Top 10 holdings
&filter=ETF_Data::Top_10_Holdings

# Sector allocation
&filter=ETF_Data::Sector_Weights

# Geographic exposure
&filter=ETF_Data::World_Regions

# Performance metrics
&filter=ETF_Data::Performance
```

See type-specific guides for complete filter references.

## Date Filtering

Date filtering with `from` and `to` parameters works **differently** depending on instrument type:

| Instrument Type | Date Filtering Support | What It Filters |
|----------------|----------------------|-----------------|
| **Common Stock** | ✅ Yes (NEW feature) | Financial statements (quarterly/yearly) |
| **ETF** | ❌ No | N/A |
| **FUND** | ❌ No | N/A |
| **Index** | ✅ Yes | Historical constituent snapshots |

### Date Filtering for Common Stocks (NEW)

Filter financial statements by date range:

```bash
# Get quarterly cash flow for Q3 and Q4 2024
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Cash_Flow::quarterly&from=2024-09-30&to=2024-12-31"
```

**Supported sections**:
- `Financials::Balance_Sheet::quarterly`
- `Financials::Balance_Sheet::yearly`
- `Financials::Cash_Flow::quarterly`
- `Financials::Cash_Flow::yearly`
- `Financials::Income_Statement::quarterly`
- `Financials::Income_Statement::yearly`

### Date Filtering for Indices

Filter historical constituent snapshots:

```bash
# Get S&P 500 constituents for 2020-2023
curl "https://eodhd.com/api/fundamentals/GSPC.INDX?api_token=demo&fmt=json&historical=1&from=2020-01-01&to=2023-01-01"
```

See [fundamentals-index.md](fundamentals-index.md) for details.

## Data Structure Comparison

### Top-Level Sections by Type

#### Common Stock

```
Common Stock Fundamentals
├── General (basic company info)
├── Highlights (key metrics)
├── Valuation (valuation ratios)
├── SharesStats (share statistics)
├── Technicals (technical indicators)
├── SplitsDividends (corporate actions)
├── AnalystRatings (analyst coverage)
├── Holders (institutional/insider ownership)
├── InsiderTransactions (recent insider activity)
├── ESGScores (ESG ratings)
├── outstandingShares (historical shares outstanding)
├── Earnings (earnings history and estimates)
│   ├── History
│   ├── Trend
│   └── Annual
└── Financials (financial statements)
    ├── Balance_Sheet (quarterly & yearly)
    ├── Cash_Flow (quarterly & yearly)
    └── Income_Statement (quarterly & yearly)
```

#### ETF

```
ETF Fundamentals
├── General (basic ETF info)
├── Technicals (aggregate metrics)
└── ETF_Data
    ├── Market_Capitalisation (cap distribution)
    ├── Asset_Allocation (asset classes)
    ├── World_Regions (geographic exposure)
    ├── Sector_Weights (sector allocation)
    ├── Fixed_Income (bond metrics)
    ├── Top_10_Holdings (top holdings)
    ├── Holdings (all holdings - very large)
    ├── Valuations_Growth (valuation & growth rates)
    ├── MorningStar (ratings)
    └── Performance (returns & risk)
```

#### Fund (Mutual Fund)

```
Fund Fundamentals
├── General (basic fund info)
└── MutualFund_Data
    ├── Asset_Allocation
    ├── World_Regions
    ├── Sector_Weights
    ├── Top_10_Holdings
    ├── Holdings
    ├── Valuations_Growth
    └── [other fund-specific sections]
```

#### Index

```
Index Fundamentals
├── General (index info)
├── Components (current constituents)
│   └── {TICKER.EXCHANGE} (component details)
└── HistoricalComponents (requires historical=1)
    └── YYYY-MM-DD (constituent snapshot by date)
        └── {TICKER.EXCHANGE}
```

## Working with Different Types

### Type Detection Pattern

```python
import requests

def get_fundamentals(ticker, api_token):
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "General"  # Always get General first
    }

    response = requests.get(url, params=params).json()
    instrument_type = response.get("Type")

    # Route to appropriate handler
    if instrument_type == "Common Stock":
        return handle_stock(ticker, api_token)
    elif instrument_type == "ETF":
        return handle_etf(ticker, api_token)
    elif instrument_type == "FUND":
        return handle_fund(ticker, api_token)
    elif instrument_type == "INDX":
        return handle_index(ticker, api_token)
    else:
        raise ValueError(f"Unknown type: {instrument_type}")
```

### Always Use Filters

```python
# ❌ Bad - Gets all data (800+ KB for AAPL)
response = requests.get(
    "https://eodhd.com/api/fundamentals/AAPL.US",
    params={"api_token": token, "fmt": "json"}
)

# ✅ Good - Gets only needed section
response = requests.get(
    "https://eodhd.com/api/fundamentals/AAPL.US",
    params={
        "api_token": token,
        "fmt": "json",
        "filter": "Highlights"
    }
)
```

## Common Use Cases

### 1. Company Financial Analysis (Common Stock)

```bash
# Get latest quarterly financials
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Financials::Income_Statement::quarterly"
```

See [fundamentals-common-stock.md](fundamentals-common-stock.md) for details.

### 2. ETF Holdings Analysis

```bash
# Get top holdings and sector weights
curl "https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Top_10_Holdings"
```

See **[fundamentals-etf.md](fundamentals-etf.md)** for complete examples.

### 3. Fund Comparison

```bash
# Compare mutual fund allocations
curl "https://eodhd.com/api/fundamentals/VFIAX.US?api_token=demo&fmt=json&filter=MutualFund_Data::Sector_Weights"
```

See [fundamentals-fund.md](fundamentals-fund.md) for details.

### 4. Index Constituent Tracking

```bash
# Get current S&P 500 constituents
curl "https://eodhd.com/api/fundamentals/GSPC.INDX?api_token=demo&fmt=json&filter=Components"
```

See [fundamentals-index.md](fundamentals-index.md) for details.

## Best Practices

### 1. Always Check the Type First

```bash
# First request - identify type
curl "https://eodhd.com/api/fundamentals/{TICKER}?api_token=demo&fmt=json&filter=General"
```

### 2. Use Specific Filters

```bash
# Don't request everything
❌ &fmt=json

# Request only what you need
✅ &fmt=json&filter=Highlights
✅ &fmt=json&filter=ETF_Data::Top_10_Holdings
```

### 3. Cache Aggressively

- **Minimum cache duration**: 24 hours
- **API cost**: 10 calls per request
- **Update frequency**: Daily at most (varies by component)

```python
import time

cache = {}
CACHE_TTL = 86400  # 24 hours

def get_fundamentals_cached(ticker, api_token, filter_param):
    cache_key = f"{ticker}:{filter_param}"

    if cache_key in cache:
        data, timestamp = cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return data

    # Make API call
    data = fetch_fundamentals(ticker, api_token, filter_param)
    cache[cache_key] = (data, time.time())
    return data
```

### 4. Handle Missing Fields

Not all instruments have all fields:

```python
# Use .get() with defaults
expense_ratio = data.get("ETF_Data", {}).get("NetExpenseRatio", "N/A")

# Check before accessing
if "Earnings" in data and "History" in data["Earnings"]:
    earnings_history = data["Earnings"]["History"]
```

### 5. Understand Update Frequencies

Different sections update at different frequencies:

| Section | Update Frequency |
|---------|-----------------|
| **General** | Daily |
| **Highlights** | Daily |
| **Technicals** | Daily |
| **Financials** | Quarterly (after earnings) |
| **Earnings::History** | Quarterly |
| **ETF_Data::Holdings** | Monthly |
| **Analyst Ratings** | Weekly |

See [update-times.md](update-times.md) for complete schedule.

## Error Handling

### Common Issues

**1. Wrong Type Expected**

```python
# Check type before processing
if data.get("General", {}).get("Type") != "ETF":
    raise ValueError("Expected ETF, got different type")
```

**2. Missing Fields**

```python
# Handle missing data gracefully
holdings = data.get("ETF_Data", {}).get("Top_10_Holdings", {})
if not holdings:
    print("Holdings data not available")
```

**3. Invalid Ticker**

```json
{
  "error": "Not found"
}
```

**Solution**: Use Symbol Search endpoint first to verify ticker exists.

**4. Rate Limit Exceeded**

```json
{
  "error": "Too many requests"
}
```

**Solution**: Implement caching and respect rate limits. See [rate-limits.md](rate-limits.md).

## Rate Limits & API Costs

| Aspect | Details |
|--------|---------|
| **API calls per request** | 10 calls |
| **Monthly quota** | Plan-dependent |
| **Recommended cache** | 24+ hours |
| **Update frequency** | Varies (daily to quarterly) |
| **Required subscription** | All-In-One or Fundamentals Data Feed |

**Optimization tips**:
1. Use filters to reduce response size
2. Cache results for 24+ hours
3. Batch requests efficiently
4. Check `/user` endpoint for remaining quota

See [rate-limits.md](rate-limits.md) for detailed optimization strategies.

## Type-Specific Guides

Choose the guide for your instrument type:

### 📊 Common Stock (Stocks)
**[fundamentals-common-stock.md](fundamentals-common-stock.md)** ✅ **Available Now**

Complete guide covering:
- General (company details, officers, identifiers)
- Highlights (key metrics, EPS, margins, returns)
- Valuation (P/E, P/S, P/B, EV ratios)
- SharesStats (outstanding, float, ownership percentages)
- Technicals (beta, moving averages, short interest)
- SplitsDividends (dividend history, split history)
- AnalystRatings (consensus, target price)
- Holders (institutions and funds with holdings)
- InsiderTransactions (Form 4 filings)
- outstandingShares (historical shares outstanding)
- Earnings (history, trend, annual estimates)
- **Financials** (Balance Sheet, Cash Flow, Income Statement)
  - ✅ **NEW: Date filtering support** with `from` and `to` parameters
  - Quarterly and yearly data
  - Historical data from 1985 (US) / 2000 (non-US)

**Tickers for testing**: `AAPL.US`, `TSLA.US`, `AMZN.US` (full demo access)

---

### 📈 ETF (Exchange-Traded Funds)
**[fundamentals-etf.md](fundamentals-etf.md)** ✅ **Available Now**

Complete guide covering:
- ETF overview and characteristics
- Holdings (top 10 and complete)
- Asset allocation and geographic exposure
- Sector weights
- Valuation and growth metrics
- Performance and risk statistics
- Morningstar ratings
- All 11 ETF_Data subsections with detailed examples

**Tickers for testing**: `VTI.US`, `SPY.US`, `QQQ.US`

---

### 🏦 Mutual Funds
**[fundamentals-fund.md](fundamentals-fund.md)** ✅ **Available Now**

Complete guide covering:
- Fund overview, summary, and family
- Asset allocation (cash, stocks, bonds)
- Value growth measures (P/E, P/B, P/S, growth rates)
- Top holdings
- Market capitalization distribution
- Sector weights (Cyclical, Defensive, Sensitive, Bond Sector)
- World regions (Americas, Greater Europe, Greater Asia)
- Top countries exposure
- Performance metrics (NAV, yields, expense ratio)
- All 8 MutualFund_Data subsections with detailed examples

**Tickers for testing**: `SWPPX.US`, `VFIAX.US`, `FXAIX.US`

---

### 📉 Indices
**[fundamentals-index.md](fundamentals-index.md)** *(coming soon)*

Will cover:
- Current constituents
- Historical constituent snapshots
- Date filtering for historical data
- Component details

**Tickers for testing**: `GSPC.INDX`, `DJI.INDX`

---

### ₿ Cryptocurrency & Currency (Forex)
**[fundamentals-crypto-currency.md](fundamentals-crypto-currency.md)** ✅ **Available Now**

Complete guide covering:
- **Cryptocurrencies**: Market statistics, supply metrics, developers, resources
  - General (name, category, description)
  - Tech (developers and technical info)
  - Resources (links, explorers, social media, thumbnail)
  - Statistics (market cap, supply, dominance, ATH/ATL)
- **Currency Pairs (Forex)**: Quote currency information
  - General (code, name, currency details)
  - Components (typically empty)

**Tickers for testing**:
- Crypto: `BTC-USD.CC`, `ETH-USD.CC`, `SOL-USD.CC`
- Forex: `EURUSD.FOREX`, `GBPUSD.FOREX`, `USDJPY.FOREX`

## Related Documentation

- **[Symbol Format](symbol-format.md)** - How to format ticker symbols correctly
- **[Exchanges](exchanges.md)** - List of supported exchanges
- **[Update Times](update-times.md)** - When fundamentals data is refreshed
- **[Authentication](authentication.md)** - API token setup
- **[Rate Limits](rate-limits.md)** - API quotas and optimization

## Quick Reference

### Python Client

```bash
# Get fundamentals (auto-detects type)
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter General

# Get specific section
python eodhd_client.py --endpoint fundamentals --symbol VTI.US --filter ETF_Data::Top_10_Holdings

# Get financial statements with date filter (NEW)
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US --filter Financials::Cash_Flow::quarterly --from-date 2024-09-30 --to-date 2024-12-31
```

### curl Examples

```bash
# Check instrument type
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=General"

# Get ETF top holdings
curl "https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data::Top_10_Holdings"

# Get stock highlights
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json&filter=Highlights"
```

### Demo Token

Test the API with the demo token:

```
api_token=demo
```

**Available demo symbols**:
- Stocks: `AAPL.US`, `MSFT.US`, `GOOGL.US`
- ETFs: `VTI.US`, `SPY.US`, `QQQ.US`
- Funds: `SWPPX.US`, `VFIAX.US`
- Indices: `GSPC.INDX`, `DJI.INDX`
- Crypto: `BTC-USD.CC`, `ETH-USD.CC`
- Forex: `EURUSD.FOREX`, `GBPUSD.FOREX`

## Summary: Key Differences by Type

| Feature | Common Stock | ETF | Fund | Index | Crypto/Forex |
|---------|-------------|-----|------|-------|--------------|
| **Type value** | "Common Stock" | "ETF" | "FUND" | "INDX" | "Crypto" / "Currency" |
| **Main data** | Financials, Earnings | Holdings, Allocations | Holdings, Allocations | Constituents | Statistics, Resources |
| **Financial statements** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Holdings** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes (components) | ❌ No |
| **Date filtering** | ✅ Yes (new) | ❌ No | ❌ No | ✅ Yes (historical) | ❌ No |
| **Response size** | Very Large (800+ KB) | Large (100+ KB) | Large (100+ KB) | Medium (50+ KB) | Small (5-20 KB) |
| **Update frequency** | Daily/Quarterly | Daily/Monthly | Daily/Monthly | Daily | Statistics: frequent |
| **Detailed guide** | **[Available](fundamentals-common-stock.md)** | **[Available](fundamentals-etf.md)** | **[Available](fundamentals-fund.md)** | Coming soon | **[Available](fundamentals-crypto-currency.md)** |

---

**Last Updated**: February 2026
**API Version**: Current
**Maintained By**: EODHD Skills Team
