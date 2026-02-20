# Skill: eodhd-api

## Purpose

Use EODHD market data APIs to fetch, normalize, and summarize financial data including:
- Prices (historical, intraday, real-time)
- Company fundamentals and financial statements
- Options data with Greeks (from EODHD Marketplace)
- Technical indicators
- News and sentiment
- Macro-economic indicators
- Corporate events (dividends, splits, earnings, IPOs)
- US Treasury interest rates (bill rates, long-term rates, yield curves, real yield curves)
- ESG / environmental scores (from EODHD Marketplace — Investverte)
- Risk analytics and multi-factor reports (from EODHD Marketplace — PRAAMS)
- Bank financials and bond analysis (from EODHD Marketplace — PRAAMS)
- Investment analytics: performance, volatility, risk/return (from EODHD Marketplace — Illio)
- Tick-level market data (from EODHD Marketplace)
- Trading hours and market status (from EODHD Marketplace — TradingHours)

Supports equities, ETFs, indices, forex, crypto, and bonds across 70+ exchanges worldwide.

## Trigger

Use this skill whenever the user's task involves **financial data, markets, investing, or building financial tools**. This includes — but is not limited to — the categories below.

### Direct data requests
- End-of-day or historical stock/ETF/index/forex/crypto prices
- Intraday price bars (1m, 5m, 1h intervals)
- Real-time or delayed quotes, extended US quotes with bid/ask
- Company fundamentals, financials, valuation metrics, or financial ratios
- Options chains, Greeks, or options analytics (from EODHD Marketplace)
- Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic, ADX, ATR, etc.)
- Company or market news, sentiment scores, trending topics
- Stock screening / filtering by fundamental or technical criteria
- Exchange listings, ticker search, or market metadata
- Macro-economic indicators (GDP, inflation, unemployment, interest rates, trade balance, etc.)
- Corporate calendar events (earnings, dividends, splits, IPOs)
- Insider trading activity (executive purchases, sales, SEC filings)
- ESG scores and environmental data — company, sector, country level (from EODHD Marketplace — Investverte)
- Risk scoring, volatility analytics, beta, risk/return profiles (from EODHD Marketplace — PRAAMS, Illio)
- Bank balance sheets, income statements, bond analysis (from EODHD Marketplace — PRAAMS)
- US Treasury rates (bill rates, long-term rates, yield curves, real yield curves)
- Historical market capitalisation
- Index composition and components
- Bulk data exports for an entire exchange
- Symbol change history and delisted tickers
- Trading hours, market status, and market holidays (from EODHD Marketplace — TradingHours)
- Company logos and branding assets

### Building financial tools and applications
Activate this skill when the user is **programming or designing** any of:
- **Stock screeners / scanners** — filtering stocks by P/E, market cap, sector, growth, dividends, etc.
- **Portfolio trackers** — tracking holdings, calculating P&L, showing allocation
- **Investment dashboards / panels** — visualising market data, watchlists, sector heatmaps
- **Trading systems / bots** — algorithmic or rule-based strategies that need price feeds
- **Backtesting engines** — testing strategies against historical price and volume data
- **Price alert / notification systems** — monitoring price levels, volume spikes, or indicator crossovers
- **Dividend trackers / income planners** — modelling dividend income from a portfolio
- **Earnings calendars / event trackers** — upcoming earnings, IPOs, splits, economic releases
- **Financial data pipelines / ETL** — ingesting market data into databases, data warehouses, or analytics platforms
- **Market data APIs or microservices** — wrapping EODHD data for downstream consumers
- **Charting / technical analysis tools** — rendering candlestick charts, overlaying indicators
- **Options analysis tools** — payoff diagrams, implied volatility surfaces, Greeks dashboards
- **Risk management tools** — VaR calculators, portfolio risk decomposition, drawdown analysis
- **Sector / industry analysis tools** — comparing metrics across sectors or industries
- **Financial reporting generators** — producing PDF / HTML reports with market data
- **Watchlist applications** — letting users curate and monitor symbol lists
- **Market data widgets or embeds** — price tickers, mini-charts, quote cards for websites
- **Robo-advisor prototypes** — automated portfolio construction using fundamental and technical data
- **Tax-loss harvesting helpers** — identifying lots to sell, calculating wash-sale windows
- **Crypto portfolio tools** — tracking crypto alongside equities, forex, and bonds

### Financial analysis, research, and advice
Activate this skill when the user is performing or asking for:
- **Fundamental analysis** — valuation (DCF, comparables), financial-statement review, ratio analysis
- **Technical analysis** — chart patterns, indicator interpretation, support/resistance, trend analysis
- **Quantitative / statistical analysis** — correlation, regression, factor models, Monte Carlo simulation using market data
- **Risk assessment** — portfolio volatility, beta, Sharpe ratio, maximum drawdown, Value at Risk
- **Peer / competitive comparison** — comparing financial metrics across a group of companies
- **Sector or industry research** — analysing sector performance, rotation, relative strength
- **Macro-economic research** — linking GDP, inflation, or interest-rate data to market performance
- **Event studies** — measuring price impact around earnings, M&A announcements, policy changes
- **Insider-activity analysis** — tracking executive buying/selling as a signal
- **ESG / sustainability research** — screening by environmental or governance scores
- **Dividend analysis** — yield, payout ratio, growth rate, sustainability
- **Earnings quality analysis** — trends, surprises, revision momentum
- **IPO research** — upcoming offerings, sector trends, pricing
- **Bond and fixed-income analysis** — yield curves, duration, credit spread trends
- **Currency / forex analysis** — exchange-rate trends, carry-trade research
- **Investment advice or recommendations** — when the user asks "what should I invest in?", "is X a good buy?", or similar questions that benefit from real market data
- **Portfolio allocation or rebalancing** — constructing or adjusting a portfolio using current and historical data
- **Retirement or financial planning** — modelling scenarios that reference market returns, inflation, interest rates
- **Academic or educational projects** — coursework, papers, or tutorials that need real market data

## Required inputs

- **API key** — the `EODHD_API_TOKEN` environment variable. If it is not set, **ask the user to provide their API key interactively**. Once received, export it in the current shell session (`export EODHD_API_TOKEN="<key>"`). The user can obtain a free or paid key at https://eodhd.com/. If the user is concerned the key may have been compromised, they can provide a new key at any time and the session variable will be updated.
- Instrument identifier in EODHD format: `{TICKER}.{EXCHANGE}` (e.g., `AAPL.US`, `BMW.XETRA`)
- Date range (`--from-date`, `--to-date`) for time-series requests
- Endpoint-specific parameters (e.g., `--function` for technical indicators)

## Workflow

1. **Clarify the request**
   - Check that `EODHD_API_TOKEN` is set; if not, ask the user for their key and export it
   - Identify objective: price analysis, screening, fundamentals, event study, etc.
   - Confirm symbol(s), date range, and specific metrics needed
   - Determine output format (tables, charts, summary)

2. **Select endpoint(s)**
   - Reference `references/endpoints.md` or `references/endpoints/` for endpoint specs
   - Choose minimal set of endpoints to satisfy the request
   - Consider endpoint-specific parameters

3. **Execute API calls**
   - Use `scripts/eodhd_client.py` for supported endpoints
   - For unsupported endpoints, construct curl commands per endpoint docs
   - Handle pagination for large result sets

4. **Validate response**
   - Confirm symbol exists and has data for requested range
   - Check for null/missing fields
   - Verify date coverage is adequate

5. **Process and present**
   - Transform data as needed (calculate returns, ratios, etc.)
   - Use `templates/analysis_report.md` for structured output
   - Include tables for comparisons, bullet points for conclusions

6. **Document reproducibility**
   - Include exact commands used
   - Note any data limitations or caveats
   - Provide token-redacted curl examples

## Supported endpoints (Python client)

| Endpoint | Description | Key Parameters |
|----------|-------------|----------------|
| `eod` | Historical OHLCV | `--symbol`, `--from-date`, `--to-date` |
| `intraday` | Intraday bars | `--symbol`, `--interval` (1m/5m/1h) |
| `real-time` | Live quotes | `--symbol` |
| `fundamentals` | Company data | `--symbol` |
| `news` | Financial news with sentiment | `--symbol`, `--limit`, `--from-date` |
| `sentiment` | Daily sentiment scores | `--symbol`, `--from-date`, `--to-date` |
| `news-word-weights` | Trending topics in news | `--symbol`, `--from-date`, `--to-date`, `--limit` |
| `technical` | Technical indicators | `--symbol`, `--function`, `--period` |
| `dividends` | Dividend history | `--symbol` |
| `splits` | Stock splits | `--symbol` |
| `macro-indicator` | Macro data | `--symbol` (country code), `--indicator` |
| `screener` | Stock screener | `--limit`, `--offset` |
| `calendar/earnings` | Earnings calendar | `--from-date`, `--to-date` or `--symbol` |
| `calendar/trends` | Earnings trends | `--symbol` (comma-separated) |
| `calendar/ipos` | IPO calendar | `--from-date`, `--to-date` |
| `calendar/splits` | Stock splits calendar | `--from-date`, `--to-date` or `--symbol` |
| `calendar/dividends` | Dividends calendar | `--symbol` |
| `economic-events` | Economic events | `--from-date`, `--to-date` |
| `insider-transactions` | Insider trading activity | `--symbol`, `--from-date`, `--to-date`, `--limit` |
| `exchange-symbol-list` | Exchange tickers | `--symbol` (exchange code) |
| `exchanges-list` | All exchanges | (no symbol needed) |
| `eod-bulk-last-day` | Bulk EOD data | `--symbol` (exchange code) |
| `bulk-fundamentals` | Bulk fundamentals for exchange | `--symbol` (exchange code), `--symbols`, `--limit`, `--offset`, `--version` |
| `user` | Account details and API usage | (no parameters needed) |
| `us-quote-delayed` | US extended quotes (Live v2) | `--symbol` (comma-separated for batch) |
| `ust/bill-rates` | US Treasury Bill Rates | `--filter-year` |
| `ust/long-term-rates` | US Treasury Long-Term Rates | `--filter-year` |
| `ust/yield-rates` | US Treasury Par Yield Curve Rates | `--filter-year` |
| `ust/real-yield-rates` | US Treasury Par Real Yield Curve Rates | `--filter-year` |

**API call costs**: Most endpoints cost 1 call. `technical` and `intraday` cost 5 calls. `fundamentals` costs 10 calls. News-related endpoints (`news`, `sentiment`, `news-word-weights`) cost 5 calls + 5 per ticker. Bulk endpoints cost 100 calls (+ N symbols if `--symbols` used). See `references/general/rate-limits.md` for full details.

## Output requirements

- **State exact parameters**: symbols, date ranges, endpoints used
- **Separate facts from interpretation**: clearly distinguish API data from analysis
- **Note limitations**: mention missing fields, null values, date gaps
- **Use appropriate formats**:
  - Tables for multi-symbol comparisons
  - Bullet points for conclusions and insights
  - JSON/code blocks for raw data samples
- **Include reproducible commands**: token-redacted curl or client commands

## Guardrails

- **Never fabricate data**: if retrieval fails, report the error and command attempted
- **Validate before acting**: confirm symbol exists before making multiple calls
- **Respect rate limits**: avoid unnecessary duplicate requests
- **Handle errors gracefully**: provide actionable error messages
- **Warn on large requests**: ask for confirmation before broad multi-exchange pulls
- **Protect the API key**: never echo or print the token in plain text to the user. Always redact it in example commands (`EODHD_API_TOKEN=***`). If the user suspects their key is compromised, prompt them to supply a new one and re-export it

## Common patterns

See `references/workflows.md` for detailed recipes.

### Core analysis workflows
1. **Single-ticker deep dive**: EOD + fundamentals + news + insider activity
2. **Peer comparison**: Screener + fundamentals for multiple symbols
3. **Event study**: Intraday bars around earnings/announcements
4. **Macro context**: Stock performance vs. economic indicators
5. **Technical analysis**: Price data + indicators (SMA, RSI, MACD)
6. **Options analysis**: Options chains + Greeks (from EODHD Marketplace)

### Building financial tools
7. **Stock screener / scanner**: Use `screener` endpoint with filters, then enrich top results with `fundamentals` and `eod` for display
8. **Portfolio dashboard**: Combine `real-time` (or `us-quote-delayed`) for live prices, `fundamentals` for holdings data, `eod` for historical P&L charts
9. **Dividend income tracker**: Use `calendar/dividends` + `fundamentals` (dividend yield, payout ratio) + `eod` for ex-date price context
10. **Earnings calendar app**: Use `calendar/earnings` + `calendar/trends` + `intraday` for pre/post-earnings price movement
11. **Backtesting engine data feed**: Bulk-fetch via `eod` or `eod-bulk-last-day`, use `technical` for indicator overlays, `splits` and `dividends` for adjustment
12. **Watchlist with alerts**: Use `real-time` or `us-quote-delayed` for price monitoring, `technical` for indicator-based triggers
13. **Market heatmap / sector view**: Use `screener` by sector, `eod-bulk-last-day` for daily moves, `index-components` for index breakdown

### Research and advice workflows
14. **Investment thesis research**: `fundamentals` (valuation, growth) + `news` (catalysts) + `insider-transactions` (conviction) + `sentiment` (market mood)
15. **Risk assessment**: `eod` (returns series) + `technical` (ATR, Bollinger) + PRAAMS risk-scoring endpoints (from EODHD Marketplace) + macro overlays
16. **ESG screening**: Investverte ESG endpoints (from EODHD Marketplace) + `fundamentals` for financial context
17. **Fixed-income analysis**: UST rate endpoints (bill, long-term, yield, real-yield) + `macro-indicator` for inflation/GDP context
18. **Currency analysis**: Forex pairs via `eod` (e.g., `EURUSD.FOREX`) + `macro-indicator` for interest-rate differentials
19. **IPO pipeline review**: `calendar/ipos` for upcoming offerings + `eod` + `fundamentals` for comparable public companies

## Example commands

```bash
# Historical prices
python eodhd_client.py --endpoint eod --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-01-31

# Company fundamentals
python eodhd_client.py --endpoint fundamentals --symbol MSFT.US

# 50-day SMA
python eodhd_client.py --endpoint technical --symbol NVDA.US --function sma --period 50

# Company news with sentiment
python eodhd_client.py --endpoint news --symbol TSLA.US --limit 10

# Daily sentiment scores
python eodhd_client.py --endpoint sentiment --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-01-31

# Trending topics in news (word weights)
python eodhd_client.py --endpoint news-word-weights --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-01-15 --limit 20

# US inflation data
python eodhd_client.py --endpoint macro-indicator --symbol USA --indicator inflation_consumer_prices_annual

# Stock screener
python eodhd_client.py --endpoint screener --limit 20

# Insider transactions
python eodhd_client.py --endpoint insider-transactions --symbol AAPL.US --from-date 2025-01-01 --limit 50

# Upcoming IPOs
python eodhd_client.py --endpoint calendar/ipos --from-date 2025-01-01 --to-date 2025-03-31

# Stock splits calendar
python eodhd_client.py --endpoint calendar/splits --from-date 2025-01-01 --to-date 2025-01-31

# Bulk fundamentals for an exchange (first 100)
python eodhd_client.py --endpoint bulk-fundamentals --symbol NASDAQ --limit 100

# Bulk fundamentals for specific symbols
python eodhd_client.py --endpoint bulk-fundamentals --symbol NASDAQ --symbols AAPL.US,MSFT.US

# User account details and API usage
python eodhd_client.py --endpoint user

# US extended quote (Live v2)
python eodhd_client.py --endpoint us-quote-delayed --symbol AAPL.US,TSLA.US

# US Treasury Bill Rates for 2012
python eodhd_client.py --endpoint ust/bill-rates --filter-year 2012 --limit 100

# US Treasury Long-Term Rates for 2020
python eodhd_client.py --endpoint ust/long-term-rates --filter-year 2020

# US Treasury Yield Curve for 2023
python eodhd_client.py --endpoint ust/yield-rates --filter-year 2023

# US Treasury Real Yield Curve for 2024
python eodhd_client.py --endpoint ust/real-yield-rates --filter-year 2024
```

## References

### General Documentation
- **Getting Started**: `references/general/README.md` - Start here for setup and basics
- **Authentication**: `references/general/authentication.md` - API tokens, protocols (HTTPS/HTTP), CORS, security
- **Symbol Format**: `references/general/symbol-format.md` - How to format tickers correctly
- **Exchanges**: `references/general/exchanges.md` - Complete list of 70+ exchanges, coverage gaps
- **Update Times**: `references/general/update-times.md` - When data is refreshed
- **Rate Limits**: `references/general/rate-limits.md` - Quotas (~17 req/sec), optimization, error codes
- **Fundamentals API**: `references/general/fundamentals-api.md` - Complete guide to company fundamentals, ETFs, funds, and indices
- **Pricing & Plans**: `references/general/pricing-and-plans.md` - Subscription tiers, WebSocket limits, marketplace
- **SDKs & Integrations**: `references/general/sdks-and-integrations.md` - Official Python/.NET/R SDKs, MCP Server, tools
- **Versioning**: `references/general/versioning.md` - API stability guarantees, backwards-compatibility
- **Glossary**: `references/general/glossary.md` - Financial, technical, and EODHD-specific terms

### Endpoint Documentation
- **Endpoint catalog**: `references/endpoints.md` - Overview of all endpoints
- **Individual endpoint docs**: `references/endpoints/*.md` - Detailed specs per endpoint
- **Analysis workflows**: `references/workflows.md` - Common usage patterns
- **Output template**: `templates/analysis_report.md` - Structured report format
