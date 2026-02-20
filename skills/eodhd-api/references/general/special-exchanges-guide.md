# Special Exchanges Guide - Complete Reference

**Purpose**: Working with exchanges not listed in the standard Exchanges API
**Last Updated**: 2024-11-27

---

## Table of Contents

1. [Overview](#overview)
2. [Special Exchange Codes](#special-exchange-codes)
3. [Finding Tickers](#finding-tickers)
4. [Indices (INDX)](#indices-indx)
5. [Forex (FOREX)](#forex-forex)
6. [Cryptocurrency (CC)](#cryptocurrency-cc)
7. [Funds (EUFUND, MONEY)](#funds-eufund-money)
8. [Government Bonds (GBOND)](#government-bonds-gbond)
9. [Hong Kong Exchange (HK)](#hong-kong-exchange-hk)
10. [Usage in APIs](#usage-in-apis)
11. [Common Tickers Reference](#common-tickers-reference)
12. [Best Practices](#best-practices)

---

## Overview

### What Are Special Exchanges?

Some exchanges are **not included** in the standard Exchanges API list (`/exchanges` endpoint), but their tickers are fully supported across EODHD APIs.

**Standard Exchanges** (listed in `/exchanges`):
- US, NYSE, LSE, TSX, etc.
- Traditional stock exchanges with trading hours
- Retrieved via: `https://eodhd.com/api/exchanges`

**Special Exchanges** (not in `/exchanges`):
- INDX (Indices)
- FOREX (Foreign Exchange)
- CC (Cryptocurrency)
- EUFUND (European Funds)
- MONEY (Money Market Funds)
- GBOND (Government Bonds)
- HK (Hong Kong Exchange)

### Why Separate?

**Indices**: Not tradable securities, just calculated values
**Forex**: 24/7 markets, no central exchange
**Crypto**: Decentralized, 24/7 trading
**Funds/Bonds**: Different trading mechanics than stocks
**HK**: Special handling for Hong Kong market

### Key Differences

| Aspect | Standard Exchanges | Special Exchanges |
|--------|-------------------|-------------------|
| **Listed in `/exchanges`** | ✅ Yes | ❌ No |
| **Has Trading Hours** | ✅ Yes | ⚠️ Varies |
| **Tickers Available** | Via `/exchange-symbol-list/{CODE}` | Via `/exchange-symbol-list/{CODE}` |
| **EOD Data Available** | ✅ Yes | ✅ Yes |
| **Intraday Data** | ✅ Yes (most) | ⚠️ Varies |

**Important**: You can use tickers from special exchanges **directly** in all relevant APIs (EOD, Intraday, Technical Indicators, etc.).

---

## Special Exchange Codes

### Complete List

| Exchange Code | Description | Example Tickers | Data Available |
|--------------|-------------|-----------------|----------------|
| **INDX** | Global Indices | GSPC.INDX (S&P 500), NDX.INDX (Nasdaq 100) | EOD, Intraday |
| **FOREX** | Foreign Exchange Pairs | EURUSD.FOREX, GBPJPY.FOREX | EOD, Intraday |
| **CC** | Cryptocurrency | BTC-USD.CC, ETH-USD.CC | EOD, Intraday |
| **EUFUND** | European Funds | Various mutual funds | EOD, Fundamentals |
| **MONEY** | Money Market Funds | Money market instruments | EOD |
| **GBOND** | Government Bonds | Government debt securities | EOD |
| **HK** | Hong Kong Exchange | 0700.HK (Tencent), 0941.HK (China Mobile) | EOD, Fundamentals |

### Ticker Format

**Standard Format**: `{SYMBOL}.{EXCHANGE_CODE}`

**Examples**:
```
GSPC.INDX           - S&P 500 Index
EURUSD.FOREX        - EUR/USD Forex Pair
BTC-USD.CC          - Bitcoin to USD
IE00B4L5Y983.EUFUND - iShares Core MSCI World UCITS ETF
US10Y.GBOND         - US 10-Year Treasury
0700.HK             - Tencent Holdings (Hong Kong)
```

---

## Finding Tickers

### Exchange Symbol List API

**Endpoint**: `/exchange-symbol-list/{EXCHANGE_CODE}`

**URL Format**:
```
https://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}?api_token={YOUR_API_TOKEN}&fmt=json
```

**Parameters**:
- `{EXCHANGE_CODE}`: One of the special exchange codes (INDX, FOREX, CC, etc.)
- `api_token`: Your EODHD API key
- `fmt`: Output format (`json` or `csv`)

### Response Format

**JSON Response Structure**:
```json
[
  {
    "Code": "GSPC",
    "Name": "S&P 500 Index",
    "Country": "USA",
    "Exchange": "INDX",
    "Currency": "USD",
    "Type": "INDEX",
    "Isin": null
  },
  {
    "Code": "NDX",
    "Name": "NASDAQ 100 Index",
    "Country": "USA",
    "Exchange": "INDX",
    "Currency": "USD",
    "Type": "INDEX",
    "Isin": null
  }
]
```

**Field Descriptions**:
- `Code`: Ticker symbol (use with `.EXCHANGE` suffix)
- `Name`: Full name of the instrument
- `Country`: Country of origin
- `Exchange`: Exchange code (INDX, FOREX, CC, etc.)
- `Currency`: Trading currency
- `Type`: Instrument type (INDEX, FOREX, CRYPTO, etc.)
- `Isin`: ISIN code (if applicable, often null for special exchanges)

### Python Example

```python
import requests
import pandas as pd

def get_special_exchange_tickers(exchange_code, api_token):
    """
    Fetch all tickers for a special exchange.

    Args:
        exchange_code: Exchange code (e.g., 'INDX', 'FOREX', 'CC')
        api_token: Your EODHD API token

    Returns:
        DataFrame with ticker information
    """
    url = f"https://eodhd.com/api/exchange-symbol-list/{exchange_code}"
    params = {
        "api_token": api_token,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data)
    return df

# Example: Get all indices
indices_df = get_special_exchange_tickers('INDX', 'your_api_token')
print(f"Total indices: {len(indices_df)}")
print(indices_df.head())

# Search for specific index
sp500 = indices_df[indices_df['Code'] == 'GSPC']
print(f"\nS&P 500: {sp500['Name'].values[0]}")
print(f"Full ticker: GSPC.INDX")
```

### Search by Name

```python
def search_ticker_by_name(exchange_code, search_term, api_token):
    """
    Search for tickers by name.

    Args:
        exchange_code: Exchange code (INDX, FOREX, CC, etc.)
        search_term: Search string (case-insensitive)
        api_token: Your API token

    Returns:
        DataFrame with matching tickers
    """
    df = get_special_exchange_tickers(exchange_code, api_token)

    # Case-insensitive search in Name field
    results = df[df['Name'].str.contains(search_term, case=False, na=False)]

    return results

# Example: Find all S&P indices
sp_indices = search_ticker_by_name('INDX', 'S&P', 'your_api_token')
print("S&P Indices:")
for idx, row in sp_indices.iterrows():
    print(f"  {row['Code']}.INDX - {row['Name']}")
```

---

## Indices (INDX)

### Overview

**Exchange Code**: `INDX`

**Description**: Global stock market indices from around the world.

**Coverage**:
- US indices (S&P 500, Nasdaq, Dow Jones)
- European indices (DAX, CAC)
- Asian indices (Nikkei, Hang Seng, Shanghai)
- Sector indices
- Custom indices

### Finding Indices

**Request**:
```bash
curl "https://eodhd.com/api/exchange-symbol-list/INDX?api_token=demo&fmt=json"
```

**Response Sample**:
```json
[
  {
    "Code": "GSPC",
    "Name": "S&P 500 Index",
    "Country": "USA",
    "Exchange": "INDX",
    "Currency": "USD",
    "Type": "INDEX",
    "Isin": null
  },
  {
    "Code": "NDX",
    "Name": "NASDAQ 100 Index",
    "Country": "USA",
    "Exchange": "INDX",
    "Currency": "USD",
    "Type": "INDEX",
    "Isin": null
  },
  {
    "Code": "DJI",
    "Name": "Dow Jones Industrial Average",
    "Country": "USA",
    "Exchange": "INDX",
    "Currency": "USD",
    "Type": "INDEX",
    "Isin": null
  },
  {
    "Code": "N225",
    "Name": "Nikkei 225",
    "Country": "Japan",
    "Exchange": "INDX",
    "Currency": "JPY",
    "Type": "INDEX",
    "Isin": null
  }
]
```

### Common Indices

**US Indices**:
```
GSPC.INDX     - S&P 500
NDX.INDX      - NASDAQ 100
DJI.INDX      - Dow Jones Industrial Average
VIX.INDX      - CBOE Volatility Index
```

**European Indices**:
```
GDAXI.INDX    - DAX (Germany)
FCHI.INDX     - CAC 40 (France)
STOXX50E.INDX - EURO STOXX 50
```

**Asian Indices**:
```
N225.INDX     - Nikkei 225 (Japan)
HSI.INDX      - Hang Seng (Hong Kong)
000001.INDX   - Shanghai Composite (China)
SENSEX.INDX   - BSE Sensex (India)
```

### Usage Example

**Get EOD Data**:
```bash
# S&P 500 daily data
curl "https://eodhd.com/api/eod/GSPC.INDX?api_token=demo&from=2023-01-01&to=2023-12-31&fmt=json"
```

**Python Example**:
```python
import requests

def get_index_data(index_code, from_date, to_date, api_token):
    """
    Fetch historical data for an index.

    Args:
        index_code: Index code (e.g., 'GSPC', 'NDX')
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        api_token: Your API token

    Returns:
        JSON data with OHLC values
    """
    ticker = f"{index_code}.INDX"
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "from": from_date,
        "to": to_date,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    return response.json()

# Example: S&P 500 data
sp500_data = get_index_data('GSPC', '2023-01-01', '2023-12-31', 'your_api_token')
print(f"Retrieved {len(sp500_data)} trading days")
print(f"S&P 500 on 2023-12-31: {sp500_data[-1]['close']}")
```

### Technical Analysis on Indices

```python
# Calculate moving average on S&P 500
url = "https://eodhd.com/api/technical/GSPC.INDX"
params = {
    "function": "sma",
    "period": 200,
    "api_token": "your_api_token",
    "fmt": "json"
}

sma_data = requests.get(url, params=params).json()
print(f"S&P 500 200-day SMA: {sma_data[-1]['sma']}")
```

---

## Forex (FOREX)

### Overview

**Exchange Code**: `FOREX`

**Description**: Foreign exchange currency pairs.

**Coverage**:
- Major pairs (EUR/USD, GBP/USD, USD/JPY)
- Minor pairs (EUR/GBP, AUD/NZD)
- Exotic pairs (USD/TRY, EUR/ZAR)
- Cross rates

**Trading**: 24/7 (Sunday evening to Friday evening)

### Finding Forex Pairs

**Request**:
```bash
curl "https://eodhd.com/api/exchange-symbol-list/FOREX?api_token=demo&fmt=json"
```

**Response Sample**:
```json
[
  {
    "Code": "EURUSD",
    "Name": "EUR/USD",
    "Country": null,
    "Exchange": "FOREX",
    "Currency": "USD",
    "Type": "CURRENCY",
    "Isin": null
  },
  {
    "Code": "GBPUSD",
    "Name": "GBP/USD",
    "Country": null,
    "Exchange": "FOREX",
    "Currency": "USD",
    "Type": "CURRENCY",
    "Isin": null
  },
  {
    "Code": "USDJPY",
    "Name": "USD/JPY",
    "Country": null,
    "Exchange": "FOREX",
    "Currency": "JPY",
    "Type": "CURRENCY",
    "Isin": null
  }
]
```

### Common Forex Pairs

**Major Pairs**:
```
EURUSD.FOREX  - Euro / US Dollar
GBPUSD.FOREX  - British Pound / US Dollar
USDJPY.FOREX  - US Dollar / Japanese Yen
USDCHF.FOREX  - US Dollar / Swiss Franc
AUDUSD.FOREX  - Australian Dollar / US Dollar
USDCAD.FOREX  - US Dollar / Canadian Dollar
NZDUSD.FOREX  - New Zealand Dollar / US Dollar
```

**Cross Pairs**:
```
EURGBP.FOREX  - Euro / British Pound
EURJPY.FOREX  - Euro / Japanese Yen
GBPJPY.FOREX  - British Pound / Japanese Yen
AUDJPY.FOREX  - Australian Dollar / Japanese Yen
```

**Exotic Pairs**:
```
USDTRY.FOREX  - US Dollar / Turkish Lira
USDZAR.FOREX  - US Dollar / South African Rand
USDMXN.FOREX  - US Dollar / Mexican Peso
USDBRL.FOREX  - US Dollar / Brazilian Real
```

### Usage Example

**Get EOD Data**:
```bash
# EUR/USD daily data
curl "https://eodhd.com/api/eod/EURUSD.FOREX?api_token=demo&from=2023-01-01&to=2023-12-31&fmt=json"
```

**Python Example**:
```python
def get_forex_data(pair_code, from_date, to_date, api_token):
    """
    Fetch forex pair historical data.

    Args:
        pair_code: Forex pair code (e.g., 'EURUSD', 'GBPJPY')
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        api_token: Your API token

    Returns:
        JSON data with exchange rates
    """
    ticker = f"{pair_code}.FOREX"
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "from": from_date,
        "to": to_date,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    return response.json()

# Example: EUR/USD data
eurusd_data = get_forex_data('EURUSD', '2023-01-01', '2023-12-31', 'your_api_token')
print(f"EUR/USD on 2023-12-31: {eurusd_data[-1]['close']}")
```

### Intraday Forex Data

```python
# Get 5-minute EUR/USD data
url = "https://eodhd.com/api/intraday/EURUSD.FOREX"
params = {
    "interval": "5m",
    "api_token": "your_api_token",
    "fmt": "json"
}

intraday_data = requests.get(url, params=params).json()
print(f"Latest EUR/USD rate: {intraday_data[-1]['close']}")
```

---

## Cryptocurrency (CC)

### Overview

**Exchange Code**: `CC`

**Description**: Cryptocurrency pairs.

**Coverage**:
- Major cryptocurrencies (Bitcoin, Ethereum, Litecoin)
- Altcoins (Ripple, Cardano, Polkadot)
- Stablecoins (USDT, USDC)
- Pairs in USD, EUR, BTC

**Trading**: 24/7/365

### Finding Crypto Pairs

**Request**:
```bash
curl "https://eodhd.com/api/exchange-symbol-list/CC?api_token=demo&fmt=json"
```

**Response Sample**:
```json
[
  {
    "Code": "BTC-USD",
    "Name": "Bitcoin USD",
    "Country": null,
    "Exchange": "CC",
    "Currency": "USD",
    "Type": "CRYPTOCURRENCY",
    "Isin": null
  },
  {
    "Code": "ETH-USD",
    "Name": "Ethereum USD",
    "Country": null,
    "Exchange": "CC",
    "Currency": "USD",
    "Type": "CRYPTOCURRENCY",
    "Isin": null
  },
  {
    "Code": "LTC-USD",
    "Name": "Litecoin USD",
    "Country": null,
    "Exchange": "CC",
    "Currency": "USD",
    "Type": "CRYPTOCURRENCY",
    "Isin": null
  }
]
```

### Common Crypto Tickers

**Major Cryptocurrencies (USD Pairs)**:
```
BTC-USD.CC    - Bitcoin to USD
ETH-USD.CC    - Ethereum to USD
LTC-USD.CC    - Litecoin to USD
XRP-USD.CC    - Ripple to USD
BCH-USD.CC    - Bitcoin Cash to USD
ADA-USD.CC    - Cardano to USD
DOT-USD.CC    - Polkadot to USD
LINK-USD.CC   - Chainlink to USD
```

**Stablecoins**:
```
USDT-USD.CC   - Tether to USD
USDC-USD.CC   - USD Coin to USD
BUSD-USD.CC   - Binance USD to USD
DAI-USD.CC    - Dai to USD
```

**BTC Pairs**:
```
ETH-BTC.CC    - Ethereum to Bitcoin
LTC-BTC.CC    - Litecoin to Bitcoin
XRP-BTC.CC    - Ripple to Bitcoin
```

### Usage Example

**Get EOD Data**:
```bash
# Bitcoin daily data
curl "https://eodhd.com/api/eod/BTC-USD.CC?api_token=demo&from=2023-01-01&to=2023-12-31&fmt=json"
```

**Python Example**:
```python
def get_crypto_data(crypto_code, from_date, to_date, api_token):
    """
    Fetch cryptocurrency historical data.

    Args:
        crypto_code: Crypto pair code (e.g., 'BTC-USD', 'ETH-USD')
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        api_token: Your API token

    Returns:
        JSON data with prices
    """
    ticker = f"{crypto_code}.CC"
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "from": from_date,
        "to": to_date,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    return response.json()

# Example: Bitcoin data
btc_data = get_crypto_data('BTC-USD', '2023-01-01', '2023-12-31', 'your_api_token')
print(f"Bitcoin on 2023-12-31: ${btc_data[-1]['close']:,.2f}")

# Calculate 2023 return
start_price = btc_data[0]['close']
end_price = btc_data[-1]['close']
btc_return = ((end_price / start_price) - 1) * 100
print(f"Bitcoin 2023 return: {btc_return:.2f}%")
```

### Crypto Fundamentals

```python
# Get Bitcoin fundamentals (supply, market cap, etc.)
url = "https://eodhd.com/api/fundamentals/BTC-USD.CC"
params = {
    "api_token": "your_api_token",
    "fmt": "json"
}

fundamentals = requests.get(url, params=params).json()
print(f"Bitcoin Market Cap: ${fundamentals['General']['MarketCapitalization']:,.0f}")
print(f"Circulating Supply: {fundamentals['Statistics']['CirculatingSupply']:,.0f}")
```

---

## Funds (EUFUND, MONEY)

### Overview

**Exchange Codes**:
- `EUFUND` - European Funds (UCITS, mutual funds)
- `MONEY` - Money Market Funds

**Description**: Mutual funds, ETFs, and money market instruments.

### Finding Funds

**Request**:
```bash
# European Funds
curl "https://eodhd.com/api/exchange-symbol-list/EUFUND?api_token=demo&fmt=json"

# Money Market Funds
curl "https://eodhd.com/api/exchange-symbol-list/MONEY?api_token=demo&fmt=json"
```

**Response Sample (EUFUND)**:
```json
[
  {
    "Code": "IE00B4L5Y983",
    "Name": "iShares Core MSCI World UCITS ETF USD (Acc)",
    "Country": "Ireland",
    "Exchange": "EUFUND",
    "Currency": "USD",
    "Type": "FUND",
    "Isin": "IE00B4L5Y983"
  },
  {
    "Code": "LU0392494562",
    "Name": "ComStage MSCI World TRN UCITS ETF",
    "Country": "Luxembourg",
    "Exchange": "EUFUND",
    "Currency": "EUR",
    "Type": "FUND",
    "Isin": "LU0392494562"
  }
]
```

### Common Fund Examples

**European UCITS ETFs**:
```
IE00B4L5Y983.EUFUND  - iShares Core MSCI World UCITS ETF
LU0392494562.EUFUND  - ComStage MSCI World TRN UCITS ETF
IE00B5BMR087.EUFUND  - iShares Core S&P 500 UCITS ETF
```

### Usage Example

```python
def get_fund_data(isin_code, from_date, to_date, api_token):
    """
    Fetch fund NAV (Net Asset Value) data.

    Args:
        isin_code: Fund ISIN code
        from_date: Start date
        to_date: End date
        api_token: Your API token

    Returns:
        JSON data with NAV prices
    """
    ticker = f"{isin_code}.EUFUND"
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "from": from_date,
        "to": to_date,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    return response.json()

# Example: iShares MSCI World fund
fund_data = get_fund_data('IE00B4L5Y983', '2023-01-01', '2023-12-31', 'your_api_token')
print(f"Fund NAV on 2023-12-31: ${fund_data[-1]['close']:.2f}")
```

---

## Government Bonds (GBOND)

### Overview

**Exchange Code**: `GBOND` - Government Bonds (treasuries, sovereign debt)

**Description**: Government bond yield data.

### Finding Bonds

**Request**:
```bash
# Government Bonds
curl "https://eodhd.com/api/exchange-symbol-list/GBOND?api_token=demo&fmt=json"
```

**Response Sample (GBOND)**:
```json
[
  {
    "Code": "US10Y",
    "Name": "United States 10-Year Bond Yield",
    "Country": "USA",
    "Exchange": "GBOND",
    "Currency": "USD",
    "Type": "BOND",
    "Isin": null
  },
  {
    "Code": "US30Y",
    "Name": "United States 30-Year Bond Yield",
    "Country": "USA",
    "Exchange": "GBOND",
    "Currency": "USD",
    "Type": "BOND",
    "Isin": null
  }
]
```

### Common Bond Tickers

**US Treasury Yields**:
```
US1M.GBOND   - US 1-Month Treasury Yield
US3M.GBOND   - US 3-Month Treasury Yield
US6M.GBOND   - US 6-Month Treasury Yield
US1Y.GBOND   - US 1-Year Treasury Yield
US2Y.GBOND   - US 2-Year Treasury Yield
US5Y.GBOND   - US 5-Year Treasury Yield
US10Y.GBOND  - US 10-Year Treasury Yield
US30Y.GBOND  - US 30-Year Treasury Yield
```

**International Government Bonds**:
```
DE10Y.GBOND  - Germany 10-Year Bund Yield
GB10Y.GBOND  - UK 10-Year Gilt Yield
JP10Y.GBOND  - Japan 10-Year JGB Yield
```

### Usage Example

```python
def get_bond_yield_data(bond_code, from_date, to_date, api_token):
    """
    Fetch bond yield data.

    Args:
        bond_code: Bond code (e.g., 'US10Y', 'DE10Y')
        from_date: Start date
        to_date: End date
        api_token: Your API token

    Returns:
        JSON data with yields
    """
    ticker = f"{bond_code}.GBOND"
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "from": from_date,
        "to": to_date,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    return response.json()

# Example: US 10-Year Treasury
us10y_data = get_bond_yield_data('US10Y', '2023-01-01', '2023-12-31', 'your_api_token')
print(f"US 10Y Yield on 2023-12-31: {us10y_data[-1]['close']:.2f}%")

# Yield curve analysis
us2y = get_bond_yield_data('US2Y', '2023-12-31', '2023-12-31', 'your_api_token')[0]['close']
us10y = get_bond_yield_data('US10Y', '2023-12-31', '2023-12-31', 'your_api_token')[0]['close']
spread = us10y - us2y
print(f"2-10 Year Spread: {spread:.2f}%")
print(f"Yield Curve: {'Inverted' if spread < 0 else 'Normal'}")
```

---

## Hong Kong Exchange (HK)

### Overview

**Exchange Code**: `HK`

**Description**: Hong Kong Stock Exchange (HKEX).

**Special Note**: HK is a regular stock exchange but may not appear in all exchange lists. Treat it similarly to other stock exchanges.

### Finding HK Stocks

**Request**:
```bash
curl "https://eodhd.com/api/exchange-symbol-list/HK?api_token=demo&fmt=json"
```

**Response Sample**:
```json
[
  {
    "Code": "0700",
    "Name": "TENCENT",
    "Country": "Hong Kong",
    "Exchange": "HK",
    "Currency": "HKD",
    "Type": "Common Stock",
    "Isin": "KYG875721634"
  },
  {
    "Code": "0941",
    "Name": "CHINA MOBILE",
    "Country": "Hong Kong",
    "Exchange": "HK",
    "Currency": "HKD",
    "Type": "Common Stock",
    "Isin": "HK0941009539"
  },
  {
    "Code": "0005",
    "Name": "HSBC HOLDINGS",
    "Country": "Hong Kong",
    "Exchange": "HK",
    "Currency": "HKD",
    "Type": "Common Stock",
    "Isin": "GB0005405286"
  }
]
```

### Common HK Stocks

**Major HK Companies**:
```
0700.HK  - Tencent Holdings
0941.HK  - China Mobile
0005.HK  - HSBC Holdings
0939.HK  - China Construction Bank
1299.HK  - AIA Group
0388.HK  - Hong Kong Exchanges and Clearing
2318.HK  - Ping An Insurance
```

### Ticker Format Note

**Important**: Hong Kong ticker codes often have leading zeros (e.g., `0700`, `0005`).

**Correct Format**:
```
0700.HK  ✅ Correct (includes leading zero)
700.HK   ⚠️ May not work
```

### Usage Example

```python
def get_hk_stock_data(stock_code, from_date, to_date, api_token):
    """
    Fetch Hong Kong stock data.

    Args:
        stock_code: HK stock code (e.g., '0700', '0941')
        from_date: Start date
        to_date: End date
        api_token: Your API token

    Returns:
        JSON data with OHLC prices in HKD
    """
    ticker = f"{stock_code}.HK"
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "from": from_date,
        "to": to_date,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    return response.json()

# Example: Tencent data
tencent_data = get_hk_stock_data('0700', '2023-01-01', '2023-12-31', 'your_api_token')
print(f"Tencent on 2023-12-31: HKD {tencent_data[-1]['close']:.2f}")
```

### HK Stock Fundamentals

```python
# Get Tencent fundamentals
url = "https://eodhd.com/api/fundamentals/0700.HK"
params = {
    "api_token": "your_api_token",
    "fmt": "json"
}

fundamentals = requests.get(url, params=params).json()
print(f"Company: {fundamentals['General']['Name']}")
print(f"Market Cap: HKD {fundamentals['Highlights']['MarketCapitalization']:,.0f}")
print(f"P/E Ratio: {fundamentals['Highlights']['PERatio']:.2f}")
```

---

## Usage in APIs

### End-of-Day Historical Data API

**All special exchange tickers work with EOD API**:

```bash
# Index
curl "https://eodhd.com/api/eod/GSPC.INDX?api_token=demo&from=2023-01-01"

# Forex
curl "https://eodhd.com/api/eod/EURUSD.FOREX?api_token=demo&from=2023-01-01"

# Crypto
curl "https://eodhd.com/api/eod/BTC-USD.CC?api_token=demo&from=2023-01-01"

# Fund
curl "https://eodhd.com/api/eod/IE00B4L5Y983.EUFUND?api_token=demo&from=2023-01-01"

# Bond
curl "https://eodhd.com/api/eod/US10Y.GBOND?api_token=demo&from=2023-01-01"

# Hong Kong
curl "https://eodhd.com/api/eod/0700.HK?api_token=demo&from=2023-01-01"
```

### Live/Intraday Data API

**Supported for most special exchanges**:

```bash
# Index (real-time)
curl "https://eodhd.com/api/real-time/GSPC.INDX?api_token=demo&fmt=json"

# Forex (real-time)
curl "https://eodhd.com/api/real-time/EURUSD.FOREX?api_token=demo&fmt=json"

# Crypto (real-time)
curl "https://eodhd.com/api/real-time/BTC-USD.CC?api_token=demo&fmt=json"

# Intraday 5-minute data
curl "https://eodhd.com/api/intraday/GSPC.INDX?interval=5m&api_token=demo&fmt=json"
```

### Technical Indicators API

**Calculate indicators on special exchange tickers**:

```bash
# SMA on S&P 500
curl "https://eodhd.com/api/technical/GSPC.INDX?function=sma&period=200&api_token=demo"

# RSI on EUR/USD
curl "https://eodhd.com/api/technical/EURUSD.FOREX?function=rsi&period=14&api_token=demo"

# MACD on Bitcoin
curl "https://eodhd.com/api/technical/BTC-USD.CC?function=macd&api_token=demo"
```

### Fundamentals API

**Available for some special exchanges**:

```bash
# Crypto fundamentals
curl "https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json"

# Fund fundamentals
curl "https://eodhd.com/api/fundamentals/IE00B4L5Y983.EUFUND?api_token=demo&fmt=json"

# HK stock fundamentals
curl "https://eodhd.com/api/fundamentals/0700.HK?api_token=demo&fmt=json"
```

**Note**: Not all special exchanges have fundamentals data (e.g., indices, forex pairs, bonds typically don't).

---

## Common Tickers Reference

### Quick Reference Table

| Asset Class | Ticker | Description | Currency |
|-------------|--------|-------------|----------|
| **US Indices** | | | |
| | GSPC.INDX | S&P 500 | USD |
| | NDX.INDX | NASDAQ 100 | USD |
| | DJI.INDX | Dow Jones | USD |
| | VIX.INDX | Volatility Index | USD |
| **International Indices** | | | |
| | GDAXI.INDX | DAX | EUR |
| | N225.INDX | Nikkei 225 | JPY |
| | HSI.INDX | Hang Seng | HKD |
| **Forex Majors** | | | |
| | EURUSD.FOREX | EUR/USD | USD |
| | GBPUSD.FOREX | GBP/USD | USD |
| | USDJPY.FOREX | USD/JPY | JPY |
| | AUDUSD.FOREX | AUD/USD | USD |
| **Cryptocurrency** | | | |
| | BTC-USD.CC | Bitcoin | USD |
| | ETH-USD.CC | Ethereum | USD |
| | LTC-USD.CC | Litecoin | USD |
| | XRP-USD.CC | Ripple | USD |
| **Government Bonds** | | | |
| | US10Y.GBOND | US 10Y Treasury | USD |
| | US2Y.GBOND | US 2Y Treasury | USD |
| | DE10Y.GBOND | German 10Y Bund | EUR |
| **Hong Kong Stocks** | | | |
| | 0700.HK | Tencent | HKD |
| | 0941.HK | China Mobile | HKD |
| | 0005.HK | HSBC Holdings | HKD |

### Python Utility Functions

```python
class SpecialExchangeHelper:
    """Utility class for working with special exchanges."""

    # Common tickers by category
    MAJOR_INDICES = {
        'S&P 500': 'GSPC.INDX',
        'NASDAQ 100': 'NDX.INDX',
        'Dow Jones': 'DJI.INDX',
        'DAX': 'GDAXI.INDX',
        'Nikkei 225': 'N225.INDX'
    }

    MAJOR_FOREX = {
        'EUR/USD': 'EURUSD.FOREX',
        'GBP/USD': 'GBPUSD.FOREX',
        'USD/JPY': 'USDJPY.FOREX',
        'AUD/USD': 'AUDUSD.FOREX',
        'USD/CAD': 'USDCAD.FOREX'
    }

    MAJOR_CRYPTO = {
        'Bitcoin': 'BTC-USD.CC',
        'Ethereum': 'ETH-USD.CC',
        'Litecoin': 'LTC-USD.CC',
        'Ripple': 'XRP-USD.CC',
        'Bitcoin Cash': 'BCH-USD.CC'
    }

    @staticmethod
    def get_ticker(name, category='index'):
        """
        Get ticker by common name.

        Args:
            name: Common name (e.g., 'S&P 500', 'Bitcoin')
            category: Category ('index', 'forex', 'crypto')

        Returns:
            Full ticker string
        """
        categories = {
            'index': SpecialExchangeHelper.MAJOR_INDICES,
            'forex': SpecialExchangeHelper.MAJOR_FOREX,
            'crypto': SpecialExchangeHelper.MAJOR_CRYPTO
        }

        ticker_dict = categories.get(category, {})
        return ticker_dict.get(name)

    @staticmethod
    def is_special_exchange(ticker):
        """Check if ticker uses a special exchange."""
        special_exchanges = ['INDX', 'FOREX', 'CC', 'EUFUND', 'MONEY', 'GBOND', 'HK']
        exchange = ticker.split('.')[-1] if '.' in ticker else None
        return exchange in special_exchanges

# Usage examples
helper = SpecialExchangeHelper()

# Get ticker by name
sp500_ticker = helper.get_ticker('S&P 500', 'index')
print(f"S&P 500: {sp500_ticker}")  # Output: GSPC.INDX

btc_ticker = helper.get_ticker('Bitcoin', 'crypto')
print(f"Bitcoin: {btc_ticker}")  # Output: BTC-USD.CC

# Check if special exchange
print(helper.is_special_exchange('AAPL.US'))        # False
print(helper.is_special_exchange('GSPC.INDX'))      # True
print(helper.is_special_exchange('BTC-USD.CC'))     # True
```

---

## Best Practices

### 1. Always Include Exchange Suffix

**DO**:
```python
ticker = "GSPC.INDX"    # Correct
ticker = "EURUSD.FOREX" # Correct
ticker = "BTC-USD.CC"   # Correct
```

**DON'T**:
```python
ticker = "GSPC"         # Ambiguous - which exchange?
ticker = "EURUSD"       # May not work
ticker = "BTC"          # Incomplete ticker
```

### 2. Use Exchange Symbol List to Discover Tickers

```python
# Don't guess ticker codes
# DO use the exchange-symbol-list API

def find_ticker(exchange_code, search_term, api_token):
    """Search for ticker in exchange."""
    url = f"https://eodhd.com/api/exchange-symbol-list/{exchange_code}"
    data = requests.get(url, params={"api_token": api_token}).json()
    df = pd.DataFrame(data)
    results = df[df['Name'].str.contains(search_term, case=False, na=False)]
    return results

# Example: Find S&P 500
sp500 = find_ticker('INDX', 'S&P 500', 'your_api_token')
print(f"Found: {sp500['Code'].values[0]}.INDX")
```

### 3. Verify Ticker Availability Before Use

```python
def verify_ticker_exists(ticker, api_token):
    """Verify ticker has data available."""
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return len(data) > 0
    except:
        return False

# Example
if verify_ticker_exists('GSPC.INDX', 'your_api_token'):
    print("Ticker is valid and has data")
else:
    print("Ticker not found or no data")
```

### 4. Handle Special Cases

**Hong Kong Leading Zeros**:
```python
# Always preserve leading zeros
hk_ticker = "0700.HK"  # Correct
# Not: "700.HK"
```

**Crypto Hyphen Format**:
```python
# Use hyphen for crypto pairs
crypto_ticker = "BTC-USD.CC"  # Correct
# Not: "BTCUSD.CC"
```

### 5. Cache Exchange Lists

```python
import json
import os

def get_cached_exchange_list(exchange_code, api_token, cache_dir='cache'):
    """
    Fetch and cache exchange ticker list.

    Exchange lists don't change often, so cache them.
    """
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f"{cache_dir}/exchange_{exchange_code}.json"

    # Check cache (valid for 7 days)
    if os.path.exists(cache_file):
        age_days = (time.time() - os.path.getmtime(cache_file)) / 86400
        if age_days < 7:
            with open(cache_file, 'r') as f:
                return json.load(f)

    # Fetch from API
    url = f"https://eodhd.com/api/exchange-symbol-list/{exchange_code}"
    data = requests.get(url, params={"api_token": api_token}).json()

    # Save to cache
    with open(cache_file, 'w') as f:
        json.dump(data, f)

    return data
```

### 6. Document Special Exchange Usage

```python
"""
Portfolio Analysis Module

Special Exchanges Used:
- INDX: For benchmark indices (S&P 500, NASDAQ 100)
- FOREX: For currency exposure analysis
- CC: For cryptocurrency holdings
- GBOND: For treasury yield data

Tickers:
- GSPC.INDX: S&P 500 benchmark
- EURUSD.FOREX: EUR/USD exchange rate
- BTC-USD.CC: Bitcoin price
- US10Y.GBOND: 10-year Treasury yield
"""
```

### 7. Error Handling for Special Exchanges

```python
def safe_get_special_exchange_data(ticker, api_token):
    """
    Safely fetch data from special exchanges with error handling.
    """
    try:
        # Verify ticker format
        if '.' not in ticker:
            raise ValueError(f"Ticker must include exchange suffix: {ticker}")

        # Extract exchange code
        exchange = ticker.split('.')[-1]

        # Verify it's a known exchange
        known_exchanges = ['INDX', 'FOREX', 'CC', 'EUFUND', 'MONEY', 'GBOND', 'HK']
        if exchange not in known_exchanges:
            raise ValueError(f"Unknown exchange: {exchange}")

        # Fetch data
        url = f"https://eodhd.com/api/eod/{ticker}"
        response = requests.get(url, params={"api_token": api_token, "fmt": "json"})
        response.raise_for_status()

        data = response.json()

        if not data:
            raise ValueError(f"No data available for {ticker}")

        return data

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
    except ValueError as e:
        print(f"Validation Error: {e}")
        return None

# Usage
data = safe_get_special_exchange_data('GSPC.INDX', 'your_api_token')
if data:
    print(f"Successfully retrieved {len(data)} data points")
```

---

## Summary

### Key Takeaways

1. **Special Exchanges Not in `/exchanges` API**
   - INDX, FOREX, CC, EUFUND, MONEY, GBOND, HK
   - Still fully supported across EODHD APIs

2. **Finding Tickers**
   - Use `/exchange-symbol-list/{EXCHANGE_CODE}`
   - Search by name or browse full list

3. **Ticker Format**
   - Always use full format: `{CODE}.{EXCHANGE}`
   - Examples: `GSPC.INDX`, `EURUSD.FOREX`, `BTC-USD.CC`

4. **Special Considerations**
   - HK: Preserve leading zeros (e.g., `0700.HK`)
   - CC: Use hyphen format (e.g., `BTC-USD.CC`)
   - INDX: Indices for benchmarking, not trading

5. **API Compatibility**
   - EOD API: ✅ All special exchanges
   - Intraday API: ✅ Most special exchanges
   - Technical Indicators: ✅ All special exchanges
   - Fundamentals: ⚠️ Limited (crypto, funds, HK stocks only)

6. **Best Practices**
   - Always include exchange suffix
   - Use exchange list API to discover tickers
   - Verify ticker availability before use
   - Cache exchange lists to reduce API calls

---

## Additional Resources

- **Exchange Symbol List API**: https://eodhd.com/financial-apis/exchanges-api-list-of-tickers-and-trading-hours/
- **EOD API Documentation**: https://eodhd.com/financial-apis/api-for-historical-data-and-volumes
- **Fundamentals API (Crypto)**: https://eodhd.com/financial-apis/crypto-currency-data-api
- **Technical Indicators API**: https://eodhd.com/financial-apis/technical-indicators-api/

---

**Document Version**: 1.0
**Last Updated**: 2024-11-27
**Maintained by**: EODHD Skills Project
