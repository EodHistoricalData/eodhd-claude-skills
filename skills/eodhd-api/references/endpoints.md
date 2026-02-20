# EODHD API Reference Documentation

This directory contains comprehensive reference documentation for the EODHD API.

## Documentation Structure

### General Documentation

For general information about working with the EODHD API, see the **[general/](general/)** directory:

- **[Authentication](general/authentication.md)** - API tokens, security, environment setup
- **[Symbol Format](general/symbol-format.md)** - How to format instrument identifiers correctly
- **[Exchanges](general/exchanges.md)** - Complete list of 70+ supported exchanges
- **[Update Times](general/update-times.md)** - When data is updated for each market
- **[Rate Limits](general/rate-limits.md)** - API quotas, rate limits, and optimization
- **[Fundamentals API](general/fundamentals-api.md)** - Complete guide to company fundamentals, ETFs, funds, and indices

👉 **Start here if you're new**: [general/README.md](general/README.md)

### Endpoint-Specific Documentation

For detailed information about specific API endpoints, see the **[endpoints/](endpoints/)** directory:

- Individual endpoint files: `endpoints/*.md`
- Endpoint index: `endpoints/README.md`

Each endpoint document includes:
- Purpose and use cases
- Required and optional parameters
- Response format and field descriptions
- Example requests and responses
- Common issues and solutions

## Quick Start

1. **Set up authentication**: Read [general/authentication.md](general/authentication.md)
2. **Learn symbol format**: Read [general/symbol-format.md](general/symbol-format.md)
3. **Understand rate limits**: Read [general/rate-limits.md](general/rate-limits.md)
4. **Explore endpoints**: Browse [endpoints/](endpoints/) directory

## Common Use Cases

### "I need to fetch stock prices"
1. Check [general/symbol-format.md](general/symbol-format.md) for correct ticker format
2. Review [endpoints/historical-stock-prices.md](endpoints/historical-stock-prices.md)
3. Check [general/update-times.md](general/update-times.md) for data availability

### "I'm getting authentication errors"
1. Read [general/authentication.md](general/authentication.md)
2. Verify your token with the `/user` endpoint
3. Check environment variables are set correctly

### "I'm hitting rate limits"
1. Read [general/rate-limits.md](general/rate-limits.md)
2. Implement caching for frequently accessed data
3. Use bulk endpoints where possible
4. Consider upgrading your plan

### "I can't find the right exchange code"
1. Check [general/exchanges.md](general/exchanges.md) for complete list
2. Use the Symbol Search endpoint: `/search/{QUERY}`
3. Review [general/symbol-format.md](general/symbol-format.md) for special formats

### "I need company fundamentals or financial statements"
1. Read [general/fundamentals-api.md](general/fundamentals-api.md) for complete guide
2. Use filter parameters to reduce response size
3. Check data type (Common Stock, ETF, FUND, or Index) in response
4. Use date filtering for specific financial periods (new feature)

## Notes

- Endpoint availability and fields vary by subscription level
- All timestamps are in UTC unless otherwise specified
- Symbol format is case-sensitive (use uppercase)
- Rate limits apply at both monthly and per-second levels
