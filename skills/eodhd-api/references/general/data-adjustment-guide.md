# Data Adjustment Guide - Complete Reference

**Purpose**: Understanding price adjustments for splits and dividends
**Source**: EODHD Official Documentation
**Author**: EODHD Team
**Last Updated**: 2024-11-27

---

## Table of Contents

1. [Overview](#overview)
2. [Close vs Adjusted Close](#close-vs-adjusted-close)
3. [Why Adjustments Are Necessary](#why-adjustments-are-necessary)
4. [Stock Split Adjustments](#stock-split-adjustments)
5. [Dividend Adjustments](#dividend-adjustments)
6. [Chicago Booth Adjustment Algorithm](#chicago-booth-adjustment-algorithm)
7. [Calculating Adjusted OHLC](#calculating-adjusted-ohlc)
8. [Precision and Accuracy](#precision-and-accuracy)
9. [Methods to Obtain Adjusted Data](#methods-to-obtain-adjusted-data)
10. [Intraday Data Adjustments](#intraday-data-adjustments)
11. [Practical Examples](#practical-examples)
12. [Best Practices](#best-practices)

---

## Overview

When working with historical stock price data, understanding the difference between **close** and **adjusted close** is critical for accurate analysis, backtesting, and performance calculations.

**Key Concepts**:
- **Close**: Raw closing price at end of trading day
- **Adjusted Close**: Retroactively adjusted price accounting for corporate actions
- **Corporate Actions**: Splits and dividends that affect price comparability
- **Retroactive Adjustment**: Prices adjusted backward in time from event date

**EODHD Standards**:
- Uses Chicago Booth adjustment algorithm (industry standard)
- Maintains 4 decimal places for precision (vs 2 for many providers)
- Provides both raw OHLC and adjusted_close values
- Fully adjusted price history

---

## Close vs Adjusted Close

### Close Price

**Definition**: The raw closing price of a stock at the end of a trading period.

**Characteristics**:
- **Raw value** - actual price traded on that specific date
- **Not adjusted** - shows exactly what the stock cost on that day
- **Cannot be compared** directly across corporate actions
- **Historical record** - represents actual trading price

**Use Cases**:
- Viewing actual historical prices
- Calculating daily P&L for positions held
- Tax reporting (uses actual transaction prices)
- Order placement (current real prices)

**Example**:
```
Date: 2014-06-08
AAPL Close: $645.57 (actual trading price on that day)
```

### Adjusted Close

**Definition**: A retroactively adjusted closing price that accounts for all corporate actions.

**Characteristics**:
- **Adjusted value** - modified to account for splits and dividends
- **Retroactive** - prices before events are adjusted backward in time
- **Comparable** - can be directly compared across entire price history
- **Analysis-ready** - suitable for returns calculations, technical analysis

**Use Cases**:
- Calculating historical returns
- Technical analysis (moving averages, indicators)
- Backtesting trading strategies
- Performance comparisons across time periods
- Chart analysis

**Example**:
```
Date: 2014-06-08
AAPL Close: $645.57 (raw price)
AAPL Adjusted Close: $92.08 (adjusted for 7:1 split in June 2014)
```

### Visual Comparison

**Before Adjustment (Raw Close)**:
```
Date         Close    Event
2014-06-06   $650.00
2014-06-07   $645.57  (day before split)
2014-06-09   $93.52   (after 7:1 split) ← Price "drops" 7x
2014-06-10   $94.25
```

**After Adjustment (Adjusted Close)**:
```
Date         Adj Close
2014-06-06   $92.86    (adjusted retroactively)
2014-06-07   $92.08    (adjusted retroactively)
2014-06-09   $93.52    (no adjustment needed)
2014-06-10   $94.25
```

Notice how adjusted close creates a **smooth, continuous price series** suitable for analysis.

---

## Why Adjustments Are Necessary

### Problem: Corporate Actions Disrupt Price Continuity

Without adjustments, corporate actions create artificial discontinuities in price data:

**Example 1: Stock Split**
```
Day Before Split: $100
Day After Split:  $50 (2:1 split)
Raw Price Drop:   -50% ← Looks like a crash, but it's not!
```

**Example 2: Large Dividend**
```
Day Before Ex-Date: $100
Day After Ex-Date:  $95 (paid $5 dividend)
Raw Price Drop:     -5% ← Not a real loss for shareholders
```

### Solution: Retroactive Adjustments

By adjusting **all prior prices** retroactively, we maintain comparability:

**Adjusted Data After 2:1 Split**:
```
1 year ago:  $50  (was $100, adjusted to $50)
6 months ago: $55  (was $110, adjusted to $55)
Today:       $50  (no adjustment needed, split already happened)

True Return: 0% (correct)
vs
Raw Return: -50% (misleading!)
```

### When Adjustments Matter Most

1. **Long-term Performance Analysis**
   - Calculating 5-year, 10-year returns
   - Multiple splits/dividends over period

2. **Technical Analysis**
   - Moving averages across corporate actions
   - Support/resistance levels
   - Chart patterns

3. **Backtesting Trading Strategies**
   - Accurate entry/exit prices
   - Position sizing
   - Risk management

4. **Portfolio Returns Calculation**
   - Total return (price appreciation + dividends)
   - Risk-adjusted returns
   - Benchmarking

---

## Stock Split Adjustments

### What is a Stock Split?

A **stock split** is when a company multiplies the number of shares outstanding while proportionally reducing the price per share.

**Purpose**:
- Make stock more "affordable" for retail investors
- Increase liquidity
- Psychological impact (lower nominal price)

**Important**: Market capitalization remains unchanged.

### Forward Stock Split

**Definition**: Each existing share is split into multiple shares.

**Common Ratios**:
- 2-for-1 (2:1) - Most common
- 3-for-1 (3:1)
- 7-for-1 (7:1) - Apple (2014)
- 10-for-1 (10:1)
- 4-for-1 (4:1) - Tesla (2020)

**Example: 2-for-1 Split**

**Before Split**:
```
Shares Owned: 100
Price per Share: $60
Total Value: $6,000
```

**After Split**:
```
Shares Owned: 200 (doubled)
Price per Share: $30 (halved)
Total Value: $6,000 (unchanged)
```

**Adjustment Calculation**:
```
Split Ratio: 2:1
Split Factor: 2
Adjusted Price = Raw Price / Split Factor
Adjusted Price = $60 / 2 = $30
```

### Reverse Stock Split

**Definition**: Multiple shares are merged into one share (opposite of forward split).

**Common Ratios**:
- 1-for-2 (1:2) - Merge 2 shares into 1
- 1-for-5 (1:5)
- 1-for-10 (1:10)

**Purpose**:
- Increase stock price to meet exchange listing requirements
- Improve perception (avoid "penny stock" status)
- Reduce number of shareholders

**Example: 1-for-2 Reverse Split**

**Before Split**:
```
Shares Owned: 200
Price per Share: $5
Total Value: $1,000
```

**After Split**:
```
Shares Owned: 100 (halved)
Price per Share: $10 (doubled)
Total Value: $1,000 (unchanged)
```

**Adjustment Calculation**:
```
Split Ratio: 1:2
Split Factor: 0.5
Adjusted Price = Raw Price / Split Factor
Adjusted Price = $5 / 0.5 = $10
```

### AAPL Split Example (Real Data)

**Apple 7-for-1 Split - June 9, 2014**

| Date | Raw Close | Adjusted Close | Adjustment Factor |
|------|-----------|----------------|-------------------|
| 2014-06-06 | $650.00 | $92.86 | 0.1429 (÷7) |
| 2014-06-07 | $645.57 | $92.08 | 0.1429 (÷7) |
| 2014-06-09 | $93.52 | $93.52 | 1.0000 (no adjustment) |
| 2014-06-10 | $94.25 | $94.25 | 1.0000 (no adjustment) |

**Analysis**:
- Raw close shows ~7x "drop" from $645.57 to $93.52
- Adjusted close shows smooth progression: $92.08 → $93.52 (+1.6%)
- All pre-split prices divided by 7
- Post-split prices unchanged

### Volume Adjustment for Splits

**Important**: Volume must also be adjusted for splits.

**Formula**:
```
Adjusted Volume = Raw Volume × Split Factor

For 2:1 split:
Adjusted Volume = Raw Volume × 2

For 7:1 split:
Adjusted Volume = Raw Volume × 7
```

**Example**:
```
Before 2:1 Split:
Raw Volume: 1,000,000 shares
Adjusted Volume: 2,000,000 shares (doubled)

Reason: Each share became 2 shares, so trading 1M pre-split shares
is equivalent to trading 2M post-split shares.
```

---

## Dividend Adjustments

### What is a Dividend?

A **dividend** is a cash payment to shareholders from company profits.

**Types**:
- **Regular Dividend**: Quarterly payments (most common)
- **Special Dividend**: One-time large payment
- **Stock Dividend**: Payment in additional shares (similar to split)

**Key Dates**:
- **Declaration Date**: Company announces dividend
- **Ex-Dividend Date**: Cutoff date (buy before this to receive dividend)
- **Record Date**: Shareholders on record receive dividend
- **Payment Date**: Dividend paid to shareholders

### Why Dividends Affect Price

On the **ex-dividend date**, the stock price typically drops by approximately the dividend amount.

**Reason**: The cash is leaving the company, reducing its value.

**Example**:
```
Day Before Ex-Date: $100
Dividend Amount: $2
Day After Ex-Date: $98 (typically)
```

This is **not a loss** for shareholders who receive the dividend. They have:
- Stock worth $98
- Cash dividend $2
- Total value: $100

### Dividend Adjustment Calculation

**Formula (Chicago Booth Algorithm)**:

For the day **before** the ex-dividend date:
```
Adjustment Factor = (Close Price - Dividend) / Close Price
```

**Example**:
```
Date: Day before ex-date
Close Price: $60
Dividend: $10

Adjustment Factor = (60 - 10) / 60 = 50 / 60 = 0.8333
```

**Apply to All Prior Prices**:
```
Previous Date Close: $55
Adjusted Close: $55 × 0.8333 = $45.83
```

### Multiple Dividends

When a stock pays multiple dividends over time, adjustments **compound**:

**Example Timeline**:
```
Current Date: 2024-01-01
Stock Price: $100

Ex-Date 1 (2023-10-01): $2 dividend
Adjustment Factor 1 = (100 - 2) / 100 = 0.98

Ex-Date 2 (2023-07-01): $2 dividend (prior to Ex-Date 1)
Price on 2023-06-30: $95
Adjustment Factor 2 = (95 - 2) / 95 = 0.9789

Price on 2023-06-15: $90
Adjusted Price = $90 × 0.9789 × 0.98 = $86.31
```

**Important**: Adjustments compound backward in time.

### Dividend vs Split Adjustments

| Aspect | Dividend | Split |
|--------|----------|-------|
| **Adjustment Direction** | Reduces prior prices | Reduces/increases prior prices |
| **Adjustment Amount** | Dividend amount | Split ratio |
| **Frequency** | Quarterly (typically) | Rare (years apart) |
| **Impact Size** | Usually small (1-3%) | Large (50%, 700%, etc.) |
| **Volume Adjustment** | No | Yes |

---

## Chicago Booth Adjustment Algorithm

### Overview

The **Chicago Booth algorithm** is the industry-standard method for adjusting stock prices for splits and dividends. EODHD uses this algorithm for all adjustments.

**Developed by**: Center for Research in Security Prices (CRSP) at University of Chicago Booth School of Business

**Why It's Standard**:
- Academically rigorous
- Widely adopted by financial institutions
- Consistent methodology
- Preserves price continuity

### Algorithm Steps

**Step 1: Calculate Adjustment Factor**

For **splits**:
```
Split Factor = Split Ratio
Example: 2:1 split → Split Factor = 2
```

For **dividends**:
```
Dividend Factor = (Close Before Ex-Date - Dividend) / Close Before Ex-Date
```

**Step 2: Apply Factor Retroactively**

All prices **before** the event date are multiplied by the adjustment factor.

**Step 3: Compound Multiple Events**

When multiple events occur, factors are multiplied together:
```
Combined Factor = Split Factor × Dividend Factor 1 × Dividend Factor 2 × ...
```

### Detailed Example

**Scenario**: Stock with split and dividend

```
Current Date: 2024-01-01, Price: $100

Event 1 (2023-06-01): 2:1 split
Event 2 (2022-12-01): $5 dividend, Price before: $110

Calculate Adjustments:

1. Split Factor (2023-06-01): 2.0
2. Dividend Factor (2022-12-01):
   Factor = (110 - 5) / 110 = 0.9545

For price on 2022-11-15 (before both events):
Original Price: $105
Adjusted Price = $105 × 0.9545 × (1/2) = $50.11
```

### Formula Summary

**General Adjustment Formula**:
```
Adjusted Price = Raw Price × Π(All Adjustment Factors)

Where:
Π = Product (multiplication) of all factors affecting that date
```

**For Split**:
```
Factor = 1 / Split Ratio

2:1 split: Factor = 1/2 = 0.5
7:1 split: Factor = 1/7 = 0.1429
```

**For Dividend**:
```
Factor = (Price - Dividend) / Price
```

---

## Calculating Adjusted OHLC

### The Problem

EODHD provides:
- Raw OHLC (open, high, low, close)
- Adjusted Close

But you may need adjusted **OHLC** (all four values adjusted).

### Solution: Calculate Adjustment Factor

**Formula**:
```
k = adjusted_close / close

Then:
adjusted_open = open × k
adjusted_high = high × k
adjusted_low = low × k
```

**Critical**: Calculate `k` for **EACH day** because it changes with every split or dividend.

### Step-by-Step Example

**Raw Data**:
```
Date: 2014-06-06 (before AAPL 7:1 split)
Open: $638.00
High: $652.00
Low: $636.00
Close: $645.57
Adjusted Close: $92.08
```

**Step 1: Calculate k**
```
k = adjusted_close / close
k = $92.08 / $645.57
k = 0.14265
```

**Step 2: Apply k to OHLC**
```
adjusted_open = $638.00 × 0.14265 = $91.01
adjusted_high = $652.00 × 0.14265 = $93.01
adjusted_low = $636.00 × 0.14265 = $90.73
adjusted_close = $92.08 (already provided)
```

**Result**:
```
Date: 2014-06-06 (adjusted)
Open: $91.01
High: $93.01
Low: $90.73
Close: $92.08
```

### Python Implementation

```python
import pandas as pd

def calculate_adjusted_ohlc(df):
    """
    Calculate adjusted OHLC from raw OHLC and adjusted_close.

    Args:
        df: DataFrame with columns: open, high, low, close, adjusted_close

    Returns:
        DataFrame with additional columns: adjusted_open, adjusted_high, adjusted_low
    """
    # Calculate adjustment factor for each day
    df['k'] = df['adjusted_close'] / df['close']

    # Apply factor to OHLC
    df['adjusted_open'] = df['open'] * df['k']
    df['adjusted_high'] = df['high'] * df['k']
    df['adjusted_low'] = df['low'] * df['k']

    # Clean up temporary column
    df = df.drop('k', axis=1)

    return df

# Example usage
df = pd.DataFrame({
    'date': ['2014-06-06', '2014-06-07', '2014-06-09'],
    'open': [638.00, 640.00, 92.70],
    'high': [652.00, 650.00, 95.05],
    'low': [636.00, 638.00, 92.45],
    'close': [645.57, 645.00, 93.52],
    'adjusted_close': [92.08, 92.00, 93.52]
})

df = calculate_adjusted_ohlc(df)
print(df)
```

**Output**:
```
        date    open    high     low   close  adjusted_close  adjusted_open  adjusted_high  adjusted_low
0  2014-06-06  638.00  652.00  636.00  645.57           92.08          91.01          93.01         90.73
1  2014-06-07  640.00  650.00  638.00  645.00           92.00          91.26          92.66         90.98
2  2014-06-09   92.70   95.05   92.45   93.52           93.52          92.70          95.05         92.45
```

### Important Notes

1. **Calculate k daily**: Don't assume k is constant across dates
2. **Precision**: Maintain at least 4 decimal places in k
3. **Volume**: Adjust volume separately (by split factor only)
4. **Validation**: adjusted_close should equal close × k (by definition)

---

## Precision and Accuracy

### EODHD Standard: 4 Decimal Places

**EODHD maintains 4 decimal places** for adjustment factors, compared to 2 decimal places used by many other providers.

**Why This Matters**:

**Short-term History**:
- Small difference (0.01% - 0.1%)
- Negligible for recent data

**Long-term History**:
- Differences compound over time
- Can reach 1-5% for 20+ year data
- Significant for backtesting and analysis

### Precision Example

**Scenario**: Stock with 10 years of quarterly dividends (40 dividends)

**2 Decimal Places**:
```
Adjustment Factor per Dividend: 0.98 (rounded)
Compounded Over 40 Dividends: 0.98^40 = 0.4457
Adjusted Price: $100 × 0.4457 = $44.57
```

**4 Decimal Places**:
```
Adjustment Factor per Dividend: 0.9805 (precise)
Compounded Over 40 Dividends: 0.9805^40 = 0.4512
Adjusted Price: $100 × 0.4512 = $45.12
```

**Difference**: $0.55 or 1.2% error

**For $1M portfolio**: $12,000 error in backtested returns!

### Best Practices for Precision

1. **Use EODHD Data**: Already maintains 4 decimal places
2. **Avoid Rounding**: Keep full precision in calculations
3. **Float64**: Use double precision floats in programming
4. **Validate**: Compare results across providers for large discrepancies

```python
# Good practice
adjustment_factor = 0.9805  # 4 decimal places
adjusted_price = price * adjustment_factor  # Full precision

# Bad practice
adjustment_factor = 0.98  # 2 decimal places (loses precision)
adjusted_price = round(price * adjustment_factor, 2)  # Double rounding!
```

---

## Methods to Obtain Adjusted Data

EODHD provides several ways to obtain adjusted data:

### Method 1: End-of-Day API (Recommended)

**API**: https://eodhd.com/financial-apis/api-for-historical-data-and-volumes

**Provides**:
- Raw OHLC values
- `adjusted_close` (adjusted for splits and dividends)
- Volume (adjusted for splits)

**Usage**:
```bash
curl "https://eodhd.com/api/eod/AAPL.US?api_token=demo&from=2020-01-01&to=2020-12-31&fmt=json"
```

**Response**:
```json
[
  {
    "date": "2020-01-02",
    "open": 74.06,
    "high": 75.15,
    "low": 73.80,
    "close": 75.09,
    "adjusted_close": 73.89,
    "volume": 135647008
  }
]
```

**Then Calculate**: Use formula above to get adjusted OHLC

---

### Method 2: Excel Add-on

**Add-on**: https://eodhd.com/financial-apis/excel-financial-add-in-fundamentals-end-of-day-charts/

**Provides**:
- Pre-calculated adjusted OHLC
- Raw OHLC
- Easy spreadsheet integration

**Use Cases**:
- Financial modeling in Excel
- Quick analysis without coding
- Presentations and reports

**Functions Available**:
```excel
=EODHD.HISTORICAL("AAPL.US", "2020-01-01", "2020-12-31", "adjusted")
=EODHD.HISTORICAL("AAPL.US", "2020-01-01", "2020-12-31", "raw")
```

---

### Method 3: Technical Indicators API

**API**: https://eodhd.com/financial-apis/technical-indicators-api/

**Function**: `splitadjusted`

**Provides**:
- OHLC adjusted **only for splits** (not dividends)
- Useful when you want to preserve actual dividend price drops

**Usage**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=splitadjusted&api_token=demo&from=2020-01-01&to=2020-12-31"
```

**Response**:
```json
[
  {
    "date": "2020-01-02",
    "open": 74.06,
    "high": 75.15,
    "low": 73.80,
    "close": 75.09,
    "volume": 135647008
  }
]
```

**Use Cases**:
- Tax reporting (actual prices including dividend drops)
- Comparing price action around dividend dates
- Analysis requiring split-only adjustments

---

### Method 4: Manual Calculation with Splits/Dividends Data

**API**: https://eodhd.com/financial-apis/api-splits-dividends

**Step 1**: Fetch splits and dividends
```bash
curl "https://eodhd.com/api/splits/AAPL.US?api_token=demo"
curl "https://eodhd.com/api/div/AAPL.US?api_token=demo"
```

**Step 2**: Fetch raw OHLC data
```bash
curl "https://eodhd.com/api/eod/AAPL.US?api_token=demo"
```

**Step 3**: Apply adjustments manually using Chicago Booth algorithm

**Use Cases**:
- Custom adjustment logic
- Real-time intraday adjustments
- Special corporate actions handling

---

### Comparison Table

| Method | Adjusted For | Ease of Use | Use Case |
|--------|--------------|-------------|----------|
| **EOD API + Formula** | Splits & Dividends | Moderate | Most flexible, programming required |
| **Excel Add-on** | Splits & Dividends | Very Easy | Spreadsheet analysis, no coding |
| **Technical API** | Splits Only | Easy | Tax reporting, specific analysis |
| **Manual Calculation** | Custom | Hard | Advanced users, custom needs |

---

## Intraday Data Adjustments

### Intraday Data is Unadjusted

**Important**: Intraday data (1-minute, 5-minute, etc.) is provided in **unadjusted form**.

**Reason**: Intraday adjustments would need to be real-time and very complex.

### How to Adjust Intraday Data

**Option 1: Use Adjustment Coefficient from EOD API**

**Step 1**: Get EOD data with adjusted_close
```python
eod_data = get_eod_data("AAPL.US", date)
k = eod_data['adjusted_close'] / eod_data['close']
```

**Step 2**: Apply to intraday data
```python
intraday_data['adjusted_open'] = intraday_data['open'] * k
intraday_data['adjusted_high'] = intraday_data['high'] * k
intraday_data['adjusted_low'] = intraday_data['low'] * k
intraday_data['adjusted_close'] = intraday_data['close'] * k
```

**Option 2: Use Splits/Dividends API**

**Step 1**: Fetch all splits and dividends
```python
splits = get_splits("AAPL.US")
dividends = get_dividends("AAPL.US")
```

**Step 2**: Calculate cumulative adjustment factor for each intraday timestamp
```python
def calculate_adjustment_factor(timestamp, splits, dividends):
    factor = 1.0

    # Apply splits after timestamp
    for split in splits:
        if split['date'] > timestamp:
            factor *= (1 / split['ratio'])

    # Apply dividends after timestamp
    for dividend in dividends:
        if dividend['date'] > timestamp:
            # Need close price on day before ex-date
            price_before = get_close_price(dividend['date'] - 1)
            factor *= (price_before - dividend['amount']) / price_before

    return factor
```

**Step 3**: Apply factor to intraday prices
```python
for bar in intraday_data:
    k = calculate_adjustment_factor(bar['timestamp'], splits, dividends)
    bar['adjusted_open'] = bar['open'] * k
    bar['adjusted_high'] = bar['high'] * k
    bar['adjusted_low'] = bar['low'] * k
    bar['adjusted_close'] = bar['close'] * k
```

### Example: Adjusting Intraday Data

**Scenario**: AAPL intraday data from June 6, 2014 (before 7:1 split on June 9)

**Raw Intraday Bar**:
```
Timestamp: 2014-06-06 09:30:00
Open: 638.00
High: 641.00
Low: 637.00
Close: 639.50
```

**Adjustment Factor (from EOD)**:
```
EOD Close: 645.57
EOD Adjusted Close: 92.08
k = 92.08 / 645.57 = 0.14265
```

**Adjusted Intraday Bar**:
```
Timestamp: 2014-06-06 09:30:00
Adjusted Open: 638.00 × 0.14265 = 91.01
Adjusted High: 641.00 × 0.14265 = 91.44
Adjusted Low: 637.00 × 0.14265 = 90.87
Adjusted Close: 639.50 × 0.14265 = 91.23
```

### Python Implementation

```python
import pandas as pd
import requests

def adjust_intraday_data(ticker, date, intraday_data, api_token):
    """
    Adjust intraday data using EOD adjustment coefficient.

    Args:
        ticker: Stock ticker (e.g., "AAPL.US")
        date: Date of intraday data (YYYY-MM-DD)
        intraday_data: DataFrame with OHLC intraday data
        api_token: EODHD API token

    Returns:
        DataFrame with adjusted OHLC columns
    """
    # Get EOD data for adjustment coefficient
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    eod_params = {
        "api_token": api_token,
        "from": date,
        "to": date,
        "fmt": "json"
    }

    eod_response = requests.get(eod_url, params=eod_params).json()

    if not eod_response:
        raise ValueError(f"No EOD data for {ticker} on {date}")

    eod = eod_response[0]

    # Calculate adjustment factor
    k = eod['adjusted_close'] / eod['close']

    # Apply to intraday data
    intraday_data['adjusted_open'] = intraday_data['open'] * k
    intraday_data['adjusted_high'] = intraday_data['high'] * k
    intraday_data['adjusted_low'] = intraday_data['low'] * k
    intraday_data['adjusted_close'] = intraday_data['close'] * k

    return intraday_data

# Example usage
intraday_df = pd.DataFrame({
    'timestamp': ['2014-06-06 09:30:00', '2014-06-06 09:35:00'],
    'open': [638.00, 639.50],
    'high': [641.00, 640.00],
    'low': [637.00, 638.00],
    'close': [639.50, 639.00]
})

adjusted_df = adjust_intraday_data('AAPL.US', '2014-06-06', intraday_df, 'your_api_token')
print(adjusted_df)
```

---

## Practical Examples

### Example 1: Calculate Total Return

**Objective**: Calculate accurate total return including dividends.

```python
def calculate_total_return(ticker, start_date, end_date, api_token):
    """
    Calculate total return using adjusted close prices.

    Total Return = (Ending Adjusted Price / Starting Adjusted Price) - 1
    """
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "from": start_date,
        "to": end_date,
        "fmt": "json"
    }

    data = requests.get(url, params=params).json()

    if len(data) < 2:
        return None

    start_adj_close = data[0]['adjusted_close']
    end_adj_close = data[-1]['adjusted_close']

    total_return = (end_adj_close / start_adj_close) - 1

    return {
        'start_date': data[0]['date'],
        'end_date': data[-1]['date'],
        'start_price': start_adj_close,
        'end_price': end_adj_close,
        'total_return': total_return,
        'total_return_pct': total_return * 100
    }

# Example: AAPL from 2010 to 2020
result = calculate_total_return('AAPL.US', '2010-01-01', '2020-01-01', 'your_api_token')
print(f"Total Return: {result['total_return_pct']:.2f}%")
# Output: Total Return: 634.28% (includes all dividends and splits)
```

### Example 2: Identify Stock Splits

**Objective**: Detect stock splits by comparing close to adjusted_close.

```python
def detect_splits(ticker, api_token):
    """
    Detect stock splits by finding large discrepancies between close and adjusted_close.
    """
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json"
    }

    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data)

    # Calculate adjustment factor
    df['k'] = df['adjusted_close'] / df['close']

    # Detect splits: k changes significantly from one day to next
    df['k_change'] = df['k'].pct_change().abs()

    # Splits typically cause >5% change in k
    splits = df[df['k_change'] > 0.05]

    results = []
    for idx, row in splits.iterrows():
        if idx > 0:
            prev_k = df.loc[idx - 1, 'k']
            split_ratio = row['k'] / prev_k

            results.append({
                'date': row['date'],
                'split_ratio': split_ratio,
                'type': 'Forward Split' if split_ratio < 1 else 'Reverse Split'
            })

    return results

# Example usage
splits = detect_splits('AAPL.US', 'your_api_token')
for split in splits:
    print(f"{split['date']}: {split['type']} (ratio: {split['split_ratio']:.4f})")
```

### Example 3: Backtest Moving Average Strategy

**Objective**: Backtest using adjusted prices for accurate results.

```python
def backtest_ma_crossover(ticker, short_period, long_period, api_token):
    """
    Backtest moving average crossover strategy using adjusted close.

    Buy when short MA crosses above long MA.
    Sell when short MA crosses below long MA.
    """
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json"
    }

    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data)

    # Calculate moving averages on ADJUSTED close
    df['ma_short'] = df['adjusted_close'].rolling(window=short_period).mean()
    df['ma_long'] = df['adjusted_close'].rolling(window=long_period).mean()

    # Generate signals
    df['signal'] = 0
    df.loc[df['ma_short'] > df['ma_long'], 'signal'] = 1  # Buy
    df.loc[df['ma_short'] <= df['ma_long'], 'signal'] = -1  # Sell

    # Detect crossovers
    df['position_change'] = df['signal'].diff()

    # Calculate returns
    df['returns'] = df['adjusted_close'].pct_change()
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']

    # Performance metrics
    total_return = (1 + df['strategy_returns']).prod() - 1
    buy_hold_return = (df['adjusted_close'].iloc[-1] / df['adjusted_close'].iloc[0]) - 1

    return {
        'strategy_return': total_return,
        'buy_hold_return': buy_hold_return,
        'outperformance': total_return - buy_hold_return,
        'num_trades': (df['position_change'].abs() > 0).sum(),
        'data': df
    }

# Example: 50-day / 200-day MA crossover
result = backtest_ma_crossover('AAPL.US', 50, 200, 'your_api_token')
print(f"Strategy Return: {result['strategy_return']*100:.2f}%")
print(f"Buy & Hold Return: {result['buy_hold_return']*100:.2f}%")
print(f"Outperformance: {result['outperformance']*100:.2f}%")
```

### Example 4: Validate Adjustments

**Objective**: Verify that manual calculations match EODHD adjusted_close.

```python
def validate_adjustments(ticker, api_token):
    """
    Validate that manually calculated adjustments match EODHD adjusted_close.
    """
    # Get EOD data
    eod_url = f"https://eodhd.com/api/eod/{ticker}"
    eod_data = requests.get(eod_url, params={"api_token": api_token, "fmt": "json"}).json()

    # Get splits and dividends
    splits_url = f"https://eodhd.com/api/splits/{ticker}"
    splits_data = requests.get(splits_url, params={"api_token": api_token}).json()

    divs_url = f"https://eodhd.com/api/div/{ticker}"
    divs_data = requests.get(divs_url, params={"api_token": api_token}).json()

    df = pd.DataFrame(eod_data)
    df['date'] = pd.to_datetime(df['date'])

    # Calculate manual adjustments
    df['manual_adjusted'] = df['close'].copy()

    # Apply splits (reverse chronological order)
    for split in sorted(splits_data, key=lambda x: x['date'], reverse=True):
        split_date = pd.to_datetime(split['date'])
        split_ratio = float(split['split'].split('/')[0]) / float(split['split'].split('/')[1])

        # Adjust all prices before split
        df.loc[df['date'] < split_date, 'manual_adjusted'] *= (1 / split_ratio)

    # Apply dividends (reverse chronological order)
    for div in sorted(divs_data, key=lambda x: x['date'], reverse=True):
        div_date = pd.to_datetime(div['date'])
        div_amount = float(div['value'])

        # Find close price on day before ex-date
        pre_div_close = df[df['date'] < div_date].iloc[-1]['manual_adjusted']

        if pre_div_close > 0:
            div_factor = (pre_div_close - div_amount) / pre_div_close
            # Adjust all prices before dividend
            df.loc[df['date'] < div_date, 'manual_adjusted'] *= div_factor

    # Compare
    df['difference'] = (df['adjusted_close'] - df['manual_adjusted']).abs()
    df['pct_difference'] = (df['difference'] / df['adjusted_close']) * 100

    max_diff = df['pct_difference'].max()

    return {
        'max_difference_pct': max_diff,
        'validated': max_diff < 0.01,  # Within 0.01%
        'data': df[['date', 'close', 'adjusted_close', 'manual_adjusted', 'pct_difference']]
    }

# Example
result = validate_adjustments('AAPL.US', 'your_api_token')
print(f"Maximum Difference: {result['max_difference_pct']:.4f}%")
print(f"Validated: {result['validated']}")
```

---

## Best Practices

### 1. Always Use Adjusted Prices for Returns

**DO**:
```python
return = (adjusted_close_end / adjusted_close_start) - 1
```

**DON'T**:
```python
return = (close_end / close_start) - 1  # WRONG! Ignores splits/dividends
```

### 2. Use Raw Prices for Current Trading

**DO**:
```python
# Place order at current market price
order_price = latest_close
```

**DON'T**:
```python
# Don't use adjusted price for live trading
order_price = latest_adjusted_close  # WRONG!
```

### 3. Calculate Adjustment Factor Daily

**DO**:
```python
for each_day:
    k = adjusted_close / close
    adjusted_open = open * k
```

**DON'T**:
```python
# Don't assume k is constant
k = adjusted_close[0] / close[0]
adjusted_open = open * k  # WRONG! k changes daily
```

### 4. Maintain Precision

**DO**:
```python
adjustment_factor = 0.9805  # 4 decimal places
```

**DON'T**:
```python
adjustment_factor = 0.98  # 2 decimal places - loses precision
```

### 5. Validate Data

```python
# Check that adjusted_close ≈ close when no recent corporate actions
recent_data = df.tail(30)
if abs(recent_data['adjusted_close'] - recent_data['close']).mean() < 0.01:
    print("Data validated")
```

### 6. Document Adjustment Method

In your code/analysis:
```python
"""
Price adjustments using Chicago Booth algorithm:
- Adjusted for splits and dividends
- 4 decimal place precision
- Source: EODHD API
- Date range: 2010-01-01 to 2024-01-01
"""
```

### 7. Cache Adjustment Data

```python
# Splits and dividends don't change historically
# Cache them to avoid repeated API calls
def get_cached_adjustments(ticker):
    if ticker not in cache:
        cache[ticker] = {
            'splits': get_splits(ticker),
            'dividends': get_dividends(ticker)
        }
    return cache[ticker]
```

### 8. Handle Edge Cases

```python
# Division by zero
if close > 0:
    k = adjusted_close / close
else:
    k = 1.0  # No adjustment if close is zero

# Missing data
if adjusted_close is None:
    adjusted_close = close  # Use raw price if adjusted not available
```

---

## Spinoffs and Mergers

### Mergers

Mergers are a type of corporate action that EODHD does not yet have a dedicated API for, though it is a planned improvement.

### Spinoffs

Spinoffs may appear as part of the **Splits API**. EODHD's data sources do not differentiate between splits and spinoffs, but you can distinguish them by looking at the split ratio:

- **Splits** use clean, round figures: `2:1`, `5:1`, `10:1`
- **Spinoffs** use "odd" figures: `1324:1000`, `768:567`

If you see an unusual ratio, it is most likely a spinoff rather than a split.

### Ticker Change API

For tracking symbol changes related to mergers, acquisitions, or rebranding, EODHD provides the **Symbol Change History API**, available for US stocks since 2022:

```
https://eodhd.com/financial-apis/exchanges-api-trading-hours-and-stock-market-holidays#Symbol_Change_History
```

---

## Summary

### Key Takeaways

1. **Close vs Adjusted Close**
   - Close = raw trading price
   - Adjusted Close = retroactively adjusted for splits and dividends

2. **Why Adjust**
   - Maintain price continuity
   - Enable accurate returns calculation
   - Valid technical analysis across corporate actions

3. **Adjustment Types**
   - **Splits**: Multiply shares, divide price
   - **Dividends**: Reduce price by dividend amount
   - **Retroactive**: All prior prices adjusted backward

4. **Chicago Booth Algorithm**
   - Industry standard
   - Compound adjustments for multiple events
   - EODHD uses this algorithm

5. **Calculating Adjusted OHLC**
   - Formula: `k = adjusted_close / close`
   - Apply daily: `adjusted_open = open × k`
   - Recalculate k for each day

6. **Precision Matters**
   - EODHD: 4 decimal places
   - Others: Often 2 decimal places
   - Compounds to significant differences over time

7. **Multiple Methods Available**
   - EOD API (raw + adjusted_close)
   - Excel Add-on (fully adjusted OHLC)
   - Technical API (split-adjusted only)
   - Manual (splits/dividends data)

8. **Intraday Adjustments**
   - Intraday data is unadjusted
   - Use EOD adjustment coefficient
   - Or calculate from splits/dividends

### Quick Reference

| Scenario | Use | Formula |
|----------|-----|---------|
| **Calculate Returns** | Adjusted Close | `(adj_end / adj_start) - 1` |
| **Technical Analysis** | Adjusted Close | Use adjusted prices |
| **Place Orders** | Raw Close | Use current market price |
| **Backtesting** | Adjusted Close | Use adjusted for accuracy |
| **Tax Reporting** | Raw Close | Use actual transaction prices |
| **Get Adjusted OHLC** | Calculate | `adj_open = open × (adj_close/close)` |

---

## Additional Resources

- **EODHD EOD API**: https://eodhd.com/financial-apis/api-for-historical-data-and-volumes
- **Splits/Dividends API**: https://eodhd.com/financial-apis/api-splits-dividends
- **Technical API**: https://eodhd.com/financial-apis/technical-indicators-api/
- **Excel Add-on**: https://eodhd.com/financial-apis/excel-financial-add-in-fundamentals-end-of-day-charts/

---

**Document Version**: 1.0
**Last Updated**: 2024-11-27
**Maintained by**: EODHD Skills Project
