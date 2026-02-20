# Praams Equity Risk & Return Scoring by Ticker API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/financial-apis/equity-risk-return-scoring-api
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/analyse/equity/ticker/{ticker}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns comprehensive risk and return analytics for a specific equity
identified by its ticker symbol. The response includes the proprietary PRAAMS
Ratio, individual risk and return scores across 12 dimensions, valuation
multiples, profitability metrics, growth momentum, dividend data, analyst
views, performance history, and detailed textual descriptions — providing
CFA-level analysis in a single API call.

**Use cases**:
- Instant risk-return assessment of any equity using the PRAAMS Ratio (1-10 scale)
- Detailed breakdown of 12 scoring dimensions (valuation, profitability, volatility, solvency, etc.)
- Valuation analysis with TTM and NTM multiples (P/E, PEG, P/B, P/S, P/FCF, EV/EBITDA)
- Performance tracking vs sector/industry peers
- Profitability analysis with margins, RoE, RoA, RoCE, and RoIC/WACC
- Growth momentum analysis (Revenue, EPS, EBITDA, FCF trends)
- Dividend history and yield analysis
- Analyst consensus price targets and recommendations
- Risk profiling: volatility, stress testing, liquidity, solvency, country risk

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with tickers `AAPL`, `TSLA`, or `AMZN`.

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticker` | string | Ticker symbol of the equity (e.g. `AAPL`, `TSLA`, `AMZN`) |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key (or `demo` for demo tickers) |

## Response (shape)

JSON object with top-level envelope:

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` if request succeeded |
| `message` | string | Status message (empty on success) |
| `errors` | array | Error objects with `code` and `description` (empty on success) |
| `item` | object | The main data payload |

### `item` object

Contains the following sections:

#### `item.asset`

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Ticker symbol |
| `name` | string | Company name |
| `isin` | string | ISIN identifier |
| `companyDescription` | string | Brief company description |
| `isActivelyTrading` | boolean | Whether the stock is currently trading |
| `assetId` | integer | Internal PRAAMS asset ID |
| `ratio` | integer | The PRAAMS Ratio (1-10 scale; higher = better risk-return) |
| `watchList` | boolean | Watchlist flag |
| `isBond` | boolean | Always `false` for equities |
| `isFinancial` | boolean | Whether the company is in the financial sector |

#### `item.description`

| Field | Type | Description |
|-------|------|-------------|
| `assetClass` | string | Always `"equity"` |
| `country` | string | Country code (e.g. `"US"`) |
| `sector` | string | Sector name (e.g. `"Technology"`) |
| `regionIds` | array of integers | Region identifiers |
| `countryId` | integer | Country identifier |
| `sectorId` | integer | Sector identifier |
| `industryId` | integer | Industry identifier |
| `currencyId` | string | Currency code (e.g. `"USD"`) |
| `otherRisks` | object | `{short, long}` — other risk assessment |
| `countryRisks` | object | `{short, long}` — country risk assessment |
| `liquidityRisk` | object | `{short, long}` — liquidity risk assessment |
| `stressTest` | object | `{short, long}` — stress test assessment |
| `volatility` | object | `{short, long}` — volatility assessment |
| `solvency` | object | `{short, long}` — solvency/default risk assessment |

Each risk object contains `short` (one-word rating like "Negligible", "Low", "Limited") and `long` (detailed explanation).

#### `item.scores`

12 scoring dimensions, each an integer (1-10 scale, lower = better for risk, higher = better for return):

| Field | Type | Description |
|-------|------|-------------|
| `valuation` | integer | Valuation score |
| `performance` | integer | Performance score |
| `profitability` | integer | Profitability score |
| `growthMom` | integer | Growth momentum score |
| `other` | integer | Other risks score |
| `countryRisk` | integer | Country risk score |
| `liquidity` | integer | Liquidity risk score |
| `stressTest` | integer | Stress test score |
| `volatility` | integer | Volatility score |
| `solvency` | integer | Solvency/default risk score |
| `analystView` | integer | Analyst view score |
| `dividends` | integer | Dividend score |

#### `item.keyFactors`

| Field | Type | Description |
|-------|------|-------------|
| `risk.characteristic` | string | Overall risk characterization (e.g. `"Low"`) |
| `risk.factors[]` | array | Key risk factors with `priority`, `text`, and `icon` (true=positive) |
| `return.characteristic` | string | Overall return characterization (e.g. `"Average"`) |
| `return.factors[]` | array | Key return factors with `priority`, `text`, and `icon` (true=positive) |

#### `item.valuation`

| Field | Type | Description |
|-------|------|-------------|
| `descriptionShort` | object | `{short, long}` — valuation summary |
| `wams` | integer | Weighted average multiple score |
| `valuations[]` | array | Individual multiples with `name`, `score`, `ttm`, `ntm` |

Multiples include: P/E, PEG, P/B, P/S, P/FCF, EV/EBITDA.

#### `item.performance`

| Field | Type | Description |
|-------|------|-------------|
| `description` | object | `{short, long}` — performance summary |
| `byPeriods[]` | array | Period returns with `period`, `asset` (decimal), `peers` (decimal) |

#### `item.analystView`

| Field | Type | Description |
|-------|------|-------------|
| `description` | object | `{short, long}` — analyst consensus summary |
| `priceTarget` | object | `{currency, average, min, max}` — consensus price targets |
| `yearPriceHistory[]` | array | Price history data points `{id, value}` |
| `currency` | string | Currency of prices |

#### `item.profitability`

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Profitability summary (e.g. `"Very strong"`) |
| `profitability[]` | array | Metrics (RoE, RoA, RoCE) with asset/peers TTM/NTM values and scores |
| `profitabilityGraph[]` | array | Margin graphs (Net margin, EBITDA margin) with historical data |
| `roICWACC` | object | RoIC/WACC analysis with `description` and `score` |

#### `item.growthMomentum`

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Growth summary (e.g. `"Average"`) |
| `absDescription` | string | Absolute growth description |
| `chgDescription` | string | Growth rate change description |
| `currencySize` | string | Currency for size metrics |
| `growthMomentum[]` | array | Metrics (EPS, Revenue, EBITDA, FCF) with `graph[]` and `growthRatesGraph[]` |

#### `item.dividend`

| Field | Type | Description |
|-------|------|-------------|
| `description` | object | `{short, long}` — dividend summary |
| `currency` | string | Dividend currency |
| `dividendPaid[]` | array | DPS history `{order, label, value, isPrediction}` |
| `annualDividendPayments[]` | array | Annual payments history |
| `dividendYield[]` | array | Yield history |
| `averageFrequency` | number | Average annual dividend payment frequency |
| `dividendsLast3Y` | number | Cumulative DPS over last 3 years |
| `dividendsLast5Y` | number | Cumulative DPS over last 5 years |

## Example Request

```bash
curl "https://eodhd.com/api/mp/praams/analyse/equity/ticker/AAPL?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/praams/analyse/equity/ticker/AAPL?api_token=demo"
```

## Example Response (abbreviated)

```json
{
  "success": true,
  "message": "",
  "errors": [],
  "item": {
    "asset": {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "isin": "US0378331005",
      "companyDescription": "Apple Inc. designs, manufactures, and markets smartphones...",
      "isActivelyTrading": true,
      "assetId": 34221,
      "ratio": 5,
      "isBond": false,
      "isFinancial": false
    },
    "description": {
      "assetClass": "equity",
      "country": "US",
      "sector": "Technology",
      "currencyId": "USD",
      "volatility": {
        "short": "Negligible",
        "long": "In normal market circumstances, AAPL is not volatile..."
      },
      "solvency": {
        "short": "Limited",
        "long": "The risk of default is minimal..."
      }
    },
    "scores": {
      "valuation": 1,
      "performance": 5,
      "profitability": 7,
      "growthMom": 4,
      "other": 1,
      "countryRisk": 1,
      "liquidity": 2,
      "stressTest": 1,
      "volatility": 1,
      "solvency": 3,
      "analystView": 5,
      "dividends": 3
    },
    "keyFactors": {
      "risk": {
        "characteristic": "Low",
        "factors": [
          {"priority": 1, "text": "Negligible price volatility", "icon": true}
        ]
      },
      "return": {
        "characteristic": "Average",
        "factors": [
          {"priority": 1, "text": "Very strong margins and returns", "icon": true}
        ]
      }
    },
    "valuation": {
      "descriptionShort": {
        "short": "Greatly overvalued",
        "long": "From both historical and forecast perspectives..."
      },
      "wams": 1,
      "valuations": [
        {"name": "P/E", "score": 1, "ttm": 37.0, "ntm": 37.2},
        {"name": "EV/EBITDA", "score": 1, "ttm": 28.7, "ntm": 29.6}
      ]
    },
    "profitability": {
      "description": "Very strong",
      "roICWACC": {
        "description": {"short": "excellent value creation", "long": "..."},
        "score": 8.4
      }
    },
    "dividend": {
      "description": {"short": "Modest", "long": "..."},
      "currency": "USD",
      "averageFrequency": 4.0,
      "dividendsLast3Y": 2.97,
      "dividendsLast5Y": 4.745
    }
  }
}
```

## Notes

- **Marketplace product**: Requires a separate PRAAMS marketplace subscription, not included in main EODHD plans.
- **PRAAMS Ratio**: The flagship metric (`item.asset.ratio`) summarizes 470+ metrics into a single 1-10 score. Higher is better.
- **Demo tickers**: `AAPL`, `TSLA`, and `AMZN` are available with `api_token=demo`.
- **Coverage**: 120,000+ global equities. Use the ISIN-based endpoint for bond analysis.
- **Score scale**: All 12 dimension scores in `item.scores` are integers. For risk dimensions (volatility, stressTest, liquidity, solvency, countryRisk, other), lower scores indicate lower risk. For return dimensions (valuation, performance, profitability, growthMom, analystView, dividends), higher scores indicate better return prospects.
- **Rich text descriptions**: Most sections include `short` (headline) and `long` (detailed paragraph) descriptions suitable for display to end users.
- **Peer comparisons**: Profitability and performance sections include peer benchmark data for the same sector/industry.
- **TTM vs NTM**: Valuation and profitability metrics include both trailing twelve months (TTM) and next twelve months (NTM, consensus estimates).
- **Related endpoint**: Use `/analyse/equity/isin/{isin}` for ISIN-based lookups (see praams-risk-scoring-by-isin.md).

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **415** | Wrong Token | Token format is invalid. |
| **420** | Operation Cancelled | Request was cancelled. |
| **430** | Data Not Found | Ticker not found in PRAAMS database. |

### Error Response Format

When an error occurs, the API returns a JSON response:

```json
{
  "success": false,
  "message": "Error description",
  "errors": [
    {
      "code": "ERROR_CODE",
      "description": "Detailed error description"
    }
  ],
  "item": null
}
```

### Handling Errors

**Python Example**:
```python
import requests

def make_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get("success"):
            errors = data.get("errors", [])
            for err in errors:
                print(f"API Error [{err.get('code')}]: {err.get('description')}")
            return None
        return data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Error: Invalid API key. Check your credentials.")
        elif e.response.status_code == 415:
            print("Error: Wrong token format.")
        elif e.response.status_code == 430:
            print("Error: Ticker not found in PRAAMS database.")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

**Best Practices**:
- Always check `success` field in the response before processing `item`
- Implement exponential backoff for rate limit errors
- Cache responses to reduce API calls — PRAAMS data updates daily
- Monitor your API usage in the user dashboard
