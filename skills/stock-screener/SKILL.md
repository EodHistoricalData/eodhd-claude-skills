---
name: stock-screener
description: >-
  Screen stocks by fundamental and technical criteria using EODHD screener —
  filter by market cap, P/E, dividend yield, sector, signals, and more.
  Use when the user wants to find stocks matching specific criteria.
version: 0.4.0
---

# Skill: stock-screener

## Purpose

Find stocks matching user-defined criteria using EODHD's screener endpoint, then enrich top results with detailed fundamentals and price data for comparison.

## Trigger

Activate when the user asks for:
- Stock screening or filtering ("find stocks with P/E under 15")
- "Best dividend stocks" or "cheap growth stocks"
- Sector-specific stock lists
- Signal-based screening (new highs, oversold, etc.)
- Comparative analysis of filtered stocks
- "What should I invest in?" (screen first, then analyze)

## Workflow

1. **Translate criteria to filters** — map user language to EODHD screener JSON filters
2. **Run screener** — `screener` endpoint with filters, sort, signals, limit
3. **Review results** — present initial list with key metrics
4. **Enrich top picks** — `fundamentals` for detailed data on top 5-10 results
5. **Add price context** — `eod` for recent price trends
6. **Compile screener report**

## Filter Format (critical)

`filters` is a **JSON array of `[field, operation, value]` triples** — NOT dot-notation
(`market_capitalization.gte`) and NOT a JSON object. If the shape is wrong, the EODHD API
silently ignores the filter and returns unfiltered, irrelevant results.

Operations: `=`, `!=`, `>`, `>=`, `<`, `<=`, `match`. A JSON object is rejected with HTTP 422.

```json
[["market_capitalization",">=",10000000000],["sector","=","Technology"]]
```

**Sort:** `--sort field.direction` (e.g. `market_capitalization.desc`, `pe.asc`). A bare field name is
rejected with HTTP 422 ("sort.0.direction is required").

**Currency caveat (important):** absolute-money fields — `market_capitalization`, `revenue`, `ebitda` — are
in each listing's **local currency**, not USD. A raw threshold leaks huge non-USD companies (e.g. a
Vietnam-listed firm at "3.88T" ₫ ≈ $150M passes `>= 10B`). Each result row has a `currency_symbol` field
indicating its currency. So:
- Filtering/sorting by an absolute-money field → **scope to one market** with `["exchange","=","us"]` (or the
  intended exchange) so the threshold is currency-consistent.
- Multi-market screens → don't compare raw caps across rows; group/label by `currency_symbol`.
- Ratio/percent fields (`pe`, `pb`, `ps`, `peg`, `roe`, `roa`, `beta`, `dividend_yield`) are
  currency-independent and safe to compare across markets.

## Available Filters

The screener supports these filter fields:
- `market_capitalization` — market cap in the listing's **local currency** (see currency caveat; scope by `exchange` for a consistent threshold)
- `earnings_share` — EPS
- `dividend_yield` — dividend yield as a **fraction** (0.03 = 3%, not 3)
- `sector` — sector name (exact match)
- `industry` — industry name (exact match)
- `exchange` — exchange code (e.g., `us`)
- `pe` — P/E ratio
- `wallstreet_target_price` — analyst target price
- Plus many more fundamental fields (see endpoint reference)

Each result row also returns `currency_symbol` (currency of the absolute-money fields) and `exchange` — surface these when presenting caps.

## Available Signals

- `50d_new_hi` / `50d_new_lo` — 50-day new high/low
- `200d_new_hi` / `200d_new_lo` — 200-day new high/low
- `bookvalue_neg` — negative book value
- `wallstreet_lo` / `wallstreet_hi` — at analyst low/high

## Output Structure

### Stock Screener Results — [Criteria Description]

**Filter Applied**
```json
{filters_used}
```

**Results ([N] matches)**
| # | Ticker | Name | Sector | Mkt Cap (ccy) | P/E | Div Yield | Price |
|---|--------|------|--------|---------------|-----|-----------|-------|

Show the `currency_symbol` alongside Mkt Cap; never render a non-USD cap as USD. If the screen spans multiple currencies, say so in the Summary caveats.

**Top Picks — Detailed Analysis**
For each top 5 result:
- Valuation metrics (P/E, P/S, P/B, EV/EBITDA)
- Growth metrics (Revenue growth, EPS growth)
- Profitability (margins, ROE)
- 30-day price trend
- Analyst target vs current price

**Sector Distribution**
| Sector | Count | Avg P/E | Avg Yield |
|--------|-------|---------|-----------|

**Summary**
- Key themes in results
- Caveats and limitations

> This is not financial advice. Data is for informational purposes only.

## Example Filters

```bash
# High-dividend large caps (dividend_yield is a fraction: 0.03 = 3%; exchange=us keeps caps in USD)
python eodhd_client.py --endpoint screener --filters '[["dividend_yield",">=",0.03],["market_capitalization",">=",10000000000],["exchange","=","us"]]' --sort market_capitalization.desc --limit 20

# Undervalued growth stocks
python eodhd_client.py --endpoint screener --filters '[["market_capitalization",">=",1000000000],["earnings_share",">=",1],["exchange","=","us"]]' --signals 200d_new_lo --limit 20

# Tech sector screening
python eodhd_client.py --endpoint screener --filters '[["sector","=","Technology"],["market_capitalization",">=",5000000000],["exchange","=","us"]]' --sort market_capitalization.desc --limit 30
```

## Endpoints Used

| Endpoint | Purpose | Cost |
|----------|---------|------|
| `screener` | Filter and rank stocks | 1 call |
| `fundamentals` | Detailed data for top picks | 10 calls/ticker |
| `eod` | Price context | 1 call/ticker |

## References

- `../eodhd-api/references/endpoints/stock-screener-data.md`
- `../eodhd-api/references/endpoints/fundamentals-data.md`
- `../eodhd-api/references/endpoints/historical-stock-prices.md`
