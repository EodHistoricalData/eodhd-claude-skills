# EODHD Skills Adapter for Claude/Codex

Reusable skills and adapters for using the [EOD Historical Data (EODHD) API](https://eodhd.com/) from Claude- and Codex-style agent workflows.

> **Disclaimer**: This skill set may differ from actual EODHD API endpoints and behavior, both due to possible errors and contradictions in the documentation and because the API is constantly changing and evolving. Furthermore, Claude and the Codex may interpret the information provided incorrectly. Some data, such as update times, is empirical in nature and is provided for guidance only. For any questions, please email supportlevel1@eodhistoricaldata.com

## Table of Contents

- [Installation](#installation)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Usage Tips](#usage-tips)
- [Supported Endpoints](#supported-endpoints)
- [General Reference Documentation](#general-reference-documentation)
- [Usage Examples](#usage-examples)
- [Workflows](#workflows)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Claude Code (Plugin System)

```bash
# Register the marketplace
/plugin marketplace add Enlavan/eodhd-claude-skills

# Install the plugin
/plugin install eodhd-api@eodhd-claude-skills
```

**Manage the plugin:**

```bash
/plugin update eodhd-api@eodhd-claude-skills      # Update to latest version
/plugin enable eodhd-api@eodhd-claude-skills       # Enable
/plugin disable eodhd-api@eodhd-claude-skills      # Disable
/plugin uninstall eodhd-api@eodhd-claude-skills    # Uninstall
```

### Manual Setup

Clone the repository and set your API token:

```bash
git clone https://github.com/Enlavan/eodhd-claude-skills.git
export EODHD_API_TOKEN="your_token_here"
```

## Overview

This repository provides a skill adapter that enables AI agents (Claude, Codex, etc.) to interact with the EODHD financial data API. It includes:

- **Skill definitions** with trigger conditions, workflows, and output standards
- **Endpoint documentation** for 72 EODHD API endpoints
- **General reference guides** covering 28 topics (exchanges, symbol format, rate limits, fundamentals, etc.)
- **A lightweight Python client** (stdlib-only, no external dependencies)
- **Analysis templates** for consistent, auditable output
- **Adapter guides** for different AI environments

## Prerequisites

1. **EODHD API Token**: Get one at [eodhd.com](https://eodhd.com/)
2. **Python 3.8+** (for the helper client)
3. No external Python packages required (stdlib-only)

## Repository Structure

```
eodhd-claude-skills/
├── .claude-plugin/
│   └── marketplace.json          # Plugin manifest for Claude Code
├── .github/
│   └── workflows/
│       └── release.yml           # Auto-release on version bump
├── skills/
│   └── eodhd-api/
│       ├── SKILL.md              # Primary skill definition
│       ├── references/
│       │   ├── general/          # General reference guides (28 files)
│       │   ├── endpoints/        # Individual endpoint docs (72 files)
│       │   ├── subscriptions/    # Subscription plan guides (7 plans)
│       │   └── workflows.md      # Common analysis patterns
│       ├── scripts/
│       │   └── eodhd_client.py   # Lightweight Python API client
│       └── templates/
│           └── analysis_report.md
├── adapters/
│   ├── claude/
│   │   └── eodhd-api.md          # Claude environment adapter
│   └── codex/
│       └── eodhd-api.md          # Codex environment adapter
├── CLAUDE.md                     # Claude Code project context
└── README.md
```

## Quick Start

### 1. Set your API token

```bash
export EODHD_API_TOKEN="your_token_here"
```

> If you installed via the plugin system, the skill is already available in Claude Code. Just set the token and start asking for financial data.

### 2. Use the helper client

```bash
# Get historical prices
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint eod \
  --symbol AAPL.US \
  --from-date 2025-01-01 \
  --to-date 2025-01-31

# Get company fundamentals
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint fundamentals \
  --symbol MSFT.US

# Get intraday data
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint intraday \
  --symbol TSLA.US \
  --interval 5m \
  --from-date 2025-01-15

# List exchange symbols
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint exchange-symbol-list \
  --symbol US
```

### 3. Use in agent prompts

```
Use the `eodhd-api` plugin. Pull daily prices for AAPL.US from 2025-01-01 to 2025-01-31,                                                           
include fundamentals summary, and return a concise analyst report with reproducible calls. Use "demo" API key.
```

## Usage Tips

After installing the skill plugin, Claude Code won't always use it automatically — you may need to nudge it. Here are a few ways to make sure the skill gets picked up:

### Prompt prefix

Start your message with a line like:

```
Use available skills and plugins you have access to whenever possible.
Get me AAPL.US daily prices for the last 30 days and summarize the trend.
```

Or reference the skill explicitly:

```
Use the eodhd-api plugin. Show me fundamentals for MSFT.US.
```

### Add a project-level instruction

Create or edit a `CLAUDE.md` in your project root and add:

```markdown
Always use available skills (especially `eodhd-api`) when handling financial data requests.
```

Claude Code reads `CLAUDE.md` at the start of every session, so this acts as a persistent hint.

### Add a global instruction

To apply the hint across all projects, add the following to your `~/.claude/CLAUDE.md`:

```markdown
Use available skills whenever they match the task at hand.
```

### Why is this needed?

Claude Code currently treats installed skills as optional context. It will use them when it recognizes a strong match, but for broad or ambiguous requests it may fall back to general knowledge. An explicit mention — either in the prompt or in `CLAUDE.md` — makes the match unambiguous.

## Supported Endpoints

### Python Client (Built-in)

| Endpoint | Description | Symbol Required |
|----------|-------------|-----------------|
| `eod` | End-of-day historical OHLCV | Yes (e.g., AAPL.US) |
| `intraday` | Intraday price bars | Yes |
| `fundamentals` | Company fundamentals | Yes |
| `exchange-symbol-list` | List symbols on exchange | Yes (exchange code, e.g., US) |
| `screener` | Stock screener | No |

See `skills/eodhd-api/SKILL.md` for the full list of client-supported endpoints.

### Documented Endpoints (72 total)

The `skills/eodhd-api/references/endpoints/` directory contains documentation for each endpoint. See `skills/eodhd-api/references/endpoints/README.md` for the complete index.

#### Market Data

| Endpoint | File |
|----------|------|
| Historical Stock Prices (EOD) | `historical-stock-prices.md` |
| Intraday Historical Data | `intraday-historical-data.md` |
| Live Price Data | `live-price-data.md` |
| US Live Extended Quotes | `us-live-extended-quotes.md` |
| WebSockets Real-Time Data | `websockets-realtime.md` |
| Technical Indicators | `technical-indicators.md` |
| Stock Screener Data | `stock-screener-data.md` |
| Stocks From Search | `stocks-from-search.md` |
| Stock Market Logos (PNG) | `stock-market-logos.md` |
| Stock Market Logos (SVG) | `stock-market-logos-svg.md` |
| Historical Market Cap | `historical-market-cap.md` |
| Symbol Change History | `symbol-change-history.md` |

#### Fundamentals & Company Data

| Endpoint | File |
|----------|------|
| Fundamentals Data | `fundamentals-data.md` |
| Bulk Fundamentals | `bulk-fundamentals.md` |
| Company News | `company-news.md` |
| Sentiment Data | `sentiment-data.md` |
| News Word Weights | `news-word-weights.md` |
| Insider Transactions | `insider-transactions.md` |

#### Calendar & Events

| Endpoint | File |
|----------|------|
| Upcoming Earnings | `upcoming-earnings.md` |
| Earnings Trends | `earnings-trends.md` |
| Upcoming Dividends | `upcoming-dividends.md` |
| Upcoming Splits | `upcoming-splits.md` |
| Upcoming IPOs | `upcoming-ipos.md` |
| Economic Events | `economic-events.md` |

#### Exchange & Index Data

| Endpoint | File |
|----------|------|
| Exchanges List | `exchanges-list.md` |
| Exchange Details | `exchange-details.md` |
| Exchange Tickers | `exchange-tickers.md` |
| Index Components | `index-components.md` |
| Indices List | `indices-list.md` |
| CBOE Index Data | `cboe-index-data.md` |
| CBOE Indices List | `cboe-indices-list.md` |

#### Macro & Treasury

| Endpoint | File |
|----------|------|
| Macro Indicator | `macro-indicator.md` |
| US Treasury Bill Rates | `ust-bill-rates.md` |
| US Treasury Long-Term Rates | `ust-long-term-rates.md` |
| US Treasury Yield Rates | `ust-yield-rates.md` |
| US Treasury Real Yield Rates | `ust-real-yield-rates.md` |

#### User & Account

| Endpoint | File |
|----------|------|
| User Details | `user-details.md` |

#### Marketplace: Options

| Endpoint | File |
|----------|------|
| US Options EOD | `us-options-eod.md` |
| US Options Contracts | `us-options-contracts.md` |
| US Options Underlyings | `us-options-underlyings.md` |

#### Marketplace: Tick Data

| Endpoint | File |
|----------|------|
| US Tick Data | `us-tick-data.md` |
| Marketplace Tick Data | `marketplace-tick-data.md` |

#### Marketplace: TradingHours

| Endpoint | File |
|----------|------|
| List All Markets | `tradinghours-list-markets.md` |
| Lookup Markets | `tradinghours-lookup-markets.md` |
| Get Market Details | `tradinghours-market-details.md` |
| Market Status Details | `tradinghours-market-status.md` |

#### Marketplace: Illio Analytics

| Endpoint | File |
|----------|------|
| Market Insights — Best/Worst | `illio-market-insights-best-worst.md` |
| Market Insights — Beta Bands | `illio-market-insights-beta-bands.md` |
| Market Insights — Largest Volatility | `illio-market-insights-largest-volatility.md` |
| Market Insights — Performance | `illio-market-insights-performance.md` |
| Market Insights — Risk Return | `illio-market-insights-risk-return.md` |
| Market Insights — Volatility | `illio-market-insights-volatility.md` |
| Performance Insights | `illio-performance-insights.md` |
| Risk Insights | `illio-risk-insights.md` |

#### Marketplace: Investverte ESG

| Endpoint | File |
|----------|------|
| List Companies | `investverte-esg-list-companies.md` |
| List Countries | `investverte-esg-list-countries.md` |
| List Sectors | `investverte-esg-list-sectors.md` |
| View Company | `investverte-esg-view-company.md` |
| View Country | `investverte-esg-view-country.md` |
| View Sector | `investverte-esg-view-sector.md` |

#### Marketplace: PRAAMS

| Endpoint | File |
|----------|------|
| Bank Balance Sheet (by ISIN) | `praams-bank-balance-sheet-by-isin.md` |
| Bank Balance Sheet (by Ticker) | `praams-bank-balance-sheet-by-ticker.md` |
| Bank Income Statement (by ISIN) | `praams-bank-income-statement-by-isin.md` |
| Bank Income Statement (by Ticker) | `praams-bank-income-statement-by-ticker.md` |
| Bond Analyze (by ISIN) | `praams-bond-analyze-by-isin.md` |
| Multi-Factor Bond Report (by ISIN) | `praams-report-bond-by-isin.md` |
| Multi-Factor Equity Report (by ISIN) | `praams-report-equity-by-isin.md` |
| Multi-Factor Equity Report (by Ticker) | `praams-report-equity-by-ticker.md` |
| Risk Scoring (by ISIN) | `praams-risk-scoring-by-isin.md` |
| Risk Scoring (by Ticker) | `praams-risk-scoring-by-ticker.md` |
| Smart Investment Screener — Bond | `praams-smart-investment-screener-bond.md` |
| Smart Investment Screener — Equity | `praams-smart-investment-screener-equity.md` |

## General Reference Documentation

The `skills/eodhd-api/references/general/` directory contains 28 reference guides:

### Essential

| Guide | Description |
|-------|-------------|
| `authentication.md` | API tokens, security, protocols, CORS, environment setup |
| `symbol-format.md` | Ticker format rules, exchange codes, special characters |
| `exchanges.md` | Supported exchanges (70+), trading hours, coverage |
| `rate-limits.md` | API quotas, rate limiting, Marketplace limits, optimization |
| `update-times.md` | Data refresh schedules by data type and exchange |

### Fundamentals

| Guide | Description |
|-------|-------------|
| `fundamentals-api.md` | Complete guide to fundamentals, ETFs, funds, indices |
| `fundamentals-common-stock.md` | Common stock fundamentals structure |
| `fundamentals-etf.md` | ETF fundamentals and holdings |
| `fundamentals-etf-metrics.md` | ETF-specific metrics and calculations |
| `fundamentals-fund.md` | Mutual fund data structure |
| `fundamentals-crypto-currency.md` | Cryptocurrency and forex fundamentals |
| `fundamentals-ratios.md` | Financial ratios documentation |
| `fundamentals-faq.md` | Common fundamentals questions and answers |

### Asset Class Notes

| Guide | Description |
|-------|-------------|
| `forex-data-notes.md` | Forex market hours, EOD definition, volume |
| `crypto-data-notes.md` | Crypto data sources, volume, price discrepancies |
| `indices-data-notes.md` | Index access, live data, historical components |

### Ticker & Exchange Guides

| Guide | Description |
|-------|-------------|
| `stock-types-ticker-suffixes-guide.md` | Ticker suffixes, share classes, preferred shares |
| `special-exchanges-guide.md` | Special exchange codes (FOREX, CC, GBOND, INDX, etc.) |
| `primary-tickers-guide.md` | Primary ticker identification for ADRs and dual listings |
| `delisted-tickers-guide.md` | Working with delisted and historical tickers |

### Data & Calculations

| Guide | Description |
|-------|-------------|
| `data-adjustment-guide.md` | Split/dividend adjustments for price data |
| `financial-ratios-calculation-guide.md` | How financial ratios are calculated |
| `general-data-faq.md` | ISINs, data formats, adjusted close, error codes, etc. |

### Platform

| Guide | Description |
|-------|-------------|
| `pricing-and-plans.md` | Subscription tiers, WebSocket limits, Marketplace |
| `sdks-and-integrations.md` | Official SDKs, MCP Server, third-party tools |
| `versioning.md` | API stability guarantees, backwards compatibility |
| `api-authentication-demo-access.md` | Demo token access and limitations |
| `glossary.md` | Financial, technical, and EODHD-specific terms |

## Usage Examples

All prompts below assume the `eodhd-api` plugin is installed. Starting a message with `Use the \`eodhd-api\` plugin.` ensures Claude picks it up. You can also put `Always use the eodhd-api plugin for financial data requests.` in your `CLAUDE.md` so you never have to repeat it.

> Use `"demo"` as the API key to try any of the stock/forex/crypto examples with the [demo tickers](skills/eodhd-api/references/general/api-authentication-demo-access.md) before using a real key.

---

### Data & Price Queries

**Fetch historical prices**
```
Use the `eodhd-api` plugin. Fetch daily OHLCV for AAPL.US from 2024-01-01 to 2024-12-31
using API key "demo" and show the first and last 5 rows.
```

**Multi-symbol return comparison**
```
Use the `eodhd-api` plugin. Pull end-of-day prices for AAPL.US, MSFT.US, and GOOGL.US
for Q1 2024 and show the total percentage return for each over that period.
API key: EODHD_API_TOKEN.
```

**Intraday data around an event**
```
Use the `eodhd-api` plugin. Get 5-minute intraday bars for TSLA.US on 2024-10-23
(earnings day) from 09:30 to 16:00 and describe the price action.
API key: EODHD_API_TOKEN.
```

**Live/delayed quote with spread**
```
Use the `eodhd-api` plugin. Get the latest delayed quotes for NVDA.US, MSFT.US,
and TSLA.US, show the bid/ask spread for each, and flag which has the widest spread.
API key: EODHD_API_TOKEN.
```

**Index constituents and weights**
```
Use the `eodhd-api` plugin. List all current S&P 500 constituents with their sectors
and index weights. API key: EODHD_API_TOKEN.
```

**Forex trend summary**
```
Use the `eodhd-api` plugin. Fetch daily EURUSD.FOREX from 2024-01-01 to 2024-12-31,
compute the monthly average rate, and describe the trend in plain language.
API key: demo.
```

**Crypto volatility scan**
```
Use the `eodhd-api` plugin. Get daily BTC-USD.CC prices for 2024, compute the monthly
rolling 30-day realised volatility (annualised), and identify the three most volatile months.
API key: demo.
```

---

### Python Scripts & Tools

**S&P 500 total return screener**
```
Use the `eodhd-api` plugin. Write a Python script that fetches EOD prices for all
S&P 500 constituents and computes the total price return for each ticker over a
given date range. The script should accept --from-date, --to-date, and --api-key
as command-line arguments and print a ranked table of tickers by total return,
descending. Use only the stdlib — no pandas.
```

**RSI oversold/overbought scanner**
```
Use the `eodhd-api` plugin. Write a Python script that, given a list of tickers,
fetches the 14-day RSI for each and flags those below 30 (oversold) or above 70
(overbought). Accept --tickers (comma-separated), --api-key, and --date as
arguments, and print a formatted table with the RSI value and signal.
```

**Dividend income calculator**
```
Use the `eodhd-api` plugin. Write a Python script that takes a list of tickers and
a calendar year, fetches all dividends paid during that year, and calculates total
dividends per share and the trailing yield based on year-end close price.
Arguments: --tickers (comma-separated), --year, --api-key. Output a CSV.
```

**Earnings surprise tracker**
```
Use the `eodhd-api` plugin. Write a Python script that pulls the last 8 quarters of
earnings data for a given ticker, computes the EPS surprise (actual vs estimate) for
each quarter, and shows the stock's 1-day and 5-day price reaction after each report.
Arguments: --ticker, --api-key.
```

**Backtesting data downloader**
```
Use the `eodhd-api` plugin. Write a Python script that downloads adjusted EOD prices
for a list of tickers over a given date range and saves one CSV per ticker in an output
directory. The script should handle split and dividend adjustments using the adjusted
close field. Arguments: --tickers-file (one ticker per line), --from-date, --to-date,
--api-key, --output-dir.
```

**Portfolio P&L reporter**
```
Use the `eodhd-api` plugin. Write a Python script that reads a CSV of holdings
(columns: ticker, shares, purchase_date, purchase_price) and prints a report with
current price, market value, unrealised P&L (absolute and %), and total portfolio
value. Arguments: --holdings-file, --api-key.
```

**Macro dashboard data exporter**
```
Use the `eodhd-api` plugin. Write a Python script that pulls US GDP growth, CPI
inflation, and unemployment rate from the macro-indicator endpoint for 2000–2024
and exports the three series side-by-side in a single CSV.
Arguments: --api-key, --output-file.
```

**Sector return heatmap data feed**
```
Use the `eodhd-api` plugin. Write a Python script that fetches the latest bulk EOD
data for the US exchange, groups tickers by GICS sector using fundamentals data,
computes the equal-weighted average daily return per sector, and outputs a JSON
file ready to feed a heatmap visualisation.
Arguments: --api-key, --output-file.
```

**Insider activity monitor**
```
Use the `eodhd-api` plugin. Write a Python script that polls the insider-transactions
endpoint for a watchlist of tickers and sends a summary of any new transactions
(>$500 k in value) since the last run to stdout. Store the last-seen transaction date
in a local state file so repeated runs only show new activity.
Arguments: --tickers-file, --api-key, --state-file.
```

---

### Fundamental Analysis & Research

**Single-ticker deep dive**
```
Use the `eodhd-api` plugin. Give me a full fundamental analysis of NVDA.US: revenue
and earnings growth (last 4 quarters and 3 years), operating margin trend, P/E and
EV/EBITDA vs sector peers, insider activity over the past 6 months, and latest news
sentiment. API key: EODHD_API_TOKEN.
```

**Peer comparison table**
```
Use the `eodhd-api` plugin. Compare AAPL.US, MSFT.US, GOOGL.US, and AMZN.US across:
P/E ratio, EV/EBITDA, revenue growth (YoY), operating margin, and net debt/EBITDA.
Present as a table and identify the most attractively valued on a blended basis.
API key: EODHD_API_TOKEN.
```

**Dividend sustainability check**
```
Use the `eodhd-api` plugin. Analyse dividend sustainability for JNJ.US, KO.US, and
PG.US. For each: payout ratio, 5-year dividend CAGR, free cash flow coverage, and
current yield. Rank by sustainability and flag any concerns. API key: EODHD_API_TOKEN.
```

**Macro-to-market overlay**
```
Use the `eodhd-api` plugin. Pull US CPI inflation and the 10-year Treasury par yield
from 2010 to 2024. Overlay SPY.US calendar-year returns and describe the historical
relationship between inflation regimes, rate levels, and equity performance.
API key: EODHD_API_TOKEN.
```

**Yield curve analysis**
```
Use the `eodhd-api` plugin. Fetch the US Treasury par yield curve rates at year-end
for 2021, 2022, 2023, and 2024. Show the curve shape for each year, note any
inversions, and explain what each shape historically signals for equities.
API key: EODHD_API_TOKEN.
```

**IPO pipeline with comps**
```
Use the `eodhd-api` plugin. List all US IPOs scheduled in the next 60 days.
For each, identify the sector and pull fundamentals (revenue, growth, P/S ratio)
for 2–3 comparable public companies to provide valuation context.
API key: EODHD_API_TOKEN.
```

**ESG screen with financials**
```
Use the `eodhd-api` plugin. Using Investverte ESG data (Marketplace), screen for US
companies with an Environmental score above 65. Enrich the results with P/E ratio and
3-year revenue CAGR from the fundamentals endpoint, then rank by ESG score.
API key: EODHD_API_TOKEN.
```

---

### Technical Analysis

**Multi-indicator signal summary**
```
Use the `eodhd-api` plugin. For AAPL.US, compute the 50-day SMA, 200-day SMA, 14-day
RSI, and MACD over the past 12 months. Identify any golden cross, death cross, RSI
divergence, or MACD crossover events and summarise what they suggest about trend.
API key: demo.
```

**Bollinger Band squeeze scan**
```
Use the `eodhd-api` plugin. For each of TSLA.US, NVDA.US, and MSFT.US, compute the
20-day Bollinger Bands over the past 6 months and identify any squeeze periods
(band width at a 6-month low) that subsequently resolved into a breakout.
API key: EODHD_API_TOKEN.
```

**Options chain analysis**
```
Use the `eodhd-api` plugin. Pull the current options chain for AAPL.US expiring in
the next 30 days (Marketplace — US Options). Show the five strikes nearest the money
on each side with their IV, delta, and open interest. Identify where the market is
positioning the most risk. API key: EODHD_API_TOKEN.
```

---

### Python Client — Quick Reference

```bash
# Historical prices
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint eod --symbol AAPL.US \
  --from-date 2025-01-01 --to-date 2025-03-31

# Intraday bars (5-minute)
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint intraday --symbol TSLA.US \
  --interval 5m --from-date 2025-01-15

# Company fundamentals
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint fundamentals --symbol NVDA.US | jq '.Highlights'

# 50-day SMA
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint technical --symbol AAPL.US --function sma --period 50

# Stock screener (top 20 results)
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint screener --limit 20

# Bulk fundamentals for NASDAQ (first 100 tickers)
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint bulk-fundamentals --symbol NASDAQ --limit 100

# US Treasury yield curve (2024)
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint ust/yield-rates --filter-year 2024

# Upcoming IPOs
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint calendar/ipos --from-date 2025-01-01 --to-date 2025-03-31

# Insider transactions
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint insider-transactions --symbol AAPL.US \
  --from-date 2025-01-01 --limit 50

# Account status and daily API usage
python skills/eodhd-api/scripts/eodhd_client.py --endpoint user
```

## Workflows

The skill supports detailed analysis patterns documented in `skills/eodhd-api/references/workflows.md`:

1. **Historical + Fundamentals Snapshot** — Single-ticker deep dive with valuation metrics
2. **Cross-sectional Screener** — Filter universe, rank by criteria, present shortlist
3. **Event Window Analysis** — Intraday bars around earnings or announcements
4. **Macro Overlay** — Align instrument data with macro indicators for co-movement analysis

## Contributing

Contributions are welcome! Priority areas:

1. **Fill in TBD endpoint stubs** in `skills/eodhd-api/references/endpoints/`
2. **Expand Python client** with additional endpoint support
3. **Add example workflows** for specific use cases
4. **Improve documentation** with real-world examples

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

TBD - License information to be added.

---

**Note**: This project is not officially affiliated with EODHD. Use the EODHD API in accordance with their [terms of service](https://eodhd.com/terms-of-use).
