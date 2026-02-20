# Primary Tickers Identification Guide

**Purpose**: Identify primary tickers for accurate fundamental data analysis
**Last Updated**: 2024-11-27
**Key Use Case**: ADRs, preferred stock, multiple listings, and cross-listed companies

---

## Table of Contents

1. [Overview](#overview)
2. [Primary vs Secondary Tickers](#primary-vs-secondary-tickers)
3. [Why Primary Tickers Matter](#why-primary-tickers-matter)
4. [The PrimaryTicker Field](#the-primaryticker-field)
5. [Identifying Primary Tickers](#identifying-primary-tickers)
6. [Using Search API](#using-search-api)
7. [Identification Methods](#identification-methods)
8. [Python Implementation](#python-implementation)
9. [Common Scenarios](#common-scenarios)
10. [Best Practices](#best-practices)

---

## Overview

### The Challenge

Companies can have multiple tickers across different exchanges and markets:
- **ADRs** (American Depositary Receipts) trading in the US
- **Primary listings** on home exchanges
- **Preferred stock** vs common stock
- **Multiple stock series** (Class A, B, C shares)
- **Cross-listings** on multiple international exchanges

**Problem**: Secondary tickers (especially ADRs) may have **inconsistent fundamental data** due to currency conversion, reporting delays, and data processing complexities.

### The Solution

Always use the **primary ticker** for fundamental data analysis:
1. Check `PrimaryTicker` field in Fundamentals API
2. If unavailable, use identification methods (stock type, liquidity, company address)
3. Validate using multiple criteria

---

## Primary vs Secondary Tickers

### What is a Primary Ticker?

The **primary ticker** is the main listing where:
- Company is originally incorporated and headquartered
- Primary trading volume occurs
- Official financial statements are filed
- Most accurate and timely fundamental data available

### What are Secondary Tickers?

**Secondary tickers** include:
- **ADRs/GDRs**: Depositary receipts trading in foreign markets
- **Preferred Stock**: Different share classes with special rights
- **Cross-listings**: Same company listed on multiple exchanges
- **Multiple Series**: Class A, B, C shares with different voting rights

### Examples

#### Example 1: ADR vs Primary Listing
```
Company: Taiwan Semiconductor Manufacturing Company (TSMC)

Primary Ticker:  2330.TW (Taiwan Stock Exchange)
Secondary Ticker: TSM.US (NYSE ADR)

Recommendation: Use 2330.TW for fundamental data
```

#### Example 2: Common vs Preferred Stock
```
Company: Bank of America

Primary Ticker:   BAC.US (Common Stock)
Secondary Tickers: BAC-PB.US, BAC-PC.US, BAC-PE.US (Preferred Stock Series)

Recommendation: Use BAC.US for fundamental data
```

#### Example 3: Multiple Stock Series
```
Company: Alphabet Inc.

Primary Ticker:   GOOGL.US (Class A - voting rights)
Secondary Ticker: GOOG.US (Class C - no voting rights)

Recommendation: Use GOOGL.US (Class A is typically primary)
```

---

## Why Primary Tickers Matter

### Data Quality Issues with Secondary Tickers

#### 1. Currency Conversion Inaccuracies

**Problem**: ADRs trade in USD but fundamentals reported in home currency.

**Impact**:
- Exchange rate fluctuations create discrepancies
- Conversion timing differences
- Rounding errors accumulate over time

**Example**:
```
TSMC Primary (2330.TW):
  Revenue = 2,160,000 million TWD
  Net Income = 768,000 million TWD

TSM ADR (TSM.US):
  Revenue = $72,000 million USD (converted at 30 TWD/USD)
  Net Income = $25,600 million USD

Issue: Exchange rate changes daily, creating inconsistencies in ratios
```

#### 2. Reporting Delays

**Problem**: Secondary tickers may have delayed financial updates.

**Impact**:
- ADR data may lag primary listing by days or weeks
- Cross-listings may not update simultaneously
- Earnings dates may differ

#### 3. Data Processing Complexities

**Problem**: Additional processing required for secondary tickers.

**Impact**:
- More opportunities for errors
- Reconciliation challenges
- Incomplete data fields

#### 4. Ratio Calculation Inconsistencies

**Problem**: Financial ratios may be calculated differently.

**Example**:
```python
# Primary Ticker (accurate)
PE_Ratio = Price(TWD) / EPS(TWD) = 420 / 28 = 15.0

# ADR (potential inconsistency)
PE_Ratio = Price(USD) / EPS(USD, converted) = 140 / 9.5 = 14.7
# Discrepancy due to different conversion rates for price vs earnings
```

### Recommendation

✅ **Always use primary ticker** for:
- Fundamental analysis
- Financial ratio calculations
- Valuation models
- Historical financial trends
- Earnings analysis

✅ **Use secondary tickers** for:
- Price data (if trading that market)
- Technical analysis (chart patterns)
- Market-specific volume analysis

---

## The PrimaryTicker Field

### Fundamentals API - PrimaryTicker Field

EODHD provides a `PrimaryTicker` field in the Fundamentals Data API that specifies the primary ticker for secondary listings.

### Accessing PrimaryTicker

**Endpoint**:
```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={YOUR_API_KEY}
```

**Location in Response**:
```json
{
  "General": {
    "Code": "TSM",
    "Type": "Common Stock",
    "Name": "Taiwan Semiconductor Manufacturing Company Ltd",
    "Exchange": "US",
    "PrimaryTicker": "2330.TW",
    ...
  }
}
```

### Using PrimaryTicker Field

```bash
# Check ADR's primary ticker
curl "https://eodhd.com/api/fundamentals/TSM.US?api_token=demo&filter=General::PrimaryTicker"

# Response
{
  "PrimaryTicker": "2330.TW"
}
```

### Field States

The `PrimaryTicker` field can have three states:

#### 1. Points to Primary Ticker (Ideal)
```json
{
  "Code": "TSM",
  "PrimaryTicker": "2330.TW"  // ✅ Use 2330.TW for fundamentals
}
```

#### 2. Empty/Null (Manual Identification Needed)
```json
{
  "Code": "XYZ",
  "PrimaryTicker": null  // ⚠️ Need to identify primary manually
}
```

#### 3. Points to Itself (Already Primary)
```json
{
  "Code": "AAPL",
  "PrimaryTicker": "AAPL.US"  // ✅ Already primary ticker
}
```

### When PrimaryTicker is Unavailable

If `PrimaryTicker` field is empty or points to itself, use these methods:
1. Search for other tickers using Search API
2. Apply identification criteria (stock type, liquidity, address, series)
3. Validate findings with multiple criteria

---

## Using Search API

### Search API Overview

**Purpose**: Find all tickers associated with a company

**Endpoint**:
```
https://eodhd.com/api/search/{QUERY}?api_token={YOUR_API_KEY}
```

**Documentation**: https://eodhd.com/financial-apis/search-api-for-stocks-etfs-mutual-funds

### Finding Company Tickers

```bash
# Search for TSMC
curl "https://eodhd.com/api/search/Taiwan%20Semiconductor?api_token=demo"

# Response
[
  {
    "Code": "2330.TW",
    "Exchange": "TW",
    "Name": "Taiwan Semiconductor Manufacturing Co Ltd",
    "Type": "Common Stock",
    "Country": "Taiwan",
    "Currency": "TWD",
    "ISIN": "US8740391003"
  },
  {
    "Code": "TSM.US",
    "Exchange": "US",
    "Name": "Taiwan Semiconductor Manufacturing Company Ltd",
    "Type": "Common Stock",
    "Country": "USA",
    "Currency": "USD",
    "ISIN": "US8740391003"
  }
]
```

### Key Fields for Identification

| Field | Usage |
|-------|-------|
| `Code` | Ticker symbol |
| `Exchange` | Exchange code |
| `Type` | "Common Stock" vs "Preferred Stock" |
| `Country` | Country of exchange |
| `Currency` | Trading currency |
| `ISIN` | International identifier (same for all tickers) |

**Note**: Same `ISIN` indicates same underlying company.

---

## Identification Methods

When `PrimaryTicker` field is unavailable, use these criteria to identify the primary ticker:

### Method 1: Preferred vs Common Stock

**Rule**: When both preferred and common stock exist, **common stock is typically primary**.

**Why**: Common stock represents the main equity of the company; preferred stock has special rights but is secondary.

**Example**:
```
Company: Bank of America

BAC.US          → Type: "Common Stock"     ✅ Primary
BAC-PB.US       → Type: "Preferred Stock"  ❌ Secondary
BAC-PC.US       → Type: "Preferred Stock"  ❌ Secondary
```

**How to Check**:
```python
def is_common_stock(ticker_data):
    """Check if ticker is common stock"""
    type_field = ticker_data.get('Type', '').lower()
    return 'common' in type_field and 'preferred' not in type_field
```

### Method 2: Multiple Stock Series

**Rule**: With multiple stock series (Class A, B, C), the primary ticker is typically the **earliest issued and most actively traded**.

**Indicators**:
- Earliest IPO date
- Highest trading volume
- Most common voting rights structure

**Example**:
```
Company: Alphabet Inc.

GOOGL.US → Class A (1 vote per share)      ✅ Primary (earlier, higher volume)
GOOG.US  → Class C (no voting rights)      ❌ Secondary (issued later)
```

**How to Check**:
```python
def get_ipo_date(ticker, exchange, api_token):
    """Get IPO date from fundamentals"""
    url = f"https://eodhd.com/api/fundamentals/{ticker}.{exchange}"
    params = {"api_token": api_token, "filter": "General::IPODate"}
    response = requests.get(url, params=params)
    return response.json().get("IPODate")

# Compare
googl_ipo = get_ipo_date("GOOGL", "US", api_token)  # Earlier
goog_ipo = get_ipo_date("GOOG", "US", api_token)    # Later
```

### Method 3: Company Address

**Rule**: The company's registered address usually aligns with the **country where the primary ticker is traded**.

**Why**: Companies are incorporated in specific countries, and their primary listing is typically on that country's main exchange.

**Example**:
```
Company: Taiwan Semiconductor Manufacturing Company

Registered Address: Hsinchu, Taiwan

2330.TW (Taiwan Stock Exchange) → ✅ Primary (matches address)
TSM.US (NYSE ADR)               → ❌ Secondary (ADR in foreign market)
```

**How to Check**:
```python
def check_address_match(ticker, exchange, api_token):
    """Check if ticker exchange matches company address"""
    url = f"https://eodhd.com/api/fundamentals/{ticker}.{exchange}"
    params = {"api_token": api_token, "filter": "General"}
    data = requests.get(url, params=params).json()

    address_country = data.get('AddressData', {}).get('Country', '')
    exchange_country = data.get('CountryName', '')

    return address_country.lower() == exchange_country.lower()

# Usage
tsmc_tw_match = check_address_match("2330", "TW", api_token)  # True ✅
tsm_us_match = check_address_match("TSM", "US", api_token)    # False ❌
```

### Method 4: Liquidity (Trading Volume)

**Rule**: The primary ticker often has the **highest liquidity**, indicated by greatest trading volume.

**Why**: Primary listings attract most trading activity; secondary listings typically have lower volume.

**Example**:
```
Company: Alibaba Group

9988.HK (Hong Kong Stock Exchange)
  Average Daily Volume: 50 million shares    ✅ Primary (higher liquidity)

BABA.US (NYSE ADR)
  Average Daily Volume: 15 million shares    ⚠️ High liquidity but still ADR
```

**How to Check**:
```python
def get_average_volume(ticker, exchange, api_token, days=30):
    """Calculate average daily volume"""
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')

    url = f"https://eodhd.com/api/eod/{ticker}.{exchange}"
    params = {
        "api_token": api_token,
        "from": from_date,
        "to": to_date,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    volumes = [d['volume'] for d in data if 'volume' in d]
    return sum(volumes) / len(volumes) if volumes else 0

# Compare
baba_us_vol = get_average_volume("BABA", "US", api_token)
alibaba_hk_vol = get_average_volume("9988", "HK", api_token)
```

### Priority Order

When multiple criteria conflict, use this priority:

1. **Company Address** (highest priority) - Most reliable indicator
2. **Stock Type** (common vs preferred) - Clear distinction
3. **Liquidity** (trading volume) - Strong indicator
4. **Stock Series** (earliest issued) - For class shares

---

## Python Implementation

### Complete Primary Ticker Identifier

```python
import requests
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class PrimaryTickerIdentifier:
    """Identify primary tickers for companies with multiple listings"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://eodhd.com/api"

    def get_primary_ticker_from_api(self, ticker: str, exchange: str) -> Optional[str]:
        """
        Get primary ticker from PrimaryTicker field in Fundamentals API.

        Args:
            ticker: Ticker code
            exchange: Exchange code

        Returns:
            Primary ticker if available, None otherwise
        """
        url = f"{self.base_url}/fundamentals/{ticker}.{exchange}"
        params = {
            "api_token": self.api_token,
            "filter": "General::PrimaryTicker"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            primary = data.get("PrimaryTicker")

            # Check if valid (not empty and not pointing to itself)
            if primary and primary != f"{ticker}.{exchange}":
                return primary

            return None

        except Exception as e:
            print(f"Error fetching PrimaryTicker: {e}")
            return None

    def search_company_tickers(self, company_name: str) -> List[Dict]:
        """
        Search for all tickers of a company.

        Args:
            company_name: Company name to search

        Returns:
            List of ticker dictionaries
        """
        url = f"{self.base_url}/search/{company_name}"
        params = {"api_token": self.api_token}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error searching tickers: {e}")
            return []

    def get_fundamentals(self, ticker: str, exchange: str,
                        filter_path: Optional[str] = "General") -> Dict:
        """Get fundamental data for ticker"""
        url = f"{self.base_url}/fundamentals/{ticker}.{exchange}"
        params = {
            "api_token": self.api_token,
            "filter": filter_path
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def is_common_stock(self, ticker: str, exchange: str) -> bool:
        """Check if ticker is common stock (not preferred)"""
        data = self.get_fundamentals(ticker, exchange)
        stock_type = data.get('Type', '').lower()

        return (
            'common' in stock_type and
            'preferred' not in stock_type and
            'pref' not in stock_type
        )

    def check_address_match(self, ticker: str, exchange: str) -> bool:
        """Check if ticker exchange matches company address country"""
        data = self.get_fundamentals(ticker, exchange)

        # Get address country
        address_data = data.get('AddressData', {})
        address_country = address_data.get('Country', '').lower()

        # Get exchange country
        exchange_country = data.get('CountryName', '').lower()
        country_iso = data.get('CountryISO', '').lower()

        # Match
        return (
            address_country == exchange_country or
            address_country == country_iso
        )

    def get_average_volume(self, ticker: str, exchange: str, days: int = 30) -> float:
        """Calculate average daily trading volume"""
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        to_date = datetime.now().strftime('%Y-%m-%d')

        url = f"{self.base_url}/eod/{ticker}.{exchange}"
        params = {
            "api_token": self.api_token,
            "from": from_date,
            "to": to_date,
            "fmt": "json"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            volumes = [d['volume'] for d in data if 'volume' in d]
            return sum(volumes) / len(volumes) if volumes else 0
        except:
            return 0

    def get_ipo_date(self, ticker: str, exchange: str) -> Optional[str]:
        """Get IPO date from fundamentals"""
        data = self.get_fundamentals(ticker, exchange)
        return data.get('IPODate')

    def identify_primary_ticker(self, ticker: str, exchange: str) -> Dict:
        """
        Identify primary ticker using multiple methods.

        Args:
            ticker: Ticker code
            exchange: Exchange code

        Returns:
            Dictionary with primary ticker identification results
        """
        result = {
            "input_ticker": f"{ticker}.{exchange}",
            "primary_ticker": None,
            "method": None,
            "confidence": "low",
            "analysis": {}
        }

        # Method 1: Check PrimaryTicker field
        primary_from_api = self.get_primary_ticker_from_api(ticker, exchange)

        if primary_from_api:
            result["primary_ticker"] = primary_from_api
            result["method"] = "PrimaryTicker API field"
            result["confidence"] = "high"
            return result

        # If PrimaryTicker not available, analyze
        fundamentals = self.get_fundamentals(ticker, exchange)

        # Check if already primary (points to itself or no PrimaryTicker)
        api_primary = fundamentals.get('PrimaryTicker')
        if not api_primary or api_primary == f"{ticker}.{exchange}":
            # This might be the primary ticker
            result["analysis"]["is_common_stock"] = self.is_common_stock(ticker, exchange)
            result["analysis"]["address_match"] = self.check_address_match(ticker, exchange)
            result["analysis"]["average_volume"] = self.get_average_volume(ticker, exchange)

            # If all criteria suggest it's primary
            if (result["analysis"]["is_common_stock"] and
                result["analysis"]["address_match"] and
                result["analysis"]["average_volume"] > 0):

                result["primary_ticker"] = f"{ticker}.{exchange}"
                result["method"] = "Multi-criteria analysis (self)"
                result["confidence"] = "medium"
            else:
                result["primary_ticker"] = f"{ticker}.{exchange}"
                result["method"] = "Assumed (no PrimaryTicker field)"
                result["confidence"] = "low"

        return result

    def compare_tickers(self, tickers: List[tuple]) -> pd.DataFrame:
        """
        Compare multiple tickers to identify primary.

        Args:
            tickers: List of (ticker, exchange) tuples

        Returns:
            DataFrame with comparison results
        """
        results = []

        for ticker, exchange in tickers:
            symbol = f"{ticker}.{exchange}"

            data = {
                "ticker": symbol,
                "is_common_stock": self.is_common_stock(ticker, exchange),
                "address_match": self.check_address_match(ticker, exchange),
                "avg_volume_30d": self.get_average_volume(ticker, exchange),
                "ipo_date": self.get_ipo_date(ticker, exchange)
            }

            # Get Type and Country
            fundamentals = self.get_fundamentals(ticker, exchange)
            data["type"] = fundamentals.get("Type", "")
            data["country"] = fundamentals.get("CountryName", "")
            data["address_country"] = fundamentals.get("AddressData", {}).get("Country", "")

            results.append(data)

        df = pd.DataFrame(results)

        # Add primary score
        df['primary_score'] = 0
        df.loc[df['is_common_stock'], 'primary_score'] += 3
        df.loc[df['address_match'], 'primary_score'] += 5  # Highest weight

        # Normalize volume score (0-2 points)
        if df['avg_volume_30d'].max() > 0:
            df['volume_score'] = (df['avg_volume_30d'] / df['avg_volume_30d'].max()) * 2
            df['primary_score'] += df['volume_score']

        # Sort by primary score
        df = df.sort_values('primary_score', ascending=False)

        return df


# Usage Examples
def main():
    api_token = "demo"  # Replace with your token
    identifier = PrimaryTickerIdentifier(api_token)

    # Example 1: Check if TSM ADR has primary ticker
    print("=" * 70)
    print("Example 1: TSM ADR - Check PrimaryTicker Field")
    print("=" * 70)

    result = identifier.identify_primary_ticker("TSM", "US")
    print(f"Input ticker: {result['input_ticker']}")
    print(f"Primary ticker: {result['primary_ticker']}")
    print(f"Method: {result['method']}")
    print(f"Confidence: {result['confidence']}")

    # Example 2: Compare multiple tickers for same company
    print("\n" + "=" * 70)
    print("Example 2: Compare TSMC Tickers")
    print("=" * 70)

    # Note: For demo purposes, this might not return all data
    tickers_to_compare = [
        ("TSM", "US"),      # ADR
        ("2330", "TW"),     # Primary listing (if demo supports)
    ]

    comparison = identifier.compare_tickers(tickers_to_compare)
    print("\nComparison Results:")
    print(comparison[['ticker', 'is_common_stock', 'address_match',
                     'avg_volume_30d', 'primary_score']].to_string())

    print("\nRecommended Primary:", comparison.iloc[0]['ticker'])

    # Example 3: Search for company tickers
    print("\n" + "=" * 70)
    print("Example 3: Search for Company Tickers")
    print("=" * 70)

    search_results = identifier.search_company_tickers("Taiwan Semiconductor")
    print(f"Found {len(search_results)} tickers")

    for result in search_results[:3]:  # Show first 3
        print(f"  {result['Code']}.{result['Exchange']} - {result['Name']} ({result['Country']})")


if __name__ == "__main__":
    main()
```

### Output Example

```
======================================================================
Example 1: TSM ADR - Check PrimaryTicker Field
======================================================================
Input ticker: TSM.US
Primary ticker: 2330.TW
Method: PrimaryTicker API field
Confidence: high

======================================================================
Example 2: Compare TSMC Tickers
======================================================================

Comparison Results:
      ticker  is_common_stock  address_match  avg_volume_30d  primary_score
0   2330.TW             True           True      50000000.0           10.0
1    TSM.US             True          False      15000000.0            3.6

Recommended Primary: 2330.TW

======================================================================
Example 3: Search for Company Tickers
======================================================================
Found 2 tickers
  2330.TW - Taiwan Semiconductor Manufacturing Co Ltd (Taiwan)
  TSM.US - Taiwan Semiconductor Manufacturing Company Ltd (USA)
```

---

## Common Scenarios

### Scenario 1: ADR with PrimaryTicker Field

**Situation**: U.S. ADR has `PrimaryTicker` field pointing to home exchange.

**Example**: Toyota Motor Corporation
```python
identifier = PrimaryTickerIdentifier(api_token)

# Check ADR
result = identifier.identify_primary_ticker("BABA", "US")
print(result)

# Output:
{
  "input_ticker": "BABA.US",
  "primary_ticker": "9988.HK",  # Hong Kong Stock Exchange
  "method": "PrimaryTicker API field",
  "confidence": "high"
}

# Recommendation: Use 9988.HK for fundamentals
```

### Scenario 2: ADR without PrimaryTicker Field

**Situation**: `PrimaryTicker` field is empty; need manual identification.

**Example**: Hypothetical ADR
```python
# Search for company
results = identifier.search_company_tickers("Company Name")

# Compare all tickers
tickers = [(r['Code'], r['Exchange']) for r in results]
comparison = identifier.compare_tickers(tickers)

# Highest primary_score is the primary ticker
primary = comparison.iloc[0]['ticker']
print(f"Primary ticker: {primary}")
```

### Scenario 3: Common vs Preferred Stock

**Situation**: Bank with multiple preferred stock series.

**Example**: Bank of America
```python
tickers = [
    ("BAC", "US"),      # Common stock
    ("BAC-PB", "US"),   # Preferred Series B
    ("BAC-PC", "US"),   # Preferred Series C
]

comparison = identifier.compare_tickers(tickers)

# Output will show BAC.US as primary (common stock scores higher)
```

### Scenario 4: Multiple Stock Classes

**Situation**: Company with Class A and Class C shares.

**Example**: Alphabet Inc.
```python
tickers = [
    ("GOOGL", "US"),  # Class A (voting)
    ("GOOG", "US"),   # Class C (non-voting)
]

comparison = identifier.compare_tickers(tickers)

# Check IPO dates and volume
for ticker, exchange in tickers:
    ipo = identifier.get_ipo_date(ticker, exchange)
    vol = identifier.get_average_volume(ticker, exchange)
    print(f"{ticker}.{exchange}: IPO={ipo}, Volume={vol:,.0f}")

# GOOGL.US typically has earlier IPO and higher volume → Primary
```

### Scenario 5: Cross-Listed European Stock

**Situation**: European company listed on home exchange and XETRA.

**Example**: Siemens AG
```python
tickers = [
    ("SIE", "XETRA"),   # XETRA (German electronic exchange)
    ("SIE", "F"),       # Frankfurt Stock Exchange
]

# Check which matches company address
for ticker, exchange in tickers:
    match = identifier.check_address_match(ticker, exchange)
    vol = identifier.get_average_volume(ticker, exchange)
    print(f"{ticker}.{exchange}: Address match={match}, Volume={vol:,.0f}")

# Primary is typically Frankfurt for German companies
```

---

## Best Practices

### 1. Always Check PrimaryTicker Field First

**Priority**: The `PrimaryTicker` field is the most reliable source.

```python
def get_primary_for_analysis(ticker, exchange, api_token):
    """Get primary ticker for fundamental analysis"""
    identifier = PrimaryTickerIdentifier(api_token)

    # First: Check API field
    result = identifier.identify_primary_ticker(ticker, exchange)

    if result['confidence'] == 'high':
        return result['primary_ticker']

    # Second: Manual identification if needed
    print(f"Warning: PrimaryTicker not available for {ticker}.{exchange}")
    print("Using multi-criteria analysis...")

    return result['primary_ticker']

# Usage
primary = get_primary_for_analysis("TSM", "US", api_token)
print(f"Use {primary} for fundamental analysis")
```

### 2. Use ISIN to Group Tickers

**Method**: Same ISIN = Same company.

```python
def group_tickers_by_isin(search_results):
    """Group search results by ISIN"""
    from collections import defaultdict

    groups = defaultdict(list)

    for result in search_results:
        isin = result.get('ISIN')
        if isin:
            groups[isin].append(result)

    return dict(groups)

# Usage
results = identifier.search_company_tickers("Taiwan Semiconductor")
groups = group_tickers_by_isin(results)

for isin, tickers in groups.items():
    print(f"\nISIN {isin}:")
    for t in tickers:
        print(f"  {t['Code']}.{t['Exchange']} - {t['Country']}")
```

### 3. Validate with Multiple Criteria

**Best Practice**: Don't rely on single criterion; use multiple indicators.

```python
def validate_primary_ticker(ticker, exchange, api_token):
    """Validate ticker as primary using multiple criteria"""
    identifier = PrimaryTickerIdentifier(api_token)

    # Check all criteria
    is_common = identifier.is_common_stock(ticker, exchange)
    address_match = identifier.check_address_match(ticker, exchange)
    volume = identifier.get_average_volume(ticker, exchange)

    # Score
    score = 0
    reasons = []

    if is_common:
        score += 3
        reasons.append("✅ Common stock")
    else:
        reasons.append("❌ Preferred stock")

    if address_match:
        score += 5
        reasons.append("✅ Address matches exchange country")
    else:
        reasons.append("⚠️ Address doesn't match exchange")

    if volume > 1000000:  # Arbitrary threshold
        score += 2
        reasons.append(f"✅ High volume ({volume:,.0f})")
    else:
        reasons.append(f"⚠️ Low volume ({volume:,.0f})")

    print(f"\nValidation for {ticker}.{exchange}:")
    print(f"Score: {score}/10")
    for reason in reasons:
        print(f"  {reason}")

    if score >= 7:
        print("✅ Likely primary ticker")
        return True
    else:
        print("⚠️ Likely secondary ticker")
        return False

# Usage
validate_primary_ticker("2330", "TW", api_token)  # TSMC primary
validate_primary_ticker("TSM", "US", api_token)   # TSMC ADR
```

### 4. Document Primary Ticker Decisions

**Best Practice**: Always document which ticker you're using and why.

```python
# Good: Documented ticker selection
"""
Analysis of Taiwan Semiconductor Manufacturing Company

Primary Ticker Used: 2330.TW (Taiwan Stock Exchange)
Reason:
  - PrimaryTicker field in TSM.US points to 2330.TW
  - Company headquartered in Taiwan (address match)
  - Highest liquidity (50M avg daily volume vs 15M for TSM.US)
  - Original listing (IPO 1994 vs ADR 1997)

Secondary Tickers:
  - TSM.US (NYSE ADR) - Not used due to currency conversion issues

Data Retrieved: 2024-11-27
"""

primary_ticker = "2330.TW"
fundamentals = get_fundamentals(primary_ticker, api_token)
```

### 5. Cache Primary Ticker Lookups

**Performance**: Avoid repeated API calls for same ticker.

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_primary_ticker(ticker, exchange, api_token):
    """Get primary ticker with caching"""
    identifier = PrimaryTickerIdentifier(api_token)
    result = identifier.identify_primary_ticker(ticker, exchange)
    return result['primary_ticker']

# Usage - subsequent calls use cache
primary1 = get_cached_primary_ticker("TSM", "US", api_token)  # API call
primary2 = get_cached_primary_ticker("TSM", "US", api_token)  # From cache
```

### 6. Handle Edge Cases

**Be Prepared**: Some tickers may not have clear primaries.

```python
def get_primary_with_fallback(ticker, exchange, api_token):
    """Get primary ticker with fallback to input"""
    try:
        identifier = PrimaryTickerIdentifier(api_token)
        result = identifier.identify_primary_ticker(ticker, exchange)

        if result['confidence'] == 'high':
            return result['primary_ticker']
        elif result['confidence'] == 'medium':
            print(f"Warning: Medium confidence for {ticker}.{exchange}")
            return result['primary_ticker']
        else:
            print(f"Warning: Low confidence, using input ticker {ticker}.{exchange}")
            return f"{ticker}.{exchange}"

    except Exception as e:
        print(f"Error identifying primary: {e}")
        print(f"Falling back to input ticker: {ticker}.{exchange}")
        return f"{ticker}.{exchange}"
```

### 7. Compare Financial Data Quality

**Validation**: Compare key ratios between primary and secondary.

```python
def compare_fundamental_quality(primary_ticker, secondary_ticker, api_token):
    """Compare fundamental data quality between tickers"""

    def get_key_metrics(ticker_full):
        ticker, exchange = ticker_full.split('.')
        fundamentals = get_fundamentals(ticker, exchange, api_token)

        return {
            "revenue": fundamentals.get("Financials", {}).get("Income_Statement", {}).get("yearly", {}).get("2023-12-31", {}).get("totalRevenue"),
            "net_income": fundamentals.get("Financials", {}).get("Income_Statement", {}).get("yearly", {}).get("2023-12-31", {}).get("netIncome"),
            "total_assets": fundamentals.get("Financials", {}).get("Balance_Sheet", {}).get("yearly", {}).get("2023-12-31", {}).get("totalAssets")
        }

    primary_metrics = get_key_metrics(primary_ticker)
    secondary_metrics = get_key_metrics(secondary_ticker)

    print(f"\nPrimary ({primary_ticker}):")
    print(f"  Revenue: {primary_metrics.get('revenue'):,}")
    print(f"  Net Income: {primary_metrics.get('net_income'):,}")

    print(f"\nSecondary ({secondary_ticker}):")
    print(f"  Revenue: {secondary_metrics.get('revenue'):,}")
    print(f"  Net Income: {secondary_metrics.get('net_income'):,}")

    # Check for discrepancies
    if primary_metrics.get('revenue') and secondary_metrics.get('revenue'):
        diff_pct = abs(primary_metrics['revenue'] - secondary_metrics['revenue']) / primary_metrics['revenue'] * 100
        if diff_pct > 5:
            print(f"\n⚠️ Warning: {diff_pct:.1f}% discrepancy in revenue")
            print("   Recommend using primary ticker for analysis")

# Usage
compare_fundamental_quality("2330.TW", "TSM.US", api_token)
```

---

## Summary

### Key Takeaways

✅ **Always use primary ticker** for fundamental analysis to avoid data inconsistencies

✅ **Check `PrimaryTicker` field** first - most reliable source

✅ **Use Search API** to find all tickers for a company when PrimaryTicker unavailable

✅ **Apply multiple criteria** to identify primary:
   1. Company address match (highest priority)
   2. Common vs preferred stock
   3. Trading volume (liquidity)
   4. IPO date (earliest issued)

✅ **ADRs are secondary** - always use home exchange for fundamentals

### Quick Decision Tree

```
Is PrimaryTicker field available?
├─ Yes → Use that ticker ✅
└─ No
   ├─ Is ticker preferred stock?
   │  └─ Yes → Find common stock version ✅
   └─ Does company address match exchange country?
      ├─ Yes → Likely primary ✅
      └─ No
         └─ Compare liquidity with other tickers
            ├─ Highest volume → Likely primary ✅
            └─ Lower volume → Likely secondary, find higher volume ticker
```

### API Endpoints Reference

```bash
# Get PrimaryTicker field
https://eodhd.com/api/fundamentals/{TICKER}?api_token={TOKEN}&filter=General::PrimaryTicker

# Search for company tickers
https://eodhd.com/api/search/{COMPANY_NAME}?api_token={TOKEN}

# Get fundamentals
https://eodhd.com/api/fundamentals/{TICKER}?api_token={TOKEN}

# Get historical prices (for volume analysis)
https://eodhd.com/api/eod/{TICKER}?api_token={TOKEN}&from={DATE}&to={DATE}
```

### Common Patterns

| Scenario | Primary Ticker | Secondary Ticker |
|----------|---------------|------------------|
| **ADR** | Home exchange (e.g., 2330.TW) | US ADR (e.g., TSM.US) |
| **Preferred Stock** | Common stock (e.g., BAC.US) | Preferred series (e.g., BAC-PB.US) |
| **Multiple Classes** | Class A (e.g., GOOGL.US) | Class C (e.g., GOOG.US) |
| **Cross-listing** | Home exchange | Foreign exchange |

---

**Related Documentation**:
- [Search API Documentation](../endpoints/search-api.md)
- [Fundamentals Data API](../endpoints/fundamentals-data.md)
- [End-of-Day Historical Data](../endpoints/eod-historical-data.md)
- [Exchange Symbol List API](../endpoints/exchange-symbol-list.md)

**External Resources**:
- [EODHD Search API](https://eodhd.com/financial-apis/search-api-for-stocks-etfs-mutual-funds)
- [Understanding ADRs](https://www.investopedia.com/terms/a/adr.asp)
- [Stock Classes Explained](https://www.investopedia.com/terms/c/classashares.asp)
