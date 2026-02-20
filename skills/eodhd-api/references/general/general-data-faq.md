# General Data FAQ

Common questions and answers about EODHD data in general, covering identifiers, data formats, data quality, asset-specific quirks, and miscellaneous topics that span multiple endpoints.

---

## Identifiers & Symbols

### ISINs

Since ISINs are not unique, EODHD does not use them to uniquely identify stocks and ETFs. The unique identifier is `TICKER + EXCHANGE` (e.g., `AAPL.US`). The same ISIN can appear on different exchanges (e.g., `AAPL.US` and `AAPL.MX`). While EODHD strives to have ISINs for all instruments, the dataset is not 100% complete — particularly for mutual funds, many ISINs may be missing. EODHD has data for more than 60,000 ISINs.

### Checking if a Stock Exists in the Database

If a ticker does not exist, the API returns an **HTTP 404** status code instead of 200. You can check the HTTP status code programmatically. Alternatively:
- Use the front page search at https://eodhd.com/
- Use the Exchange Symbol List API to get all symbols for an exchange: https://eodhd.com/knowledgebase/list-symbols-exchange/

### Type Field Values

The possible values for the `Type` field in the exchange symbol list are:

Common Stock, Preferred Stock, ETF, ETC, ETN, FUND, Currency, Futures, Commodity, INDEX, BOND, Rate, Certificate, Warrant, MONEY, Mutual Fund, Note.

There is no API endpoint that exposes this list dynamically.

### AMEX Exchange Code

AMEX is the old name of the exchange. It is now:
- **NYSE ARCA** — for ETFs
- **NYSE American** (code: `NYSE MKT` in EODHD) — for smaller-cap companies

If you query AMEX and get very few results, the tickers have likely been mapped to their current exchange codes.

### Ampersand (&) in Ticker Names

Some ticker names contain the `&` character. Because `&` is a URL delimiter, the part after `&` gets interpreted as a new query parameter. Always replace `&` with `%26` in the URL.

### Dot in Search Query

The EODHD Search API does not support dots (`.`) in the search string — the dot is a reserved administering symbol. For example, searching for `Amazon.com` will not return results. Use `Amazon` instead.

---

## Data Formats & Precision

### Four Decimal Places

EODHD uses up to **4 decimal places** where applicable (more than many other data providers who truncate to 2). However, trailing zeros are not displayed:
- `10.5000` displays as `10.5`
- `21.6800` displays as `21.68`
- `45.7382` displays as `45.7382`

For the latest prices, most sources provide 2 decimals. On any adjustment (splits, dividends), the full 4 decimal places are preserved.

### JSON Data Encoding

All JSON responses use **UTF-8** encoding.

---

## Price Data

### Adjusted Close — Retroactive

Adjusted close works **retroactively**. When a corporate action (split or dividend) is recorded, the adjusted close changes for all historical dates **backwards** from that event. Dates going forward remain untouched (adjusted close equals close) until the next corporate action occurs.

Example: If a split occurs on April 22, adjusted close will change for April 21, April 20, April 19, etc. — all the way to the first available date. April 23 and later dates are unaffected.

### API OHLC vs EODLoader OHLC

With the regular API, OHLC prices are provided in **raw** form (unadjusted). The `adjusted_close` field is adjusted for both splits and dividends.

To calculate fully adjusted OHLC prices:

```
k = adjusted_close / close
adjusted_open = open * k
adjusted_high = high * k
adjusted_low = low * k
```

**Important**: Calculate `k` for **each day** separately, as it changes on each split or dividend.

For split-only adjusted prices, use the Technical Indicators API: https://eodhd.com/knowledgebase/technical-indicators-api/

The EODLoader tool provides both adjusted and non-adjusted data sets.

### NYSE Data vs NASDAQ Data

While real-time prices on NYSE and NASDAQ may differ slightly, EODHD's data is not real-time — so this difference is negligible. EODHD provides NASDAQ data for US stocks. There is no practical reason to request NYSE data separately.

### No Value for Open Price (Real-Time)

If the real-time API shows no open price for a ticker, it means there have been **no trades for that ticker today**. The API can only provide the price of the latest trading day, which appears in `previousClose`.

### Pre-Calculated Returns

EODHD does not provide pre-calculated returns (5-day, 1-month, 3-month, etc.) directly. These must be calculated from historical price data. The Screener API does provide `refund_1d_p`, `refund_5d_p`, and `refund_ytd_p` for the latest day.

---

## Dividends & Corporate Actions

### Splits and Dividends Data Sources

The data for splits and dividends comes from **news and announcements**.

### History of Dividends

Dividend history is typically available from **January 2000**. EODHD does not support non-US mutual funds for dividend data.

---

## Exchange & Currency Quirks

### GBX vs GBP Currency

LSE (London Stock Exchange) provides most stock prices in **GBX (pence)**, not GBP (pounds). EODHD provides the data in the same currency as the exchange. To convert GBX to GBP, simply divide by 100.

This is a common industry issue. Several exchanges worldwide provide data in subunits:
- **LSE**: GBX (pence) vs GBP (pounds)
- **JSE (South Africa)**: ZAC (cents) vs ZAR (rand)
- **TASE (Tel Aviv)**: Agorot vs Shekels

In rare cases, a ticker may switch between GBP and GBX or vice versa.

### XETRA vs Frankfurt (F)

XETRA is the larger and newer exchange; Frankfurt (`F`) is an older exchange with lower volumes. EODHD recommends using **XETRA** when possible.

### Server Timezone

The EODHD server timezone is **GMT**.

### Approved Exchange Data Vendor Disclaimer

EODHD data is sourced from market makers and is **delayed** — it is not real-time exchange data. Real-time data without delay is provided by exchanges and requires separate licensing. Prices are indicative and may not be appropriate for trading purposes. All CFDs (stocks, indices, futures, mutual funds, ETFs), cryptocurrencies, and Forex are provided by market makers, not exchanges.

Market makers include brokerage companies, CFD brokerages, and big financial institutions.

### US Tickers and Multiple Trading Venues

All US securities trade on multiple venues, not just a single exchange. The API shows only the primary exchange for the ticker, but data may be aggregated across venues.

---

## Asset-Specific Questions

### Cryptocurrency Volume

Different data providers aggregate volume from different sets of exchanges, so cryptocurrency volume figures may differ between EODHD and other sources (e.g., Yahoo Finance). There are hundreds of cryptocurrency exchanges worldwide, and it is impossible to sum data from all of them. What matters for analysis is typically the **volume change** (relative), not the absolute number.

### Forex Volume

EODHD does not provide volume data for Forex. Forex is traded across many decentralized venues (banks, market makers, OTC), making it nearly impossible to calculate a correct aggregate volume.

### Monthly Sector Returns

EODHD does not provide downloading data by sector or pre-calculated sector returns. To get sector-level data, download fundamentals data and aggregate it on your side.

### OTC Equities / ADRs

ADR tickers traded on OTC exchanges may have **incomplete or incorrect** fundamental data because ADR companies often do not report full information to the SEC. EODHD recommends using fundamentals from the **primary exchange** for any company. For example, for `ADKCF` (OTC), use `4401.TSE` (Tokyo) instead — the primary exchange typically has more complete and accurate data.

### Warrants

EODHD does not currently separate warrants from stocks in its data. Warrant identification is planned for a future update but has no ETA. If you have a list of warrant tickers for a specific exchange, EODHD may be able to look into adding them.

### Order Books

EODHD does not provide order book data (for crypto or any other asset class).

### Investment Certificates

EODHD does not support investment certificates at this time.

### MorningStar Categories for Equities

ETFs and Mutual Funds have MorningStar category data in the Fundamentals API, but **equities do not**. MorningStar categories are only available for funds and ETFs.

---

## News Data

### News Coverage Depth

The News API has been providing news since **2016**. Since **2022**, EODHD expanded its pool of news suppliers, resulting in greater volume of news from that point onward.

Reference: https://eodhd.com/financial-apis/stock-market-financial-news-api

---

## Data Quality

### Data Checks for Missing Data

EODHD checks data and re-updates missed stocks up to **5 times per day** when updates are not received. If there is an issue with the data source, changing the source for specific stocks is not automatic and requires manual intervention. After resolution, data updates resume normally.

### Manual Action for Data Issues

EODHD has dozens of automatic routines for data quality checks internally. However, not all cases can be checked and fixed automatically. Low-volume tickers often have non-trading days that may appear as gaps in history — these are not necessarily data errors.

### IPO Exchange Determination

There is no API indicator showing which exchange hosted a company's original IPO. As a rule of thumb, when comparing fundamental data from several exchanges for the same company, the exchange with the **most complete data** is typically the primary exchange — though this is not true for 100% of cases.

### Data Back-Adjustments

Data may occasionally be corrected (back-adjusted) hours, days, or even weeks after initial publication. This can happen due to:
- Corporate actions (splits) requiring recalculation of the entire history
- Data providers sending faulty data points that need correction later
- Companies releasing financial information later than expected

This is common across all financial data providers. The vast majority of data is correct, but corrections are applied as needed when issues are detected.

### HTTP Error Codes

| Code | Meaning |
|------|---------|
| **200** | OK — request succeeded |
| **402** | Payment Required — API call limit exhausted |
| **403** | Forbidden — API key is not valid |
| **404** | Not Found — ticker does not exist |
| **429** | Too Many Requests — per-minute rate limit exceeded |

### Fed Interest Rate History

Historical Federal Reserve interest rate decisions are available through the **Economic Events API** as "Fed Interest Rate" events. See the Economic Events endpoint documentation.

### One Fundamentals File Per Listing

Different listings of the same company (e.g., `AAPL.US` and `APC.XETRA`) have **separate fundamentals files** in the EODHD database. The outputs may differ between exchanges. There is no unified fundamentals response across all listings of a single company — each ticker has its own fundamentals data.

### First Full Year of Fundamental Data

There is no reliable way to automatically detect the first complete financial year for a company. Challenges include:
- Even the earliest SEC filing typically contains comparison data from prior periods
- The depth of prior data varies by company and changes over time
- Some companies file annual reports for incomplete years (due to fiscal year transitions, mergers, etc.)

As a general rule for US-reporting companies, the year **after** the IPO year should be considered "definitely complete." However, occasional missing reports can occur even well after an IPO.

### Bespoke Support

EODHD generally tries to fulfil user requests. Whether custom work is done free of charge or for a one-time payment depends on the specific request. Contact EODHD support for inquiries.

---

**Last Updated**: February 2026
**Source**: EODHD Official Documentation
**Maintained By**: EODHD Skills Team
