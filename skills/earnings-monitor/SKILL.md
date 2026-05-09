---
name: earnings-monitor
description: >-
  Monitor upcoming and recent earnings — calendar, trends, news context, and
  options activity around earnings dates. Use when the user asks about earnings
  season, upcoming reports, earnings surprises, or pre/post-earnings analysis.
version: 0.4.0
---

# Skill: earnings-monitor

## Purpose

Track and analyze earnings events using EODHD data — upcoming earnings calendar, historical earnings trends (EPS estimates vs actuals), related news, and intraday price action around earnings dates.

## Trigger

Activate when the user asks for:
- Upcoming earnings calendar or "who reports this week"
- Earnings history, surprises, or beat/miss analysis
- Pre-earnings or post-earnings price movement
- Earnings trends and estimate revisions
- Event-driven analysis around earnings dates

## Workflow

1. **Determine scope** — specific ticker(s) or date range for calendar view
2. **Fetch earnings calendar** — `calendar/earnings` with date range or symbols
3. **Fetch earnings trends** — `calendar/trends` for EPS estimates, revisions, growth
4. **Fetch related news** — `news` endpoint filtered around earnings dates
5. **Fetch price action** — `intraday` or `eod` around earnings date for reaction analysis
6. **Compile earnings report**

## Output Structure

### Earnings Monitor — [Ticker or Date Range]

**Upcoming Earnings**
| Date | Company | Ticker | EPS Estimate | Revenue Estimate | Time |
|------|---------|--------|-------------|-----------------|------|

**Earnings Trends** (for specific tickers)
- EPS trend (last 4 quarters): actual vs estimate
- Revenue trend (last 4 quarters)
- Surprise history (% beat/miss)
- Analyst revision direction (up/down/flat)

**Price Reaction Analysis**
- Pre-earnings drift (5 days before)
- Post-earnings move (day of + next day)
- Historical earnings-day volatility

**Related News**
- Headlines around earnings date with sentiment

**Key Insights**
- Notable surprises or misses
- Sectors with heavy reporting
- Estimate revision trends

> This is not financial advice. Data is for informational purposes only.

## Endpoints Used

| Endpoint | Purpose | Cost |
|----------|---------|------|
| `calendar/earnings` | Earnings dates and estimates | 1 call |
| `calendar/trends` | EPS/revenue trends and revisions | 1 call |
| `news` | Earnings-related news | 5 + 5/ticker |
| `eod` | Price around earnings | 1 call |
| `intraday` | Intraday reaction | 5 calls |

## References

- `../eodhd-api/references/endpoints/upcoming-earnings.md`
- `../eodhd-api/references/endpoints/earnings-trends.md`
- `../eodhd-api/references/endpoints/company-news.md`
- `../eodhd-api/references/endpoints/intraday-historical-data.md`
