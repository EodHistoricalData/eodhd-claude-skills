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

## Available Filters

The screener supports these filter fields:
- `market_capitalization` — market cap range
- `earnings_share` — EPS
- `dividend_yield` — dividend yield %
- `sector` — sector name
- `industry` — industry name
- `exchange` — exchange code
- `wallstreet_target_price` — analyst target price
- Plus many more fundamental fields

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
| # | Ticker | Name | Sector | Mkt Cap | P/E | Div Yield | Price |
|---|--------|------|--------|---------|-----|-----------|-------|

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
# High-dividend large caps
python eodhd_client.py --endpoint screener --filters '{"market_capitalization.gte":10000000000,"dividend_yield.gte":3}' --sort market_capitalization.desc --limit 20

# Undervalued growth stocks
python eodhd_client.py --endpoint screener --filters '{"market_capitalization.gte":1000000000,"earnings_share.gte":1}' --signals 200d_new_lo --limit 20

# Tech sector screening
python eodhd_client.py --endpoint screener --filters '{"sector":"Technology","market_capitalization.gte":5000000000}' --limit 30
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
