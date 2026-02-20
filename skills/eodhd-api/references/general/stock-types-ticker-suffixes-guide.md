# Stock Types and Ticker Suffixes Guide

**Purpose**: Understand different stock types and ticker symbol conventions across global exchanges
**Last Updated**: 2024-11-27
**Coverage**: Common stock types, preferred stocks, depositary receipts, and exchange-specific suffixes

---

## Table of Contents

1. [Overview](#overview)
2. [Common Stock Types](#common-stock-types)
3. [US Stock Suffixes](#us-stock-suffixes)
4. [Depositary Receipts](#depositary-receipts)
5. [Thailand -R Stocks (NVDR)](#thailand--r-stocks-nvdr)
6. [Other Exchange-Specific Conventions](#other-exchange-specific-conventions)
7. [EODHD Ticker Format](#eodhd-ticker-format)
8. [Python Implementation](#python-implementation)
9. [Best Practices](#best-practices)

---

## Overview

### Why Ticker Suffixes Matter

Stock tickers often include **suffixes** that indicate special characteristics:
- **Stock class** (voting rights, dividends)
- **Depositary receipts** (ADR, GDR, NVDR)
- **Preferred stock series**
- **Special trading conditions**
- **Exchange-specific designations**

Understanding these suffixes is crucial for:
- Accurate data retrieval
- Proper fundamental analysis
- Correct ticker identification
- Regulatory compliance

### Ticker Format

Most exchanges use a format: `BASE_SYMBOL` + `SUFFIX`

**Examples**:
- `BAC-PB.US` - Bank of America Preferred Series B
- `GOOGL.US` - Alphabet Class A shares
- `PTT-R.BK` - PTT Public Company Limited NVDR (Thailand)
- `BRK-B.US` - Berkshire Hathaway Class B shares

---

## Common Stock Types

### 1. Common Stock

**Definition**: Standard equity ownership with voting rights and dividends (if declared).

**Characteristics**:
- Voting rights at shareholder meetings
- Residual claim on assets (after debt, preferred stock)
- Variable dividends (not guaranteed)
- Highest risk, highest potential return

**Ticker Format**: Usually no suffix (clean ticker)

**Examples**:
```
AAPL.US    - Apple Inc. (Common Stock)
MSFT.US    - Microsoft Corporation (Common Stock)
JPM.US     - JPMorgan Chase & Co. (Common Stock)
```

**EODHD Type Field**: `"Type": "Common Stock"`

### 2. Preferred Stock

**Definition**: Equity security with preferential dividend payments and priority over common stock in liquidation.

**Characteristics**:
- Fixed dividend payments (priority over common stock)
- No voting rights (typically)
- Higher claim on assets than common stock
- Less volatile than common stock
- Callable by issuer

**Ticker Format**: Hyphen + series letter(s) (US convention)

**Examples**:
```
BAC-PB.US  - Bank of America Preferred Series B
JPM-PC.US  - JPMorgan Chase Preferred Series C
C-PJ.US    - Citigroup Preferred Series J
WFC-PL.US  - Wells Fargo Preferred Series L
```

**EODHD Type Field**: `"Type": "Preferred Stock"`

**Fundamentals Data**:
- ✅ Available for preferred stocks via Fundamentals API
- ⚠️ **Usually has less data** than common stock (fewer financial metrics)
- ✅ Still includes: General info, dividends, some valuation metrics
- 💡 **Recommendation**: Use common stock ticker for **most complete** fundamental analysis

### 3. Multiple Share Classes

**Definition**: Companies issue different classes with varying voting rights or dividend structures.

**Common Classes**:
- **Class A**: Typically voting shares (more votes per share)
- **Class B**: Often held by founders/insiders (supervoting rights)
- **Class C**: No voting rights (common for public trading)

**Ticker Format**: Hyphen + class letter OR distinct ticker

**Examples**:

#### Hyphen Format:
```
BRK-A.US   - Berkshire Hathaway Class A (~$500k per share, 1 vote)
BRK-B.US   - Berkshire Hathaway Class B (~$330 per share, 1/10000 vote)
```

#### Distinct Ticker Format:
```
GOOGL.US   - Alphabet Class A (1 vote per share)
GOOG.US    - Alphabet Class C (no voting rights)
```

**EODHD Type Field**: `"Type": "Common Stock"` (both classes)

---

## US Stock Suffixes

### Preferred Stock Series (Hyphen Format)

**Format**: `TICKER-P{SERIES}`

Where:
- `TICKER` = Base ticker symbol
- `-P` = Preferred indicator (may be omitted in some cases)
- `{SERIES}` = Series letter (A, B, C, etc.)

**Examples**:
```
JPM-PA.US  - JPMorgan Chase Preferred Series A
JPM-PC.US  - JPMorgan Chase Preferred Series C
BAC-PE.US  - Bank of America Preferred Series E
```

**Alternative Format** (without P):
```
BAC-B.US   - Bank of America Preferred Series B
C-J.US     - Citigroup Preferred Series J
```

### Units, Rights, Warrants

**Format**: `TICKER-{SUFFIX}` or `TICKER{SUFFIX}`

| Suffix | Meaning | Example                   |
|-----|---------|---------------------------|
| `U` | Units (stock + warrant) | `SPCE-U.US` or `SPCEU.US` |
| `W` | Warrants | `SPCEW.US` or `SPCE-W.US` |
| `R` | Rights | `XYZ-R.US`   or `XYZR.US` |
| `WT` | Warrants (alternative) | `ABC-WT.US`  or `ABCWT.US`          |

**Note**: Not all exchanges use these conventions. Check exchange-specific rules.

---

## Depositary Receipts

### American Depositary Receipts (ADR)

**Definition**: Securities representing shares of non-US companies traded on US exchanges.

**Characteristics**:
- Traded in US dollars
- Settles through US clearing system
- Represents underlying foreign shares (ratio varies)
- Dividends converted to USD
- May have different ticker than home exchange

**Ticker Format**: Distinct ticker on US exchange (usually no suffix)

**Examples**:
```
TSM.US     - Taiwan Semiconductor Manufacturing (ADR)
  Primary: 2330.TW (Taiwan Stock Exchange)
  Ratio: 1 ADR = 5 ordinary shares

BABA.US    - Alibaba Group (ADR)
  Primary: 9988.HK (Hong Kong Stock Exchange)

NVO.US     - Novo Nordisk (ADR)
  Primary: NOVO-B.CO (Copenhagen Stock Exchange)
```

**EODHD Type Field**: `"Type": "Common Stock"` (ADRs listed as common)

**Important**: Use `PrimaryTicker` field to identify home exchange listing for fundamental data. See [Primary Tickers Guide](./primary-tickers-guide.md).

### Global Depositary Receipts (GDR)

**Definition**: Similar to ADR but traded on exchanges outside the US.

**Characteristics**:
- Traded on London Stock Exchange, Luxembourg Stock Exchange, etc.
- Similar structure to ADR
- Represents underlying shares

**Examples**:
```
SBER.IL    - Sberbank GDR (London)
GAZP.IL    - Gazprom GDR (London)
```

---

## Thailand -R Stocks (NVDR)

### What is NVDR?

**NVDR** = **Non-Voting Depositary Receipts**

**Definition**: A special type of depositary receipt issued by the Thai NVDR Company Limited for stocks listed on the Stock Exchange of Thailand (SET).

**Official Documentation**: https://www.set.or.th/nvdr/en/about/whatis.html

### Characteristics

**1. No Voting Rights**:
- NVDR holders do **NOT** have voting rights at shareholder meetings
- Cannot participate in company decisions
- Cannot vote on board elections, mergers, etc.

**2. All Other Rights Preserved**:
- ✅ Receive **dividends** (same as ordinary shareholders)
- ✅ **Stock dividends** and stock splits
- ✅ Rights to **subscribe to new shares** (rights offerings)
- ✅ **Trading rights** (can buy/sell freely)
- ✅ Right to **convert** back to ordinary shares (subject to foreign ownership limits)

**3. Purpose**:
- Allows **foreign investors** to invest in Thai stocks subject to foreign ownership limits
- When foreign ownership limit reached for ordinary shares, -R (NVDR) remains available
- Provides liquidity for foreign investors

**4. Conversion**:
- Can convert NVDR → ordinary shares (if foreign ownership limit not reached)
- Can convert ordinary shares → NVDR (always possible)

### Ticker Format

**Format**: `{BASE_TICKER}-R.BK`

Where:
- `{BASE_TICKER}` = Company's base ticker symbol
- `-R` = Restricted/NVDR indicator
- `.BK` = Bangkok Stock Exchange code (in EODHD format)

### Examples

| Company | Ordinary Shares | NVDR (Restricted) |
|---------|----------------|-------------------|
| **PTT Public Company Limited** | `PTT.BK` | `PTT-R.BK` |
| **Kasikornbank** | `KBANK.BK` | `KBANK-R.BK` |
| **CP ALL** | `CPALL.BK` | `CPALL-R.BK` |
| **Advanced Info Service** | `ADVANC.BK` | `ADVANC-R.BK` |
| **Airports of Thailand** | `AOT.BK` | `AOT-R.BK` |

### Data Comparison

```bash
# Ordinary shares
curl "https://eodhd.com/api/eod/PTT.BK?api_token=YOUR_API_KEY&fmt=json"

# NVDR (Restricted shares)
curl "https://eodhd.com/api/eod/PTT-R.BK?api_token=YOUR_API_KEY&fmt=json"
```

**Expected Differences**:
- **Price**: Usually very similar (small premium/discount)
- **Volume**: May differ significantly
- **Fundamentals**: Use ordinary shares (`PTT.BK`) for fundamental data

### When to Use Each

| Use Case | Ordinary Shares | NVDR (-R) |
|----------|----------------|-----------|
| **Fundamental Analysis** | ✅ Use this | ❌ Don't use |
| **Price Data (foreign investor)** | If available | ✅ Use this if ordinary unavailable |
| **Volume Analysis** | ✅ Primary liquidity | Secondary liquidity |
| **Voting on company decisions** | ✅ Yes | ❌ No |
| **Dividends** | ✅ Yes | ✅ Yes (same) |

### Foreign Ownership Limits

**Background**: Thailand restricts foreign ownership in certain sectors (e.g., telecommunications, banking, media).

**Typical Limits**:
- Most companies: 49% foreign ownership
- Some sectors: 25% or lower
- Exceptions: Companies in Board of Investment (BOI) promoted sectors

**How NVDR Helps**:
```
Example: Kasikornbank (KBANK)
- Foreign ownership limit: 49% of total shares
- Foreign ownership of KBANK.BK: 49% (FULL - cannot buy more)
- Solution: Buy KBANK-R.BK (NVDR) instead
  - No voting rights
  - But same dividends and price performance
  - Bypasses foreign ownership limit
```

### Python Example

```python
def analyze_thailand_nvdr(base_ticker, api_token):
    """
    Compare ordinary shares vs NVDR in Thailand.

    Args:
        base_ticker: Base ticker without -R (e.g., 'PTT')
        api_token: EODHD API token

    Returns:
        Comparison dictionary
    """
    import requests

    ordinary_ticker = f"{base_ticker}.BK"
    nvdr_ticker = f"{base_ticker}-R.BK"

    # Get latest prices
    def get_latest_price(ticker):
        url = f"https://eodhd.com/api/eod/{ticker}"
        params = {"api_token": api_token, "fmt": "json", "order": "d"}
        response = requests.get(url, params=params)
        data = response.json()
        if data:
            return data[0]
        return None

    ordinary_data = get_latest_price(ordinary_ticker)
    nvdr_data = get_latest_price(nvdr_ticker)

    if not ordinary_data or not nvdr_data:
        return {"error": "Data not available"}

    # Calculate price difference
    price_diff = nvdr_data['close'] - ordinary_data['close']
    price_diff_pct = (price_diff / ordinary_data['close']) * 100

    return {
        "ordinary": {
            "ticker": ordinary_ticker,
            "price": ordinary_data['close'],
            "volume": ordinary_data['volume'],
            "date": ordinary_data['date']
        },
        "nvdr": {
            "ticker": nvdr_ticker,
            "price": nvdr_data['close'],
            "volume": nvdr_data['volume'],
            "date": nvdr_data['date']
        },
        "comparison": {
            "price_difference": price_diff,
            "price_difference_pct": price_diff_pct,
            "volume_ratio": nvdr_data['volume'] / ordinary_data['volume'] if ordinary_data['volume'] > 0 else 0
        },
        "recommendation": {
            "for_fundamentals": ordinary_ticker,
            "for_foreign_investors": nvdr_ticker if abs(price_diff_pct) < 1 else "Check price difference"
        }
    }

# Usage
result = analyze_thailand_nvdr("PTT", "YOUR_API_KEY")
print(f"Ordinary shares: {result['ordinary']['ticker']} @ {result['ordinary']['price']}")
print(f"NVDR: {result['nvdr']['ticker']} @ {result['nvdr']['price']}")
print(f"Price difference: {result['comparison']['price_difference_pct']:.2f}%")
print(f"Use for fundamentals: {result['recommendation']['for_fundamentals']}")
```

### Important Notes

✅ **Always use ordinary shares** (without -R) for fundamental analysis

✅ **NVDR suitable for** foreign investors when ordinary shares unavailable due to foreign ownership limit

✅ **Price parity**: NVDR and ordinary shares should trade at similar prices (arbitrage keeps them close)

⚠️ **Liquidity**: Check volume - ordinary shares typically more liquid

⚠️ **Corporate actions**: Both receive same dividends and stock splits

---

## Other Exchange-Specific Conventions

### Hong Kong Stock Exchange

**Leading Zeros**: Hong Kong tickers preserve leading zeros

**Format**: `{NUMBER}.HK`

**Examples**:
```
0700.HK    - Tencent Holdings (NOT 700.HK)
0001.HK    - CK Hutchison Holdings (NOT 1.HK)
0005.HK    - HSBC Holdings (NOT 5.HK)
```

**Important**: Always use leading zeros for Hong Kong tickers.

### London Stock Exchange

**Pence vs Pounds**: Some stocks traded in pence (GBp) vs pounds (GBP)

**Examples**:
```
BP.LSE     - BP plc (traded in pence)
RDSA.LSE   - Royal Dutch Shell A (traded in pence)
```

**Note**: EODHD prices typically in pence (GBp) for LSE stocks.

### Canadian Stock Exchange

**Ticker Format**: Clean ticker with exchange suffix

**Venture Exchange** (TSXV):
```
TICKER.V   - TSXV listed stocks
```

**Examples**:
```
WELL.TO    - WELL Health Technologies (TSX)
WELL.V     - (if listed on TSXV instead)
```

### German Exchanges

**Multiple Exchanges**: Same company can trade on multiple German exchanges

**Examples**:
```
SIE.XETRA  - Siemens AG (XETRA)
SIE.F      - Siemens AG (Frankfurt)
SIE.BE     - Siemens AG (Berlin)
```

**Recommendation**: Use XETRA for most liquid German stocks.

---

## EODHD Ticker Format

### General Format

```
{TICKER_SYMBOL}.{EXCHANGE_CODE}
```

**Examples**:
```
AAPL.US          - Apple Inc. (US)
2330.TW          - TSMC (Taiwan)
PTT-R.BK         - PTT NVDR (Thailand)
BAC-PB.US        - Bank of America Preferred B (US)
0700.HK          - Tencent (Hong Kong - with leading zero)
```

### Type Field in Fundamentals API

The `Type` field in EODHD Fundamentals API indicates stock type:

```json
{
  "General": {
    "Code": "BAC",
    "Type": "Common Stock",
    ...
  }
}
```

**Common Values**:
- `"Common Stock"` - Standard equity
- `"Preferred Stock"` - Preferred shares
- `"ETF"` - Exchange-traded fund
- `"Fund"` - Mutual fund
- `"ADR"` - American Depositary Receipt (sometimes listed as "Common Stock")

### Checking Stock Type

```bash
# Get stock type
curl "https://eodhd.com/api/fundamentals/BAC-PB.US?api_token=demo&filter=General::Type"

# Response
{
  "Type": "Preferred Stock"
}
```

### Handling Dots in Ticker Symbols

**CRITICAL RULE**: Only **ONE dot** is allowed in the full ticker string, and it must be between the ticker code and exchange code.

#### The Problem

Some stocks have dots in their ticker symbols on the original exchange:
- `BF.B` - Brown-Forman Corporation Class B
- `AZA.A` - Azad Engineering Company Class A
- `BRK.A` - Berkshire Hathaway Class A
- `BRK.B` - Berkshire Hathaway Class B

**Issue**: If you directly append `.US`, you get `BF.B.US` (TWO dots) which is invalid.

#### The Solution

**Replace all separator dots with hyphens** in the ticker symbol before adding the exchange code.

**Format**: `{TICKER-WITH-HYPHENS}.{EXCHANGE}`

#### Conversion Examples

| Original Ticker | EODHD Format | Explanation |
|----------------|--------------|-------------|
| `BF.B` | `BF-B.US` | Dot replaced with hyphen |
| `AZA.A` | `AZA-A.US` | Dot replaced with hyphen |
| `BRK.A` | `BRK-A.US` | Dot replaced with hyphen |
| `BRK.B` | `BRK-B.US` | Dot replaced with hyphen |

#### API Usage

```bash
# WRONG - Two dots (will fail)
curl "https://eodhd.com/api/eod/BF.B.US?api_token=demo"  # ❌ Invalid

# CORRECT - Replace dot with hyphen
curl "https://eodhd.com/api/eod/BF-B.US?api_token=demo"  # ✅ Correct

# WRONG - Two dots (will fail)
curl "https://eodhd.com/api/fundamentals/BRK.A.US?api_token=demo"  # ❌ Invalid

# CORRECT - Replace dot with hyphen
curl "https://eodhd.com/api/fundamentals/BRK-A.US?api_token=demo"  # ✅ Correct
```

#### Python Helper Function

```python
def format_ticker_for_eodhd(ticker_symbol: str, exchange: str) -> str:
    """
    Format ticker symbol for EODHD API by replacing dots with hyphens.

    Args:
        ticker_symbol: Original ticker (e.g., 'BF.B', 'AZA.A')
        exchange: Exchange code (e.g., 'US', 'IN')

    Returns:
        Properly formatted ticker for EODHD (e.g., 'BF-B.US')

    Example:
        >>> format_ticker_for_eodhd('BF.B', 'US')
        'BF-B.US'

        >>> format_ticker_for_eodhd('BRK.A', 'US')
        'BRK-A.US'
    """
    # Replace all dots in ticker with hyphens
    formatted_ticker = ticker_symbol.replace('.', '-')

    # Append exchange with single dot
    return f"{formatted_ticker}.{exchange}"


# Usage examples
print(format_ticker_for_eodhd('BF.B', 'US'))     # Output: BF-B.US
print(format_ticker_for_eodhd('AZA.A', 'US'))    # Output: AZA-A.US
print(format_ticker_for_eodhd('BRK.A', 'US'))    # Output: BRK-A.US
print(format_ticker_for_eodhd('BRK.B', 'US'))    # Output: BRK-B.US
```

#### Complete Example with API Call

```python
import requests

def get_stock_data_with_dot_handling(original_ticker, exchange, api_token):
    """
    Fetch stock data handling tickers with dots.

    Args:
        original_ticker: Ticker as listed on exchange (e.g., 'BF.B')
        exchange: Exchange code (e.g., 'US')
        api_token: EODHD API token

    Returns:
        Stock data dictionary
    """
    # Format ticker correctly
    formatted_ticker = original_ticker.replace('.', '-')
    full_symbol = f"{formatted_ticker}.{exchange}"

    print(f"Original ticker: {original_ticker}")
    print(f"Formatted for EODHD: {full_symbol}")

    # Make API request
    url = f"https://eodhd.com/api/eod/{full_symbol}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "order": "d",
        "period": "d"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if data:
        latest = data[0]
        print(f"Latest close: ${latest['close']:.2f}")
        print(f"Date: {latest['date']}")
        return data

    return None


# Example usage
data = get_stock_data_with_dot_handling('BF.B', 'US', 'YOUR_API_TOKEN')

# Output:
# Original ticker: BF.B
# Formatted for EODHD: BF-B.US
# Latest close: $64.25
# Date: 2024-11-27
```

#### Applies to All EODHD APIs

This dot-to-hyphen conversion applies to **ALL** EODHD API endpoints:

✅ **End-of-Day API**:
```bash
https://eodhd.com/api/eod/BF-B.US?api_token=YOUR_TOKEN
```

✅ **Fundamentals API**:
```bash
https://eodhd.com/api/fundamentals/BF-B.US?api_token=YOUR_TOKEN
```

✅ **Technical Indicators API**:
```bash
https://eodhd.com/api/technical/BRK-A.US?function=sma&period=50&api_token=YOUR_TOKEN
```

✅ **Intraday API**:
```bash
https://eodhd.com/api/intraday/BRK-B.US?interval=5m&api_token=YOUR_TOKEN
```

✅ **Real-Time / Live API**:
```bash
https://eodhd.com/api/real-time/BF-B.US?api_token=YOUR_TOKEN
```

#### Common Mistakes

❌ **WRONG - Including the dot**:
```python
# This will FAIL
ticker = "BF.B.US"
url = f"https://eodhd.com/api/eod/{ticker}"
# Error: Invalid ticker format (two dots)
```

❌ **WRONG - Not converting before appending exchange**:
```python
# This will FAIL
ticker = "BF.B"
full_symbol = f"{ticker}.US"  # Results in "BF.B.US" (two dots)
```

✅ **CORRECT - Replace dots first**:
```python
# This will SUCCEED
ticker = "BF.B"
formatted_ticker = ticker.replace('.', '-')
full_symbol = f"{formatted_ticker}.US"  # Results in "BF-B.US" (one dot)
```

#### Validation Function

```python
def validate_eodhd_ticker(ticker_string: str) -> bool:
    """
    Validate ticker format for EODHD API.

    Rules:
    - Must contain exactly ONE dot
    - Dot must separate ticker from exchange code
    - Format: TICKER.EXCHANGE

    Args:
        ticker_string: Full ticker (e.g., 'BF-B.US')

    Returns:
        True if valid, False otherwise
    """
    # Count dots
    dot_count = ticker_string.count('.')

    if dot_count != 1:
        print(f"❌ Invalid: Found {dot_count} dots (expected 1)")
        return False

    # Check format
    parts = ticker_string.split('.')
    if len(parts) != 2:
        print(f"❌ Invalid: Cannot split into ticker and exchange")
        return False

    ticker, exchange = parts

    if not ticker or not exchange:
        print(f"❌ Invalid: Empty ticker or exchange")
        return False

    print(f"✅ Valid: {ticker}.{exchange}")
    return True


# Test cases
validate_eodhd_ticker('BF-B.US')      # ✅ Valid
validate_eodhd_ticker('BF.B.US')      # ❌ Invalid (two dots)
validate_eodhd_ticker('AAPL.US')      # ✅ Valid
validate_eodhd_ticker('BRK-A.US')     # ✅ Valid
validate_eodhd_ticker('BRK.A.US')     # ❌ Invalid (two dots)
```

#### Key Takeaways

🔑 **Only ONE dot** allowed in the complete ticker string

🔑 **Replace ALL dots** in the ticker symbol with hyphens **before** adding exchange code

🔑 **Format**: `TICKER-WITH-HYPHENS.EXCHANGE`

🔑 **Applies to ALL APIs**: EOD, Fundamentals, Technical, Intraday, Options, Real-Time

🔑 **Original ticker**: `BF.B` → **EODHD format**: `BF-B.US`

---

## Python Implementation

### Stock Type Identifier

```python
import requests
from typing import Dict, Optional

class StockTypeIdentifier:
    """Identify stock types and ticker characteristics"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://eodhd.com/api"

    def identify_ticker_type(self, ticker: str, exchange: str) -> Dict:
        """
        Identify stock type and characteristics from ticker symbol.

        Args:
            ticker: Ticker symbol (e.g., 'BAC-PB', 'PTT-R', 'GOOGL')
            exchange: Exchange code (e.g., 'US', 'BK', 'HK')

        Returns:
            Dictionary with ticker analysis
        """
        result = {
            "ticker": f"{ticker}.{exchange}",
            "base_ticker": ticker,
            "exchange": exchange,
            "characteristics": []
        }

        # US Preferred Stock (hyphen format)
        if '-P' in ticker or (ticker.count('-') == 1 and exchange == 'US'):
            result["characteristics"].append("Preferred Stock")
            base = ticker.split('-')[0]
            series = ticker.split('-')[1]
            result["base_ticker"] = base
            result["series"] = series
            result["type"] = "Preferred Stock"

        # Thailand NVDR (-R suffix)
        elif ticker.endswith('-R') and exchange == 'BK':
            result["characteristics"].append("NVDR (Non-Voting Depositary Receipt)")
            result["base_ticker"] = ticker[:-2]  # Remove -R
            result["type"] = "NVDR"
            result["voting_rights"] = False
            result["ordinary_ticker"] = f"{result['base_ticker']}.{exchange}"

        # Multiple share classes (hyphen format, e.g., BRK-A, BRK-B)
        # Note: this is handled by the hyphen check above for US stocks.
        # Class shares use hyphens just like preferred stocks.

        # Hong Kong leading zeros
        elif exchange == 'HK' and ticker[0] == '0':
            result["characteristics"].append("Hong Kong Stock (with leading zeros)")
            result["type"] = "Common Stock"

        # Standard common stock
        else:
            result["type"] = "Common Stock (assumed)"

        # Get actual type from API
        api_type = self.get_type_from_api(ticker, exchange)
        if api_type:
            result["api_type"] = api_type
            result["type"] = api_type

        return result

    def get_type_from_api(self, ticker: str, exchange: str) -> Optional[str]:
        """Get stock type from EODHD API"""
        url = f"{self.base_url}/fundamentals/{ticker}.{exchange}"
        params = {
            "api_token": self.api_token,
            "filter": "General::Type"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("Type")
        except:
            return None

    def compare_ordinary_vs_restricted(self, base_ticker: str,
                                      exchange: str = 'BK') -> Dict:
        """
        Compare ordinary shares vs restricted shares (Thailand).

        Args:
            base_ticker: Base ticker without -R (e.g., 'PTT')
            exchange: Exchange code (default: 'BK' for Bangkok)

        Returns:
            Comparison dictionary
        """
        ordinary = f"{base_ticker}.{exchange}"
        restricted = f"{base_ticker}-R.{exchange}"

        # Get latest prices
        ordinary_data = self.get_latest_price(ordinary)
        restricted_data = self.get_latest_price(restricted)

        if not ordinary_data or not restricted_data:
            return {
                "error": "Data not available for one or both tickers",
                "ordinary": ordinary,
                "restricted": restricted
            }

        # Calculate differences
        price_diff = restricted_data['close'] - ordinary_data['close']
        price_diff_pct = (price_diff / ordinary_data['close']) * 100
        volume_ratio = (restricted_data['volume'] / ordinary_data['volume']
                       if ordinary_data['volume'] > 0 else 0)

        return {
            "ordinary_shares": {
                "ticker": ordinary,
                "price": ordinary_data['close'],
                "volume": ordinary_data['volume'],
                "date": ordinary_data['date'],
                "voting_rights": True
            },
            "restricted_shares": {
                "ticker": restricted,
                "price": restricted_data['close'],
                "volume": restricted_data['volume'],
                "date": restricted_data['date'],
                "voting_rights": False,
                "type": "NVDR"
            },
            "comparison": {
                "price_difference": price_diff,
                "price_difference_pct": price_diff_pct,
                "volume_ratio": volume_ratio,
                "volume_ratio_pct": volume_ratio * 100
            },
            "recommendations": {
                "for_fundamentals": ordinary,
                "for_foreign_investors": (restricted if abs(price_diff_pct) < 2
                                        else f"Check price gap: {price_diff_pct:.2f}%"),
                "more_liquid": ordinary if ordinary_data['volume'] > restricted_data['volume'] else restricted
            }
        }

    def get_latest_price(self, symbol: str) -> Optional[Dict]:
        """Get latest price data for symbol"""
        url = f"{self.base_url}/eod/{symbol}"
        params = {
            "api_token": self.api_token,
            "fmt": "json",
            "order": "d",
            "period": "d"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data[0] if data else None
        except:
            return None


# Usage Examples
def main():
    api_token = "demo"  # Replace with your token
    identifier = StockTypeIdentifier(api_token)

    # Example 1: Identify various ticker types
    print("=" * 70)
    print("Example 1: Identify Ticker Types")
    print("=" * 70)

    tickers_to_check = [
        ("BAC-PB", "US"),      # Preferred stock
        ("GOOGL", "US"),       # Common stock
        ("PTT-R", "BK"),       # Thailand NVDR
        ("0700", "HK"),        # Hong Kong with leading zero
    ]

    for ticker, exchange in tickers_to_check:
        result = identifier.identify_ticker_type(ticker, exchange)
        print(f"\n{result['ticker']}:")
        print(f"  Type: {result['type']}")
        print(f"  Characteristics: {', '.join(result['characteristics'])}")
        if 'base_ticker' in result:
            print(f"  Base ticker: {result['base_ticker']}")
        if 'voting_rights' in result:
            print(f"  Voting rights: {result['voting_rights']}")

    # Example 2: Compare Thailand ordinary vs NVDR
    print("\n" + "=" * 70)
    print("Example 2: Thailand Ordinary vs NVDR Comparison")
    print("=" * 70)

    # Note: This requires production API token with Thailand data access
    comparison = identifier.compare_ordinary_vs_restricted("PTT")

    if "error" not in comparison:
        print(f"\nOrdinary Shares: {comparison['ordinary_shares']['ticker']}")
        print(f"  Price: ฿{comparison['ordinary_shares']['price']:.2f}")
        print(f"  Volume: {comparison['ordinary_shares']['volume']:,}")
        print(f"  Voting: {comparison['ordinary_shares']['voting_rights']}")

        print(f"\nNVDR (Restricted): {comparison['restricted_shares']['ticker']}")
        print(f"  Price: ฿{comparison['restricted_shares']['price']:.2f}")
        print(f"  Volume: {comparison['restricted_shares']['volume']:,}")
        print(f"  Voting: {comparison['restricted_shares']['voting_rights']}")

        print(f"\nComparison:")
        print(f"  Price difference: {comparison['comparison']['price_difference_pct']:.2f}%")
        print(f"  NVDR volume is {comparison['comparison']['volume_ratio_pct']:.1f}% of ordinary")

        print(f"\nRecommendations:")
        print(f"  For fundamentals: {comparison['recommendations']['for_fundamentals']}")
        print(f"  For foreign investors: {comparison['recommendations']['for_foreign_investors']}")
        print(f"  More liquid: {comparison['recommendations']['more_liquid']}")
    else:
        print(f"Error: {comparison['error']}")


if __name__ == "__main__":
    main()
```

---

## Best Practices

### 1. Always Verify Stock Type

**Check Before Analysis**:

```python
def verify_stock_type(ticker, exchange, api_token):
    """Verify stock type before analysis"""
    url = f"https://eodhd.com/api/fundamentals/{ticker}.{exchange}"
    params = {"api_token": api_token, "filter": "General"}

    response = requests.get(url, params=params)
    data = response.json()

    stock_type = data.get("Type")

    if "Preferred" in stock_type:
        print(f"⚠️ Note: {ticker}.{exchange} is preferred stock")
        print("   Fundamentals available but may have less data than common stock")
        print("   Consider using common stock for more complete fundamental analysis")
        return True  # Still can proceed, but with warning

    return True

# Usage
if verify_stock_type("BAC-PB", "US", api_token):
    # Can proceed with analysis
    # Note: If preferred stock, data may be less complete
    fundamentals = get_fundamentals("BAC-PB", "US", api_token)
else:
    # Other validation failed
    pass
```

### 2. Use Ordinary Shares for Fundamentals

**Thailand NVDR Example**:

```python
def get_fundamentals_thailand(ticker, exchange, api_token):
    """Get fundamentals using ordinary shares for Thailand stocks"""

    # If NVDR ticker, convert to ordinary
    if ticker.endswith('-R') and exchange == 'BK':
        ordinary_ticker = ticker[:-2]  # Remove -R
        print(f"Using ordinary shares {ordinary_ticker}.{exchange} for fundamentals")
        ticker = ordinary_ticker

    # Fetch fundamentals
    url = f"https://eodhd.com/api/fundamentals/{ticker}.{exchange}"
    params = {"api_token": api_token}

    response = requests.get(url, params=params)
    return response.json()

# Usage
fundamentals = get_fundamentals_thailand("PTT-R", "BK", api_token)
# Automatically uses PTT.BK for fundamentals
```

### 3. Document Ticker Conventions

**In Your Code**:

```python
"""
Ticker Conventions Used:

US Stocks:
- Common: TICKER.US (e.g., AAPL.US)
- Preferred: TICKER-P{SERIES}.US (e.g., BAC-PB.US)
- Class shares: Distinct tickers (GOOGL.US, GOOG.US)

Thailand Stocks:
- Ordinary: TICKER.BK (e.g., PTT.BK)
- NVDR: TICKER-R.BK (e.g., PTT-R.BK)
- Always use ordinary for fundamentals

Hong Kong:
- Preserve leading zeros: 0700.HK (NOT 700.HK)
"""
```

### 4. Handle Suffix Edge Cases

**Robust Suffix Detection**:

```python
def parse_ticker_suffix(full_ticker):
    """Parse ticker and identify suffix type"""

    # Split ticker and exchange
    if '.' not in full_ticker:
        return {"error": "Invalid format, expected TICKER.EXCHANGE"}

    parts = full_ticker.rsplit('.', 1)
    ticker = parts[0]
    exchange = parts[1]

    result = {
        "full_ticker": full_ticker,
        "ticker": ticker,
        "exchange": exchange,
        "base_ticker": ticker,
        "suffix": None,
        "type": "common"  # default
    }

    # Check for hyphen suffix (preferred, NVDR, class shares, etc.)
    if '-' in ticker:
        base, suffix = ticker.split('-', 1)
        result["base_ticker"] = base
        result["suffix"] = suffix

        # Determine type
        if exchange == 'BK' and suffix == 'R':
            result["type"] = "nvdr"
        elif exchange == 'US' and (suffix.startswith('P') or len(suffix) <= 2):
            # Could be preferred (BAC-PB) or class shares (BRK-A, BRK-B)
            result["type"] = "preferred_or_class"
        else:
            result["type"] = "unknown_suffix"

    return result

# Usage
print(parse_ticker_suffix("PTT-R.BK"))
# {'type': 'nvdr', 'base_ticker': 'PTT', 'suffix': 'R'}

print(parse_ticker_suffix("BAC-PB.US"))
# {'type': 'preferred_or_class', 'base_ticker': 'BAC', 'suffix': 'PB'}

print(parse_ticker_suffix("BRK-B.US"))
# {'type': 'preferred_or_class', 'base_ticker': 'BRK', 'suffix': 'B'}
```

### 5. Price Comparison Validation

**Check for Arbitrage Opportunities**:

```python
def validate_price_parity(ordinary_ticker, restricted_ticker, api_token, threshold_pct=2.0):
    """
    Validate price parity between ordinary and restricted shares.

    Args:
        ordinary_ticker: Ordinary shares ticker
        restricted_ticker: Restricted shares ticker (NVDR)
        api_token: API token
        threshold_pct: Alert threshold (default 2%)
    """
    identifier = StockTypeIdentifier(api_token)

    ord_data = identifier.get_latest_price(ordinary_ticker)
    res_data = identifier.get_latest_price(restricted_ticker)

    if not ord_data or not res_data:
        print("Error: Cannot fetch price data")
        return

    price_diff_pct = abs(res_data['close'] - ord_data['close']) / ord_data['close'] * 100

    print(f"Ordinary: {ordinary_ticker} = ฿{ord_data['close']:.2f}")
    print(f"NVDR:     {restricted_ticker} = ฿{res_data['close']:.2f}")
    print(f"Difference: {price_diff_pct:.2f}%")

    if price_diff_pct > threshold_pct:
        print(f"⚠️  WARNING: Price difference exceeds {threshold_pct}% threshold!")
        print("    This may indicate:")
        print("    - Liquidity issues")
        print("    - Foreign ownership limit reached")
        print("    - Market inefficiency (arbitrage opportunity)")
    else:
        print(f"✅ Price parity maintained (within {threshold_pct}% threshold)")

# Usage
validate_price_parity("PTT.BK", "PTT-R.BK", api_token)
```

---

## Summary

### Key Takeaways

🔑 **CRITICAL: Dots in tickers** - Replace ALL dots with hyphens before adding exchange:
   - Original: `BF.B` → EODHD format: `BF-B.US`
   - Original: `BRK.A` → EODHD format: `BRK-A.US`
   - Only ONE dot allowed (between ticker and exchange)

✅ **Ticker suffixes** indicate special stock characteristics (preferred, NVDR, class shares)

✅ **Thailand -R stocks (NVDR)** are non-voting depositary receipts:
   - Allow foreign investors to bypass ownership limits
   - Same dividends as ordinary shares
   - No voting rights
   - Always use ordinary shares for fundamentals

✅ **US preferred stocks** use hyphen format (`TICKER-P{SERIES}.US`)

✅ **ADRs** are depositary receipts for foreign stocks trading in US
   - Use `PrimaryTicker` field to find home exchange listing
   - Use primary listing for fundamentals

✅ **Hong Kong tickers** preserve leading zeros (`0700.HK` not `700.HK`)

✅ **Multiple share classes** have different voting rights:
   - Class A typically voting shares
   - Class C typically non-voting
   - Use more liquid class for price analysis

### Quick Reference Table

| Suffix/Format | Example | Meaning | Use For Fundamentals? |
|---------------|---------|---------|----------------------|
| Clean ticker | `AAPL.US` | Common stock | ✅ Yes (most complete data) |
| Dot in ticker | `BF.B` → `BF-B.US` | Class shares (dot → hyphen) | ✅ Yes (convert dots first!) |
| `-P{SERIES}` | `BAC-PB.US` | Preferred stock | ⚠️ Available but limited (use common for complete data) |
| `-R` (Thailand) | `PTT-R.BK` | NVDR (no voting) | ❌ No (use ordinary) |
| Distinct class | `GOOGL.US`, `GOOG.US` | Different classes | ✅ Yes (prefer higher volume) |
| `0{NUMBER}` (HK) | `0700.HK` | Hong Kong stock | ✅ Yes |
| US ticker | `TSM.US` | ADR | ❌ No (use primary: `2330.TW`) |

### API Endpoints

```bash
# Get stock type
https://eodhd.com/api/fundamentals/{TICKER}.{EXCHANGE}?api_token={TOKEN}&filter=General::Type

# Get primary ticker (for ADRs)
https://eodhd.com/api/fundamentals/{TICKER}.{EXCHANGE}?api_token={TOKEN}&filter=General::PrimaryTicker

# Get price data
https://eodhd.com/api/eod/{TICKER}.{EXCHANGE}?api_token={TOKEN}
```

---

**Related Documentation**:
- [Primary Tickers Guide](./primary-tickers-guide.md)
- [API Authentication & Demo Access](./api-authentication-demo-access.md)
- [Special Exchanges Guide](./special-exchanges-guide.md)
- [Fundamentals Data API](../endpoints/fundamentals-data.md)

**External Resources**:
- [Thailand NVDR Official Guide](https://www.set.or.th/nvdr/en/about/whatis.html)
- [US Preferred Stock Guide](https://www.investopedia.com/terms/p/preferredstock.asp)
- [Understanding ADRs](https://www.investopedia.com/terms/a/adr.asp)
- [Stock Classes Explained](https://www.investopedia.com/ask/answers/062215/what-difference-between-class-shares-and-other-common-shares-companys-stock.asp)
