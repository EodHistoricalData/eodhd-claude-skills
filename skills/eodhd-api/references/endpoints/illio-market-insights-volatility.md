# Illio Market Insights — Volatility Bands API

Status: complete
Source: marketplace (illio)
Provider: illio via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/illio/chapters`
Path: `/volatility/{id}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns data about instruments' volatility compared to the market over the last year. Shows each constituent's annualized volatility alongside the market's volatility, helping users understand each instrument's risk and implied daily move potential.

**Use cases**:
- Compare individual stock volatility to the overall market
- Identify high- and low-volatility constituents for strategy construction
- Estimate implied daily moves based on annualized volatility
- Assess portfolio risk exposure across index members

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
  "insightId": "VOLATILITY_BANDS_MARKET",
  "categoryId": "RISK",
  "title": "Volatility and Day moves",
  "watchlistName": "US 500 Stocks",
  "insight": {
    "id": "VOLATILITY_BANDS_MARKET",
    "title": "Volatility and Day moves",
    "whyImportant": "This helps you understand each instrument's risk in the context of the amount it could move on an average day. The volatility bands are based on a typical balanced multi-asset portfolio.",
    "description": "Over the last year, the market had a volatility of 12.75%. 495 out of 496 instruments (99.8%) in this index have a volatility above the market.",
    "stats": [
      { "text": "The instrument with the highest volatility is SMCI at 119.65%. This implies a potential daily move of 7.42%." }
    ]
  },
  "chart": {
    "title": "Volatility Compared To The Market",
    "data": {
      "items": [
        { "symbol": "Market", "group": "MARKET", "value": 23.35 },
        { "symbol": "Apple Inc", "group": "Shares", "value": 31.98 },
        { "symbol": "NVIDIA Corporation", "group": "Shares", "value": 44.38 }
      ]
    }
  }
}
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `insightId` | string | Always `"VOLATILITY_BANDS_MARKET"` |
| `categoryId` | string | Always `"RISK"` |
| `title` | string | Human-readable insight title |
| `watchlistName` | string | Name of the index |
| `insight.id` | string | Insight identifier |
| `insight.title` | string | Insight title |
| `insight.whyImportant` | string | Explanation of why volatility matters |
| `insight.description` | string | Summary — market volatility, number of instruments above/below it |
| `insight.stats[]` | array | Key statistics — highest/lowest volatility instruments and implied daily moves |
| `chart.title` | string | Chart title |
| `chart.data.items[]` | array | All instruments plus the market benchmark |
| `chart.data.items[].symbol` | string | Instrument name (or `"Market"` for the benchmark) |
| `chart.data.items[].group` | string | `"MARKET"` for the benchmark, `"Shares"` for instruments |
| `chart.data.items[].value` | float | Annualized volatility (%) |

> The first item in `items[]` with `group: "MARKET"` represents the overall market/index volatility. All other items are individual constituents.

## Example Requests

### Get S&P 500 volatility bands

```bash
curl "https://eodhd.com/api/mp/illio/chapters/volatility/SnP500?api_token=YOUR_API_TOKEN"
```

### Get Nasdaq-100 volatility bands

```bash
curl "https://eodhd.com/api/mp/illio/chapters/volatility/NDX?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/illio/chapters/volatility/SnP500?api_token=demo"
```

## Notes

- **Marketplace product**: Requires a separate illio marketplace subscription, not included in main EODHD plans.
- **Market benchmark**: The first item with `group: "MARKET"` is the index-level volatility. Compare individual instruments against this value.
- **Implied daily move**: Annualized volatility can be converted to an implied daily move by dividing by sqrt(252). For example, 23.35% annualized ≈ 1.47% daily.
- **One-year lookback**: Volatility is calculated over the last year of trading data.
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
