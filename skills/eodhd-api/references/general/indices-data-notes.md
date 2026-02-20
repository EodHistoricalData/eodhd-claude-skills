# Indices (INDX) Data Notes

This document covers common questions and data characteristics specific to EODHD's index data.

## Historical Data Access

Subscriptions that have access to EOD data also have access to indices EOD data — no separate subscription is required.

## Index List

You can get the list of available indices using the exchange code `INDX` with the Exchange Symbols API:

```
https://eodhd.com/financial-apis/exchanges-api-list-of-tickers-and-trading-hours#Get_List_of_Tickers_Exchange_Symbols
```

## Live Data for Indices

Subscriptions that have access to live data also have access to indices live data. However, live data is not available for 100% of indices — some may not have it.

## Historical Index Components

Historical constituent data is available through two sources:

1. **Fundamentals API** (included with Fundamentals or All-In-One plans) — historical components for the S&P 500 index:
   ```
   https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds#Historical_Constituents_for_the_SP_500_GSPC
   ```

2. **Marketplace subscription** — historical components for multiple S&P Global indices (including S&P 500):
   ```
   https://eodhd.com/marketplace/unicornbay/spglobal
   ```

## Missing Components — Use ETF Holdings

If index components are not available for a particular index, a recommended workaround is to use an **ETF that tracks the index** and check that ETF's holdings via the Fundamentals API. In many cases this provides even better data, because ETF holdings include **weights** (percentage allocations).

## Price vs Total Return Indices

All indices are **price indices** by default, except indices with `TR` or `T` at the end of the ticker code, which are **Total Return** indices (price change plus reinvested dividends).

---

**Last Updated**: February 2026
**Source**: EODHD Official Documentation
**Maintained By**: EODHD Skills Team
