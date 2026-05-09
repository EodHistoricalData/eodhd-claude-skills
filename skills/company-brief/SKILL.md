---
name: company-brief
description: >-
  Generate a comprehensive company snapshot using EODHD data — profile,
  fundamentals, recent news, sentiment, insider transactions, and key metrics.
  Use when the user asks about a specific company, wants a stock overview,
  or needs a quick investment brief.
version: 0.4.0
---

# Skill: company-brief

## Purpose

Build a comprehensive company brief combining multiple EODHD data sources into a single actionable snapshot. Covers company profile, financial fundamentals, recent news with sentiment, insider activity, and key valuation/growth metrics.

## Trigger

Activate when the user asks for:
- Company overview, profile, or "tell me about [ticker]"
- Stock summary or investment brief
- Company fundamentals with context
- "What does [company] do?" with financial data
- Quick due diligence on a ticker

## Workflow

1. **Identify the ticker** — resolve to `TICKER.EXCHANGE` format (e.g., `AAPL.US`)
2. **Fetch fundamentals** — `fundamentals` endpoint for profile, valuation, financials
3. **Fetch recent prices** — `eod` endpoint for last 30-90 days of price history
4. **Fetch news** — `news` endpoint (limit 10) for recent headlines and sentiment
5. **Fetch sentiment** — `sentiment` endpoint for daily sentiment scores
6. **Fetch insider activity** — `insider-transactions` endpoint for recent insider trades
7. **Compile brief** using the structure below

## Output Structure

### [Company Name] (`TICKER.EXCHANGE`) — Company Brief

**Profile**
- Sector, Industry, Country, Exchange
- Market Cap, Enterprise Value
- Employees, IPO Date
- Business description (2-3 sentences)

**Valuation Snapshot**
| Metric | Value |
|--------|-------|
| P/E (TTM) | — |
| Forward P/E | — |
| P/S | — |
| P/B | — |
| EV/EBITDA | — |
| Dividend Yield | — |

**Financial Highlights (TTM)**
- Revenue, Net Income, EPS
- Revenue Growth YoY
- Gross Margin, Operating Margin, Net Margin
- ROE, ROA, ROIC

**Price Action (last 30 days)**
- Current price, 30d change %
- 52-week high/low, distance from highs

**Recent News & Sentiment**
- Top 5 headlines with dates and sentiment scores
- Average sentiment trend

**Insider Activity**
- Recent insider buys/sells (last 90 days)
- Net insider sentiment (buying vs selling)

**Key Takeaways**
- 3-5 bullet points summarizing the investment picture

> This is not financial advice. Data is for informational purposes only.

## Endpoints Used

| Endpoint | Purpose | Cost |
|----------|---------|------|
| `fundamentals` | Profile, valuation, financials | 10 calls |
| `eod` | Price history | 1 call |
| `news` | Recent headlines + sentiment | 5 + 5/ticker |
| `sentiment` | Daily sentiment scores | 5 + 5/ticker |
| `insider-transactions` | Insider trading activity | 1 call |

## References

- `../eodhd-api/references/endpoints/fundamentals-data.md`
- `../eodhd-api/references/endpoints/historical-stock-prices.md`
- `../eodhd-api/references/endpoints/company-news.md`
- `../eodhd-api/references/endpoints/sentiment-data.md`
- `../eodhd-api/references/endpoints/insider-transactions.md`
- `../eodhd-api/references/general/fundamentals-api.md`
