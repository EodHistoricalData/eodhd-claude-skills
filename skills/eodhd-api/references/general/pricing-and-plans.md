# EODHD Pricing & Plans

This document summarizes EODHD subscription plans and feature access, so agents can advise users on plan requirements.

## Self-Serve Plans

Self-serve subscriptions are available via [eodhd.com](https://eodhd.com). See the website for current pricing.

A **free plan** is available for testing and evaluation, with limited API call allowances.

## B2B / Enterprise Pricing

Enterprise pricing is divided into licensing models based on how data is used:

| Model | Description |
|-------|-------------|
| **Internal Use (All-in-One)** | For internal analytics, research, backtesting. Data NOT shown to end-users |
| **Display Use (All-in-One)** | For showing data to end-users in apps, dashboards, websites |
| **Display Per-Data-Feed** | For customers needing only specific data feeds in display mode |

## WebSocket Tiers

| Tier | Ticker Count |
|------|-------------|
| Basic | 2,500 |
| Pro | 5,000 |
| Advanced | 10,000 |
| Enterprise | 20,000 |

**Default per-connection limit**: 50 symbols (upgradeable via dashboard).

## Subscriptions

Subscriptions are **monthly-based** and **automatically renewed**. The minimum paid period is one month. After canceling, access continues until the end of the paid period. EODHD supports both **PayPal** and **Stripe** (credit card); Stripe is recommended as a more flexible and convenient method.

### Canceling a Subscription

- **Credit card (Stripe)**: Cancel at https://eodhd.com/pricing
- **PayPal**: Cancel via your PayPal profile

If you are unable to cancel on your own, EODHD support can do it from their side.

## API Call Limits

Additional API calls can be purchased as add-ons beyond plan limits.

### Additional API Calls Pricing

The default limit is **100,000 daily API calls**. Every additional 100k calls costs the price of your current subscription, with volume discounts starting at 400k total daily calls:

| Daily API Calls | Pricing Formula |
|----------------|-----------------|
| 100k (base) | 1x subscription price |
| 200k | 2x subscription price |
| 300k | 3x subscription price |
| 400k+ | Base + 0.8x for each additional 100k above base |

**Formula example (400k)**: If subscription price is X, then total = X + (0.8 × 3X)

**Upgrade process**:
- **PayPal**: Purchase additional subscriptions that sum to your desired limit, then contact EODHD to increase the limit.
- **Credit card (Stripe)**: Purchase one subscription, then contact EODHD with your desired new daily limit. They will adjust it seamlessly. The API key remains the same in all cases.

## Self-Serve vs B2B Comparison

| Aspect | Self-Serve | B2B / Enterprise |
|--------|-----------|------------------|
| Signup | Website | Sales contact |
| Pricing | Published tiers | Custom negotiation |
| Contract | Click-through | MSA + Order Form (DocuSign) |
| Support | Standard | Dedicated |
| Integration | Self-guided | Assisted |
| Payment | Stripe only | Stripe + Wise (USD) + Qonto (EUR) |

## Testing Options

- **Demo API key** (`api_token=demo`) for select endpoints and symbols
- **Free plan** for testing with limited calls
- Browser-ready examples in documentation
- Postman collection available

## Data Marketplace

EODHD hosts a marketplace where third-party data providers sell data through the EODHD platform. Marketplace data is accessed through the same API and billing system — no separate contracts needed.

Key partnerships include:
- **ASX** (Australian Securities Exchange) — referral partner
- **Deutsche Borse** — real-time market data partnership (Xetra, regional exchanges)

## Related Resources

- **Subscription Plans (detailed)**: See `../subscriptions/README.md` for per-plan feature breakdowns
- **Rate Limits**: See `rate-limits.md` for quota details
- **Authentication**: See `authentication.md` for API key setup
- **Pricing Page**: https://eodhd.com/pricing
