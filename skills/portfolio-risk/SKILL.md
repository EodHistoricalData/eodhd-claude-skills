---
name: portfolio-risk
description: >-
  Analyze portfolio risk — technical indicators, sentiment shifts, insider
  alerts, ESG scores, and volatility metrics. Use when the user asks about
  portfolio risk, wants to assess holdings, or needs risk/reward analysis.
version: 0.4.0
---

# Skill: portfolio-risk

## Purpose

Perform multi-dimensional risk analysis on a portfolio or individual holdings using EODHD data — combining technical indicators, sentiment analysis, insider activity signals, and fundamental risk metrics.

## Trigger

Activate when the user asks for:
- Portfolio risk analysis or assessment
- Risk/reward evaluation of holdings
- Volatility analysis or drawdown risk
- Insider selling alerts for portfolio positions
- Sentiment shifts or deterioration for holdings
- Concentration risk or sector exposure analysis

## Workflow

1. **Get portfolio** — confirm ticker list and optional weights
2. **Fetch price history** — `eod` for each holding (6-12 months)
3. **Calculate risk metrics** — returns, volatility, max drawdown, correlation
4. **Fetch technicals** — `technical` for RSI, Bollinger Bands, ATR per holding
5. **Fetch sentiment** — `sentiment` for each holding (recent trend)
6. **Fetch insider activity** — `insider-transactions` for each holding
7. **Fetch fundamentals** — `fundamentals` for debt ratios, beta, sector allocation
8. **Compile risk report**

## Output Structure

### Portfolio Risk Analysis — [Date]

**Portfolio Composition**
| Ticker | Weight | Sector | Market Cap |
|--------|--------|--------|-----------|

**Risk Metrics**
| Metric | Portfolio | Benchmark (S&P) |
|--------|-----------|-----------------|
| Annualized Volatility | — | — |
| Max Drawdown (12M) | — | — |
| Beta | — | — |
| Sharpe Ratio | — | — |

**Per-Holding Risk Signals**
| Ticker | RSI | Bollinger %B | ATR% | Sentiment | Insider Net |
|--------|-----|-------------|------|-----------|------------|

**Risk Alerts**
- Overbought/oversold signals (RSI > 70 or < 30)
- Negative sentiment trends
- Significant insider selling
- High concentration in single sector/stock
- Elevated volatility vs historical norms

**Sector Exposure**
| Sector | Weight | Count |
|--------|--------|-------|

**Recommendations**
- Diversification suggestions
- Hedging considerations
- Positions requiring attention

> This is not financial advice. Data is for informational purposes only.

## Endpoints Used

| Endpoint | Purpose | Cost |
|----------|---------|------|
| `eod` | Price history for returns | 1 call/ticker |
| `technical` | RSI, Bollinger, ATR | 5 calls/ticker |
| `sentiment` | Sentiment scores | 5 + 5/ticker |
| `insider-transactions` | Insider activity | 1 call/ticker |
| `fundamentals` | Beta, debt, sector | 10 calls/ticker |

## References

- `../eodhd-api/references/endpoints/technical-indicators.md`
- `../eodhd-api/references/endpoints/sentiment-data.md`
- `../eodhd-api/references/endpoints/insider-transactions.md`
- `../eodhd-api/references/endpoints/fundamentals-data.md`
- `../eodhd-api/references/endpoints/historical-stock-prices.md`
