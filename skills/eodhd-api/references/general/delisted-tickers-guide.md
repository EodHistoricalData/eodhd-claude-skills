# Delisted Tickers Data Guide

**Purpose**: Access historical data for delisted companies and understand ticker reuse patterns
**Last Updated**: 2024-11-27
**Coverage**: 26,000+ US tickers (from Jan 2000), 42,000+ non-US tickers (latest 6-7 years)

---

## Table of Contents

1. [Overview](#overview)
2. [Why Choose EODHD for Delisted Data](#why-choose-eodhd-for-delisted-data)
3. [Data Coverage](#data-coverage)
4. [How Delisted Tickers Work](#how-delisted-tickers-work)
5. [Finding Delisted Tickers](#finding-delisted-tickers)
6. [Accessing Delisted Data](#accessing-delisted-data)
7. [Ticker Renaming & Reuse](#ticker-renaming--reuse)
8. [Fundamentals for Delisted Companies](#fundamentals-for-delisted-companies)
9. [Python Implementation](#python-implementation)
10. [Common Use Cases](#common-use-cases)
11. [Best Practices](#best-practices)

---

## Overview

### The Challenge

Finding delisted stock price history can be a daunting quest:
- Unknown sources with questionable reliability
- Incomplete data coverage
- Limited access to historical information
- Data scattered across multiple platforms
- Endless fruitless searches

### The Solution

EODHD provides comprehensive archives of delisted stock data:
- **26,000+ US stock tickers** (mostly from January 2000)
- **42,000+ non-US tickers** (mostly within latest 6-7 years)
- Better coverage than 90% of common data sources
- Continuously updated and replenished archives

### What is a Delisted Ticker?

A ticker becomes **delisted** when:
- Company is acquired or merged with another company
- Company goes bankrupt or ceases operations
- Company voluntarily delists from the exchange
- Company moves to a different exchange (redomiciliation)
- Regulatory reasons or compliance failures

**Important**: When a ticker is delisted, EODHD **does not remove it** from the system. Instead, it is marked as "delisted" and remains accessible using its original ticker symbol.

---

## Why Choose EODHD for Delisted Data

### 1. Extensive Data Coverage

**Most Complete Archives**: EODHD offers the most comprehensive and up-to-date archives of historical stock prices for delisted companies.

**Wide Industry Coverage**: Database encompasses companies from various industries and sectors worldwide.

**Better Than Alternatives**: Coverage exceeds 90% of most common data sources.

### 2. User-Friendly Interface

**Simple API Access**: No tedious searches across multiple platforms.

**Intuitive Design**: Swift and efficient data retrieval through well-documented APIs.

**Consistent Format**: Same API structure for both active and delisted tickers.

### 3. Data Reliability

**Trusted Sources**: Only work with verified, authoritative data sources.

**Quality Assurance**: Accuracy and reliability of information is guaranteed.

**Regular Updates**: Archives continuously replenished and validated.

### 4. Customer Support

**24/7 Availability**: Support team ready to assist with any questions.

**Expert Assistance**: Help with difficulties or additional data needs.

**Active Maintenance**: Ongoing updates and improvements to delisted data.

### 5. Comprehensive Data Types

**Available for Delisted Tickers**:
- End-of-Day historical prices
- Intraday data (where available)
- Fundamentals data (if delisted after 2018)
- Corporate actions (splits, dividends)
- Company information

---

## Data Coverage

### US Stock Tickers

**Coverage**: 26,000+ delisted US stock tickers

**Historical Period**: Mostly from **January 2000** to delisting date

**Exchanges Covered**:
- NYSE (New York Stock Exchange)
- NASDAQ
- AMEX (American Stock Exchange)
- Other US exchanges

**Example Delisted US Tickers**:
- Companies acquired (e.g., LinkedIn before Microsoft acquisition)
- Bankrupt companies (e.g., Lehman Brothers, Enron)
- Merged companies
- Voluntarily delisted companies

### Non-US Tickers

**Coverage**: 42,000+ delisted non-US stock tickers

**Historical Period**: Mostly within **latest 6-7 years** to delisting date

**Global Coverage**: Major exchanges worldwide including:
- London Stock Exchange (LSE)
- Toronto Stock Exchange (TSX)
- Deutsche Börse (XETRA)
- Euronext exchanges
- Asian exchanges (Tokyo, Hong Kong, Shanghai)
- And many more

### Data Availability by Exchange

| Exchange Type | Ticker Count | Historical Period | Notes |
|--------------|--------------|-------------------|-------|
| **US Exchanges** | 26,000+ | From ~Jan 2000 | Most comprehensive coverage |
| **Non-US Exchanges** | 42,000+ | Latest 6-7 years | Continuously expanding |
| **Total** | **68,000+** | Varies by exchange | Better than 90% of sources |

### Critical Data Availability Note

⚠️ **IMPORTANT**: While EODHD lists 68,000+ delisted tickers, **actual historical data availability** is limited:

**Delisting Date Cutoff**: For most tickers delisted **prior to approximately 2014** (with some exceptions), EODHD does **not have historical price data** available.

**What This Means**:
- **Ticker appears in delisted list** (via `exchange-symbol-list` with `delisted=1`)
- **BUT historical data may not exist** (EOD API returns empty or error)

**Data Availability Timeline**:
- **Delisted before ~2014**: Generally no data (with rare exceptions)
- **Delisted 2014-2017**: Generally have EOD, splits, dividends data
- **Delisted 2018+**: Generally have EOD, splits, dividends, **and fundamentals** data

**Recommendation**: Always **verify data availability** by attempting to fetch historical data before assuming it exists for a delisted ticker.

---

## How Delisted Tickers Work

### System Behavior

#### When a Ticker is Delisted

**EODHD Does NOT Remove It**: Instead, the ticker is:
1. Marked with `"IsDelisted": true` flag
2. Kept in the system with its original symbol
3. Accessible via all standard APIs (if data exists)
4. Historical data available **if delisted after ~2014** (with exceptions)

#### When a Ticker is Renamed

**Update to New Symbol**: Typically, the original symbol is updated to reflect the new name.

**Old Code Unavailable**: Data will no longer be available under the old ticker code.

**Exception**: In some cases, the old ticker is marked as "delisted," allowing access to historical data using the previous symbol.

#### When a Ticker is Reused

**Original Ticker Gets Suffix**: If a ticker was previously assigned to a different company and is later reused:

1. **First Reuse**: Original ticker gets `_old` suffix (e.g., `ABC` becomes `ABC_old`)
2. **Multiple Reuses**: Incremental numbers added (e.g., `ABC_old1`, `ABC_old2`)
3. **Historical Cases**: Some variations exist for tickers reused long ago (may have number without `_old` suffix)

**Current Ticker**: The most recent company keeps the clean ticker symbol without suffix.

### Examples of Ticker Evolution

#### Example 1: Simple Delisting
```
Company XYZ acquired by Company ABC
Before: XYZ.US (active)
After:  XYZ.US (marked as delisted, data still accessible)
```

#### Example 2: Ticker Reuse (First Time)
```
Old Company ABC goes bankrupt
New Company ABC starts trading with same ticker

Old company: ABC_old.US (historical data)
New company: ABC.US (current data)
```

#### Example 3: Ticker Reuse (Multiple Times)
```
Four different companies have used ticker "XYZ" over time:

Original company:    XYZ_old.US (oldest, first to get suffix)
Second company:      XYZ_old1.US (second period)
Third company:       XYZ_old2.US (third period)
Current company:     XYZ.US (current)
```

---

## Finding Delisted Tickers

### Exchange Symbol List API with Delisted Flag

**Endpoint**:
```
https://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}?api_token=YOUR_API_KEY&delisted=1
```

**Parameters**:
- `{EXCHANGE_CODE}`: Exchange code (e.g., `US`, `LSE`, `TSX`)
- `api_token`: Your API token
- `delisted=1`: **Required parameter** to include delisted tickers

### Response Format

```json
[
  {
    "Code": "AAAB",
    "Name": "AAB Financial Corporation",
    "Country": "USA",
    "Exchange": "US",
    "Currency": "USD",
    "Type": "Common Stock",
    "Isin": "US0000123456",
    "IsDelisted": true
  },
  {
    "Code": "ZZZZ_old",
    "Name": "Old Company Name",
    "Country": "USA",
    "Exchange": "US",
    "Currency": "USD",
    "Type": "Common Stock",
    "Isin": "US9999999999",
    "IsDelisted": true
  }
]
```

**Key Fields**:
- `Code`: Ticker symbol (may have `_old`, `_old1`, etc. suffix)
- `Name`: Company name at time of delisting
- `Isin`: International Securities Identification Number (useful for searching)
- `IsDelisted`: Always `true` when using `delisted=1` parameter

### Examples by Exchange

#### US Delisted Tickers
```bash
https://eodhd.com/api/exchange-symbol-list/US?api_token=YOUR_API_KEY&delisted=1
```

#### London Stock Exchange Delisted Tickers
```bash
https://eodhd.com/api/exchange-symbol-list/LSE?api_token=YOUR_API_KEY&delisted=1
```

#### Toronto Stock Exchange Delisted Tickers
```bash
https://eodhd.com/api/exchange-symbol-list/TSX?api_token=YOUR_API_KEY&delisted=1
```

### Searching for Specific Delisted Ticker

Once you have the list, you can search by:
1. **Ticker Code**: Direct match on `Code` field
2. **Company Name**: Partial or full match on `Name` field
3. **ISIN**: Exact match on `Isin` field (most reliable for renamed companies)

---

## Accessing Delisted Data

### Step-by-Step Process

#### Step 1: Get Delisted Tickers List

```bash
# Get all US delisted tickers
curl "https://eodhd.com/api/exchange-symbol-list/US?api_token=YOUR_API_KEY&delisted=1&fmt=json"
```

#### Step 2: Find Your Ticker

Search the output by:
- Ticker code
- Company name
- ISIN

#### Step 3: Access Historical Data (If Available)

**IMPORTANT**: Data availability depends on delisting date.

Use the ticker code in any relevant API endpoint:

```bash
# End-of-Day historical data (if ticker delisted after ~2014)
https://eodhd.com/api/eod/AAAB.US?api_token=YOUR_API_KEY&fmt=json

# Intraday data (if available for the period and delisted after ~2014)
https://eodhd.com/api/intraday/AAAB.US?interval=1h&api_token=YOUR_API_KEY&fmt=json

# Fundamentals data (only if delisted after 2018)
https://eodhd.com/api/fundamentals/AAAB.US?api_token=YOUR_API_KEY&fmt=json

# Splits and dividends (if ticker delisted after ~2014)
https://eodhd.com/api/splits/AAAB.US?api_token=YOUR_API_KEY&fmt=json
https://eodhd.com/api/div/AAAB.US?api_token=YOUR_API_KEY&fmt=json
```

### Data Availability by Delisting Date

**Critical Limitation**: For most tickers delisted **prior to approximately 2014** (with some exceptions), EODHD does not have historical data available.

| Delisting Period | Data Availability |
|------------------|-------------------|
| **Before ~2014** | ❌ Generally **no data** available (with rare exceptions) |
| **After ~2014** | ✅ EOD, intraday, splits, dividends typically available |
| **After 2018** | ✅ EOD, intraday, splits, dividends, **and fundamentals** available |

### Available APIs for Delisted Tickers

| API | Available | Notes |
|-----|-----------|-------|
| **End-of-Day Historical** | ⚠️ Conditional | Only if delisted after ~2014 (with exceptions) |
| **Intraday Historical** | ⚠️ Conditional | Only if delisted after ~2014 and intraday existed for that period |
| **Live/Real-Time** | ❌ No | Only for currently listed tickers |
| **Fundamentals** | ⚠️ Conditional | Only if delisted after 2018 |
| **Calendar Data** | ⚠️ Conditional | Only if delisted after ~2014 |
| **Technical Indicators** | ⚠️ Conditional | Only if price data available (delisted after ~2014) |
| **Splits** | ⚠️ Conditional | Only if delisted after ~2014 |
| **Dividends** | ⚠️ Conditional | Only if delisted after ~2014 |

**Note**: The ~2014 cutoff is approximate. Some tickers delisted before 2014 may have data, and some after 2014 may not. Always verify by attempting to fetch data for the specific ticker.

---

## Ticker Renaming & Reuse

### Scenario 1: Ticker Renaming

**What Happens**:
When a company changes its ticker symbol (without delisting), EODHD typically updates the original symbol to reflect the new one.

**Result**:
- Data available under **new ticker code** only
- Old ticker code **no longer accessible** (in most cases)
- Historical data transferred to new symbol

**Exception**:
In some cases, the old ticker is marked as "delisted," allowing access to historical data using the previous symbol.

**Example**:
```
Company XYZ Corp changes ticker to ABC Corp
Result: Historical data now under ABC.US
Old ticker XYZ.US may not be accessible (unless marked as delisted)
```

### Scenario 2: Ticker Reuse (First Time)

**What Happens**:
A ticker previously used by one company is assigned to a new company.

**Result**:
- Original company: Gets `_old` suffix added to ticker
- New company: Uses clean ticker symbol

**Example**:
```
1990-2010: ABC Corp trades as ABC.US (goes bankrupt in 2010)
2015-now: New ABC Inc. starts trading as ABC.US

Data access:
- ABC_old.US → Historical data for original ABC Corp (1990-2010)
- ABC.US → Data for new ABC Inc. (2015-present)
```

### Scenario 3: Ticker Reuse (Multiple Times)

**What Happens**:
A ticker has been reused by three or more different companies over time.

**Result**:
- Oldest company: `TICKER_old` (first to get suffix)
- Second company: `TICKER_old1`
- Third company: `TICKER_old2`
- Current company: `TICKER` (clean symbol)

**Example**:
```
1980-1995: Original XYZ Corp → XYZ_old.US (oldest, first to get suffix)
1998-2005: Second XYZ Inc. → XYZ_old1.US
2008-2015: Third XYZ LLC → XYZ_old2.US
2018-now:  Current XYZ Co. → XYZ.US
```

### Scenario 4: Historical Reuse Variations

**What Happens**:
For tickers reused a long time ago, there may be some variations in naming conventions.

**Result**:
- May have number added without `_old` prefix
- May use different suffix patterns
- Requires searching the exchange symbol list to identify

**Example**:
```
Some historical variations:
- ABC1.US, ABC2.US (instead of ABC_old1, ABC_old2)
- ABC-OLD.US (hyphen instead of underscore)
- ABCZ.US (letter suffix instead of _old)
```

### How to Identify Ticker History

#### Method 1: Search by ISIN

**Most Reliable**: ISIN (International Securities Identification Number) remains constant even when ticker changes.

```python
def find_ticker_by_isin(exchange, isin, api_token):
    """Find ticker using ISIN (most reliable for renamed companies)"""
    url = f"https://eodhd.com/api/exchange-symbol-list/{exchange}"
    params = {"api_token": api_token, "delisted": 1, "fmt": "json"}

    response = requests.get(url, params=params)
    tickers = response.json()

    # Find all tickers with matching ISIN
    matches = [t for t in tickers if t.get("Isin") == isin]
    return matches

# Usage
matches = find_ticker_by_isin("US", "US0378331005", "demo")
# Might return: [{"Code": "AAPL.US", ...}] and historical versions if renamed
```

#### Method 2: Search by Company Name

**Useful for Mergers**: Search for old company names.

```python
def find_ticker_by_name(exchange, company_name, api_token):
    """Find tickers by company name (partial match)"""
    url = f"https://eodhd.com/api/exchange-symbol-list/{exchange}"
    params = {"api_token": api_token, "delisted": 1, "fmt": "json"}

    response = requests.get(url, params=params)
    tickers = response.json()

    # Find tickers with matching name (case-insensitive, partial match)
    matches = [
        t for t in tickers
        if company_name.lower() in t.get("Name", "").lower()
    ]
    return matches

# Usage
matches = find_ticker_by_name("US", "Financial Corporation", "demo")
# Returns all tickers with "Financial Corporation" in name
```

#### Method 3: Pattern Matching for Reused Tickers

**Find All Versions**: Search for ticker and all its `_old` variants.

```python
def find_ticker_versions(exchange, base_ticker, api_token):
    """Find all versions of a reused ticker"""
    url = f"https://eodhd.com/api/exchange-symbol-list/{exchange}"
    params = {"api_token": api_token, "delisted": 1, "fmt": "json"}

    response = requests.get(url, params=params)
    tickers = response.json()

    # Find base ticker and all _old variants
    pattern = base_ticker.upper()
    matches = [
        t for t in tickers
        if t.get("Code", "").startswith(pattern)
    ]

    # Sort by Code (current ticker first, then _old, _old1, _old2, etc.)
    matches.sort(key=lambda x: x.get("Code", ""))

    return matches

# Usage
versions = find_ticker_versions("US", "ABC", "demo")
# Might return: ABC.US, ABC_old.US, ABC_old1.US, ABC_old2.US
```

---

## Fundamentals for Delisted Companies

### Availability

**Fundamental data is available for delisted tickers**, but with important conditions:

**Condition**: The ticker must have been removed from the exchange **no earlier than 2018**.

**Coverage**:
- ✅ Delisted in **2018 or later**: Fundamentals data available
- ❌ Delisted **before 2018**: Fundamentals data typically not available

**Individual Review**: Each ticker needs to be reviewed individually to confirm availability.

### What Fundamentals Data Includes

When available, fundamentals for delisted companies include:

- **Financials**: Income Statement, Balance Sheet, Cash Flow
- **General Information**: Company profile, sector, industry
- **Highlights**: Key metrics at time of delisting
- **Valuation**: Historical valuation ratios
- **Earnings**: Historical earnings data
- **Analyst Ratings**: If available before delisting

### Accessing Fundamentals for Delisted Tickers

```bash
# Check if fundamentals available
https://eodhd.com/api/fundamentals/TICKER.US?api_token=YOUR_API_KEY&fmt=json

# If available, use filters for specific data
https://eodhd.com/api/fundamentals/TICKER.US?api_token=YOUR_API_KEY&filter=Financials::Balance_Sheet::yearly&fmt=json
```

### Example Response (If Available)

```json
{
  "General": {
    "Code": "XYZ",
    "Type": "Common Stock",
    "Name": "XYZ Corporation",
    "Exchange": "US",
    "IsDelisted": true,
    "DelistingDate": "2020-03-15"
  },
  "Financials": {
    "Balance_Sheet": {
      "yearly": {
        "2019-12-31": {
          "totalAssets": 1500000000,
          "totalLiab": 800000000,
          "totalStockholderEquity": 700000000
        }
      }
    }
  }
}
```

### If Fundamentals Not Available

**What You Still Have**:
- ✅ End-of-Day historical prices
- ✅ Intraday data (if available for period)
- ✅ Corporate actions (splits, dividends)
- ✅ Basic company information from exchange symbol list

**Workaround**:
- Check third-party financial data sources
- Use SEC filings (for US companies) via EDGAR database
- Contact EODHD support for specific cases

---

## Python Implementation

### Complete Delisted Ticker Manager

```python
import requests
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime

class DelistedTickerManager:
    """Comprehensive manager for delisted ticker data"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://eodhd.com/api"
        self.cache = {}  # Cache delisted lists by exchange

    def get_delisted_tickers(self, exchange: str, use_cache: bool = True) -> pd.DataFrame:
        """
        Get all delisted tickers for an exchange.

        Args:
            exchange: Exchange code (e.g., 'US', 'LSE', 'TSX')
            use_cache: Use cached data if available

        Returns:
            DataFrame with delisted ticker information
        """
        # Check cache
        if use_cache and exchange in self.cache:
            return self.cache[exchange]

        url = f"{self.base_url}/exchange-symbol-list/{exchange}"
        params = {
            "api_token": self.api_token,
            "delisted": 1,
            "fmt": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)

        # Cache the result
        self.cache[exchange] = df

        return df

    def search_by_name(self, exchange: str, company_name: str) -> pd.DataFrame:
        """
        Search delisted tickers by company name.

        Args:
            exchange: Exchange code
            company_name: Company name (partial match)

        Returns:
            DataFrame with matching tickers
        """
        df = self.get_delisted_tickers(exchange)

        # Case-insensitive partial match on Name
        mask = df['Name'].str.contains(company_name, case=False, na=False)
        return df[mask]

    def search_by_isin(self, exchange: str, isin: str) -> pd.DataFrame:
        """
        Search delisted tickers by ISIN (most reliable).

        Args:
            exchange: Exchange code
            isin: International Securities Identification Number

        Returns:
            DataFrame with matching tickers
        """
        df = self.get_delisted_tickers(exchange)

        # Exact match on ISIN
        return df[df['Isin'] == isin]

    def find_ticker_versions(self, exchange: str, base_ticker: str) -> pd.DataFrame:
        """
        Find all versions of a ticker (including _old variants).

        Args:
            exchange: Exchange code
            base_ticker: Base ticker symbol (e.g., 'ABC')

        Returns:
            DataFrame with all ticker versions, sorted
        """
        df = self.get_delisted_tickers(exchange)

        # Find tickers starting with base_ticker
        pattern = base_ticker.upper()
        mask = df['Code'].str.startswith(pattern, na=False)
        matches = df[mask].copy()

        # Sort by Code (current, _old, _old1, _old2, etc.)
        matches = matches.sort_values('Code')

        return matches

    def get_historical_prices(self, ticker: str, exchange: str,
                            from_date: Optional[str] = None,
                            to_date: Optional[str] = None) -> pd.DataFrame:
        """
        Get historical End-of-Day prices for delisted ticker.

        Args:
            ticker: Ticker code (e.g., 'AAAB')
            exchange: Exchange code (e.g., 'US')
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            DataFrame with historical prices
        """
        symbol = f"{ticker}.{exchange}"
        url = f"{self.base_url}/eod/{symbol}"

        params = {
            "api_token": self.api_token,
            "fmt": "json"
        }

        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)

        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')

        return df

    def get_fundamentals(self, ticker: str, exchange: str,
                        filter_path: Optional[str] = None) -> Dict:
        """
        Get fundamental data for delisted ticker (if available).

        Args:
            ticker: Ticker code
            exchange: Exchange code
            filter_path: Optional filter (e.g., 'General')

        Returns:
            Dictionary with fundamental data
        """
        symbol = f"{ticker}.{exchange}"
        url = f"{self.base_url}/fundamentals/{symbol}"

        params = {
            "api_token": self.api_token
        }

        if filter_path:
            params["filter"] = filter_path

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def check_fundamentals_available(self, ticker: str, exchange: str) -> bool:
        """
        Check if fundamental data is available for delisted ticker.

        Args:
            ticker: Ticker code
            exchange: Exchange code

        Returns:
            True if fundamentals available, False otherwise
        """
        try:
            data = self.get_fundamentals(ticker, exchange, filter_path="General")
            # Check if we got valid data (not empty or error)
            return bool(data and not data.get('error'))
        except:
            return False

    def analyze_delisted_ticker(self, ticker: str, exchange: str) -> Dict:
        """
        Comprehensive analysis of a delisted ticker.

        Args:
            ticker: Ticker code
            exchange: Exchange code

        Returns:
            Dictionary with analysis results
        """
        result = {
            "ticker": ticker,
            "exchange": exchange,
            "found": False,
            "versions": [],
            "price_data_available": False,
            "fundamentals_available": False,
            "data_summary": {}
        }

        # Find ticker in delisted list
        df = self.get_delisted_tickers(exchange)
        ticker_info = df[df['Code'] == ticker]

        if ticker_info.empty:
            return result

        result["found"] = True
        result["info"] = ticker_info.iloc[0].to_dict()

        # Find all versions of this ticker
        versions = self.find_ticker_versions(exchange, ticker.replace("_old", "").replace("_old1", "").replace("_old2", ""))
        result["versions"] = versions['Code'].tolist()

        # Check historical price data
        try:
            prices = self.get_historical_prices(ticker, exchange)
            if not prices.empty:
                result["price_data_available"] = True
                result["data_summary"]["first_date"] = prices['date'].min().strftime('%Y-%m-%d')
                result["data_summary"]["last_date"] = prices['date'].max().strftime('%Y-%m-%d')
                result["data_summary"]["total_records"] = len(prices)

                # Estimate if delisted before 2014 (likely no data cutoff)
                last_date = prices['date'].max()
                if last_date.year < 2014:
                    result["data_summary"]["warning"] = "Delisted before ~2014 (rare to have data)"
            else:
                result["data_summary"]["warning"] = "No price data available (likely delisted before ~2014)"
        except:
            result["data_summary"]["warning"] = "No price data available (likely delisted before ~2014)"

        # Check fundamentals
        result["fundamentals_available"] = self.check_fundamentals_available(ticker, exchange)

        return result


# Usage Examples
def main():
    api_token = "demo"  # Replace with your token
    manager = DelistedTickerManager(api_token)

    # Example 1: Get all US delisted tickers
    print("=" * 60)
    print("Example 1: Get US Delisted Tickers")
    print("=" * 60)
    us_delisted = manager.get_delisted_tickers("US")
    print(f"Total US delisted tickers: {len(us_delisted)}")
    print(f"\nFirst 5 delisted tickers:")
    print(us_delisted[['Code', 'Name', 'Type']].head())

    # Example 2: Search by company name
    print("\n" + "=" * 60)
    print("Example 2: Search by Company Name")
    print("=" * 60)
    financial_companies = manager.search_by_name("US", "Financial")
    print(f"Found {len(financial_companies)} delisted companies with 'Financial' in name")
    print(financial_companies[['Code', 'Name']].head())

    # Example 3: Find ticker versions
    print("\n" + "=" * 60)
    print("Example 3: Find Ticker Versions")
    print("=" * 60)
    versions = manager.find_ticker_versions("US", "ABC")
    print(f"Found {len(versions)} versions of ABC ticker:")
    print(versions[['Code', 'Name']])

    # Example 4: Analyze specific delisted ticker
    print("\n" + "=" * 60)
    print("Example 4: Analyze Delisted Ticker")
    print("=" * 60)
    analysis = manager.analyze_delisted_ticker("AAAB", "US")
    print(f"Ticker: {analysis['ticker']}")
    print(f"Found: {analysis['found']}")
    print(f"Price data available: {analysis['price_data_available']}")
    print(f"Fundamentals available: {analysis['fundamentals_available']}")
    if analysis['data_summary']:
        print(f"Date range: {analysis['data_summary'].get('first_date')} to {analysis['data_summary'].get('last_date')}")
        print(f"Total records: {analysis['data_summary'].get('total_records')}")


if __name__ == "__main__":
    main()
```

### Output Example

```
============================================================
Example 1: Get US Delisted Tickers
============================================================
Total US delisted tickers: 26000+

First 5 delisted tickers:
    Code                                          Name            Type
0   AAAB                      AAB Financial Corporation    Common Stock
1   AABC                        AAB Corporation Limited    Common Stock
2   AACQ                          AAC Acquisition Corp.    Common Stock
3   AADR_old                        AdvisorShares Trust             ETF
4   AAMC                         Altisource Asset Mgmt    Common Stock

============================================================
Example 2: Search by Company Name
============================================================
Found 234 delisted companies with 'Financial' in name
    Code                                          Name
0   AAAB                      AAB Financial Corporation
1   AFIN                  American Financial Services
2   BFIN                    Boston Financial Holdings
...

============================================================
Example 3: Find Ticker Versions
============================================================
Found 3 versions of ABC ticker:
    Code                            Name
0   ABC                   ABC Corporation
1   ABC_old         Old ABC Company Inc.
2   ABC_old1    Original ABC Industries

============================================================
Example 4: Analyze Delisted Ticker
============================================================
Ticker: AAAB
Found: True
Price data available: True
Fundamentals available: False
Date range: 2000-01-03 to 2015-06-30
Total records: 3891
```

---

## Common Use Cases

### Use Case 1: Research Bankrupt Companies

**Scenario**: Analyze historical performance of companies that went bankrupt.

```python
def analyze_bankruptcy(ticker, exchange, api_token):
    """Analyze stock performance leading to bankruptcy"""
    manager = DelistedTickerManager(api_token)

    # Get historical prices
    prices = manager.get_historical_prices(ticker, exchange)

    if prices.empty:
        return None

    # Calculate key metrics
    prices = prices.sort_values('date')

    # Find peak and final price
    peak_price = prices['close'].max()
    peak_date = prices.loc[prices['close'].idxmax(), 'date']
    final_price = prices.iloc[-1]['close']
    final_date = prices.iloc[-1]['date']

    # Calculate decline
    decline_pct = ((final_price - peak_price) / peak_price) * 100

    return {
        "ticker": ticker,
        "peak_price": peak_price,
        "peak_date": peak_date,
        "final_price": final_price,
        "final_date": final_date,
        "decline_percent": decline_pct,
        "trading_days": len(prices)
    }

# Example: Lehman Brothers (if available)
result = analyze_bankruptcy("LEHMQ", "US", "demo")
if result:
    print(f"Peak: ${result['peak_price']:.2f} on {result['peak_date']}")
    print(f"Final: ${result['final_price']:.2f} on {result['final_date']}")
    print(f"Decline: {result['decline_percent']:.1f}%")
```

### Use Case 2: Track Mergers & Acquisitions

**Scenario**: Analyze acquisition premium by comparing pre-acquisition price to acquisition price.

```python
def analyze_acquisition(ticker, exchange, acquisition_date, acquisition_price, api_token):
    """Analyze acquisition premium"""
    manager = DelistedTickerManager(api_token)

    # Get prices around acquisition
    from_date = (pd.to_datetime(acquisition_date) - pd.Timedelta(days=90)).strftime('%Y-%m-%d')
    to_date = acquisition_date

    prices = manager.get_historical_prices(ticker, exchange, from_date, to_date)

    if prices.empty:
        return None

    # Average price 30 days before acquisition
    pre_acquisition = prices.tail(30)
    avg_price_30d = pre_acquisition['close'].mean()

    # Calculate premium
    premium_pct = ((acquisition_price - avg_price_30d) / avg_price_30d) * 100

    return {
        "ticker": ticker,
        "avg_price_30d_before": avg_price_30d,
        "acquisition_price": acquisition_price,
        "premium_percent": premium_pct,
        "acquisition_date": acquisition_date
    }

# Example
result = analyze_acquisition("LNKD", "US", "2016-12-08", 196.00, "demo")
if result:
    print(f"LinkedIn Acquisition Analysis")
    print(f"30-day avg before: ${result['avg_price_30d_before']:.2f}")
    print(f"Acquisition price: ${result['acquisition_price']:.2f}")
    print(f"Premium: {result['premium_percent']:.1f}%")
```

### Use Case 3: Historical Industry Analysis

**Scenario**: Analyze how many companies in a specific industry have delisted.

```python
def analyze_industry_delistings(exchange, industry_keyword, api_token):
    """Analyze delistings in specific industry"""
    manager = DelistedTickerManager(api_token)

    # Get all delisted tickers
    delisted = manager.get_delisted_tickers(exchange)

    # Filter by industry (using name as proxy)
    industry_delistings = delisted[
        delisted['Name'].str.contains(industry_keyword, case=False, na=False)
    ]

    # Group by Type
    by_type = industry_delistings.groupby('Type').size()

    return {
        "total_delistings": len(industry_delistings),
        "by_type": by_type.to_dict(),
        "companies": industry_delistings[['Code', 'Name']].to_dict('records')
    }

# Example: Tech companies
tech_analysis = analyze_industry_delistings("US", "Technology", "demo")
print(f"Total tech delistings: {tech_analysis['total_delistings']}")
print(f"By type: {tech_analysis['by_type']}")
```

### Use Case 4: Validate Ticker Reuse

**Scenario**: Ensure you're using the correct ticker version for your analysis period.

```python
def validate_ticker_for_period(ticker, exchange, start_date, end_date, api_token):
    """Validate ticker version for specific time period"""
    manager = DelistedTickerManager(api_token)

    # Get all versions of ticker
    versions = manager.find_ticker_versions(exchange, ticker)

    results = []
    for _, version in versions.iterrows():
        code = version['Code']

        # Try to get data for this period
        try:
            prices = manager.get_historical_prices(code, exchange, start_date, end_date)

            if not prices.empty:
                results.append({
                    "ticker": code,
                    "name": version['Name'],
                    "has_data": True,
                    "first_date": prices['date'].min().strftime('%Y-%m-%d'),
                    "last_date": prices['date'].max().strftime('%Y-%m-%d'),
                    "records": len(prices)
                })
        except:
            results.append({
                "ticker": code,
                "name": version['Name'],
                "has_data": False
            })

    return results

# Example: Find correct ABC ticker for 2005-2010 period
results = validate_ticker_for_period("ABC", "US", "2005-01-01", "2010-12-31", "demo")
for r in results:
    if r['has_data']:
        print(f"{r['ticker']}: {r['first_date']} to {r['last_date']} ({r['records']} records)")
    else:
        print(f"{r['ticker']}: No data for period")
```

---

## Best Practices

### 1. Always Search by ISIN When Possible

**Most Reliable Method**: ISIN doesn't change when ticker is renamed.

```python
# Good: Search by ISIN
results = manager.search_by_isin("US", "US1234567890")

# Less reliable: Search by old ticker name (might have changed)
results = manager.search_by_name("US", "Old Company Name")
```

### 2. Check for Ticker Versions

**Before Analysis**: Always check if ticker has been reused.

```python
# Check for _old variants before analyzing
versions = manager.find_ticker_versions("US", "ABC")

if len(versions) > 1:
    print("Warning: Ticker has multiple versions")
    print("Make sure you're using the correct one for your time period")
```

### 3. Cache Delisted Lists

**Performance**: Delisted lists are large and change infrequently.

```python
# Cache the delisted list
delisted_df = manager.get_delisted_tickers("US", use_cache=True)

# Subsequent searches use cached data (much faster)
tech = delisted_df[delisted_df['Name'].str.contains("Tech", case=False)]
finance = delisted_df[delisted_df['Name'].str.contains("Financial", case=False)]
```

### 4. Handle Missing Fundamentals Gracefully

**Check Availability**: Not all delisted tickers have fundamentals.

```python
def get_fundamentals_safe(ticker, exchange, api_token):
    """Safely attempt to get fundamentals"""
    manager = DelistedTickerManager(api_token)

    if manager.check_fundamentals_available(ticker, exchange):
        return manager.get_fundamentals(ticker, exchange)
    else:
        print(f"Fundamentals not available for {ticker}.{exchange}")
        print("Likely delisted before 2018")
        return None
```

### 5. Validate Date Ranges

**Check Data Availability**: Ensure your requested date range has data.

```python
def get_prices_with_validation(ticker, exchange, from_date, to_date, api_token):
    """Get prices with date range validation"""
    manager = DelistedTickerManager(api_token)

    # Get all available data first
    all_data = manager.get_historical_prices(ticker, exchange)

    if all_data.empty:
        raise ValueError(f"No price data available for {ticker}.{exchange}")

    # Check if requested range is valid
    first_available = all_data['date'].min()
    last_available = all_data['date'].max()

    requested_from = pd.to_datetime(from_date)
    requested_to = pd.to_datetime(to_date)

    if requested_from < first_available:
        print(f"Warning: Requested from {from_date}, but data starts {first_available.strftime('%Y-%m-%d')}")

    if requested_to > last_available:
        print(f"Warning: Requested to {to_date}, but data ends {last_available.strftime('%Y-%m-%d')}")

    # Return filtered data
    return manager.get_historical_prices(ticker, exchange, from_date, to_date)
```

### 6. Document Ticker Assumptions

**Code Comments**: Always document which ticker version you're using.

```python
# Analyzing LinkedIn before Microsoft acquisition
# Using LNKD.US (delisted 2016-12-08 after Microsoft acquisition)
# Data range: 2011-05-19 (IPO) to 2016-12-08 (delisting)
linkedin_data = manager.get_historical_prices(
    "LNKD", "US",
    from_date="2011-05-19",
    to_date="2016-12-08"
)
```

### 7. Handle Errors Appropriately

**Robust Error Handling**: Delisted tickers may have incomplete data.

```python
def robust_delisted_analysis(ticker, exchange, api_token):
    """Robust analysis with comprehensive error handling"""
    try:
        manager = DelistedTickerManager(api_token)

        # Check if ticker exists
        delisted_df = manager.get_delisted_tickers(exchange)
        if ticker not in delisted_df['Code'].values:
            return {"error": f"Ticker {ticker} not found in delisted list"}

        # Try to get price data
        try:
            prices = manager.get_historical_prices(ticker, exchange)
            if prices.empty:
                return {"error": f"No price data available for {ticker}"}
        except Exception as e:
            return {"error": f"Price data fetch failed: {str(e)}"}

        # Try to get fundamentals (may not be available)
        fundamentals = None
        try:
            if manager.check_fundamentals_available(ticker, exchange):
                fundamentals = manager.get_fundamentals(ticker, exchange, "General")
        except:
            pass  # Fundamentals not available, continue anyway

        return {
            "success": True,
            "price_records": len(prices),
            "date_range": {
                "from": prices['date'].min().strftime('%Y-%m-%d'),
                "to": prices['date'].max().strftime('%Y-%m-%d')
            },
            "has_fundamentals": fundamentals is not None
        }

    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
```

---

## Summary

### Key Takeaways

✅ **Extensive Coverage**: 68,000+ delisted tickers (26,000+ US from ~2000, 42,000+ non-US from ~6-7 years)

⚠️ **DATA AVAILABILITY LIMITATION**: For most tickers delisted **before ~2014**, historical data is **NOT available** (with some exceptions)

✅ **Data Preserved**: Delisted tickers are never removed from system, only marked as delisted

⚠️ **API Access Conditional**: Same APIs work, BUT data only available if ticker delisted after ~2014

✅ **Ticker Reuse Handled**: `_old`, `_old1`, `_old2` suffixes for reused tickers

✅ **ISIN Search**: Most reliable method for finding renamed companies

✅ **Fundamentals Available**: Only for tickers delisted in 2018 or later (individual review required)

✅ **Always Verify**: Check data availability before assuming it exists for a delisted ticker

### Quick Reference

```bash
# Get delisted tickers list
https://eodhd.com/api/exchange-symbol-list/US?api_token=demo&delisted=1

# Try to get EOD data (may return empty if delisted before ~2014)
https://eodhd.com/api/eod/AAAB.US?api_token=demo&fmt=json

# Try to get fundamentals (only if delisted after 2018)
https://eodhd.com/api/fundamentals/AAAB.US?api_token=demo&fmt=json
```

**Important**: Being in the delisted list does NOT guarantee historical data exists. Always verify by attempting to fetch data.

### Common Patterns

| Pattern | Meaning | Example |
|---------|---------|---------|
| `ABC.US` | Current/most recent company using ticker | ABC Corp (2020-present) |
| `ABC_old.US` | First/oldest company (first to get suffix) | Oldest ABC Co (1990-1999) |
| `ABC_old1.US` | Second company | Original ABC LLC (2000-2009) |
| `ABC_old2.US` | Third company | Old ABC Inc (2010-2019) |

### When to Use Delisted Data

✅ **Backtesting strategies** that need complete market history
✅ **Academic research** on corporate failures
✅ **M&A analysis** for acquisition premiums
✅ **Industry studies** tracking sector consolidation
✅ **Risk modeling** including bankrupt companies
✅ **Historical benchmarking** against no-longer-existing companies

---

**Related Documentation**:
- [Exchange Symbol List API](../endpoints/exchange-symbol-list.md)
- [End-of-Day Historical Data](../endpoints/eod-historical-data.md)
- [Fundamentals Data API](../endpoints/fundamentals-data.md)
- [API Authentication & Demo Access](./api-authentication-demo-access.md)

**External Resources**:
- [EODHD Registration](https://eodhd.com/register)
- [Delisted Data Overview](https://eodhd.com/delisted-stock-data)
