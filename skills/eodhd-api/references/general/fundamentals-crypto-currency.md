# Cryptocurrency & Currency Fundamentals API - Complete Guide

This guide covers the Fundamentals API for **Cryptocurrencies** and **Currency Pairs (Forex)**.

## Overview

The EODHD API provides fundamental data for cryptocurrencies and currency pairs. Unlike stocks, ETFs, and funds, these instruments have simpler fundamental structures focused on metadata, statistics, and resources.

**Key Characteristics**:
- **API calls consumption**: 10 calls per request
- **Format**: JSON only
- **Response size**: Small to medium (5-20 KB)
- **Filter support**: Available but less critical due to smaller response size
- **Type field**: `"Type": "Crypto"` or `"Type": "Currency"`

## Two Distinct Types

| Type | Description | Exchange Code | Example Ticker |
|------|-------------|---------------|----------------|
| **Cryptocurrency** | Digital currencies and tokens | `.CC` | `BTC-USD.CC`, `ETH-USD.CC` |
| **Currency (Forex)** | Fiat currency pairs | `.FOREX` | `EURUSD.FOREX`, `GBPUSD.FOREX` |

---

# Part 1: Cryptocurrency Fundamentals

## API Endpoint

### Base URL Format

```
https://eodhd.com/api/fundamentals/{CRYPTO_TICKER}?api_token={API_TOKEN}&fmt=json
```

**Parameters**:
- `{CRYPTO_TICKER}`: Format `{BASE}-{QUOTE}.CC` (e.g., `BTC-USD.CC`, `ETH-USD.CC`)
- `{API_TOKEN}`: Your API key
- `fmt=json`: Required (JSON only format)
- `filter=`: Optional parameter to limit data returned

**Example**:
```
https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json
```

## Data Structure

Cryptocurrency fundamental data has **four top-level sections**:

| Section | Description | Use Filter |
|---------|-------------|------------|
| **General** | Basic cryptocurrency information | `&filter=General` |
| **Tech** | Technical information and developers | `&filter=Tech` |
| **Resources** | Links and resources | `&filter=Resources` |
| **Statistics** | Market statistics and metrics | `&filter=Statistics` |

## Section 1: General

Returns basic cryptocurrency information including name, type, category, and description.

### Request

```
https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json&filter=General
```

Or generally:
```
https://eodhd.com/api/fundamentals/{CRYPTO_TICKER}?api_token={API_TOKEN}&fmt=json&filter=General
```

### Response Structure

```json
{
  "Name": "Bitcoin",
  "Type": "Crypto",
  "Category": "coin",
  "WebURL": "https://bitcoin.org/",
  "Description": "Bitcoin is a cryptocurrency and worldwide payment system. It is the first decentralized digital currency, as the system works without a central bank or single administrator."
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | Full name of the cryptocurrency |
| `Type` | string | Always "Crypto" for cryptocurrencies |
| `Category` | string | Type of crypto asset (coin, token, etc.) |
| `WebURL` | string | Official website URL |
| `Description` | string | Detailed description of the cryptocurrency |

**Category Values**:
- `coin` - Native blockchain cryptocurrency (e.g., Bitcoin, Ethereum)
- `token` - Token on another blockchain (e.g., ERC-20 tokens on Ethereum)

## Section 2: Tech

Returns technical information including developers and blockchain details.

### Request

```
https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json&filter=Tech
```

Or generally:
```
https://eodhd.com/api/fundamentals/{CRYPTO_TICKER}?api_token={API_TOKEN}&fmt=json&filter=Tech
```

### Response Structure

```json
{
  "Developers": {
    "0": "Satoshi Nakamoto - Founder",
    "1": "Wladimir J. van der Laan - Blockchain Developer",
    "2": "Jonas Schnelli - Blockchain Developer",
    "3": "Marco Falke - Blockchain Developer"
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `Developers` | object | Array-indexed list of developers and their roles |

**Structure**:
- Indexed by position (`"0"`, `"1"`, `"2"`, etc.)
- Each entry: `"Name - Role"` format
- Common roles: Founder, Blockchain Developer, Core Developer, Lead Developer

## Section 3: Resources

Returns links to various resources including social media, explorers, and source code.

### Request

```
https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json&filter=Resources
```

Or generally:
```
https://eodhd.com/api/fundamentals/{CRYPTO_TICKER}?api_token={API_TOKEN}&fmt=json&filter=Resources
```

### Response Structure

```json
{
  "Links": {
    "reddit": {
      "0": "https://www.reddit.com/r/bitcoin"
    },
    "website": {
      "0": "https://bitcoin.org/"
    },
    "youtube": {
      "0": "https://www.youtube.com/watch?v=Gc2en3nHxA4&"
    },
    "explorer": {
      "0": "http://blockchain.com/explorer",
      "1": "https://blockstream.info/",
      "2": "https://blockchair.com/bitcoin",
      "3": "https://live.blockcypher.com/btc/",
      "4": "https://btc.cryptoid.info/btc/"
    },
    "facebook": {
      "0": "https://www.facebook.com/bitcoins/"
    },
    "source_code": {
      "0": "https://github.com/bitcoin/bitcoin"
    }
  },
  "Thumbnail": "https://finage.s3.eu-west-2.amazonaws.com/cryptocurrency/128x128/bitcoin.png"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `Links` | object | Collection of resource links organized by type |
| `Thumbnail` | string | URL to cryptocurrency logo/icon (128x128 px) |

### Links Categories

Each category contains an array-indexed object of URLs:

| Category | Description |
|----------|-------------|
| `website` | Official website(s) |
| `source_code` | GitHub or source code repository |
| `explorer` | Blockchain explorer(s) |
| `reddit` | Reddit community |
| `facebook` | Facebook page |
| `twitter` | Twitter account |
| `youtube` | YouTube channel |
| `telegram` | Telegram group |
| `discord` | Discord server |

**Notes**:
- Each category is an object with numeric indices (`"0"`, `"1"`, etc.)
- Multiple links can exist per category (especially for explorers)
- Not all cryptocurrencies have all link types

## Section 4: Statistics

Returns market statistics and key metrics.

### Request

```
https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json&filter=Statistics
```

Or generally:
```
https://eodhd.com/api/fundamentals/{CRYPTO_TICKER}?api_token={API_TOKEN}&fmt=json&filter=Statistics
```

### Response Structure

```json
{
  "MarketCapitalization": 1379488693452.08,
  "MarketCapitalizationDiluted": 1449401615670.83,
  "CirculatingSupply": 19987050,
  "TotalSupply": 19987050,
  "MaxSupply": 21000000,
  "MarketCapDominance": 58.6798,
  "TechnicalDoc": "https://bitcoin.org/bitcoin.pdf",
  "Explorer": "https://blockchain.info/",
  "SourceCode": "https://github.com/bitcoin/bitcoin",
  "MessageBoard": "https://coinmarketcap.com/community/search/top/bitcoin",
  "LowAllTime": 0.04864654,
  "HighAllTime": 126198.06960343386
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `MarketCapitalization` | number | Current market capitalization (USD) |
| `MarketCapitalizationDiluted` | number | Fully diluted market cap (if all tokens were minted) |
| `CirculatingSupply` | number | Number of coins currently in circulation |
| `TotalSupply` | number | Total number of coins minted minus burned |
| `MaxSupply` | number | Maximum possible supply (null if unlimited) |
| `MarketCapDominance` | number | Market cap as percentage of total crypto market |
| `TechnicalDoc` | string | URL to whitepaper or technical documentation |
| `Explorer` | string | Primary blockchain explorer URL |
| `SourceCode` | string | Source code repository URL |
| `MessageBoard` | string | Community message board URL |
| `LowAllTime` | number | All-time low price (USD) |
| `HighAllTime` | number | All-time high price (USD) |

### Key Metrics Explained

**Supply Metrics**:
- **CirculatingSupply**: Currently available coins
- **TotalSupply**: Circulating + locked/reserved coins
- **MaxSupply**: Hard cap (if exists)
  - Bitcoin: 21,000,000 (fixed)
  - Ethereum: null (no hard cap)

**Market Cap Calculations**:
- **MarketCapitalization** = `CirculatingSupply × Current Price`
- **MarketCapitalizationDiluted** = `MaxSupply × Current Price`

**Market Dominance**:
- Percentage of total crypto market cap
- Bitcoin typically 40-60%
- Useful for comparing relative market position

## Filter Parameter Reference

### Single Filter Examples

```bash
# General information
&filter=General

# Technical info and developers
&filter=Tech

# Links and resources
&filter=Resources

# Market statistics
&filter=Statistics
```

### Multiple Sections

To get multiple sections, make separate API calls or request full data (response is relatively small).

## Common Use Cases

### 1. Cryptocurrency Profile

Get complete information about a cryptocurrency:

```bash
python eodhd_client.py --endpoint fundamentals --symbol BTC-USD.CC
```

**Use case**: Building crypto information pages, research.

### 2. Market Cap Analysis

Compare market caps and dominance:

```bash
curl "https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json&filter=Statistics" | jq '{MarketCapitalization, MarketCapDominance}'
```

**Use case**: Market analysis, portfolio allocation.

### 3. Supply Analysis

Check supply metrics and tokenomics:

```bash
curl "https://eodhd.com/api/fundamentals/ETH-USD.CC?api_token=demo&fmt=json&filter=Statistics" | jq '{CirculatingSupply, TotalSupply, MaxSupply}'
```

**Use case**: Tokenomics research, scarcity analysis.

### 4. Developer Information

Get development team information:

```bash
python eodhd_client.py --endpoint fundamentals --symbol BTC-USD.CC --filter Tech
```

**Use case**: Due diligence, project evaluation.

### 5. Resource Links

Get all official links and explorers:

```bash
python eodhd_client.py --endpoint fundamentals --symbol BTC-USD.CC --filter Resources
```

**Use case**: Building reference lists, verification.

### 6. Historical Price Range

Get all-time high and low:

```bash
curl "https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json&filter=Statistics" | jq '{HighAllTime, LowAllTime}'
```

**Use case**: Price context, volatility analysis.

---

# Part 2: Currency (Forex) Fundamentals

## API Endpoint

### Base URL Format

```
https://eodhd.com/api/fundamentals/{FOREX_TICKER}?api_token={API_TOKEN}&fmt=json
```

**Parameters**:
- `{FOREX_TICKER}`: Format `{BASE}{QUOTE}.FOREX` (e.g., `EURUSD.FOREX`, `GBPUSD.FOREX`)
- `{API_TOKEN}`: Your API key
- `fmt=json`: Required (JSON only format)

**Example**:
```
https://eodhd.com/api/fundamentals/EURUSD.FOREX?api_token=demo&fmt=json
```

## Data Structure

Currency pair fundamental data has **two top-level sections**:

| Section | Description | Use Filter |
|---------|-------------|------------|
| **General** | Basic currency pair information | `&filter=General` |
| **Components** | Component currencies (typically empty) | `&filter=Components` |

## Section 1: General

Returns basic currency pair information.

### Request

```
https://eodhd.com/api/fundamentals/EURUSD.FOREX?api_token=demo&fmt=json&filter=General
```

Or generally:
```
https://eodhd.com/api/fundamentals/{FOREX_TICKER}?api_token={API_TOKEN}&fmt=json&filter=General
```

### Response Structure

```json
{
  "Code": "EURUSD",
  "Type": "Currency",
  "Name": "EUR/USD",
  "Exchange": "FOREX",
  "MarketCap": null,
  "CurrencyCode": "USD",
  "CurrencyName": "US Dollar",
  "CurrencySymbol": "$",
  "CountryName": "Unknown",
  "CountryISO": "NA",
  "OpenFigi": null
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `Code` | string | Currency pair code (e.g., "EURUSD") |
| `Type` | string | Always "Currency" for forex pairs |
| `Name` | string | Formatted pair name (e.g., "EUR/USD") |
| `Exchange` | string | Always "FOREX" |
| `MarketCap` | null | Not applicable for currency pairs |
| `CurrencyCode` | string | Quote currency code (ISO 4217) |
| `CurrencyName` | string | Quote currency full name |
| `CurrencySymbol` | string | Quote currency symbol |
| `CountryName` | string | Typically "Unknown" for currency pairs |
| `CountryISO` | string | Typically "NA" for currency pairs |
| `OpenFigi` | null | Typically not available for forex |

### Understanding Currency Pairs

**Format**: `{BASE}{QUOTE}.FOREX`
- **Base currency**: First currency (e.g., EUR in EURUSD)
- **Quote currency**: Second currency (e.g., USD in EURUSD)
- **Exchange rate**: How much quote currency to buy 1 unit of base currency

**Example**:
- Pair: `EURUSD.FOREX`
- Price: 1.0850
- Meaning: 1 EUR = 1.0850 USD

**Note**: The API returns information about the **quote currency** (second currency in the pair).

## Section 2: Components

Returns component information (typically empty for currency pairs).

### Request

```
https://eodhd.com/api/fundamentals/EURUSD.FOREX?api_token=demo&fmt=json&filter=Components
```

### Response Structure

```json
{
}
```

**Note**: This section is typically empty for currency pairs. It exists for API consistency but contains no data.

## Common Use Cases

### 1. Currency Pair Information

Get basic information about a forex pair:

```bash
python eodhd_client.py --endpoint fundamentals --symbol EURUSD.FOREX
```

**Use case**: Identifying quote currency, pair verification.

### 2. Multi-Currency Portfolio

Get information about multiple currency pairs:

```bash
# EUR/USD
curl "https://eodhd.com/api/fundamentals/EURUSD.FOREX?api_token=demo&fmt=json&filter=General"

# GBP/USD
curl "https://eodhd.com/api/fundamentals/GBPUSD.FOREX?api_token=demo&fmt=json&filter=General"

# USD/JPY
curl "https://eodhd.com/api/fundamentals/USDJPY.FOREX?api_token=demo&fmt=json&filter=General"
```

**Use case**: Multi-currency exposure tracking.

### 3. Quote Currency Identification

Programmatically identify quote currency:

```python
import requests

response = requests.get(
    "https://eodhd.com/api/fundamentals/EURUSD.FOREX",
    params={"api_token": "demo", "fmt": "json", "filter": "General"}
).json()

quote_currency = response["CurrencyCode"]  # "USD"
quote_symbol = response["CurrencySymbol"]   # "$"
print(f"Quote currency: {quote_currency} ({quote_symbol})")
```

**Use case**: Currency conversion calculations, display formatting.

---

# Combined Best Practices

## For Both Cryptocurrencies and Currencies

### 1. Check the Type Field

Always verify the instrument type:

```python
import requests

response = requests.get(
    "https://eodhd.com/api/fundamentals/BTC-USD.CC",
    params={"api_token": "demo", "fmt": "json", "filter": "General"}
).json()

if response.get("Type") == "Crypto":
    # Handle cryptocurrency
    process_crypto(response)
elif response.get("Type") == "Currency":
    # Handle forex pair
    process_currency(response)
```

### 2. Handle Array-Indexed Fields (Crypto)

Many crypto fields use numeric indices:

```python
# Developers
developers = data["Tech"]["Developers"]
for idx, dev_info in developers.items():
    print(f"{idx}: {dev_info}")

# Explorer links
explorers = data["Resources"]["Links"]["explorer"]
for idx, url in explorers.items():
    print(f"Explorer {idx}: {url}")
```

### 3. Handle Null/Missing Fields

Not all fields are always present:

```python
# Cryptocurrency
max_supply = data["Statistics"].get("MaxSupply")
if max_supply is None:
    print("Unlimited supply")
else:
    print(f"Max supply: {max_supply:,.0f}")

# Currency
open_figi = data["General"].get("OpenFigi")
if open_figi is None:
    print("OpenFIGI not available")
```

### 4. Cache Data Appropriately

**Cryptocurrencies**:
- Market statistics change frequently (every few minutes)
- Cache for 5-15 minutes for Statistics
- Cache General, Tech, Resources for 24+ hours

**Currencies**:
- Fundamental data rarely changes
- Cache for 24+ hours or longer

### 5. Use Filters When Needed

For cryptocurrencies, if you only need specific sections:

```bash
# Only get statistics (most frequently changing data)
&filter=Statistics

# Only get resources (least frequently changing)
&filter=Resources
```

For currencies, the response is small enough that filtering is usually unnecessary.

## Error Handling

### Common Issues

**1. Wrong Ticker Format**

**Problem**: Using wrong format for crypto or forex
```python
# Wrong
"BTC.CC"      # Missing quote currency
"EURUSD"      # Missing .FOREX suffix

# Correct
"BTC-USD.CC"  # Crypto with quote currency
"EURUSD.FOREX" # Forex with suffix
```

**2. Invalid Crypto Pair**

**Problem**: Cryptocurrency pair doesn't exist
```json
{
  "error": "Not found"
}
```

**Solution**: Verify ticker with search endpoint or use common pairs (BTC-USD, ETH-USD).

**3. Missing Statistics Fields**

**Problem**: Not all cryptocurrencies have all statistics
**Solution**: Use `.get()` with defaults:
```python
max_supply = data["Statistics"].get("MaxSupply", "Unlimited")
dominance = data["Statistics"].get("MarketCapDominance", 0)
```

**4. Empty Components (Forex)**

**Problem**: Expecting data in Components section
**Solution**: This is normal - Components is typically empty for forex pairs.

## Rate Limits & API Costs

- **API calls per request**: 10 calls
- **Recommended cache duration**:
  - Crypto Statistics: 5-15 minutes
  - Crypto General/Tech/Resources: 24+ hours
  - Forex: 24+ hours
- **Update frequency**:
  - Crypto prices: Real-time (separate endpoint)
  - Crypto fundamentals: Daily or as changed
  - Forex fundamentals: Rarely changes

See [rate-limits.md](rate-limits.md) for optimization strategies.

## Related Documentation

- **[Fundamentals API Overview](fundamentals-api.md)** - Compare all instrument types
- **[Symbol Format](symbol-format.md)** - How to format crypto and forex tickers
- **[Exchanges](exchanges.md)** - List of supported exchanges
- **[Update Times](update-times.md)** - When data is refreshed
- **[Rate Limits](rate-limits.md)** - API quotas and optimization

## Quick Reference

### Cryptocurrency Structure

```
Crypto Fundamentals (BTC-USD.CC)
├── General
│   ├── Name
│   ├── Type ("Crypto")
│   ├── Category (coin/token)
│   ├── WebURL
│   └── Description
├── Tech
│   └── Developers (array-indexed)
├── Resources
│   ├── Links
│   │   ├── website
│   │   ├── source_code
│   │   ├── explorer
│   │   ├── reddit
│   │   ├── facebook
│   │   ├── twitter
│   │   └── [others]
│   └── Thumbnail
└── Statistics
    ├── MarketCapitalization
    ├── MarketCapitalizationDiluted
    ├── CirculatingSupply
    ├── TotalSupply
    ├── MaxSupply
    ├── MarketCapDominance
    ├── TechnicalDoc
    ├── Explorer
    ├── SourceCode
    ├── MessageBoard
    ├── LowAllTime
    └── HighAllTime
```

### Currency (Forex) Structure

```
Currency Fundamentals (EURUSD.FOREX)
├── General
│   ├── Code
│   ├── Type ("Currency")
│   ├── Name
│   ├── Exchange ("FOREX")
│   ├── CurrencyCode (quote currency)
│   ├── CurrencyName
│   ├── CurrencySymbol
│   ├── CountryName
│   ├── CountryISO
│   └── OpenFigi
└── Components (typically empty)
```

### Python Client Examples

**Cryptocurrency**:
```bash
# Get all crypto fundamentals
python eodhd_client.py --endpoint fundamentals --symbol BTC-USD.CC

# Get only statistics
python eodhd_client.py --endpoint fundamentals --symbol BTC-USD.CC --filter Statistics

# Get only resources
python eodhd_client.py --endpoint fundamentals --symbol ETH-USD.CC --filter Resources
```

**Currency**:
```bash
# Get forex pair info
python eodhd_client.py --endpoint fundamentals --symbol EURUSD.FOREX

# Get only general section
python eodhd_client.py --endpoint fundamentals --symbol GBPUSD.FOREX --filter General
```

### curl Examples

**Cryptocurrency**:
```bash
# Full data
curl "https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json"

# Market statistics only
curl "https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json&filter=Statistics"

# Extract specific fields
curl "https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json&filter=Statistics" | jq '{MarketCap: .MarketCapitalization, Dominance: .MarketCapDominance}'
```

**Currency**:
```bash
# Full data
curl "https://eodhd.com/api/fundamentals/EURUSD.FOREX?api_token=demo&fmt=json"

# General section only
curl "https://eodhd.com/api/fundamentals/EURUSD.FOREX?api_token=demo&fmt=json&filter=General"

# Extract quote currency
curl "https://eodhd.com/api/fundamentals/EURUSD.FOREX?api_token=demo&fmt=json&filter=General" | jq '{QuoteCurrency: .CurrencyCode, Symbol: .CurrencySymbol}'
```

### Popular Symbols for Testing

**Cryptocurrencies**:
- `BTC-USD.CC` - Bitcoin
- `ETH-USD.CC` - Ethereum
- `BNB-USD.CC` - Binance Coin
- `ADA-USD.CC` - Cardano
- `SOL-USD.CC` - Solana
- `XRP-USD.CC` - Ripple
- `DOT-USD.CC` - Polkadot

**Currency Pairs**:
- `EURUSD.FOREX` - Euro / US Dollar
- `GBPUSD.FOREX` - British Pound / US Dollar
- `USDJPY.FOREX` - US Dollar / Japanese Yen
- `AUDUSD.FOREX` - Australian Dollar / US Dollar
- `USDCAD.FOREX` - US Dollar / Canadian Dollar
- `USDCHF.FOREX` - US Dollar / Swiss Franc

## Summary: Key Differences

| Feature | Cryptocurrency | Currency (Forex) |
|---------|---------------|------------------|
| **Type value** | "Crypto" | "Currency" |
| **Ticker format** | `{BASE}-{QUOTE}.CC` | `{BASE}{QUOTE}.FOREX` |
| **Sections** | General, Tech, Resources, Statistics | General, Components |
| **Response size** | Small-Medium (5-20 KB) | Very Small (< 2 KB) |
| **Key data** | Market cap, supply, developers, resources | Quote currency info |
| **Update frequency** | Statistics: frequent; Others: rare | Rarely changes |
| **Use filter** | Optional (response is small) | Usually unnecessary |
| **Complexity** | Medium (array-indexed fields) | Very simple |

---

**Last Updated**: February 2026
**API Version**: Current
**Maintained By**: EODHD Skills Team
