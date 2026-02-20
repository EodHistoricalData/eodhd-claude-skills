# Illio Market Insights — Beta Bands API

Status: complete
Source: marketplace (illio)
Provider: illio via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/illio/chapters`
Path: `/beta-bands/{id}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns data about how instruments react to overall market movements based on their Beta values. Beta measures an instrument's sensitivity to market moves — a beta of 1.0 means the instrument moves in line with the market, >1.0 means it amplifies market moves, <1.0 means it dampens them.

**Use cases**:
- Identify high-beta stocks that amplify market moves (useful in bull markets)
- Find low-beta or negative-beta stocks for defensive positioning (useful in bear markets)
- Construct beta-neutral or beta-tilted portfolios
- Understand portfolio sensitivity to broad market direction

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
  "insightId": "BETA_BANDS",
  "categoryId": "RISK",
  "title": "Market Impact Bands",
  "watchlistName": "US 500 Stocks",
  "insight": {
    "id": "BETA_BANDS",
    "title": "How do these instruments react when the overall markets moves?",
    "whyImportant": "Beta tells you how much the instrument reacts to a move in the overall market.",
    "description": "When the market moves by 10.0%, 72.0% of these instruments are likely to move by less.",
    "stats": [
      { "text": "The most concentrated Beta bracket is 0.00 to 0.75." }
    ]
  },
  "chart": {
    "title": "Beta Bands",
    "data": {
      "items": [
        { "label": "Ameriprise Financial Inc", "value": 0.89 }
      ]
    }
  }
}
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `insightId` | string | Always `"BETA_BANDS"` |
| `categoryId` | string | Always `"RISK"` |
| `title` | string | Human-readable insight title |
| `watchlistName` | string | Name of the index |
| `insight.id` | string | Insight identifier |
| `insight.title` | string | Question the insight answers |
| `insight.whyImportant` | string | Explanation of what beta measures |
| `insight.description` | string | Summary — what percentage of instruments move less than the market |
| `insight.stats[]` | array | Key statistics — most concentrated beta bracket, highest/lowest beta instruments |
| `chart.title` | string | Chart title |
| `chart.data.items[]` | array | All instruments with their beta values |
| `chart.data.items[].label` | string | Instrument name |
| `chart.data.items[].value` | float | Beta value relative to the index |

### Beta Value Interpretation

| Beta Range | Meaning |
|------------|---------|
| > 1.0 | Amplifies market moves (e.g., 1.5 = moves 15% when market moves 10%) |
| = 1.0 | Moves in line with the market |
| 0.0 – 1.0 | Dampens market moves (e.g., 0.5 = moves 5% when market moves 10%) |
| < 0.0 | Moves inversely to the market |

## Example Requests

### Get S&P 500 beta bands

```bash
curl "https://eodhd.com/api/mp/illio/chapters/beta-bands/SnP500?api_token=YOUR_API_TOKEN"
```

### Get Nasdaq-100 beta bands

```bash
curl "https://eodhd.com/api/mp/illio/chapters/beta-bands/NDX?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/illio/chapters/beta-bands/SnP500?api_token=demo"
```

## Notes

- **Marketplace product**: Requires a separate illio marketplace subscription, not included in main EODHD plans.
- **Flat list**: Unlike some other illio endpoints, the `items[]` array is a flat list of instruments with beta values (not bucketed).
- **Negative beta**: Some instruments may have negative beta values, meaning they tend to move inversely to the market.
- **Expected range**: Most instruments have beta between 0.75 and 1.25. Values outside this range indicate unusually high or low market sensitivity.
- **Bull vs bear**: In bull markets, prefer high-beta instruments for amplified upside. In bear markets, prefer low-beta for reduced downside.
- **All constituents included**: Every member of the selected index appears in the response.
- **Supported indices**: S&P 500 (`SnP500`), Dow Jones (`DJI`), Nasdaq-100 (`NDX`).
- **Disclaimer**: Data does not constitute financial advice or investment recommendations.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **429** | Too Many Requests | Rate limit exceeded (1,000 req/min or 100,000 calls/24h). |
