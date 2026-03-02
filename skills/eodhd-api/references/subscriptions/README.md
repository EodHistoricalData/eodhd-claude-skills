# EODHD Subscription Plans

This directory contains detailed documentation for each EODHD subscription plan, including features, data access, and API limits.

> **Note**: Prices listed are indicative. See the [actual pricing page](https://eodhd.com/pricing) for current rates.

## Plans

| Plan | Price | API Calls/Day | Key Focus |
|------|------|---------------|-----------|
| [Free](free.md) | 0/mo | 20 | Testing and evaluation |
| [EOD Historical Data — All World](eod-historical-data-all-world.md) | 19.99/mo | 100,000 | EOD prices, splits, dividends |
| [Calendar Feed](calendar-feed.md) | 19.99/mo | 100,000 | Earnings, IPOs, splits & dividends calendars |
| [EOD+Intraday — All World Extended](eod-intraday-all-world-extended.md) | 29.99/mo | 100,000 | EOD + intraday + technicals + WebSocket |
| [Fundamentals Data Feed](fundamentals-data-feed.md) | 59.99/mo | 100,000 | Company fundamentals, financials, macro |
| [All-In-One](all-in-one.md) | 99.99/mo | 100,000 | All data feeds combined |
| [All-In-One with Extended Fundamentals](all-in-one-extended-fundamentals.md) | 119.99/mo | 100,000 | All-In-One + extended fundamentals |

## Choosing a Plan

- **Just need historical prices?** — [EOD Historical Data — All World](eod-historical-data-all-world.md)
- **Need intraday bars, technicals, or WebSocket streaming?** — [EOD+Intraday — All World Extended](eod-intraday-all-world-extended.md)
- **Need company financials, ETF data, or macro indicators?** — [Fundamentals Data Feed](fundamentals-data-feed.md)
- **Need earnings calendars, IPO dates, splits & dividends schedules?** — [Calendar Feed](calendar-feed.md)
- **Need everything?** — [All-In-One](all-in-one.md) or [All-In-One with Extended Fundamentals](all-in-one-extended-fundamentals.md)
- **Just exploring?** — [Free](free.md)

## Common Across All Paid Plans

- **100,000 API calls/day** (default daily limit)
- **1,000 API requests/minute**
- **500 welcome bonus API calls**
- **30+ years** of data history
- **Personal use** license
- Additional API calls available by request

## Related Resources

- **Pricing Page**: https://eodhd.com/pricing
- **Rate Limits**: `../general/rate-limits.md` — API call consumption and quotas
- **Pricing Overview**: `../general/pricing-and-plans.md` — billing, enterprise, marketplace summary
- **Authentication**: `../general/authentication.md` — API key setup
- **User Endpoint**: `../endpoints/user-details.md` — check account status and usage via API
