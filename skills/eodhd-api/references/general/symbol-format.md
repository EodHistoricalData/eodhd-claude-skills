# EODHD Symbol Format Guide

This document explains how to format instrument identifiers correctly for EODHD API requests.

## Overview

EODHD uses a standardized symbol format across all endpoints:

```
{TICKER}.{EXCHANGE_CODE}
```

**Examples**:
- `AAPL.US` - Apple Inc. on US exchanges
- `BMW.XETRA` - BMW on German XETRA
- `EURUSD.FOREX` - EUR/USD currency pair
- `BTC-USD.CC` - Bitcoin in USD

## General Symbol Format

### Basic Structure

```
TICKER.EXCHANGE
```

**Rules**:
1. Ticker and exchange code are separated by a dot (`.`)
2. Both parts are case-sensitive (use uppercase)
3. No spaces allowed
4. Special characters in ticker require URL encoding

### Component Details

**Ticker Part**:
- Usually 1-5 characters
- Can contain letters, numbers, hyphens
- Examples: `AAPL`, `MSFT`, `BRK-B`, `GSPC`

**Exchange Part**:
- 2-6 character exchange code
- Identifies the market/exchange
- Examples: `US`, `XETRA`, `LSE`, `FOREX`

## Exchange-Specific Formats

### US Stocks (US)

**Format**: `{TICKER}.US`

**Examples**:
- `AAPL.US` - Apple Inc.
- `MSFT.US` - Microsoft
- `GOOGL.US` - Alphabet Class A
- `BRK-B.US` - Berkshire Hathaway Class B (hyphen replaces dot)
- `BRK-A.US` - Berkshire Hathaway Class A (hyphen replaces dot)

**Notes**:
- US code covers NYSE, NASDAQ, and AMEX
- Class shares use hyphens: `BRK-A`, `BRK-B`, `BF-B`
- Preferred shares: `BAC-PL`, `JPM-PC`
- Only ONE dot allowed in the full ticker string (between ticker code and exchange code). If the original ticker contains dots (e.g., `BRK.A` on the exchange), replace them with hyphens: `BRK-A.US`

### European Stocks

**Format**: `{TICKER}.{EXCHANGE}`

**Common European Exchanges**:

| Exchange Code | Name | Examples |
|--------------|------|----------|
| LSE | London Stock Exchange | `BP.LSE`, `VOD.LSE`, `HSBA.LSE` |
| XETRA | Deutsche Börse | `BMW.XETRA`, `SAP.XETRA`, `SIE.XETRA` |
| PA | Euronext Paris | `AI.PA`, `MC.PA`, `OR.PA` |
| AS | Euronext Amsterdam | `ASML.AS`, `PHIA.AS` |
| SW | SIX Swiss Exchange | `NESN.SW`, `NOVN.SW`, `ROG.SW` |

**Special Cases**:
- German stocks on Frankfurt: `BMW.F` (different from `BMW.XETRA`)
- ADRs trade on US exchanges: use `.US` suffix

### Asian Stocks

**Format**: `{TICKER}.{EXCHANGE}`

**Common Asian Exchanges**:

| Exchange Code | Name | Ticker Format | Examples |
|--------------|------|---------------|----------|
| HK | Hong Kong | 4-digit number | `0700.HK` (Tencent), `9988.HK` (Alibaba) |
| SHG | Shanghai | 6-digit number | `600519.SHG` (Moutai) |
| SHE | Shenzhen | 6-digit number | `000001.SHE` |
| KO | Korea Stock Exchange | 6-digit number | `005930.KO` (Samsung) |

**Notes**:
- Hong Kong includes leading zeros: `0700.HK` not `700.HK`
- Chinese A-shares: Shanghai (SHG) or Shenzhen (SHE)

### Canadian Stocks

**Format**: `{TICKER}.{EXCHANGE}`

**Canadian Exchanges**:
- `TO` - Toronto Stock Exchange: `SHOP.TO`, `RY.TO`
- `V` - TSX Venture: `GOLD.V`

### ETFs

**Format**: Same as stocks - `{TICKER}.{EXCHANGE}`

**Examples**:
- `SPY.US` - SPDR S&P 500 ETF
- `QQQ.US` - Invesco QQQ Trust
- `VWCE.XETRA` - Vanguard FTSE All-World UCITS ETF
- `IWDA.AS` - iShares Core MSCI World

**Notes**:
- Use the primary listing exchange
- Some ETFs trade on multiple exchanges

## Special Asset Classes

### Forex Pairs

**Format**: `{BASE}{QUOTE}.FOREX`

**Important**: No separator between base and quote currency codes

**Examples**:
- `EURUSD.FOREX` - Euro/US Dollar
- `GBPUSD.FOREX` - British Pound/US Dollar
- `USDJPY.FOREX` - US Dollar/Japanese Yen
- `AUDUSD.FOREX` - Australian Dollar/US Dollar
- `USDCAD.FOREX` - US Dollar/Canadian Dollar
- `USDCHF.FOREX` - US Dollar/Swiss Franc

**Common Currency Codes**:
- USD (US Dollar), EUR (Euro), GBP (British Pound)
- JPY (Japanese Yen), CHF (Swiss Franc), CAD (Canadian Dollar)
- AUD (Australian Dollar), NZD (New Zealand Dollar)
- CNY (Chinese Yuan), INR (Indian Rupee)

**Cross Pairs**:
- `EURGBP.FOREX` - Euro/British Pound
- `EURJPY.FOREX` - Euro/Japanese Yen
- `GBPJPY.FOREX` - British Pound/Japanese Yen

### Cryptocurrencies

**Format**: `{CRYPTO}-{QUOTE}.CC`

**Important**: Hyphen separator between crypto and quote currency

**Examples**:
- `BTC-USD.CC` - Bitcoin/US Dollar
- `ETH-USD.CC` - Ethereum/US Dollar
- `BNB-USD.CC` - Binance Coin/US Dollar
- `XRP-USD.CC` - Ripple/US Dollar
- `ADA-USD.CC` - Cardano/US Dollar
- `SOL-USD.CC` - Solana/US Dollar
- `DOGE-USD.CC` - Dogecoin/US Dollar

**Other Quote Currencies**:
- `BTC-EUR.CC` - Bitcoin/Euro
- `ETH-BTC.CC` - Ethereum/Bitcoin
- `BTC-GBP.CC` - Bitcoin/British Pound

**Stablecoins**:
- `USDT-USD.CC` - Tether/US Dollar
- `USDC-USD.CC` - USD Coin/US Dollar

### Government Bonds

**Format**: `{INSTRUMENT_CODE}.GBOND`

**Government Bond Yields**:
- `US10Y.GBOND` - US 10-year Treasury yield
- `US2Y.GBOND` - US 2-year Treasury yield
- `US30Y.GBOND` - US 30-year Treasury yield
- `DE10Y.GBOND` - German 10-year Bund yield
- `GB10Y.GBOND` - UK 10-year Gilt yield
- `JP10Y.GBOND` - Japan 10-year JGB yield

### Indices

**Format**: `{INDEX_CODE}.INDX`

**US Indices**:
- `GSPC.INDX` - S&P 500
- `DJI.INDX` - Dow Jones Industrial Average
- `IXIC.INDX` - NASDAQ Composite
- `VIX.INDX` - CBOE Volatility Index

**International Indices**:
- `GDAXI.INDX` - DAX (Germany)
- `FCHI.INDX` - CAC 40 (France)
- `N225.INDX` - Nikkei 225 (Japan)
- `HSI.INDX` - Hang Seng (Hong Kong)
- `SENSEX.INDX` - BSE Sensex (India)

## Special Characters & Encoding

### Characters in Tickers

**Hyphens** (`-`):
- Used for share classes: `BRK-B.US`
- Used in crypto pairs: `BTC-USD.CC`
- No encoding needed in URLs

**Dots** (`.`) in Tickers:
- Dots are **NOT allowed** in the ticker part — only ONE dot in the full string (between ticker and exchange)
- If the original exchange ticker contains a dot (e.g., `BRK.A`), replace it with a hyphen: `BRK-A.US`
- See the "Handling Dots in Ticker Symbols" section in `stock-types-ticker-suffixes-guide.md`

**Carets** (`^`):
- Some tickers use caret prefix
- URL encode as `%5E` in API requests

### URL Encoding

When constructing API URLs, special characters should be encoded:

| Character | URL Encoded | Example |
|-----------|-------------|---------|
| `^` | `%5E` | `%5EAEX.AS` |
| `&` | `%26` | `A%26B.US` |
| Space | `%20` | (avoid spaces) |
| `/` | `%2F` | (avoid in tickers) |

> **Note**: Dots in ticker symbols should be replaced with hyphens (`BRK.A` → `BRK-A.US`), not URL-encoded.

**Important**: The `&` character is a URL query parameter delimiter. If a ticker name contains `&`, the part after `&` will be interpreted as a separate query parameter. Always encode `&` as `%26` in ticker names.

**Note**: Most HTTP libraries handle URL encoding automatically.

## Finding the Correct Symbol

### Method 1: Symbol Search API

Use the search endpoint to find symbols:

```bash
curl "https://eodhd.com/api/search/Apple?api_token=YOUR_TOKEN"
```

Returns all matching symbols across exchanges.

### Method 2: Exchange Symbol List

Get all symbols for a specific exchange:

```bash
curl "https://eodhd.com/api/exchange-symbol-list/US?api_token=YOUR_TOKEN"
```

### Method 3: Check Exchange Details

Some exchanges provide symbol conventions:

```bash
curl "https://eodhd.com/api/exchanges/US?api_token=YOUR_TOKEN"
```

## Common Mistakes & Solutions

### Mistake 1: Missing Exchange Code
❌ `AAPL`
✅ `AAPL.US`

**Solution**: Always include the exchange suffix.

### Mistake 2: Wrong Exchange Code
❌ `AAPL.NASDAQ`
✅ `AAPL.US`

**Solution**: Use standard exchange codes (US, not NASDAQ/NYSE).

### Mistake 3: Incorrect Forex Format
❌ `EUR-USD.FOREX`
❌ `EUR/USD.FOREX`
✅ `EURUSD.FOREX`

**Solution**: No separator in forex pairs.

### Mistake 4: Wrong Crypto Format
❌ `BTCUSD.CC`
❌ `BTC_USD.CC`
✅ `BTC-USD.CC`

**Solution**: Use hyphen separator in crypto pairs.

### Mistake 5: Lowercase Symbols
❌ `aapl.us`
✅ `AAPL.US`

**Solution**: Use uppercase for both ticker and exchange.

### Mistake 6: Wrong Leading Zeros
❌ `700.HK` (Hong Kong)
✅ `0700.HK`

**Solution**: Maintain leading zeros for numeric tickers.

## Symbol Validation

### Valid Symbol Pattern

Regular expression for basic validation:

```regex
^[A-Z0-9\-\^]+\.(US|LSE|XETRA|PA|AS|...|FOREX|CC|MONEY|GBOND|EUFUND|INDX)$
```

> **Note**: Dots are not allowed in the ticker part — only hyphens, letters, numbers, and carets.

### Validation Steps

1. **Check format**: Contains exactly one dot separating ticker and exchange
2. **Verify exchange code**: Exists in supported exchanges list
3. **Check ticker rules**: Follows exchange-specific conventions
4. **Test with API**: Use search endpoint to verify

## Symbol Aliases & Alternatives

Some instruments have multiple valid symbols:

**S&P 500**:
- `GSPC.INDX` - Direct index
- `SPY.US` - ETF tracking the index

**Berkshire Hathaway Class A**:
- `BRK-A.US` - Dot replaced with hyphen (original exchange ticker: `BRK.A`)

**Dual Listings**:
- Companies listed on multiple exchanges have multiple symbols
- Example: Alibaba
  - `BABA.US` - US ADR on NYSE
  - `9988.HK` - Hong Kong listing

## Symbol Changes

Symbols may change due to:
- Corporate actions (mergers, acquisitions)
- Rebranding
- Exchange migrations
- Ticker symbol changes

**Use the Symbol Change History API**:
```bash
curl "https://eodhd.com/api/symbol-change-history?api_token=YOUR_TOKEN"
```

## Best Practices

1. **Always use full format**: Include exchange suffix
2. **Validate before use**: Test unknown symbols with search API
3. **Cache symbol mappings**: Reduce API calls for known symbols
4. **Handle delisted symbols**: Check for null/error responses
5. **Monitor symbol changes**: Subscribe to symbol change notifications
6. **Use canonical format**: Prefer standard formats over aliases
7. **Document assumptions**: Note which exchange you're using
8. **Test with examples**: Verify format with working examples

## Quick Reference

| Asset Type | Format | Example        |
|-----------|--------|----------------|
| US Stock | `{TICKER}.US` | `AAPL.US`      |
| European Stock | `{TICKER}.{EXCHANGE}` | `BMW.XETRA`    |
| Asian Stock | `{TICKER}.{EXCHANGE}` | `0700.HK`      |
| ETF | `{TICKER}.{EXCHANGE}` | `SPY.US`       |
| Forex | `{BASE}{QUOTE}.FOREX` | `EURUSD.FOREX` |
| Crypto | `{CRYPTO}-{QUOTE}.CC` | `BTC-USD.CC`   |
| Government Bond | `{CODE}.GBOND` | `US10Y.GBOND`  |
| Index | `{CODE}.INDX` | `GSPC.INDX`    |
