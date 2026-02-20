# API Authentication & Demo Access Guide

**Purpose**: Understand EODHD API authentication methods and demo access capabilities
**Last Updated**: 2024-11-27
**Applies To**: All main REST API endpoints (not Marketplace APIs)

---

## Table of Contents

1. [Overview](#overview)
2. [API Token Types](#api-token-types)
3. [Demo API Key](#demo-api-key)
4. [Authentication Methods](#authentication-methods)
5. [Demo Access Limitations](#demo-access-limitations)
6. [Demo Tickers by Asset Class](#demo-tickers-by-asset-class)
7. [Testing Examples](#testing-examples)
8. [Upgrading to Production](#upgrading-to-production)
9. [Best Practices](#best-practices)

---

## Overview

### Authentication System

EODHD API uses **API token-based authentication** for all endpoints. Every request must include a valid API token to access data.

**Two Types of Access**:
1. **Demo Access** - Free testing with limited tickers
2. **Production Access** - Paid plans with full market coverage

### Scope

This guide covers authentication for **main REST API endpoints**, including:
- End-of-Day Historical Data
- Intraday Historical Data
- Live (Delayed) Stock Prices
- Fundamentals Data
- Calendar Data (Earnings, Splits, IPOs)
- Technical Indicators
- Exchanges & Symbols Lists
- Bulk API
- And more...

**Note**: Marketplace APIs may have different authentication requirements. See individual Marketplace product documentation.

---

## API Token Types

### Demo Token

**Token Value**: `demo`

**Purpose**:
- Test API functionality
- Explore data structure
- Develop and debug integrations
- Learn API capabilities

**Access Level**: Limited to specific demo tickers (see below)

**Cost**: Free

**Use Cases**:
- Initial exploration and testing
- Educational purposes
- Demo applications
- Code examples and tutorials

### Production Token

**Token Format**: Alphanumeric string (e.g., `65f3a2b1c4d5e6f7.89012345`)

**Purpose**: Full production access to all markets and tickers

**Access Level**: Based on subscription plan:
- **All-World Plan**: All markets globally
- **All-In-One Plan**: All markets + real-time data
- **Custom Plans**: Specific exchanges or asset classes

**Cost**: Subscription-based (see pricing page)

**Obtain Token**:
1. Sign up at [eodhd.com/register](https://eodhd.com/register)
2. Choose subscription plan
3. Access token in user dashboard

---

## Demo API Key

### Overview

The demo API key `"demo"` provides **free testing access** to a curated set of popular tickers across all major asset classes.

### Demo Tickers

The following tickers work with the `demo` API key in **all relevant REST API endpoints**:

| Asset Class | Ticker | Name | Exchange |
|-------------|--------|------|----------|
| **US Stocks** | `AAPL.US` | Apple Inc. | NASDAQ |
| | `MSFT.US` | Microsoft Corporation | NASDAQ |
| | `TSLA.US` | Tesla Inc. | NASDAQ |
| **ETF** | `VTI.US` | Vanguard Total Stock Market ETF | NYSE Arca |
| **Mutual Fund** | `SWPPX.US` | Schwab S&P 500 Index Fund | US Mutual Funds |
| **Forex** | `EURUSD.FOREX` | Euro / US Dollar | Forex |
| **Cryptocurrency** | `BTC-USD.CC` | Bitcoin / US Dollar | Crypto |

### What "All Relevant APIs" Means

These demo tickers work across **every main REST endpoint** where the asset class is supported:

#### Historical Data APIs
- End-of-Day Historical Data
- Intraday Historical Data (1m, 5m, 1h)
- Live (Delayed) Stock Prices
- Historical Market Capitalization

#### Fundamental Data APIs
- Fundamentals Data (income statement, balance sheet, cash flow)
- Calendar Data (earnings dates, dividends, splits)
- Insider Transactions
- Institutional Holdings

#### Technical Analysis APIs
- Technical Indicators (SMA, EMA, RSI, MACD, etc.)

#### Reference Data APIs
- Exchange Symbol List
- Exchanges List
- Stock Market Tickers List

#### Bulk Data APIs
- Bulk EOD Data
- Bulk Fundamental Data
- Bulk Splits/Dividends

**Important**: Demo access applies to **main REST endpoints** only. Marketplace products (like Alternative Data, Sentiment Data, etc.) may have separate demo access or require production keys.

---

## Authentication Methods

### Method 1: Query Parameter (Recommended)

Add `api_token` as a query parameter to the URL.

**Format**:
```
https://eodhd.com/api/endpoint?api_token=YOUR_API_KEY&other_params=value
```

**Examples**:

```bash
# Demo key - End-of-Day data
https://eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=json

# Demo key - Fundamentals data
https://eodhd.com/api/fundamentals/MSFT.US?api_token=demo

# Production key - End-of-Day data
https://eodhd.com/api/eod/IBM.US?api_token=65f3a2b1c4d5e6f7.89012345&fmt=json
```

**Advantages**:
- Simple and straightforward
- Works in browsers for quick testing
- Easy to debug
- Compatible with all HTTP clients

**Disadvantages**:
- API token visible in URLs (logs, browser history)
- Less secure for production use

### Method 2: Authorization Header

Pass the API token in the HTTP Authorization header.

**Format**:
```
Authorization: Bearer YOUR_API_KEY
```

**Examples**:

**cURL**:
```bash
curl -H "Authorization: Bearer demo" \
  "https://eodhd.com/api/eod/AAPL.US?fmt=json"
```

**Python (requests)**:
```python
import requests

headers = {"Authorization": "Bearer demo"}
response = requests.get(
    "https://eodhd.com/api/eod/AAPL.US",
    headers=headers,
    params={"fmt": "json"}
)
data = response.json()
```

**JavaScript (fetch)**:
```javascript
const headers = {
    "Authorization": "Bearer demo"
};

fetch("https://eodhd.com/api/eod/AAPL.US?fmt=json", { headers })
    .then(response => response.json())
    .then(data => console.log(data));
```

**Advantages**:
- More secure (token not in URL)
- Better for production systems
- Tokens not logged in URL access logs
- Industry standard practice

**Disadvantages**:
- Requires HTTP client that supports headers
- Can't test directly in browser address bar

### Method 3: POST Body (Limited Support)

Some endpoints accept the API token in the POST request body.

**Format**:
```json
{
    "api_token": "YOUR_API_KEY",
    "other_params": "value"
}
```

**Note**: This method is **not universally supported**. Use query parameter or header methods for maximum compatibility.

### Recommendation

**For Testing & Development**: Use query parameter method with `demo` key
**For Production**: Use Authorization header with production key for better security

---

## Demo Access Limitations

### Ticker Restrictions

**What's Limited**:
- Only 7 demo tickers available (AAPL.US, MSFT.US, TSLA.US, VTI.US, SWPPX.US, EURUSD.FOREX, BTC-USD.CC)
- Cannot access other tickers even if they exist in the database

**Example**:
```bash
# ✅ Works - Demo ticker
https://eodhd.com/api/eod/AAPL.US?api_token=demo

# ❌ Fails - Not a demo ticker
https://eodhd.com/api/eod/GOOGL.US?api_token=demo
# Returns plain text: Unauthenticated
```

### No Time Restrictions

**Full Historical Access**: Demo key provides access to the **complete historical dataset** for demo tickers.

**Example**:
```bash
# ✅ Works - Access historical data from 2000
https://eodhd.com/api/eod/AAPL.US?api_token=demo&from=2000-01-01&to=2023-12-31&fmt=json
```

**No Date Limits**: You can query any historical date range for demo tickers.

### Feature Access

**Full Feature Access**: Demo key has access to all features and endpoints that support the demo tickers.

**Examples**:

```bash
# ✅ Technical Indicators
https://eodhd.com/api/technical/AAPL.US?function=sma&period=50&api_token=demo&fmt=json

# ✅ Fundamentals Data
https://eodhd.com/api/fundamentals/MSFT.US?api_token=demo&fmt=json

# ✅ Intraday Data
https://eodhd.com/api/intraday/TSLA.US?interval=5m&api_token=demo&fmt=json

# ✅ Calendar Data
https://eodhd.com/api/calendar/earnings?symbols=AAPL.US&api_token=demo&fmt=json
```

### Rate Limits

**Demo Rate Limits**: More restrictive than production keys

| Metric | Demo Key | Production Key |
|--------|----------|----------------|
| **Requests per day** | 20 requests/day (may vary) | Based on plan (typically unlimited for paid plans) |
| **Requests per second** | 1 request/second | Based on plan (up to 100/second for premium plans) |
| **Concurrent connections** | 1 connection | Multiple connections allowed |

**Note**: Exact rate limits may vary. Check EODHD documentation or user dashboard for current limits.

### Real-Time Data

**WebSockets**: Demo key works for real-time WebSocket streams with a specific set of tickers. Note that WebSocket endpoints use short symbols **without** the exchange suffix (e.g., `AAPL` not `AAPL.US`), and the demo symbol set differs from the main REST API set:

| Asset Class | Demo Tickers (WebSocket format) |
|-------------|--------------------------------|
| US Stocks | `AAPL`, `MSFT`, `TSLA` |
| Forex | `EURUSD` |
| Crypto | `BTC-USD`, `ETH-USD` |

```bash
# US Stocks
wss://ws.eodhistoricaldata.com/ws/us?api_token=demo
{"action": "subscribe", "symbols": "AAPL,MSFT,TSLA"}

# Forex
wss://ws.eodhistoricaldata.com/ws/forex?api_token=demo
{"action": "subscribe", "symbols": "EURUSD"}

# Crypto
wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo
{"action": "subscribe", "symbols": "BTC-USD,ETH-USD"}
```

**Live (Delayed) API**: Works with demo tickers (15-20 min delay for stocks)

```bash
# ✅ Works - Live delayed data
https://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json
```

---

## Demo Tickers by Asset Class

### US Stocks (3 tickers)

#### AAPL.US - Apple Inc.
```bash
# End-of-Day Data
https://eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=json

# Fundamentals
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json

# Intraday 5-minute
https://eodhd.com/api/intraday/AAPL.US?interval=5m&api_token=demo&fmt=json

# Technical Indicators - SMA
https://eodhd.com/api/technical/AAPL.US?function=sma&period=50&api_token=demo&fmt=json
```

#### MSFT.US - Microsoft Corporation
```bash
# End-of-Day Data
https://eodhd.com/api/eod/MSFT.US?api_token=demo&fmt=json

# Fundamentals with filter
https://eodhd.com/api/fundamentals/MSFT.US?api_token=demo&filter=Financials::Balance_Sheet::quarterly&fmt=json

# Calendar - Earnings
https://eodhd.com/api/calendar/earnings?symbols=MSFT.US&api_token=demo&fmt=json

# Insider Transactions
https://eodhd.com/api/insider-transactions?code=MSFT.US&api_token=demo&fmt=json
```

#### TSLA.US - Tesla Inc.
```bash
# End-of-Day Data with date range
https://eodhd.com/api/eod/TSLA.US?api_token=demo&from=2020-01-01&to=2023-12-31&fmt=json

# Live (Delayed) Price
https://eodhd.com/api/real-time/TSLA.US?api_token=demo&fmt=json

# Technical Indicators - RSI
https://eodhd.com/api/technical/TSLA.US?function=rsi&period=14&api_token=demo&fmt=json

# Splits History
https://eodhd.com/api/splits/TSLA.US?api_token=demo&fmt=json
```

### ETF (1 ticker)

#### VTI.US - Vanguard Total Stock Market ETF
```bash
# End-of-Day Data
https://eodhd.com/api/eod/VTI.US?api_token=demo&fmt=json

# Fundamentals (ETF-specific data)
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json

# ETF Holdings
https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&filter=ETF_Data::Holdings&fmt=json

# Technical Indicators
https://eodhd.com/api/technical/VTI.US?function=ema&period=20&api_token=demo&fmt=json
```

### Mutual Fund (1 ticker)

#### SWPPX.US - Schwab S&P 500 Index Fund
```bash
# End-of-Day Data
https://eodhd.com/api/eod/SWPPX.US?api_token=demo&fmt=json

# Fundamentals (Mutual Fund data)
https://eodhd.com/api/fundamentals/SWPPX.US?api_token=demo&fmt=json

# Historical data with range
https://eodhd.com/api/eod/SWPPX.US?api_token=demo&from=2015-01-01&fmt=json
```

### Forex (1 pair)

#### EURUSD.FOREX - Euro / US Dollar
```bash
# End-of-Day Data
https://eodhd.com/api/eod/EURUSD.FOREX?api_token=demo&fmt=json

# Intraday 1-minute
https://eodhd.com/api/intraday/EURUSD.FOREX?interval=1m&api_token=demo&fmt=json

# Live (Delayed) - ~1 min delay
https://eodhd.com/api/real-time/EURUSD.FOREX?api_token=demo&fmt=json

# Technical Indicators - MACD
https://eodhd.com/api/technical/EURUSD.FOREX?function=macd&api_token=demo&fmt=json

# WebSocket Real-Time
wss://ws.eodhistoricaldata.com/ws/forex?api_token=demo
# Then: {"action": "subscribe", "symbols": "EURUSD"}
```

### Cryptocurrency (1 pair)

#### BTC-USD.CC - Bitcoin / US Dollar
```bash
# End-of-Day Data
https://eodhd.com/api/eod/BTC-USD.CC?api_token=demo&fmt=json

# Intraday 1-hour
https://eodhd.com/api/intraday/BTC-USD.CC?interval=1h&api_token=demo&fmt=json

# Live (Delayed)
https://eodhd.com/api/real-time/BTC-USD.CC?api_token=demo&fmt=json

# Technical Indicators - Bollinger Bands
https://eodhd.com/api/technical/BTC-USD.CC?function=bbands&period=20&api_token=demo&fmt=json

# WebSocket Real-Time
wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo
# Then: {"action": "subscribe", "symbols": "BTC-USD"}
```

---

## Testing Examples

### Python - Testing Multiple Demo Tickers

```python
import requests

def test_demo_access():
    """Test demo API access across multiple tickers"""
    api_token = "demo"
    base_url = "https://eodhd.com/api/eod"

    demo_tickers = [
        "AAPL.US",
        "MSFT.US",
        "TSLA.US",
        "VTI.US",
        "SWPPX.US",
        "EURUSD.FOREX",
        "BTC-USD.CC"
    ]

    print("Testing Demo API Access\n" + "=" * 50)

    for ticker in demo_tickers:
        url = f"{base_url}/{ticker}"
        params = {
            "api_token": api_token,
            "fmt": "json",
            "period": "d",
            "order": "d"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Get latest price
            if data:
                latest = data[0]
                print(f"✅ {ticker:20} | "
                      f"Date: {latest['date']} | "
                      f"Close: ${latest['close']:.2f}")
            else:
                print(f"⚠️  {ticker:20} | No data returned")

        except requests.exceptions.HTTPError as e:
            print(f"❌ {ticker:20} | Error: {e}")

if __name__ == "__main__":
    test_demo_access()
```

**Output**:
```
Testing Demo API Access
==================================================
✅ AAPL.US              | Date: 2023-12-29 | Close: $193.15
✅ MSFT.US              | Date: 2023-12-29 | Close: $374.58
✅ TSLA.US              | Date: 2023-12-29 | Close: $248.48
✅ VTI.US               | Date: 2023-12-29 | Close: $234.23
✅ SWPPX.US             | Date: 2023-12-29 | Close: $67.89
✅ EURUSD.FOREX         | Date: 2023-12-29 | Close: $1.1045
✅ BTC-USD.CC           | Date: 2023-12-29 | Close: $42150.50
```

### Python - Test Fundamentals Access

```python
import requests

def test_fundamentals_demo():
    """Test fundamentals API with demo tickers"""
    api_token = "demo"
    base_url = "https://eodhd.com/api/fundamentals"

    # Test stock fundamentals
    stock_tickers = ["AAPL.US", "MSFT.US", "TSLA.US"]

    print("Testing Fundamentals API\n" + "=" * 60)

    for ticker in stock_tickers:
        url = f"{base_url}/{ticker}"
        params = {
            "api_token": api_token,
            "filter": "General"  # Get general company info
        }

        response = requests.get(url, params=params)
        data = response.json()

        print(f"\n{ticker}")
        print(f"  Name: {data.get('Name', 'N/A')}")
        print(f"  Sector: {data.get('Sector', 'N/A')}")
        print(f"  Industry: {data.get('Industry', 'N/A')}")
        print(f"  Market Cap: ${data.get('MarketCapitalization', 0):,.0f}")

if __name__ == "__main__":
    test_fundamentals_demo()
```

**Output**:
```
Testing Fundamentals API
============================================================

AAPL.US
  Name: Apple Inc
  Sector: Technology
  Industry: Consumer Electronics
  Market Cap: $3,010,000,000,000

MSFT.US
  Name: Microsoft Corporation
  Sector: Technology
  Industry: Software—Infrastructure
  Market Cap: $2,780,000,000,000

TSLA.US
  Name: Tesla, Inc.
  Sector: Consumer Cyclical
  Industry: Auto Manufacturers
  Market Cap: $789,000,000,000
```

### Python - Test Technical Indicators

```python
import requests
import pandas as pd

def test_technical_indicators_demo():
    """Test technical indicators API with demo tickers"""
    api_token = "demo"
    base_url = "https://eodhd.com/api/technical"

    ticker = "AAPL.US"
    indicators = [
        {"function": "sma", "period": 50},
        {"function": "ema", "period": 20},
        {"function": "rsi", "period": 14},
    ]

    print(f"Testing Technical Indicators for {ticker}\n" + "=" * 60)

    for indicator in indicators:
        url = f"{base_url}/{ticker}"
        params = {
            "api_token": api_token,
            "function": indicator["function"],
            "period": indicator["period"],
            "fmt": "json"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data:
            # Get last 3 values
            recent = data[:3]
            print(f"\n{indicator['function'].upper()}({indicator['period']}):")
            for entry in recent:
                value_key = f"{indicator['function']}"
                print(f"  {entry['date']}: {entry[value_key]:.2f}")

if __name__ == "__main__":
    test_technical_indicators_demo()
```

### cURL - Quick Command-Line Tests

```bash
# Test all demo tickers with one-liners

# AAPL - Latest EOD
curl "https://eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=json&order=d&period=d" | jq '.[0]'

# MSFT - Fundamentals General Info
curl "https://eodhd.com/api/fundamentals/MSFT.US?api_token=demo&filter=General" | jq '.Name, .Sector, .Industry'

# TSLA - Technical Indicator (SMA 50)
curl "https://eodhd.com/api/technical/TSLA.US?function=sma&period=50&api_token=demo&fmt=json" | jq '.[0]'

# VTI - ETF Holdings
curl "https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&filter=ETF_Data::Holdings" | jq '.[:5]'

# EURUSD - Intraday 5-minute
curl "https://eodhd.com/api/intraday/EURUSD.FOREX?interval=5m&api_token=demo&fmt=json" | jq '.[0:3]'

# BTC-USD - Live Delayed Price
curl "https://eodhd.com/api/real-time/BTC-USD.CC?api_token=demo&fmt=json" | jq '.'
```

### JavaScript - Browser Testing

```html
<!DOCTYPE html>
<html>
<head>
    <title>EODHD Demo API Test</title>
</head>
<body>
    <h1>EODHD Demo API Test</h1>
    <button onclick="testDemoAPI()">Test Demo Tickers</button>
    <pre id="output"></pre>

    <script>
        async function testDemoAPI() {
            const apiToken = 'demo';
            const tickers = ['AAPL.US', 'MSFT.US', 'TSLA.US'];
            const output = document.getElementById('output');
            output.textContent = 'Loading...\n\n';

            for (const ticker of tickers) {
                const url = `https://eodhd.com/api/eod/${ticker}?api_token=${apiToken}&fmt=json&period=d&order=d`;

                try {
                    const response = await fetch(url);
                    const data = await response.json();

                    if (data && data.length > 0) {
                        const latest = data[0];
                        output.textContent += `${ticker}: $${latest.close} (${latest.date})\n`;
                    }
                } catch (error) {
                    output.textContent += `${ticker}: Error - ${error.message}\n`;
                }
            }
        }
    </script>
</body>
</html>
```

---

## Upgrading to Production

### Why Upgrade?

**Access All Markets**:
- 70+ exchanges worldwide
- 150,000+ stocks, ETFs, and funds
- 1,100+ Forex pairs
- 1,000+ cryptocurrencies
- Bonds, indices

**Higher Rate Limits**:
- Unlimited daily requests (on most plans)
- Up to 100 requests/second
- Multiple concurrent connections

**Real-Time Data** (with appropriate plans):
- US stocks with <50ms latency
- Pre/post-market hours
- 50+ concurrent WebSocket symbols

**Advanced Features**:
- Bulk data downloads
- Historical market cap
- Sentiment data
- News API
- Screener API

### How to Upgrade

1. **Sign Up**: Visit [eodhd.com/register](https://eodhd.com/register)

2. **Choose Plan**:
   - **All-World**: All historical data for all markets
   - **EOD+Intraday**: Historical + intraday (1m/5m/1h)
   - **All-In-One**: Everything + real-time data
   - **Custom**: Select specific exchanges

3. **Get API Token**:
   - Access user dashboard after signup
   - Copy your unique API token
   - Replace `demo` with your token in all requests

4. **Update Code**:
   ```python
   # Before (demo)
   api_token = "demo"

   # After (production)
   api_token = "65f3a2b1c4d5e6f7.89012345"  # Your actual token

   # Better: Use environment variable
   import os
   api_token = os.environ.get("EODHD_API_TOKEN")
   ```

5. **Test Production Access**:
   ```bash
   # Test with a non-demo ticker
   curl "https://eodhd.com/api/eod/IBM.US?api_token=YOUR_TOKEN&fmt=json"
   ```

### Migration Checklist

- [ ] Sign up for EODHD account
- [ ] Select appropriate subscription plan
- [ ] Obtain production API token from dashboard
- [ ] Store token securely (environment variable, secrets manager)
- [ ] Update all code references from `demo` to production token
- [ ] Test with non-demo tickers
- [ ] Update rate limiting logic for higher limits
- [ ] Remove demo ticker restrictions from code
- [ ] Update documentation/comments
- [ ] Monitor usage in dashboard

---

## Best Practices

### 1. Secure Token Management

**Never Hardcode Tokens**:
```python
# ❌ Bad - Hardcoded token
api_token = "65f3a2b1c4d5e6f7.89012345"

# ✅ Good - Environment variable
import os
api_token = os.getenv("EODHD_API_TOKEN")

# ✅ Good - Config file (not in version control)
import json
with open("config.json") as f:
    config = json.load(f)
    api_token = config["api_token"]
```

**Use Environment Variables**:
```bash
# .env file (add to .gitignore)
EODHD_API_TOKEN=65f3a2b1c4d5e6f7.89012345

# Load in Python (using python-dotenv)
from dotenv import load_dotenv
import os

load_dotenv()
api_token = os.getenv("EODHD_API_TOKEN")
```

**Use Secrets Managers** (production):
- AWS Secrets Manager
- Azure Key Vault
- Google Cloud Secret Manager
- HashiCorp Vault

### 2. Error Handling

**Handle Authentication Errors**:
```python
import requests

def make_api_request(url, params):
    """Make API request with proper error handling"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise ValueError("Rate limit exceeded")
        else:
            raise

    # Check for plain text "Unauthenticated" response
    if response.text.strip() == "Unauthenticated":
        raise ValueError("Invalid or expired API token")

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API request failed: {e}")

# Usage
try:
    data = make_api_request(
        "https://eodhd.com/api/eod/AAPL.US",
        {"api_token": api_token, "fmt": "json"}
    )
except ValueError as e:
    print(f"Authentication error: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
```

### 3. Rate Limit Awareness

**Respect Rate Limits**:
```python
import time
from functools import wraps

def rate_limit(calls_per_second=1):
    """Decorator to enforce rate limiting"""
    min_interval = 1.0 / calls_per_second
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_second=1)  # Demo key limit
def fetch_eod_data(ticker, api_token):
    """Fetch EOD data with rate limiting"""
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {"api_token": api_token, "fmt": "json"}
    response = requests.get(url, params=params)
    return response.json()

# Usage
for ticker in ["AAPL.US", "MSFT.US", "TSLA.US"]:
    data = fetch_eod_data(ticker, "demo")
    print(f"{ticker}: {len(data)} records")
```

### 4. Caching

**Cache Demo Data**:
```python
import requests
from functools import lru_cache
import hashlib
import json

@lru_cache(maxsize=128)
def fetch_cached_data(url, params_hash):
    """Fetch data with caching"""
    params = json.loads(params_hash)
    response = requests.get(url, params=params)
    return response.json()

def get_eod_data(ticker, api_token, from_date=None, to_date=None):
    """Get EOD data with automatic caching"""
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json"
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    # Create hashable params string
    params_hash = json.dumps(params, sort_keys=True)

    return fetch_cached_data(url, params_hash)

# Usage - subsequent calls use cache
data1 = get_eod_data("AAPL.US", "demo", from_date="2023-01-01")
data2 = get_eod_data("AAPL.US", "demo", from_date="2023-01-01")  # From cache
```

### 5. Testing Strategy

**Develop with Demo, Deploy with Production**:
```python
import os

class EODHDClient:
    """EODHD API client with environment-aware token"""

    def __init__(self, env="development"):
        self.env = env
        self.api_token = self._get_api_token()
        self.base_url = "https://eodhd.com/api"

    def _get_api_token(self):
        """Get API token based on environment"""
        if self.env == "development":
            return "demo"
        elif self.env == "production":
            token = os.getenv("EODHD_API_TOKEN")
            if not token:
                raise ValueError("EODHD_API_TOKEN not set for production")
            return token
        else:
            raise ValueError(f"Unknown environment: {self.env}")

    def get_eod_data(self, ticker):
        """Fetch EOD data"""
        url = f"{self.base_url}/eod/{ticker}"
        params = {"api_token": self.api_token, "fmt": "json"}
        response = requests.get(url, params=params)
        return response.json()

# Usage
# Development
dev_client = EODHDClient(env="development")
data = dev_client.get_eod_data("AAPL.US")  # Uses demo key

# Production
prod_client = EODHDClient(env="production")
data = prod_client.get_eod_data("IBM.US")  # Uses production key
```

### 6. Demo Ticker Validation

**Validate Tickers for Demo**:
```python
DEMO_TICKERS = {
    "AAPL.US", "MSFT.US", "TSLA.US",  # US Stocks
    "VTI.US",                          # ETF
    "SWPPX.US",                        # Mutual Fund
    "EURUSD.FOREX",                    # Forex
    "BTC-USD.CC"                       # Crypto
}

def is_demo_ticker(ticker):
    """Check if ticker is available with demo key"""
    return ticker in DEMO_TICKERS

def validate_ticker_for_demo(ticker):
    """Validate ticker before making demo API request"""
    if not is_demo_ticker(ticker):
        available = ", ".join(sorted(DEMO_TICKERS))
        raise ValueError(
            f"Ticker '{ticker}' not available with demo key. "
            f"Available tickers: {available}"
        )

# Usage
try:
    validate_ticker_for_demo("GOOGL.US")
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Ticker 'GOOGL.US' not available with demo key...
```

### 7. Documentation

**Document API Token Requirements**:
```python
def fetch_fundamentals(ticker, api_token):
    """
    Fetch fundamental data for a ticker.

    Args:
        ticker (str): Ticker symbol (e.g., 'AAPL.US', 'EURUSD.FOREX')
        api_token (str): EODHD API token
            - Use "demo" for testing (limited tickers)
            - Use production token for full access

    Returns:
        dict: Fundamental data

    Raises:
        ValueError: If ticker not available with demo key
        requests.HTTPError: If API request fails

    Demo tickers:
        - US Stocks: AAPL.US, MSFT.US, TSLA.US
        - ETF: VTI.US
        - Mutual Fund: SWPPX.US
        - Forex: EURUSD.FOREX
        - Crypto: BTC-USD.CC

    Example:
        >>> # Demo access
        >>> data = fetch_fundamentals("AAPL.US", "demo")
        >>> print(data['General']['Name'])
        'Apple Inc'

        >>> # Production access
        >>> data = fetch_fundamentals("IBM.US", os.getenv("EODHD_API_TOKEN"))
    """
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {"api_token": api_token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
```

---

## Summary

### Demo API Key Overview

**Token**: `demo`

**Demo Tickers** (works in all relevant REST endpoints):
- **US Stocks**: AAPL.US, MSFT.US, TSLA.US
- **ETF**: VTI.US
- **Mutual Fund**: SWPPX.US
- **Forex**: EURUSD.FOREX
- **Cryptocurrency**: BTC-USD.CC

**What Works**:
✅ All main REST API endpoints
✅ Full historical data access (no date restrictions)
✅ All features (fundamentals, technicals, calendar, etc.)
✅ Intraday data
⚠️ WebSocket real-time streaming — works, but may use a different demo symbol set than the main REST API; check WebSocket endpoint docs

**What's Limited**:
❌ Only 7 demo tickers on main REST endpoints; special endpoints (WebSockets, Marketplace APIs) may have their own demo symbol sets
❌ Lower rate limits
❌ Does not work for non-demo tickers

**Best For**:
- Testing and development
- Learning the API
- Creating demos and tutorials
- Evaluating before purchasing

**Upgrade For**:
- Access to all tickers and markets
- Higher rate limits
- Production applications
- Commercial use

### Authentication Methods

1. **Query Parameter**: `?api_token=demo` (easiest for testing)
2. **Authorization Header**: `Bearer demo` (best for production)
3. **POST Body**: Limited support

### Quick Start

```bash
# Test demo access immediately
curl "https://eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=json"
```

```python
# Python quick start
import requests
data = requests.get(
    "https://eodhd.com/api/eod/AAPL.US",
    params={"api_token": "demo", "fmt": "json"}
).json()
print(f"AAPL latest close: ${data[0]['close']}")
```

---

**Related Documentation**:
- [WebSockets Real-Time API](../endpoints/websockets-realtime.md)
- [End-of-Day Historical Data](../endpoints/eod-historical-data.md)
- [Fundamentals Data API](../endpoints/fundamentals-data.md)
- [Technical Indicators API](../endpoints/technical-indicators.md)

**External Resources**:
- [EODHD Registration](https://eodhd.com/register)
- [Pricing & Plans](https://eodhd.com/pricing)
- [User Dashboard](https://eodhd.com/cp)
