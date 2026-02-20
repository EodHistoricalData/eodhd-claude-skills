# Illio Market Insights — Best and Worst Days API

Status: complete
Source: marketplace (illio)
Provider: illio via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/illio/chapters`
Path: `/best-and-worst/{id}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns data about instruments with the largest one-day gains and losses over the last year. Identifies which index constituents had the biggest single-day price swings, useful for understanding potential future moves and managing risk.

**Use cases**:
- Identify stocks with the largest single-day price moves
- Assess tail risk for individual constituents
- Screen for event-driven volatility and momentum
- Understand historical price shock magnitude for position sizing

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
  "insightId": "BEST_AND_WORST_DAYS",
  "categoryId": "PERFORMANCE",
  "title": "Largest 1 Day Moves",
  "watchlistName": "US 500 Stocks",
  "insight": {
    "id": "BEST_AND_WORST_DAYS",
    "title": "Which of these instruments had the largest one day moves over the last year?",
    "whyImportant": "When considering allocations or strategies, you should be mindful of these large single day swings.",
    "description": "Over the last year, FISV had the largest one day gain and GL had the largest one day loss.",
    "stats": [
      { "text": "Over the last year, FISV, SMCI and DELL had the largest one-day gains with 75.7%, 35.9% and 31.6%." }
    ]
  },
  "chart": {
    "title": "Largest 1 Day Moves Over Past Year",
    "data": {
      "best": [
        { "label": "Fiserv Inc.", "value": 75.7 }
      ],
      "worst": [
        { "label": "Globe Life Inc", "value": -53.1 }
      ]
    }
  }
}
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `insightId` | string | Always `"BEST_AND_WORST_DAYS"` |
| `categoryId` | string | Always `"PERFORMANCE"` |
| `title` | string | Human-readable insight title |
| `watchlistName` | string | Name of the index |
| `insight.id` | string | Insight identifier |
| `insight.title` | string | Question the insight answers |
| `insight.whyImportant` | string | Explanation of why this metric matters |
| `insight.description` | string | Summary identifying the best and worst performers |
| `insight.stats[]` | array | Key statistics — top 3 gains and top 3 losses with percentages |
| `chart.title` | string | Chart title |
| `chart.data.best[]` | array | Instruments with the largest one-day **gains** |
| `chart.data.best[].label` | string | Instrument name |
| `chart.data.best[].value` | float | Largest single-day gain (%) — positive |
| `chart.data.worst[]` | array | Instruments with the largest one-day **losses** |
| `chart.data.worst[].label` | string | Instrument name |
| `chart.data.worst[].value` | float | Largest single-day loss (%) — negative |

> **Note**: Unlike other illio endpoints, this response uses `chart.data.best[]` and `chart.data.worst[]` instead of `chart.data.items[]`.

## Example Requests

### Get S&P 500 best and worst days

```bash
curl "https://eodhd.com/api/mp/illio/chapters/best-and-worst/SnP500?api_token=YOUR_API_TOKEN"
```

### Get Nasdaq-100 best and worst days

```bash
curl "https://eodhd.com/api/mp/illio/chapters/best-and-worst/NDX?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/illio/chapters/best-and-worst/SnP500?api_token=demo"
```

## Notes

- **Marketplace product**: Requires a separate illio marketplace subscription, not included in main EODHD plans.
- **Top movers**: The `best` and `worst` arrays are sorted by magnitude — largest moves first.
- **One-year lookback**: Data covers the last year of trading.
- **Stats include top 3**: The `stats` array provides the top 3 gainers and top 3 losers with their percentages.
- **Supported indices**: S&P 500 (`SnP500`), Dow Jones (`DJI`), Nasdaq-100 (`NDX`).
- **Disclaimer**: Data does not constitute financial advice or investment recommendations.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **429** | Too Many Requests | Rate limit exceeded (1,000 req/min or 100,000 calls/24h). |
