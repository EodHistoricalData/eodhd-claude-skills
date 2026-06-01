---
name: macro-dashboard
description: >-
  Macro-economic dashboard — GDP, CPI, unemployment, interest rates, Treasury
  yields, trade balance, and economic events calendar. Use when the user asks
  about the economy, macro trends, interest rates, or economic indicators.
version: 0.4.0
---

# Skill: macro-dashboard

## Purpose

Build a comprehensive macro-economic dashboard using EODHD data — combining macro indicators across countries, Treasury yield curves, and economic events calendar for a complete economic picture.

## Trigger

Activate when the user asks for:
- Macro-economic overview or dashboard
- GDP, inflation, unemployment data
- Interest rate trends or yield curve analysis
- Economic calendar or upcoming events
- Country economic comparison
- "How's the economy?"
- Trade balance or current account data
- Central bank policy context

## Workflow

1. **Determine scope** — country/countries and indicators of interest
2. **Fetch macro indicators** — `macro-indicator` for GDP, CPI, unemployment, etc.
3. **Fetch Treasury rates** — `ust/yield-rates`, `ust/bill-rates`, `ust/long-term-rates`, `ust/real-yield-rates`
4. **Fetch economic events** — `economic-events` for upcoming releases. Always pass an explicit
   `--from-date`/`--to-date` window (e.g. today → +14d) and `--country` — without them the API returns
   arbitrary far-future events with empty fields. Field mapping: event name = `type` (NOT `event`),
   forecast = `estimate` (NOT `forecast`), plus `previous`/`actual` (`actual` is null until released).
5. **Calculate trends** — YoY changes, trends, inflection points
6. **Compile dashboard**

## Available Macro Indicators

Key indicators available via `macro-indicator` endpoint:
- `gdp_current_usd` — GDP in current USD
- `gdp_growth_annual` — Annual GDP growth %
- `inflation_consumer_prices_annual` — CPI annual %
- `unemployment_total_percent` — Unemployment rate %
- `interest_rate` — Central bank policy rate
- `trade_balance_percent_gdp` — Trade balance as % of GDP
- `current_account_percent_gdp` — Current account as % of GDP
- `government_debt_percent_gdp` — Government debt as % of GDP
- `population_total` — Total population
- Many more (50+ indicators per country)

Country codes: `USA`, `GBR`, `DEU`, `JPN`, `CHN`, `FRA`, `CAN`, `AUS`, etc.

## Output Structure

### Macro Dashboard — [Country/Region] — [Date]

**Key Economic Indicators**
| Indicator | Latest | Previous | YoY Change | Trend |
|-----------|--------|----------|-----------|-------|
| GDP Growth | — | — | — | ↑/↓/→ |
| CPI (Annual) | — | — | — | ↑/↓/→ |
| Unemployment | — | — | — | ↑/↓/→ |
| Interest Rate | — | — | — | ↑/↓/→ |
| Trade Balance | — | — | — | ↑/↓/→ |
| Govt Debt/GDP | — | — | — | ↑/↓/→ |

**US Treasury Yield Curve**
| Maturity | Current Yield | 1M Ago | 1Y Ago |
|----------|--------------|--------|--------|
| 1M | — | — | — |
| 3M | — | — | — |
| 6M | — | — | — |
| 1Y | — | — | — |
| 2Y | — | — | — |
| 5Y | — | — | — |
| 10Y | — | — | — |
| 20Y | — | — | — |
| 30Y | — | — | — |

- 2Y-10Y Spread: — bps (normal/inverted)
- Real yields (inflation-adjusted): 5Y —, 10Y —, 30Y —

**Upcoming Economic Events**
| Date | Event | Country | Actual | Forecast | Previous |
|------|-------|---------|--------|----------|----------|

**Economic Narrative**
- Summary of current economic cycle phase
- Key risks and tailwinds
- Central bank policy outlook
- Cross-country comparisons (if multi-country)

> This is not financial advice. Data is for informational purposes only.

## Endpoints Used

| Endpoint | Purpose | Cost |
|----------|---------|------|
| `macro-indicator` | GDP, CPI, unemployment, etc. | 1 call each |
| `ust/yield-rates` | Par yield curve | 1 call |
| `ust/bill-rates` | Short-term Treasury rates | 1 call |
| `ust/long-term-rates` | Long-term Treasury rates | 1 call |
| `ust/real-yield-rates` | Inflation-adjusted yields | 1 call |
| `economic-events` | Upcoming economic releases | 1 call |

## References

- `../eodhd-api/references/endpoints/macro-indicator.md`
- `../eodhd-api/references/endpoints/ust-yield-rates.md`
- `../eodhd-api/references/endpoints/ust-bill-rates.md`
- `../eodhd-api/references/endpoints/ust-long-term-rates.md`
- `../eodhd-api/references/endpoints/ust-real-yield-rates.md`
- `../eodhd-api/references/endpoints/economic-events.md`
