# Illio Market Insights — Performance vs Market API

Status: complete
Source: marketplace (illio)
Provider: illio via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/illio/chapters`
Path: `/performance/{id}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns data about how instruments performed compared to the market over the last year. Shows the percentage of constituents that outperformed, underperformed, or performed in line with their index, along with per-instrument relative performance values.

**Use cases**:
- Identify which index constituents outperformed or underperformed the market
- Assess market breadth — how many stocks are driving index performance
- Screen for momentum/contrarian ideas based on relative performance
- Research articles and market commentary

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

```json
{
  "insightId": "PERFORMANCE_VS_MARKET",
  "categoryId": "PERFORMANCE",
  "title": "Performance vs Market",
  "watchlistName": "US 500 Stocks",
  "insight": {
    "id": "PERFORMANCE_VS_MARKET",
    "title": "How did these instruments perform compared to the market?",
    "whyImportant": "To help you see in one place how all the instruments in the group have performed relative to the market.",
    "description": "Over the last year, excluding any income, most of the instruments underperformed their market.",
    "stats": [
      { "text": "29.44% of instruments outperformed their market." }
    ]
  },
  "chart": {
    "title": "Relative Performance Vs The Market",
    "data": {
      "items": [
        {
          "code": "Out-performed the market",
          "label": "Out-performed the market",
          "value": 29.44,
          "instruments": [
            { "label": "Ameriprise Financial Inc", "value": 21.89 }
          ]
        },
        {
          "code": "Under-performed the market",
          "label": "Under-performed the market",
          "value": 57.43,
          "instruments": [
            { "label": "Adobe Systems Incorporated", "value": -43.28 }
          ]
        },
        {
          "code": "Performed in line with the market",
          "label": "Performed in line with the market",
          "value": 1.98,
          "instruments": [
            { "label": "Exelon Corporation", "value": 14.59 }
          ]
        }
      ]
    }
  }
}
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `insightId` | string | Always `"PERFORMANCE_VS_MARKET"` |
| `categoryId` | string | Always `"PERFORMANCE"` |
| `title` | string | Human-readable insight title |
| `watchlistName` | string | Name of the index (e.g., "Nasdaq 100", "US 500 Stocks") |
| `insight.id` | string | Insight identifier |
| `insight.title` | string | Question the insight answers |
| `insight.whyImportant` | string | Explanation of why this metric matters |
| `insight.description` | string | Summary of findings |
| `insight.stats[]` | array | Key statistics as text strings |
| `chart.title` | string | Chart title |
| `chart.data.items[]` | array | Performance buckets |
| `chart.data.items[].code` | string | Bucket identifier (e.g., "Out-performed the market") |
| `chart.data.items[].label` | string | Display label for the bucket |
| `chart.data.items[].value` | float | Percentage of instruments in this bucket |
| `chart.data.items[].instruments[]` | array | List of instruments in this bucket |
| `chart.data.items[].instruments[].label` | string | Instrument name |
| `chart.data.items[].instruments[].value` | float | Relative performance vs market (%) |

## Example Requests

### Get S&P 500 performance vs market

```bash
curl "https://eodhd.com/api/mp/illio/chapters/performance/SnP500?api_token=YOUR_API_TOKEN"
```

### Get Nasdaq-100 performance vs market

```bash
curl "https://eodhd.com/api/mp/illio/chapters/performance/NDX?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/illio/chapters/performance/SnP500?api_token=demo"
```

## Notes

- **Marketplace product**: Requires a separate illio marketplace subscription, not included in main EODHD plans.
- **Three buckets**: Instruments are categorized as outperforming, underperforming, or in line (within +/-2%) with the market.
- **Relative performance**: `instruments[].value` is the relative total performance vs the market over the last year (positive = outperformed, negative = underperformed).
- **All constituents listed**: Every constituent of the index is included in the response, grouped by performance bucket.
- **Supported indices**: S&P 500 (`SnP500`), Dow Jones (`DJI`), Nasdaq-100 (`NDX`).
- **Disclaimer**: Data does not constitute financial advice or investment recommendations.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **429** | Too Many Requests | Rate limit exceeded (1,000 req/min or 100,000 calls/24h). |
