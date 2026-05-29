# EODHD Financial Data Plugin for Claude

Developer-first financial data for Claude — 150,000+ tickers across 70+ exchanges, powered by [EODHD API](https://eodhd.com/) and an OAuth-secured MCP Server.

> **Disclaimer**: This plugin may differ from actual EODHD API behavior due to documentation discrepancies or API evolution. Claude may interpret information incorrectly. For questions, email supportlevel1@eodhistoricaldata.com

## Highlights

- **MCP Server v2** with OAuth 2.0 — 75 tools, 100+ embedded docs, smart ticker resolution
- **7 curated workflow skills** — company briefs, earnings, market overview, screening, risk, macro, options
- **Financial analyst agent** — autonomous multi-source analysis
- **5 slash commands** — `/eodhd-analyze`, `/eodhd-compare`, `/eodhd-market`, `/eodhd-screen`, `/eodhd-macro`
- **72 endpoint docs** + 28 general reference guides
- **Stdlib-only Python client** — zero dependencies, 30+ endpoints

## Installation

### Claude Code (Plugin System)

```bash
# Register the marketplace
/plugin marketplace add EodHistoricalData/eodhd-claude-skills

# Install the plugin
/plugin install eodhd-api@eodhd-claude-skills
```

### MCP Server (Direct)

The plugin includes `.mcp.json` for automatic MCP Server connection:

```json
{
  "eodhd": {
    "type": "http",
    "url": "https://mcpv2.eodhd.dev/v2/mcp"
  }
}
```

### Manual Setup

```bash
git clone https://github.com/EodHistoricalData/eodhd-claude-skills.git
export EODHD_API_TOKEN="your_token_here"
```

## Prerequisites

1. **EODHD API Token** — get one at [eodhd.com](https://eodhd.com/) (free tier available)
2. **Python 3.8+** for the helper client (stdlib-only, no pip install needed)

## Repository Structure

```
eodhd-claude-skills/
├── .claude-plugin/
│   ├── marketplace.json            # Plugin manifest for Claude Code
│   └── plugin.json                 # Extended plugin metadata
├── .claude/
│   └── commands/                   # Slash commands
│       ├── eodhd-analyze.md        # /eodhd-analyze <ticker>
│       ├── eodhd-compare.md        # /eodhd-compare <ticker1> <ticker2>
│       ├── eodhd-market.md         # /eodhd-market
│       ├── eodhd-screen.md         # /eodhd-screen <criteria>
│       └── eodhd-macro.md          # /eodhd-macro
├── .mcp.json                       # MCP Server connector (OAuth)
├── agents/
│   └── financial-analyst.md        # Financial analyst agent definition
├── skills/
│   ├── eodhd-api/                  # Core skill — full API access
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── general/            # 28 general guides
│   │   │   ├── endpoints/          # 72 endpoint docs
│   │   │   ├── subscriptions/      # 7 subscription plans
│   │   │   └── workflows.md
│   │   ├── scripts/
│   │   │   └── eodhd_client.py     # Python API client (stdlib-only)
│   │   └── templates/
│   │       └── analysis_report.md
│   ├── company-brief/              # Company snapshot workflow
│   ├── earnings-monitor/           # Earnings tracking workflow
│   ├── market-overview/            # Market summary workflow
│   ├── portfolio-risk/             # Risk analysis workflow
│   ├── stock-screener/             # Stock screening workflow
│   ├── macro-dashboard/            # Macro-economic dashboard
│   └── options-analyzer/           # Options analysis workflow
├── adapters/
│   ├── claude/eodhd-api.md
│   └── codex/eodhd-api.md
├── CLAUDE.md
├── LICENSE                         # MIT
└── README.md
```

## Quick Start

### 1. Set your API token

```bash
export EODHD_API_TOKEN="your_token_here"
```

### 2. Use slash commands

```
/eodhd-analyze AAPL           # Full company analysis
/eodhd-compare AAPL MSFT      # Side-by-side comparison
/eodhd-market                  # Market overview
/eodhd-screen high dividend large cap   # Stock screening
/eodhd-macro                   # Macro dashboard
```

### 3. Use the Python client directly

```bash
python skills/eodhd-api/scripts/eodhd_client.py --endpoint eod --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-03-31
python skills/eodhd-api/scripts/eodhd_client.py --endpoint fundamentals --symbol MSFT.US
python skills/eodhd-api/scripts/eodhd_client.py --endpoint screener --limit 20
```

### 4. Use in prompts

```
Use the eodhd-api plugin. Pull daily prices for AAPL.US from 2025-01-01 to 2025-03-31
and give me a trend analysis with key support/resistance levels.
```

## Skills

### Core Skill: `eodhd-api`

Full access to all 72 EODHD endpoints via Python client and curl. Handles any financial data request.

### Workflow Skills

| Skill | Purpose | Key Endpoints |
|-------|---------|---------------|
| `company-brief` | Company snapshot — profile, fundamentals, news, sentiment, insiders | fundamentals, eod, news, sentiment, insider-transactions |
| `earnings-monitor` | Earnings calendar, trends, surprises, price reactions | calendar/earnings, calendar/trends, news, intraday |
| `market-overview` | Market summary — indices, sectors, Treasury, commodities, macro | eod, eod-bulk, ust/yield-rates, macro-indicator |
| `portfolio-risk` | Risk analysis — technicals, sentiment, insider alerts, volatility | eod, technical, sentiment, insider-transactions, fundamentals |
| `stock-screener` | Screen stocks by fundamental/technical criteria | screener, fundamentals, eod |
| `macro-dashboard` | Economic dashboard — GDP, CPI, rates, yield curve, events | macro-indicator, ust/*, economic-events |
| `options-analyzer` | Options chains, IV, Greeks, strategy evaluation | us-options-eod, us-options-underlyings (Marketplace) |

## Agent

### Financial Analyst

The `agents/financial-analyst.md` agent autonomously:
- Selects appropriate skills based on the query
- Combines multiple data sources for comprehensive analysis
- Leads with conclusions, then supporting data
- Includes disclaimers and data freshness notes

## Slash Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/eodhd-analyze <ticker>` | Full company analysis | `/eodhd-analyze NVDA` |
| `/eodhd-compare <tickers>` | Side-by-side comparison | `/eodhd-compare AAPL MSFT GOOGL` |
| `/eodhd-market` | Broad market overview | `/eodhd-market` |
| `/eodhd-screen <criteria>` | Stock screening | `/eodhd-screen tech P/E under 20` |
| `/eodhd-macro` | Macro-economic dashboard | `/eodhd-macro USA vs EU` |

## MCP Server

The EODHD MCP Server v2 provides:
- **75 tools** across 15 categories (prices, fundamentals, options, technicals, news, sentiment, macro, etc.)
- **OAuth 2.0** authentication
- **100+ embedded docs** as MCP resources
- **3 prompt templates** for common workflows
- **Smart ticker resolution** — handles ambiguous symbols
- **Rate limiting & retry** — built-in resilience

Connection via `.mcp.json`:
```json
{
  "eodhd": {
    "type": "http",
    "url": "https://mcpv2.eodhd.dev/v2/mcp"
  }
}
```

## Supported Endpoints (72)

### Market Data
Historical prices, intraday bars, live quotes, US extended quotes, WebSockets, technical indicators, screener, search, logos, historical market cap, symbol changes

### Fundamentals & Company
Company fundamentals, bulk fundamentals, news, sentiment, word weights, insider transactions

### Calendar & Events
Earnings, earnings trends, dividends, splits, IPOs, economic events

### Exchange & Index
Exchange list/details/tickers, index components, indices list, CBOE indices

### Macro & Treasury
Macro indicators (50+ per country), US Treasury bill/long-term/yield/real-yield rates

### Marketplace
Options (EOD chains, contracts, underlyings), tick data, trading hours, Illio analytics, Investverte ESG, PRAAMS risk/bank/bond

See `skills/eodhd-api/references/endpoints/README.md` for the complete index.

## Usage Tips

Claude Code treats installed skills as optional context. To ensure the skill activates:

1. **Mention it explicitly**: `Use the eodhd-api plugin. ...`
2. **Add to CLAUDE.md**: `Always use available skills for financial data requests.`
3. **Use slash commands**: They always activate the skill

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Priority areas:
- Expand Python client with additional endpoints
- Add example workflows
- Improve documentation with real-world examples

## License

MIT — see [LICENSE](LICENSE).

---

Built by [EOD Historical Data](https://eodhd.com/) — developer-first financial data for 150,000+ instruments across 70+ global exchanges.
