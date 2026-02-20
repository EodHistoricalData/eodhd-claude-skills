# Illio Performance Insights API

Status: complete
Source: marketplace (illio)
Provider: illio via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/illio/categories`
Path: `/performance/{id}`
Method: GET
Auth: `api_token` query parameter

> **Note**: This endpoint uses `/categories/performance/` (not `/chapters/` like the illio Market Insights endpoints).

## Purpose

Returns comprehensive performance filter data for all constituents of a given index. Provides multiple insight categories covering market outperformance, price returns, total returns, distance to highs/lows, up/down day analysis, and average move sizes — all across multiple time periods.

**Use cases**:
- Screen for outperformers/underperformers across multiple timeframes (1d to 5y)
- Identify instruments closest to breaking out above highs or below lows
- Analyze up/down day patterns and average move sizes
- Compare price return vs total return (with income/dividends)
- Research and article enrichment with ranked constituent data

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
    "displayName": "US 500 Stocks",
    "id": "SnP500"
  },
  "insight": [
    {
      "id": "PERFORMANCE_VS_MARKET",
      "title": "Largest Market Out and Under Performers",
      "chart": [
        {
          "subTitle": null,
          "whyImportant": "This helps you assess whether the instrument has beaten the market over the last year...",
          "rows": [
            {
              "label": "Highest",
              "instruments": [
                {
                  "instrumentId": 4115,
                  "name": "Palantir Technologies Inc. Class A Common Stock",
                  "label": "PLTR",
                  "value": "+310.3%",
                  "icon": "images/logos/eod/PLTR.US.png"
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
| `chart[].subTitle` | string or null | Time period label (e.g., "1 month", "3 months", "1 Year", "Year to Date"). `null` for insights without time periods |
| `chart[].whyImportant` | string | Explanation of what this metric measures |
| `chart[].rows[]` | array | Contains `"Highest"` and `"Lowest"` ranked lists |
| `chart[].children[]` | array | Always empty in current implementation |

### Row / Instrument Object

| Field | Type | Description |
|-------|------|-------------|
| `rows[].label` | string | `"Highest"` or `"Lowest"` |
| `rows[].instruments[]` | array | Top 10 instruments for this ranking |
| `instruments[].instrumentId` | integer | Internal instrument identifier |
| `instruments[].name` | string | Full instrument name |
| `instruments[].label` | string | Ticker symbol (e.g., `"AAPL.US"`, `"PLTR"`) |
| `instruments[].value` | string | Formatted value with sign and % (e.g., `"+310.3%"`, `"-72.8%"`, `"156"`) |
| `instruments[].icon` | string or null | Path to instrument logo image (may be `null`) |

## Insight Categories

The response includes the following insight sections, each with their own time-period breakdowns:

| Insight ID | Title | Time Periods | Description |
|------------|-------|--------------|-------------|
| `LARGEST_MARKET_OUT_PERFORMANCE` | Largest Market Out and Under Performers | 1m, 3m, 6m, 1y, YTD, 3y, 5y | Outperformance vs index (total return of instrument minus total return of market) |
| `PRICE_RETURN` | Price Return | 1d, 1w, 1m, 3m, 6m, 1y, 3y, 5y, YTD | Pure price change (excludes dividends) |
| `TOTAL_RETURN` | Total Return | 1m, 3m, 6m, 1y, YTD, 3y, 5y | Price change including income/dividends |
| `POTENTIAL_BREAK_OUTS` | Closest to high | 1m, 3m, 6m, 1y | Distance from current price to period high (lower % = closer to breakout) |
| `POTENTIAL_BREAK_DOWNS` | Closest to low | 1m, 3m, 6m, 1y | Distance from current price to period low (lower % = closer to breakdown) |
| `AVERAGE_UP_DAYS` | Average Up Day Price Move | single (no subTitle) | Average positive daily move over last year |
| `AVERAGE_DOWN_DAYS` | Average Down Day Price Move | single (no subTitle) | Average negative daily move over last year |
| `UP_DAYS` | Up Days | single (no subTitle) | Count of positive-return trading days over last year |
| `DOWN_DAYS` | Down Days | single (no subTitle) | Count of negative-return trading days over last year |

## Example Requests

### Get S&P 500 performance insights

```bash
curl "https://eodhd.com/api/mp/illio/categories/performance/SnP500?api_token=YOUR_API_TOKEN"
```

### Get Nasdaq-100 performance insights

```bash
curl "https://eodhd.com/api/mp/illio/categories/performance/NDX?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/illio/categories/performance/SnP500?api_token=demo"
```

## Notes

- **Marketplace product**: Requires a separate illio marketplace subscription, not included in main EODHD plans.
- **URL path uses `/categories/`**: This endpoint is at `/api/mp/illio/categories/performance/{id}`, not `/chapters/` like the other illio Market Insights endpoints.
- **Large response**: The response contains 9 insight categories with multiple time periods each, totaling a significant amount of data per request. Cache responses where possible.
- **Top 10 per rank**: Each `rows[]` entry contains up to 10 instruments for both "Highest" and "Lowest" rankings.
- **String-formatted values**: Unlike other illio endpoints that return numeric values, `instruments[].value` is a pre-formatted string (e.g., `"+310.3%"`, `"156"`). Parse accordingly.
- **Breakout/breakdown distance**: For `POTENTIAL_BREAK_OUTS` and `POTENTIAL_BREAK_DOWNS`, lower values in "Highest" mean the instrument is closest to the high/low (most likely to break out/down).
- **Up/Down days**: `UP_DAYS` and `DOWN_DAYS` values are integer counts (as strings), not percentages.
- **Supported indices**: S&P 500 (`SnP500`), Dow Jones (`DJI`), Nasdaq-100 (`NDX`).
- **Disclaimer**: Data does not constitute financial advice or investment recommendations.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | No access to this marketplace product. |
| **429** | Too Many Requests | Rate limit exceeded (1,000 req/min or 100,000 calls/24h). |
