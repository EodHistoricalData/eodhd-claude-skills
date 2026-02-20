# Illio Market Insights — Risk-Return API

Status: complete
Source: marketplace (illio)
Provider: illio via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/illio/chapters`
Path: `/risk/{id}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns data about the risk-return tradeoffs of instruments in the specified index. Shows each constituent's return, volatility, and risk-return ratio, helping users identify instruments that reward well (or poorly) for the risk taken.

**Use cases**:
- Identify stocks with the best risk-adjusted returns
- Screen for high-Sharpe-ratio ideas within an index
- Compare return-per-unit-of-risk across all constituents
- Portfolio construction — favor instruments with ratio > 1

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
  "insightId": "RISK_RETURN",
  "categoryId": "RISK",
  "title": "Risk-return",
  "watchlistName": "US 500 Stocks",
  "insight": {
    "id": "RISK_RETURN",
    "title": "What are the instrument risk-return tradeoffs?",
    "whyImportant": "Instruments with a risk-return ratio greater than 1 reward you well for the risk you take and instruments below 1 do not reward you well for the risk you take.",
    "description": "The top 3 instruments by Risk Return ratio are Targa Resources Inc, Vistra Energy Corp and Palantir Technologies Inc. Class A Common Stock.",
    "stats": [
      { "text": "The top 3 instruments by Risk Return are Targa Resources Inc, Vistra Energy Corp and Palantir Technologies Inc. Class A Common Stock with 6.97, 5.75 and 5.21 respectively." }
    ]
  },
  "chart": {
    "title": "Risk-Return Ratios",
    "data": {
      "items": [
        {
          "label": "Ameriprise Financial Inc",
          "return": 49.97,
          "volatility": 21.44,
          "ratio": 2.33126
        }
      ]
    }
  }
}
```

### Response Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `insightId` | string | Always `"RISK_RETURN"` |
| `categoryId` | string | Always `"RISK"` |
| `title` | string | Human-readable insight title |
| `watchlistName` | string | Name of the index |
| `insight.id` | string | Insight identifier |
| `insight.title` | string | Question the insight answers |
| `insight.whyImportant` | string | Explanation of risk-return ratio interpretation |
| `insight.description` | string | Summary — top 3 instruments by ratio |
| `insight.stats[]` | array | Key statistics — top 3 and bottom 3 by risk-return ratio |
| `chart.title` | string | Chart title |
| `chart.data.items[]` | array | All instruments with risk-return data |
| `chart.data.items[].label` | string | Instrument name |
| `chart.data.items[].return` | float | Total return over the last year (%) |
| `chart.data.items[].volatility` | float | Annualized volatility (%) |
| `chart.data.items[].ratio` | float | Risk-return ratio (return / volatility). >1 = well rewarded, <1 = poorly rewarded |

## Example Requests

### Get S&P 500 risk-return data

```bash
curl "https://eodhd.com/api/mp/illio/chapters/risk/SnP500?api_token=YOUR_API_TOKEN"
```

### Get Nasdaq-100 risk-return data

```bash
curl "https://eodhd.com/api/mp/illio/chapters/risk/NDX?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/illio/chapters/risk/SnP500?api_token=demo"
```

## Notes

- **Marketplace product**: Requires a separate illio marketplace subscription, not included in main EODHD plans.
- **Ratio interpretation**: Ratio > 1 means the instrument rewards you well for the risk taken. Ratio < 1 (or negative) means the risk is not well compensated.
- **Three data points per instrument**: Each item includes `return`, `volatility`, and `ratio` — suitable for scatter plot visualization.
- **Negative ratios**: Instruments with negative returns will have negative ratios, indicating loss relative to risk.
- **One-year lookback**: Return and volatility are calculated over the last year.
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
