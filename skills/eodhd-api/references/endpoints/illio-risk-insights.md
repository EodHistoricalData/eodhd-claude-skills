# Illio Risk Insights API

Status: complete
Source: marketplace (illio)
Provider: illio via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/illio/categories`
Path: `/risk/{id}`
Method: GET
Auth: `api_token` query parameter

> **Note**: This endpoint uses `/categories/risk/` (not `/chapters/` like the illio Market Insights endpoints).

## Purpose

Returns comprehensive risk filter data for all constituents of a given index. Provides multiple insight categories covering beta analysis (market, upside, downside), risk-return ratios, volatility metrics, correlation to the market, and average daily moves — all across multiple time periods.

**Use cases**:
- Screen for high-beta or low-beta instruments across multiple timeframes (6m to 5y)
- Identify instruments with the best or worst risk-return trade-offs
- Analyze upside vs downside beta asymmetry for individual equities
- Track volatility changes to spot instruments becoming more or less risky
- Measure correlation to the market to find natural portfolio hedges
- Estimate expected daily price moves based on annualized volatility
- Research and article enrichment with ranked constituent risk data

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

## Parameters

### Path (required)

| Parameter | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `id` | string | enum: `SnP500`, `DJI`, `NDX` | Index watchlist identifier |

- `SnP500` — S&P 500 Index
- `DJI` — Dow Jones Industrial Average
- `NDX` — Nasdaq-100 Index

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key |

## Response (shape)

The response contains a `watchlist` object and an `insight[]` array. Each insight has an `id`, `title`, and `chart[]` array with time-period breakdowns. Each chart entry contains `rows[]` with `"Highest"` and `"Lowest"` ranked instruments (top 10 each).

```json
{
  "watchlist": {
    "displayName": "Nasdaq 100",
    "id": "NDX"
  },
  "insight": [
    {
      "id": "MARKET_IMPACT",
      "title": "Market Impact (Beta)",
      "chart": [
        {
          "subTitle": "6 months",
          "whyImportant": "Beta tells you how much the instrument's price moves compared to a move in the overall market based on the last six months...",
          "rows": [
            {
              "label": "Highest",
              "instruments": [
                {
                  "instrumentId": 5176,
                  "name": "Micron Technology Inc",
                  "label": "MU.US",
                  "value": "2.5x",
                  "icon": "images/logos/eod/MU.US.png"
                }
              ]
            },
            {
              "label": "Lowest",
              "instruments": [ ... ]
            }
          ],
          "children": []
        }
      ]
    }
  ]
}
```

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `watchlist.displayName` | string | Human-readable index name (e.g., "Nasdaq 100") |
| `watchlist.id` | string | Watchlist identifier matching the path parameter |
| `insight[]` | array | Array of insight categories (see below) |

### Insight Object

| Field | Type | Description |
|-------|------|-------------|
| `insight[].id` | string | Insight identifier (see Insight Categories table) |
| `insight[].title` | string | Human-readable insight title |
| `insight[].chart[]` | array | Time-period breakdowns for this insight |

### Chart Object

| Field | Type | Description |
|-------|------|-------------|
| `chart[].subTitle` | string or null | Time period label (e.g., "6 months", "1 year", "3 years", "30 days"). `null` for insights without time periods |
| `chart[].whyImportant` | string | Explanation of what this metric measures and why it matters |
| `chart[].rows[]` | array | Contains `"Highest"` and `"Lowest"` ranked lists |
| `chart[].children[]` | array | Always empty in current implementation |

### Row / Instrument Object

| Field | Type | Description |
|-------|------|-------------|
| `rows[].label` | string | `"Highest"` or `"Lowest"` |
| `rows[].instruments[]` | array | Top 10 instruments for this ranking |
| `instruments[].instrumentId` | integer | Internal instrument identifier |
| `instruments[].name` | string | Full instrument name |
| `instruments[].label` | string | Ticker symbol with exchange suffix (e.g., `"MU.US"`, `"PLTR.US"`) |
| `instruments[].value` | string | Formatted value with unit suffix (e.g., `"2.5x"`, `"85.9%"`, `"+62.0%"`, `"0.83x"`, `"5.3%"`, `"1.3"`) |
| `instruments[].icon` | string or null | Path to instrument logo image (may be `null`) |

## Insight Categories

The response includes the following 12 insight sections, each with their own time-period breakdowns:

| Insight ID | Title | Time Periods | Value Format | Description |
|------------|-------|--------------|--------------|-------------|
| `MARKET_IMPACT` | Market Impact (Beta) | 6m, 1y, 3y, 5y | `"2.5x"` | How much the instrument moves relative to the market. Expected range 0.75x–1.25x. Higher beta = more market sensitivity. |
| `UPSIDE_IMPACT` | Upside Impact (Beta) | 6m, 1y, 3y, 5y | `"2.8x"` | Beta when the market moves **up**. Shows how much the instrument gains when the market rises. |
| `DOWNSIDE_IMPACT` | Downside Impact (Beta) | 6m, 1y, 3y, 5y | `"3.2x"` | Beta when the market moves **down**. Shows how much the instrument drops when the market falls. |
| `RISK_RETURN` | Risk-Return | 3m, 6m, 1y, 3y, 5y | `"1.3"` | Total return divided by volatility. Values > 1 are desirable. |
| `RISK_RETURN_VS_MARKET` | Risk-Return vs Market | 3m, 6m, 1y, 3y, 5y | `"1.5"` | Excess risk-return (instrument risk-return minus market risk-return). Values > 0 are desirable. |
| `RISK_RETURN_CHANGE` | Risk-Return Change (Absolute) | single (no subTitle) | `"5.4"` | Change in 1-year risk-return compared to the prior year. Positive = improving risk-return. |
| `VOLATILITY_ANNUALISED` | Volatility (Annualized) | 30d, 3m, 100d, 6m, 1y, 3y, 5y | `"85.9%"` | Degree of price variation annualized. Lower volatility = less risky for a given return. |
| `VOLATILITY_CHANGE` | Volatility Change (Absolute) | 30d, 3m, 100d, 6m, 1y | `"+62.0%"` | Absolute change in volatility vs prior period. Negative = becoming less volatile. |
| `VOLATILITY_CHANGE_PERCENTAGE` | Volatility Change (Percentage) | 30d, 3m, 100d, 6m, 1y | `"+324.9%"` | Percentage change in volatility vs prior period. Negative = becoming less volatile. |
| `AVERAGE_VOL_MOVE` | Average Daily Move | single (no subTitle) | `"5.3%"` | Expected daily price move based on 1-year annualized volatility. |
| `CORRELATION` | Correlation | 6m, 1y, 3y, 5y | `"0.83x"` | How the instrument moves relative to the market (-1 to +1). Negative correlation = potential hedge. |
| `CORRELATION_CHANGE` | Correlation Change (Absolute) | single (no subTitle) | `"+0.41%"` | Change in 1-year correlation vs prior year. Increase = more market-aligned. |

### Value Interpretation Guide

| Metric | Good for Bull Market | Good for Bear Market | Ideal |
|--------|---------------------|---------------------|-------|
| Beta (Market/Upside/Downside) | Higher beta (> 1x) | Lower beta (< 1x) | High upside beta + low downside beta |
| Risk-Return | > 1 | > 1 | As high as possible |
| Risk-Return vs Market | > 0 | > 0 | As high as possible |
| Volatility | Context-dependent | Lower preferred | Low volatility for a given return |
| Volatility Change | Context-dependent | Decreasing | Negative (becoming less volatile) |
| Correlation | High (move with market) | Low/negative (hedge) | Depends on portfolio strategy |

## Example Requests

### Get S&P 500 risk insights

```bash
curl "https://eodhd.com/api/mp/illio/categories/risk/SnP500?api_token=YOUR_API_TOKEN"
```

### Get Nasdaq-100 risk insights

```bash
curl "https://eodhd.com/api/mp/illio/categories/risk/NDX?api_token=YOUR_API_TOKEN"
```

### Get Dow Jones risk insights

```bash
curl "https://eodhd.com/api/mp/illio/categories/risk/DJI?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/illio/categories/risk/SnP500?api_token=demo"
```

## Notes

- **Marketplace product**: Requires a separate illio marketplace subscription, not included in main EODHD plans.
- **URL path uses `/categories/`**: This endpoint is at `/api/mp/illio/categories/risk/{id}`, not `/chapters/` like the other illio Market Insights endpoints.
- **Large response**: The response contains 12 insight categories with multiple time periods each, totaling a significant amount of data per request. Cache responses where possible.
- **Top 10 per rank**: Each `rows[]` entry contains up to 10 instruments for both "Highest" and "Lowest" rankings.
- **String-formatted values**: All `instruments[].value` fields are pre-formatted strings. Beta values use `"x"` suffix (e.g., `"2.5x"`), volatility/change values use `"%"` suffix (e.g., `"85.9%"`, `"+62.0%"`), risk-return values are plain numbers (e.g., `"1.3"`), correlation values use `"x"` suffix (e.g., `"0.83x"`). Parse accordingly.
- **Signed values**: Volatility change values include explicit `+`/`-` signs (e.g., `"+62.0%"`, `"-21.9%"`). Beta and correlation values may be negative without a sign prefix (e.g., `"-0.4x"`).
- **Asymmetric beta analysis**: Compare `UPSIDE_IMPACT` and `DOWNSIDE_IMPACT` for the same instrument and timeframe to assess beta asymmetry — ideally an instrument has high upside beta and low downside beta.
- **Risk-return interpretation**: For `RISK_RETURN`, values > 1 indicate the instrument's return exceeds its volatility (favorable). For `RISK_RETURN_VS_MARKET`, values > 0 indicate the instrument's risk-return exceeds the market's (outperformance on a risk-adjusted basis).
- **Volatility change periods**: `VOLATILITY_CHANGE` and `VOLATILITY_CHANGE_PERCENTAGE` compare a period with the immediately preceding period of equal length (e.g., last 30 days vs prior 30 days).
- **Supported indices**: S&P 500 (`SnP500`), Dow Jones (`DJI`), Nasdaq-100 (`NDX`).
- **Disclaimer**: Data does not constitute financial advice or investment recommendations.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **429** | Too Many Requests | Rate limit exceeded (1,000 req/min or 100,000 calls/24h). |
