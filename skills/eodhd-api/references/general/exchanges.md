# EODHD Supported Exchanges

This document provides a comprehensive list of exchanges supported by EODHD, based on the actual `/exchanges-list` API response.

## Overview

EODHD provides data for 70+ exchanges worldwide covering:
- **Equities** - Stocks, ETFs, preferred shares
- **Indices** - Major market indices
- **Forex** - Currency pairs
- **Cryptocurrencies** - Digital assets
- **Bonds** - Government bonds
- **Money Markets** - Interest rates and money market instruments
- **European Funds** - Fund data via virtual exchange

## Exchange Code Format

Symbol format: `{TICKER}.{EXCHANGE_CODE}`

Examples:
- `AAPL.US` - Apple Inc. on NYSE/NASDAQ (US stocks)
- `BMW.XETRA` - BMW on XETRA (Germany)
- `EURUSD.FOREX` - EUR/USD currency pair
- `BTC-USD.CC` - Bitcoin/USD on cryptocurrency exchanges
- `US10Y.GBOND` - US 10-year Treasury yield

## Exchanges by Region

All exchanges below are confirmed present in the `/exchanges-list` API response.

### North America

| Code | Exchange Name | Country | Currency | OperatingMIC |
|------|---------------|---------|----------|--------------|
| US | USA Stocks | USA | USD | XNAS, XNYS, OTCM |
| TO | Toronto Exchange | Canada | CAD | XTSE |
| V | TSX Venture Exchange | Canada | CAD | XTSX |
| NEO | NEO Exchange | Canada | CAD | NEOE |
| MX | Mexican Exchange | Mexico | MXN | XMEX |

**Note**: The `US` code combines NYSE, NASDAQ, and OTC Markets into a single virtual exchange.

### Europe

| Code | Exchange Name | Country | Currency | OperatingMIC |
|------|---------------|---------|----------|--------------|
| LSE | London Exchange | UK | GBP | XLON |
| XETRA | XETRA Stock Exchange | Germany | EUR | XETR |
| F | Frankfurt Exchange | Germany | EUR | XFRA |
| BE | Berlin Exchange | Germany | EUR | XBER |
| HM | Hamburg Exchange | Germany | EUR | XHAM |
| DU | Dusseldorf Exchange | Germany | EUR | XDUS |
| MU | Munich Exchange | Germany | EUR | XMUN |
| STU | Stuttgart Exchange | Germany | EUR | XSTU |
| HA | Hanover Exchange | Germany | EUR | XHAN |
| PA | Euronext Paris | France | EUR | XPAR |
| AS | Euronext Amsterdam | Netherlands | EUR | XAMS |
| BR | Euronext Brussels | Belgium | EUR | XBRU |
| LS | Euronext Lisbon | Portugal | EUR | XLIS |
| MC | Madrid Exchange | Spain | EUR | BMEX |
| SW | SIX Swiss Exchange | Switzerland | CHF | XSWX |
| VI | Vienna Exchange | Austria | EUR | XWBO |
| LU | Luxembourg Stock Exchange | Luxembourg | EUR | XLUX |
| ST | Stockholm Exchange | Sweden | SEK | XSTO |
| OL | Oslo Stock Exchange | Norway | NOK | XOSL |
| HE | Helsinki Exchange | Finland | EUR | XHEL |
| CO | Copenhagen Exchange | Denmark | DKK | XCSE |
| IC | Iceland Exchange | Iceland | ISK | XICE |
| IR | Irish Exchange | Ireland | EUR | XDUB |
| WAR | Warsaw Stock Exchange | Poland | PLN | XWAR |
| PR | Prague Stock Exchange | Czech Republic | CZK | XPRA |
| BUD | Budapest Stock Exchange | Hungary | HUF | XBUD |
| AT | Athens Exchange | Greece | EUR | ASEX |
| RO | Bucharest Stock Exchange | Romania | RON | XBSE |
| ZSE | Zagreb Stock Exchange | Croatia | EUR | XZAG |

### Asia-Pacific

| Code | Exchange Name | Country | Currency | OperatingMIC |
|------|---------------|---------|----------|--------------|
| SHG | Shanghai Stock Exchange | China | CNY | XSHG |
| SHE | Shenzhen Stock Exchange | China | CNY | XSHE |
| KO | Korea Stock Exchange | Korea | KRW | XKRX |
| KQ | KOSDAQ | Korea | KRW | XKOS |
| TW | Taiwan Stock Exchange | Taiwan | TWD | XTAI |
| TWO | Taiwan OTC Exchange | Taiwan | TWD | ROCO |
| KLSE | Kuala Lumpur Exchange | Malaysia | MYR | XKLS |
| BK | Thailand Exchange | Thailand | THB | XBKK |
| JK | Jakarta Exchange | Indonesia | IDR | XIDX |
| PSE | Philippine Stock Exchange | Philippines | PHP | XPHS |
| VN | Vietnam Stocks | Vietnam | VND | XSTC |
| CM | Colombo Stock Exchange | Sri Lanka | LKR | XCOL |
| KAR | Karachi Stock Exchange | Pakistan | PKR | XKAR |
| AU | Australian Securities Exchange | Australia | AUD | XASX |

### Middle East

| Code | Exchange Name | Country | Currency | OperatingMIC |
|------|---------------|---------|----------|--------------|
| TA | Tel Aviv Stock Exchange | Israel | ILS | XTAE |

### Africa

| Code | Exchange Name | Country | Currency | OperatingMIC |
|------|---------------|---------|----------|--------------|
| JSE | Johannesburg Exchange | South Africa | ZAR | XJSE |
| EGX | Egyptian Exchange | Egypt | EGP | NILX |
| BC | Casablanca Stock Exchange | Morocco | MAD | XCAS |
| GSE | Ghana Stock Exchange | Ghana | GHS | XGHA |
| XBOT | Botswana Stock Exchange | Botswana | BWP | XBOT |
| XNAI | Nairobi Securities Exchange | Kenya | KES | XNAI |
| XNSA | Nigerian Stock Exchange | Nigeria | NGN | XNSA |
| SEM | Stock Exchange of Mauritius | Mauritius | MUR | XMAU |
| MSE | Malawi Stock Exchange | Malawi | MWK | XMSW |
| RSE | Rwanda Stock Exchange | Rwanda | RWF | RSEX |
| DSE | Dar es Salaam Stock Exchange | Tanzania | TZS | XDAR |
| USE | Uganda Securities Exchange | Uganda | UGX | XUGA |
| LUSE | Lusaka Stock Exchange | Zambia | ZMW | XLUS |
| XZIM | Zimbabwe Stock Exchange | Zimbabwe | ZWL | XZIM |
| VFEX | Victoria Falls Stock Exchange | Zimbabwe | ZWL | VFEX |

### Latin America

| Code | Exchange Name | Country | Currency | OperatingMIC |
|------|---------------|---------|----------|--------------|
| SA | Sao Paulo Exchange | Brazil | BRL | BVMF |
| BA | Buenos Aires Exchange | Argentina | ARS | XBUE |
| SN | Chilean Stock Exchange | Chile | CLP | XSGO |
| LIM | Bolsa de Valores de Lima | Peru | PEN | XLIM |

## Special Exchange Codes

These virtual exchanges also appear in the `/exchanges-list` response.

| Code | Name | Currency | OperatingMIC |
|------|------|----------|--------------|
| FOREX | FOREX | Unknown | CDSL |
| CC | Cryptocurrencies | USD | CRYP |
| GBOND | Government Bonds | Unknown | null |
| MONEY | Money Market Virtual Exchange | Unknown | null |
| EUFUND | Europe Fund Virtual Exchange | EUR | null |

**Note**: The `INDX` (Indices) code is used as a symbol suffix but does **not** appear in the `/exchanges-list` endpoint response.

### Forex (FOREX)

Currency pairs use the `.FOREX` suffix:

Examples:
- `EURUSD.FOREX` - Euro/US Dollar
- `GBPUSD.FOREX` - British Pound/US Dollar
- `USDJPY.FOREX` - US Dollar/Japanese Yen
- `AUDUSD.FOREX` - Australian Dollar/US Dollar

**Format**: `{BASE}{QUOTE}.FOREX` (no separator between currencies)

### Cryptocurrencies (CC)

Cryptocurrency pairs use the `.CC` suffix:

Examples:
- `BTC-USD.CC` - Bitcoin/US Dollar
- `ETH-USD.CC` - Ethereum/US Dollar
- `BNB-USD.CC` - Binance Coin/US Dollar
- `XRP-USD.CC` - Ripple/US Dollar

**Format**: `{CRYPTO}-{QUOTE}.CC` (hyphen separator)

### Government Bonds (GBOND)

Government bonds use the `.GBOND` suffix:

Examples:
- `US10Y.GBOND` - US 10-year Treasury yield
- `US2Y.GBOND` - US 2-year Treasury yield
- `DE10Y.GBOND` - German 10-year Bund yield
- `GB10Y.GBOND` - UK 10-year Gilt yield

### Money Markets (MONEY)

Money market instruments use the `.MONEY` suffix.

### European Funds (EUFUND)

European fund data uses the `.EUFUND` suffix.

### Indices (INDX)

Major indices use the `.INDX` suffix:

Examples:
- `GSPC.INDX` - S&P 500 Index
- `DJI.INDX` - Dow Jones Industrial Average
- `IXIC.INDX` - NASDAQ Composite
- `GDAXI.INDX` - DAX
- `N225.INDX` - Nikkei 225

## Exchange Status & Data Availability

### Real-Time Data
Some exchanges provide real-time data, while others have a 15-20 minute delay:
- **Real-time**: US (with appropriate subscription), major European exchanges
- **15-minute delay**: Most exchanges in standard plans
- **End-of-day only**: Some smaller exchanges

### Historical Data Coverage

| Region | Start Date | Notes |
|--------|-----------|-------|
| US exchanges | 1980s+ | Most liquid stocks have data from 1980s |
| Major European | 1990s+ | Varies by exchange |
| Asian markets | 1990s+ | Varies by exchange |
| Cryptocurrencies | 2010+ | Bitcoin from ~2010, others vary |
| Forex | 1990s+ | Major pairs have extensive history |

## Finding the Right Exchange Code

### Method 1: Symbol Search API
Use the `/search/{QUERY}` endpoint to find the correct symbol:

```bash
curl "https://eodhd.com/api/search/Apple?api_token=YOUR_TOKEN"
```

Returns symbols across all exchanges.

### Method 2: Exchange Symbol List
Get all symbols for a specific exchange:

```bash
curl "https://eodhd.com/api/exchange-symbol-list/US?api_token=YOUR_TOKEN"
```

### Method 3: Exchanges List API
List all available exchanges:

```bash
curl "https://eodhd.com/api/exchanges-list/?api_token=YOUR_TOKEN&fmt=json"
```

## Common Issues & Solutions

### Issue: Symbol not found
- **Solution**: Verify exchange code is correct
- Try searching for the company name using the search endpoint
- Some symbols require specific exchange codes (e.g., `AAPL.US`, not just `AAPL`)

### Issue: No data returned
- **Solution**: Check if the exchange is supported for the asset type
- Verify trading hours and market holidays
- Some instruments may have limited historical data

### Issue: Incorrect exchange code
- **Solution**: Use the exchange symbol list to verify correct ticker format
- Check if the symbol has been delisted or merged

## Additional Resources

- **Exchange Symbol List API**: `/exchange-symbol-list/{EXCHANGE_CODE}` - List all symbols on an exchange
- **Symbol Search API**: `/search/{QUERY}` - Search for symbols by name or ticker

## Data Freshness by Type

| Data Type          | Freshness | Notes |
|--------------------|-----------|-------|
| EOD Prices         | After market close | Daily OHLCV, adjusted for splits/dividends |
| Intraday           | 2-3 hours after close | 1m, 5m, 1h bars |
| Real-Time (WebSocket) | < 50 ms | US stocks, Forex, Crypto only |
| Delayed Quotes     | 15-20 min | REST API live endpoint |
| Fundamentals       | Varies | Updated as filings are published |

## Notes

1. Exchange codes are case-sensitive in some contexts
2. Always use the full symbol format: `TICKER.EXCHANGE`
3. Some exchanges trade multiple sessions (pre-market, regular, post-market)
4. Holiday schedules vary by exchange and country
5. Corporate actions (splits, dividends) are automatically adjusted in historical data
