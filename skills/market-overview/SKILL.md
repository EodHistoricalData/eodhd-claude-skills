---
name: market-overview
description: >-
  Generate a broad market overview — major indices, sector performance, top
  movers, macro indicators, Treasury rates, and commodities. Use when the user
  asks "how's the market?", wants a daily market summary, or needs a macro
  context for investment decisions.
version: 0.4.0
---

# Skill: market-overview

## Purpose

Produce a comprehensive market overview combining index performance, sector breakdown, macro-economic data, Treasury rates, and commodity prices from EODHD data.

## Trigger

Activate when the user asks for:
- Market overview, market summary, or "how's the market?"
- Sector performance or rotation analysis
- Daily/weekly market recap
- Macro context for the market
- Treasury yield curve or interest rate overview
- Commodity prices overview

## Workflow

1. **Fetch major indices** — `eod` for S&P 500 (`GSPC.INDX`), Nasdaq (`IXIC.INDX`), Dow (`DJI.INDX`), Russell 2000 (`RUT.INDX`)
2. **Fetch international indices** — FTSE, DAX, Nikkei, Shanghai as needed
3. **Fetch sector ETFs** — `eod-bulk-last-day` or individual sector ETF prices (XLK, XLF, XLV, XLE, XLI, etc.)
4. **Fetch Treasury rates** — `ust/yield-rates`, `ust/bill-rates` for yield curve
5. **Fetch macro data** — `macro-indicator` for latest GDP, CPI, unemployment
6. **Fetch commodities** — `eod` for gold (`GC.COMEX`), oil (`CL.COMEX`), etc.
7. **Compile overview**

## Output Structure

### Market Overview — [Date]

**Major Indices**
| Index | Last | Change | % Change | YTD |
|-------|------|--------|----------|-----|
| S&P 500 | — | — | — | — |
| Nasdaq Composite | — | — | — | — |
| Dow Jones | — | — | — | — |
| Russell 2000 | — | — | — | — |

**Sector Performance (Today)**
| Sector | ETF | Change % |
|--------|-----|----------|
| Technology | XLK | — |
| Financials | XLF | — |
| Healthcare | XLV | — |
| Energy | XLE | — |
| ... | ... | ... |

**Treasury Yield Curve**
| Maturity | Yield | Change |
|----------|-------|--------|
| 1M | — | — |
| 3M | — | — |
| 2Y | — | — |
| 10Y | — | — |
| 30Y | — | — |
- Spread (10Y-2Y): — bps
- Curve shape: normal / flat / inverted

**Commodities**
| Commodity | Price | Change % |
|-----------|-------|----------|
| Gold | — | — |
| Crude Oil (WTI) | — | — |
| Silver | — | — |
| Natural Gas | — | — |

**Macro Snapshot**
- GDP Growth (latest): —
- CPI (latest): —
- Unemployment Rate: —
- Fed Funds Rate: —

**Key Takeaways**
- 3-5 bullet points on market themes

> This is not financial advice. Data is for informational purposes only.

## Endpoints Used

| Endpoint | Purpose | Cost |
|----------|---------|------|
| `eod` | Index/commodity prices | 1 call each |
| `eod-bulk-last-day` | Sector ETFs in bulk | 100 calls |
| `ust/yield-rates` | Treasury yield curve | 1 call |
| `ust/bill-rates` | Short-term rates | 1 call |
| `macro-indicator` | GDP, CPI, unemployment | 1 call each |

## References

- `../eodhd-api/references/endpoints/historical-stock-prices.md`
- `../eodhd-api/references/endpoints/ust-yield-rates.md`
- `../eodhd-api/references/endpoints/ust-bill-rates.md`
- `../eodhd-api/references/endpoints/macro-indicator.md`
- `../eodhd-api/references/general/indices-data-notes.md`
