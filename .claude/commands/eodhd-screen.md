Screen stocks using EODHD screener based on these criteria: $ARGUMENTS

Translate the user's criteria into EODHD screener filters. Common mappings:
- "large cap" → market_capitalization.gte: 10000000000
- "mid cap" → market_capitalization.gte: 2000000000, market_capitalization.lte: 10000000000
- "small cap" → market_capitalization.lte: 2000000000
- "high dividend" → dividend_yield.gte: 3
- "low P/E" or "cheap" → earnings_share.gte: 0 (positive earnings) + sort by P/E
- "tech" → sector: Technology
- "healthcare" → sector: Healthcare
- Sector names, industry names, exchange codes as filters

Use the `stock-screener` skill workflow:
1. Run screener with translated filters (limit 20)
2. For top 5-10 results, fetch fundamentals for deeper detail
3. Fetch recent price data for performance context

Present:
- **Filters Applied** — show the JSON filter used
- **Results Table** — ticker, name, sector, market cap, P/E, dividend yield, price, 30d change
- **Top 5 Deep Dive** — expanded valuation and growth metrics for best matches
- **Summary** — key themes and patterns in results

If criteria are vague, ask for clarification or suggest reasonable defaults.

Include disclaimer: "This is not financial advice. Data is for informational purposes only."
