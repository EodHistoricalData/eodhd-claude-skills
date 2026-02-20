# Illio Market Insights — Largest Volatility Change API

Status: complete
Source: marketplace (illio)
Provider: illio via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/illio/chapters`
Path: `/volume/{id}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns data about instruments with the largest changes in volatility over the past year. Shows which constituents experienced significant increases or decreases in 100-day volatility, helping users focus on names where risk characteristics are shifting.

**Use cases**:
- Identify stocks with rapidly increasing or decreasing volatility
- Detect regime changes in individual names (e.g., post-earnings, sector rotation)
- Screen for names entering or exiting high-volatility regimes
- Adjust position sizing based on changing volatility profiles

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
  "insightId": "LARGEST_VOL_MOVE",
  "categoryId": "RISK",
  "title": "Largest Volatility Change",
  "watchlistName": "US 500 Stocks",
  "insight": {
    "id": "LARGEST_VOL_MOVE",
    "title": "Which instruments have had the biggest changes in volatility?",
    "whyImportant": "This helps you focus on those instruments which, over the past year, have experienced a significant change in the amount they move per day.",
    "description": "Over the past year, 51.4% of these instruments had a volatility increase and 48.6% of these instruments had a volatility decrease.",
    "stats": [
      { "text": "Over the past year, the 100d volatility of Fiserv Inc. increased from 0% to 122.2%. This absolute increase of 122.2% is the largest of all the instruments." }
    ]
  },
  "chart": {
    "title": "Largest Increase and Decrease in Volatility Over The Past Year",
    "data": {
      "items": [
        {
          "code": "Volatility Increase",
          "label": "Volatility Increase",
          "value": 60.4,
          "instruments": [
            { "label": "Seagate Technology PLC", "value": 48.3 }
          ]
        },
        {
          "code": "Volatility Decrease",
          "label": "Volatility Decrease",
          "value": 39.6,
          "instruments": [
            { "label": "Tesla Inc", "value": -26.8 }
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
| `insightId` | string | Always `"LARGEST_VOL_MOVE"` |
| `categoryId` | string | Always `"RISK"` |
| `title` | string | Human-readable insight title |
| `watchlistName` | string | Name of the index |
| `insight.id` | string | Insight identifier |
| `insight.title` | string | Question the insight answers |
| `insight.whyImportant` | string | Explanation of why volatility changes matter |
| `insight.description` | string | Summary — percentage of instruments with increasing/decreasing volatility |
| `insight.stats[]` | array | Key statistics — largest absolute increase and decrease with from/to values |
| `chart.title` | string | Chart title |
| `chart.data.items[]` | array | Two buckets: Volatility Increase and Volatility Decrease |
| `chart.data.items[].code` | string | Bucket identifier (`"Volatility Increase"` or `"Volatility Decrease"`) |
| `chart.data.items[].label` | string | Display label for the bucket |
| `chart.data.items[].value` | float | Percentage of instruments in this bucket |
| `chart.data.items[].instruments[]` | array | Instruments in this bucket, sorted by magnitude |
| `chart.data.items[].instruments[].label` | string | Instrument name |
| `chart.data.items[].instruments[].value` | float | Absolute change in 100-day volatility (percentage points). Positive = increase, negative = decrease |

## Example Requests

### Get S&P 500 largest volatility changes

```bash
curl "https://eodhd.com/api/mp/illio/chapters/volume/SnP500?api_token=YOUR_API_TOKEN"
```

### Get Nasdaq-100 largest volatility changes

```bash
curl "https://eodhd.com/api/mp/illio/chapters/volume/NDX?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/illio/chapters/volume/SnP500?api_token=demo"
```

## Notes

- **Marketplace product**: Requires a separate illio marketplace subscription, not included in main EODHD plans.
- **URL path is `/volume/`**: Despite being a volatility endpoint, the URL path uses `/volume/{id}`.
- **100-day volatility**: The change is measured as the absolute difference in 100-day rolling volatility over the past year.
- **Two buckets**: Instruments are split into "Volatility Increase" and "Volatility Decrease" groups.
- **Stats detail from/to**: The stats text includes the starting and ending volatility values for the largest movers.
- **Sorted by magnitude**: Instruments within each bucket are sorted by the size of their volatility change (largest first).
- **Supported indices**: S&P 500 (`SnP500`), Dow Jones (`DJI`), Nasdaq-100 (`NDX`).
- **Disclaimer**: Data does not constitute financial advice or investment recommendations.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **429** | Too Many Requests | Rate limit exceeded (1,000 req/min or 100,000 calls/24h). |
