# EODHD API General Documentation

This directory contains general information about working with the EODHD API, including setup, authentication, rate limits, and best practices.

## Quick Links

### Essential Reading

1. **[Authentication](authentication.md)** - How to get and use your API token
2. **[Symbol Format](symbol-format.md)** - How to format instrument identifiers correctly
3. **[Rate Limits](rate-limits.md)** - API quotas, rate limits, and optimization strategies

### Reference Guides

4. **[Exchanges](exchanges.md)** - Comprehensive list of supported exchanges, coverage gaps
5. **[Update Times](update-times.md)** - When data is updated for each market
6. **[Fundamentals API](fundamentals-api.md)** - Complete guide to company fundamentals, ETFs, funds, and indices
7. **[Pricing & Plans](pricing-and-plans.md)** - Subscription tiers, WebSocket limits, marketplace
8. **[SDKs & Integrations](sdks-and-integrations.md)** - Official SDKs, MCP Server, third-party tools
9. **[Versioning](versioning.md)** - API stability guarantees, backwards-compatibility policy
10. **[Glossary](glossary.md)** - Financial, technical, and EODHD-specific terms

## Documentation Overview

### [Authentication](authentication.md)

**What you'll learn**:
- How to obtain your API token
- How to authenticate API requests
- Security best practices for storing tokens
- Using environment variables
- Troubleshooting authentication issues

**Key topics**:
- API token basics
- Demo token for testing
- Environment variable setup
- Security guidelines
- Multi-token management

**Start here if**: You're new to EODHD or setting up a new application

---

### [Symbol Format](symbol-format.md)

**What you'll learn**:
- How to format symbols correctly for all asset types
- Exchange-specific symbol conventions
- Special formats for Forex, Crypto, Bonds, Indices
- Common mistakes and how to avoid them
- How to find the right symbol

**Key topics**:
- Standard format: `{TICKER}.{EXCHANGE}`
- Forex: `{BASE}{QUOTE}.FOREX`
- Crypto: `{CRYPTO}-{QUOTE}.CC`
- Government Bonds: `{CODE}.GBOND`
- Indices
- URL encoding for special characters

**Start here if**: You're getting "symbol not found" errors or unsure about ticker format

---

### [Exchanges](exchanges.md)

**What you'll learn**:
- Complete list of 70+ supported exchanges
- Exchange codes for all regions
- Special exchange codes (FOREX, CC, MONEY, GBOND, EUFUND, INDX)
- Trading hours by exchange
- Data coverage and availability

**Key topics**:
- North American exchanges (US, TO, V, MX)
- European exchanges (LSE, XETRA, PA, AS, MI, etc.)
- Asian markets (T, HK, SHG, NSE, BSE, etc.)
- Special markets (Forex, Crypto, Bonds, Indices)
- Finding correct exchange codes

**Start here if**: You need to know which exchange code to use or want to see all supported markets

---

### [Update Times](update-times.md)

**What you'll learn**:
- When EOD data is available for each exchange
- Intraday data update frequencies
- Fundamentals and calendar data refresh schedules
- Real-time vs delayed data timing
- Best times to fetch data

**Key topics**:
- EOD update times by region
- Intraday data availability
- Real-time quote latency
- Fundamentals refresh schedule
- Calendar events update frequency
- Market hours and time zones

**Start here if**: You need to know when data will be available or planning scheduled data fetches

---

### [Rate Limits](rate-limits.md)

**What you'll learn**:
- How API calls are counted
- Monthly quotas and daily limits
- Rate limiting strategies
- Optimization techniques
- Handling rate limit errors

**Key topics**:
- API call consumption (1 call vs 5+5N calls)
- Plan-based quotas
- Per-second rate limits
- Checking usage with `/user` endpoint
- Caching strategies
- Bulk endpoints optimization
- Exponential backoff for retries

**Start here if**: You're planning API usage, hitting rate limits, or optimizing call efficiency

---

### [Fundamentals API](fundamentals-api.md)

**What you'll learn**:
- How to fetch company fundamentals, ETF data, fund data, and index constituents
- Understanding the 4 different data types returned by the API
- Using filter parameters to reduce response size
- Date filtering for financial statements (new feature)
- Working with large response payloads

**Key topics**:
- Data type detection (Common Stock, ETF, FUND, INDX)
- Filter parameter syntax (nested with `::`)
- Date filtering with `from` and `to` parameters
- Financial statements (Balance Sheet, Income Statement, Cash Flow)
- ETF holdings and allocations
- Mutual fund composition
- Index constituents and historical snapshots
- Two-step approach for retrieving specific financial periods
- Best practices for managing large responses (800+ KB)

**Start here if**: You need company financials, ETF holdings, fund data, or index composition

---

## Common Use Cases

### Setting Up a New Project

1. Read [Authentication](authentication.md) to set up your API token
2. Review [Symbol Format](symbol-format.md) to understand ticker conventions
3. Check [Rate Limits](rate-limits.md) to plan your usage
4. Explore endpoint-specific docs in `../endpoints/`

### Troubleshooting Symbol Errors

1. Check [Symbol Format](symbol-format.md) for correct format
2. Use [Exchanges](exchanges.md) to verify exchange code
3. Try the Symbol Search endpoint: `/api/search/{QUERY}`

### Optimizing API Usage

1. Review [Rate Limits](rate-limits.md) optimization section
2. Implement caching for EOD and fundamentals data
3. Use bulk endpoints when fetching multiple symbols
4. Check [Update Times](update-times.md) to schedule fetches efficiently

### Planning Data Fetching Schedule

1. Check [Update Times](update-times.md) for your target exchanges
2. Schedule EOD fetches after market close + processing time
3. Use [Rate Limits](rate-limits.md) to avoid hitting quotas
4. Implement retries for 429 errors

### Working with Multiple Markets

1. Use [Exchanges](exchanges.md) to find all relevant exchange codes
2. Note different [Update Times](update-times.md) for each market
3. Plan [Rate Limits](rate-limits.md) across time zones
4. Use correct [Symbol Format](symbol-format.md) for each market

## Quick Reference

### Essential API Patterns

**Standard Stock**:
```
Symbol: AAPL.US
Endpoint: /api/eod/AAPL.US?api_token=TOKEN&fmt=json
```

**Forex Pair**:
```
Symbol: EURUSD.FOREX
Endpoint: /api/eod/EURUSD.FOREX?api_token=TOKEN&fmt=json
```

**Cryptocurrency**:
```
Symbol: BTC-USD.CC
Endpoint: /api/eod/BTC-USD.CC?api_token=TOKEN&fmt=json
```

**Government Bond**:
```
Symbol: US10Y.GBOND
Endpoint: /api/eod/US10Y.GBOND?api_token=TOKEN&fmt=json
```

### Environment Setup

```bash
# Set API token
export EODHD_API_TOKEN="your_token_here"

# Test connection
curl "https://eodhd.com/api/internal-user?api_token=$EODHD_API_TOKEN"
```

### Rate Limit Check

```bash
# Check remaining quota (main subscription)
curl "https://eodhd.com/api/internal-user?api_token=$EODHD_API_TOKEN" | jq '{apiRequests, dailyRateLimit, extraLimit}'

# Check Marketplace quota
curl "https://eodhd.com/api/internal-user?api_token=$EODHD_API_TOKEN" | jq '.availableMarketplaceDataFeeds'
```

### Symbol Search

```bash
# Find correct symbol
curl "https://eodhd.com/api/search/Apple?api_token=$EODHD_API_TOKEN"
```

## Related Documentation

### Endpoint-Specific Docs

For detailed information about specific API endpoints:
- **Endpoint Reference**: `../endpoints/` directory
- **Endpoint Index**: `../endpoints/README.md`

Each endpoint has its own documentation covering:
- Purpose and use cases
- Required and optional parameters
- Response format and fields
- Example requests and responses
- Common issues and solutions

### Subscription Plans

- **Subscriptions**: `../subscriptions/` directory — detailed per-plan feature breakdown
- **Plans Index**: `../subscriptions/README.md` — plan comparison and choosing guide

### Other Resources

- **Workflows**: `../workflows.md` - Common API usage patterns
- **SKILL.md**: `../../SKILL.md` - Skill configuration and triggers
- **Python Client**: `../../scripts/eodhd_client.py` - Ready-to-use client

## Getting Help

### Documentation

1. Check this directory for general topics
2. Check `../endpoints/` for endpoint-specific docs
3. Review examples in each document

### API Testing

1. Use demo token: `api_token=demo` (free, no registration needed — see [demo access guide](api-authentication-demo-access.md))
2. Demo tickers (work across all relevant main REST endpoints): `AAPL.US`, `MSFT.US`, `TSLA.US` (stocks), `VTI.US` (ETF), `SWPPX.US` (mutual fund), `EURUSD.FOREX`, `BTC-USD.CC`
3. Check responses for error messages
4. **Note**: WebSocket and Marketplace endpoints may use a different demo symbol set — check their individual docs

### Support Channels

- **EODHD Documentation**: https://eodhd.com/financial-apis/
- **Account Dashboard**: https://eodhd.com/cp/
- **Support**: https://eodhd.com/contact
- **API Status**: Check for known issues or maintenance

## Contributing

Found an error or have a suggestion?
- File an issue in the repository
- Submit a pull request with corrections
- Share feedback with the team

## Document Index

| Document | Topics Covered | When to Use |
|----------|---------------|-------------|
| [authentication.md](authentication.md) | API tokens, security, protocols, CORS, environment setup | Setting up authentication |
| [symbol-format.md](symbol-format.md) | Ticker formats, exchange codes, special characters | Formatting symbols correctly |
| [exchanges.md](exchanges.md) | Supported exchanges, trading hours, coverage, known gaps | Finding exchange codes |
| [update-times.md](update-times.md) | Data refresh schedules, market hours | Planning data fetches |
| [rate-limits.md](rate-limits.md) | Quotas, rate limiting (~17 req/sec), optimization | Managing API usage |
| [fundamentals-api.md](fundamentals-api.md) | Company fundamentals, ETF/fund data, filter parameters, date filtering | Fetching financial statements and company data |
| [fundamentals-faq.md](fundamentals-faq.md) | Fundamentals FAQ: null values, CSV export, earnings, financials, ETF/fund specifics | Answering common fundamentals questions |
| [forex-data-notes.md](forex-data-notes.md) | Forex market hours, EOD definition, volume, exchange rate source | Understanding forex data behavior |
| [crypto-data-notes.md](crypto-data-notes.md) | Crypto data sources, volume aggregation, price discrepancies, market cap | Understanding crypto data behavior |
| [indices-data-notes.md](indices-data-notes.md) | Index access, live data, historical components, price vs total return | Understanding indices data behavior |
| [general-data-faq.md](general-data-faq.md) | ISINs, identifiers, data formats, decimals, adjusted close, GBX/GBP, OTC, warrants, data quality, error codes, XETRA vs F, back-adjustments | Answering miscellaneous data questions |
| [pricing-and-plans.md](pricing-and-plans.md) | Subscription tiers, WebSocket limits, B2B vs self-serve | Understanding plan requirements |
| [sdks-and-integrations.md](sdks-and-integrations.md) | Official SDKs, MCP Server, third-party integrations | Choosing client libraries and tools |
| [versioning.md](versioning.md) | API stability, backwards compatibility, breaking changes | Understanding API change policy |
| [glossary.md](glossary.md) | Financial, technical, EODHD-specific terms | Quick term reference |

---

**Last Updated**: February 2026
**EODHD API Version**: Current
**Maintained By**: EODHD Skills Team
