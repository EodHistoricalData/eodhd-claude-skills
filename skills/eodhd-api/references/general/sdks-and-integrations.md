# EODHD SDKs & Integrations

This document lists official SDKs, AI integrations, and third-party tools for the EODHD API.

## Official SDKs

### Python SDK (Active)

| Attribute | Value |
|-----------|-------|
| Language | Python |
| Status | Active, maintained |
| Repository | [EODHD-APIs-Python-Financial-Library](https://github.com/EodHistoricalData/EODHD-APIs-Python-Financial-Library) |
| Install | `pip install eodhd` |

**Features**: EOD data, live/real-time prices, fundamentals, technical indicators, screener, news/sentiment, WebSocket streaming, marketplace datasets.

### .NET SDK (Active)

| Attribute | Value |
|-----------|-------|
| Language | C#, .NET Standard 2.0 |
| Status | Active, maintained |
| Repository | [EODHistoricalData.Wrapper](https://github.com/EodHistoricalData/EODHistoricalData.Wrapper) |

**Features**: Historical prices, splits, dividends, technical indicators, fundamentals.

### R Package — eodhdR2 (Active)

| Attribute | Value |
|-----------|-------|
| Language | R |
| Status | Active, maintained |
| Repository | [R-Library-for-financial-data-2024](https://github.com/EodHistoricalData/R-Library-for-financial-data-2024) |
| Install | `install.packages("eodhdR2")` (CRAN) |

**Features**: Full API access, local caching system, quota management, data aggregation in wide/long format.

### Excel Add-In (Active)

| Attribute | Value |
|-----------|-------|
| Platform | .NET, Microsoft Excel |
| Status | Active, maintained |
| Repository | [Excel-Add-In-for-Financial-Data-APIs](https://github.com/EodHistoricalData/Excel-Add-In-for-Financial-Data-APIs) |

**Features**: Excel function integration for financial data, direct spreadsheet population.

## AI Integrations

### MCP Server (Active)

Model Context Protocol server for AI assistants (Claude, ChatGPT).

| Attribute | Value |
|-----------|-------|
| Language | Python 3.10+ |
| Status | Active (beta) |
| Repository | [EODHD-MCP-Server](https://github.com/EodHistoricalData/EODHD-MCP-Server) |

**Features**: Provides AI assistants with access to EODHD API data, 150,000+ tickers across 70+ exchanges, rate limiting and retry logic built in.

### This Skills Package

The `eodhd-claude-skills` package (this project) provides a stdlib-only Python client and structured skill definitions for Claude Code and other AI agents.

## Other Integrations

| Integration | Type | Description |
|-------------|------|-------------|
| **Power BI Connector** | BI Tool | Power BI data connector |
| **Postman Collection** | API Testing | Pre-built API request collection |
| **NinjaTrader Adapter** | Trading Platform | NinjaTrader integration |
| **XLQ2** | Spreadsheet | Spreadsheet data connector |
| **ChatGPT Assistant** | AI | Data pulls via natural language prompts |
| **Telegram Bot** | Messaging | Price alerts and trading signals |
| **F# / Matlab** | Language | Available via SDKs |

## Related Resources

- **Authentication**: See `authentication.md` for API key setup
- **Rate Limits**: See `rate-limits.md` — the R package and MCP Server include built-in quota management
