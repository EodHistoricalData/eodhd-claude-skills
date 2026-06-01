---
name: options-analyzer
description: >-
  Analyze options chains, implied volatility, Greeks, and strategy payoffs
  using EODHD Marketplace options data. Use when the user asks about options,
  implied volatility, Greeks, or options strategies.
version: 0.4.0
---

# Skill: options-analyzer

## Purpose

Analyze US equity options using EODHD Marketplace data — options chains with Greeks, implied volatility analysis, contract comparison, and strategy evaluation.

## Trigger

Activate when the user asks for:
- Options chain for a ticker
- Implied volatility analysis or IV rank
- Greeks analysis (delta, gamma, theta, vega)
- Options strategy evaluation (covered calls, spreads, straddles, etc.)
- Put/call ratio or options flow
- Unusual options activity
- Options expiration analysis

## Workflow

1. **Identify the underlying** — resolve to `TICKER.US` format (US options only)
2. **Fetch options contracts list** — `us-options-underlyings` for available expirations
3. **Fetch options chain** — `us-options-eod` for specific expiration with Greeks
4. **Fetch underlying price** — `eod` or `real-time` for current price context
5. **Analyze** — IV analysis, strategy payoff, Greeks exposure
6. **Compile options report**

> **Note:** Options endpoints (`us-options-eod`, `us-options-underlyings`) are **not wired into the
> `eodhd_client.py` helper** — call them with `curl` per the endpoint docs. Access depends on your plan/tier:
> on many paid plans the US options endpoints return data directly (HTTP 200), so don't assume a separate
> Marketplace add-on is required — verify against your account before telling the user it's gated. Option
> chains can be large (multi-MB); summarize, don't dump raw JSON into the chat.

## Output Structure

### Options Analysis — [Ticker] — [Date]

**Underlying Context**
- Current Price: —
- 52-Week Range: —
- Next Earnings: —
- Historical Volatility (30d): —

**Options Chain Summary**
| Expiration | Days to Exp | Calls OI | Puts OI | P/C Ratio | ATM IV |
|-----------|------------|---------|---------|-----------|--------|

**Selected Chain — [Expiration Date]**

*Calls*
| Strike | Last | Bid | Ask | Vol | OI | IV | Delta | Gamma | Theta | Vega |
|--------|------|-----|-----|-----|----|----|-------|-------|-------|------|

*Puts*
| Strike | Last | Bid | Ask | Vol | OI | IV | Delta | Gamma | Theta | Vega |
|--------|------|-----|-----|-----|----|----|-------|-------|-------|------|

**IV Analysis**
- ATM Implied Volatility: —
- IV Rank (vs 52-week range): —
- IV Skew (puts vs calls): —
- Term structure (near vs far expirations)

**Strategy Analysis** (if requested)
- Strategy description
- Max profit / Max loss / Breakeven
- Greeks exposure (net delta, gamma, theta, vega)
- Probability of profit estimate

> This is not financial advice. Data is for informational purposes only.
> Options trading involves significant risk. Past performance does not guarantee future results.

## Endpoints Used

| Endpoint | Purpose | Cost | Access |
|----------|---------|------|--------|
| `us-options-underlyings` | Available contracts | 10 calls | Marketplace |
| `us-options-eod` | EOD chain with Greeks | 10 calls | Marketplace |
| `us-options-contracts` | Historical contract data | 10 calls | Marketplace |
| `eod` | Underlying price history | 1 call | Standard |
| `technical` | Historical volatility | 5 calls | Standard |

## References

- `../eodhd-api/references/endpoints/us-options-underlyings.md`
- `../eodhd-api/references/endpoints/us-options-eod.md`
- `../eodhd-api/references/endpoints/us-options-contracts.md`
- `../eodhd-api/references/endpoints/historical-stock-prices.md`
- `../eodhd-api/references/endpoints/technical-indicators.md`
