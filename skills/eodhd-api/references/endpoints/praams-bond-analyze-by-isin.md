# Praams Bond Analysis by ISIN API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/financial-apis/equity-risk-return-scoring-api
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/analyse/bond/{isin}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns comprehensive risk and return analytics for a specific bond identified
by its ISIN code. The response includes the proprietary PRAAMS Ratio, individual
risk and return scores across 12 dimensions, coupon details, profitability
metrics of the issuer, growth momentum, market view with spread/yield analysis,
performance history, and detailed textual descriptions — providing CFA-level
bond analysis in a single API call.

This endpoint is the bond-specific counterpart to the equity ISIN endpoint.
It shares a similar overall structure but includes bond-specific sections
(`coupon`, `marketView`, `bondType`) and omits equity-specific sections
(`analystView`, `dividend`).

**Use cases**:
- Instant risk-return assessment of any bond using the PRAAMS Ratio (1-10 scale)
- ISIN-based bond lookup for global fixed income securities
- Detailed breakdown of 12 scoring dimensions (coupon, valuation, volatility, solvency, etc.)
- Credit risk assessment including subordination and recovery rate analysis
- Spread analysis vs peer bonds with similar risk profiles
- Stress testing and volatility scoring for bond price risk
- Issuer profitability analysis with margins, RoE, RoA, RoCE, and RoIC/WACC
- Issuer growth momentum analysis (Revenue, EPS, EBITDA, FCF trends)
- Country and liquidity risk profiling
- Call risk assessment for callable bonds

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with ISINs `US7593518852` or `US91282CJN20`.

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `isin` | string | ISIN code of the bond (e.g. `US7593518852`, `US91282CJN20`) |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key (or `demo` for demo ISINs) |

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
| `ticker` | string | Bond description/name (e.g. `"RGA float 15-Oct-52"`) |
| `name` | string | Issuer name |
| `isin` | string | ISIN identifier |
| `companyDescription` | string | Issuer company description |
| `isActivelyTrading` | boolean | Whether the bond is currently trading |
| `assetId` | integer | Internal PRAAMS asset ID |
| `ratio` | integer | The PRAAMS Ratio (1-10 scale; higher = better risk-return). May be `0` when insufficient data. |
| `watchList` | boolean | Watchlist flag |
| `isBond` | boolean | Always `true` for bonds |
| `bondType` | string | Bond classification (e.g. `"Corporate"`) |
| `isFinancial` | boolean | Whether the issuer is in the financial sector |

> **Note**: Unlike equities, the `ticker` field contains a descriptive bond name (coupon type, maturity date) rather than a stock ticker symbol. The `isBond` field is always `true`.

#### `item.description`

| Field | Type | Description |
|-------|------|-------------|
| `assetClass` | string | Always `"bond"` |
| `country` | string | Country code (e.g. `"US"`) |
| `sector` | string | Sector name (e.g. `"Financial Services"`) |
| `regionIds` | array of integers | Region identifiers |
| `countryId` | integer | Country identifier |
| `sectorId` | integer | Sector identifier |
| `industryId` | integer | Industry identifier |
| `cohortId` | integer | Bond cohort/peer group identifier |
| `currencyId` | string | Currency code (e.g. `"USD"`) |
| `otherRisks` | object | `{short, long}` — other risk assessment (subordination, call risk, etc.) |
| `countryRisks` | object | `{short, long}` — country risk assessment |
| `liquidityRisk` | object | `{short, long}` — liquidity risk assessment |
| `stressTest` | object | `{short, long}` — stress test assessment |
| `volatility` | object | `{short, long}` — volatility assessment |
| `solvency` | object | `{short, long}` — solvency/default risk assessment |

Each risk object contains `short` (one-word rating like "Negligible", "Very low", "Small", "Moderate", "Considerable", "Very high", "No data") and `long` (detailed explanation).

> **Bond-specific fields**: `cohortId` is unique to the bond endpoint and identifies the peer group for spread comparisons. The `otherRisks` section often contains subordination and call risk details. The `solvency` section includes recovery rate estimates for subordinated bonds.

#### `item.profile`

| Field | Type | Description |
|-------|------|-------------|
| `companyProfileDescription` | object | `{short, long}` — issuer company profile descriptions |
| `finStatementAnalysisShort` | string | Short financial statement analysis (may be empty) |
| `finStatementAnalysis` | string | Financial analysis notes (e.g. `"Next call date 15-Oct-27"`) |

> **Note**: The bond profile does not include `parentAsset` or `parentNote` fields (unlike the equity ISIN endpoint). The `finStatementAnalysis` field may contain bond-specific notes such as the next call date.

#### `item.scores`

12 scoring dimensions, each an integer (1-10 scale). For bonds, the scoring dimensions differ slightly from equities:

| Field | Type | Description |
|-------|------|-------------|
| `marketView` | integer | Market view/spread score (bond-specific, replaces `analystView`) |
| `coupon` | integer | Coupon score (bond-specific, replaces `dividends`) |
| `valuation` | integer | Valuation score |
| `performance` | integer | Performance score |
| `profitability` | integer | Issuer profitability score |
| `growthMom` | integer | Issuer growth momentum score |
| `other` | integer | Other risks score |
| `countryRisk` | integer | Country risk score |
| `liquidity` | integer | Liquidity risk score |
| `stressTest` | integer | Stress test score |
| `volatility` | integer | Volatility score |
| `solvency` | integer | Solvency/default risk score |

A score of `0` indicates insufficient data for that dimension.

> **Score interpretation**: For risk dimensions (volatility, stressTest, liquidity, solvency, countryRisk, other), lower scores indicate lower risk. For return dimensions (valuation, performance, profitability, growthMom, marketView, coupon), higher scores indicate better return prospects. A score of `0` means "no data".

#### `item.keyFactors`

| Field | Type | Description |
|-------|------|-------------|
| `risk.characteristic` | string | Overall risk characterization (e.g. `"Considerable"`) |
| `risk.factors[]` | array | Key risk factors with `priority`, `text`, and `icon` (true=positive) |
| `return.characteristic` | string | Overall return characterization (e.g. `"Average"`) |
| `return.factors[]` | array | Key return factors with `priority`, `text`, and `icon` (true=positive) |

#### `item.valuation`

For bonds, valuation may be a simple text description rather than the structured multiples object used for equities:

| Field | Type | Description |
|-------|------|-------------|
| `short` | string | Valuation summary (e.g. `"No data"`) |
| `long` | string | Detailed valuation description |

> **Note**: When the bond is not actively trading, valuation returns a flat `{short, long}` object instead of the equity-style object with `descriptionShort`, `wams`, and `valuations[]`.

#### `item.performance`

| Field | Type | Description |
|-------|------|-------------|
| `description` | object | `{short, long}` — performance summary |
| `byPeriods[]` | array | Period returns with `period`, `asset` (decimal), `peers` (decimal). Empty array when no data available. |

#### `item.marketView` (bond-specific)

Replaces `analystView` from the equity endpoint. Provides spread and yield analysis vs peer bonds:

| Field | Type | Description |
|-------|------|-------------|
| `description` | object | `{short, long}` — market view summary with peer spread context |
| `yearSpreadHistory[]` | array | Historical spread data points (empty when insufficient data) |
| `yearPriceHistory[]` | array | Historical price data points (empty when insufficient data) |
| `yearYieldHistory[]` | array | Historical yield data points (empty when insufficient data) |
| `yearPeersSpreadHistory[]` | array | Peer group spread history (empty when insufficient data) |
| `firstSpreadDateInArray` | string | Start date of spread data (ISO 8601 format) |
| `lastSpreadDateInArray` | string | End date of spread data (ISO 8601 format) |
| `leftPeersValue` | number | Lower bound of comparable peer spread range (bps) |
| `rightPeersValue` | number | Upper bound of comparable peer spread range (bps) |

> **Spread interpretation**: The `leftPeersValue` and `rightPeersValue` define the spread range for comparable bonds. A spread below `leftPeersValue` generally means the bond is "expensive", while a spread above `rightPeersValue` implies the bond is "cheap".

#### `item.profitability`

Issuer profitability metrics (same structure as equity endpoint):

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Profitability summary (e.g. `"Average"`) |
| `profitability[]` | array | Metrics (RoE, RoA, RoCE) with `name`, `description`, `assets` and `peers` objects containing TTM/NTM values and scores |
| `profitabilityGraph[]` | array | Margin graphs (Net margin, EBITDA margin) with `name`, `shortDesc`, and `graph[]` containing historical data points |
| `roICWACC` | object | RoIC/WACC analysis with `description` `{short, long}` and `score` |
| `profitabilityPeerMargins[]` | array | Peer margin comparison with `name`, `scoreTTM`, `scoreNTM` |

#### `item.growthMomentum`

Issuer growth metrics (same structure as equity endpoint):

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Growth summary (e.g. `"Average"`) |
| `absDescription` | string | Absolute growth description |
| `chgDescription` | string | Growth rate change description |
| `currencySize` | string | Currency for size metrics |
| `growthMomentum[]` | array | Metrics (EPS, Revenue, EBITDA, FCF) with `name`, `graph[]` and `growthRatesGraph[]` |

Each metric's `graph[]` contains `{order, label, value, isPrediction}` data points. The `growthRatesGraph[]` contains the same structure with year-over-year growth rates as decimals.

#### `item.coupon` (bond-specific)

Replaces `dividend` from the equity endpoint. Provides coupon details:

| Field | Type | Description |
|-------|------|-------------|
| `short` | string | Coupon characterization (e.g. `"Reasonable"`) |
| `long` | string | Detailed coupon description including formula for floating-rate bonds |

> **Floating-rate bonds**: For floating-rate bonds, the `long` field describes the coupon formula (e.g. "7.125% from settlement date until 15.10.2027, then 5Y UST Yield + 3.456% to maturity").

## Example Request

```bash
curl "https://eodhd.com/api/mp/praams/analyse/bond/US7593518852?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/praams/analyse/bond/US7593518852?api_token=demo"
```

## Example Response (abbreviated)

```json
{
  "success": true,
  "message": "",
  "errors": [],
  "item": {
    "asset": {
      "ticker": "RGA float 15-Oct-52",
      "name": "Reinsurance Group of America, Incorporated",
      "isin": "US7593518852",
      "companyDescription": "Reinsurance Group of America, Incorporated engages in reinsurance business...",
      "isActivelyTrading": true,
      "assetId": 1336253,
      "ratio": 0,
      "isBond": true,
      "bondType": "Corporate",
      "isFinancial": false
    },
    "description": {
      "assetClass": "bond",
      "country": "US",
      "sector": "Financial Services",
      "cohortId": 8,
      "currencyId": "USD",
      "otherRisks": {
        "short": "Moderate",
        "long": "The bond is subordinated...This bond has a built-in call option..."
      },
      "volatility": {
        "short": "Very high",
        "long": "In normal market circumstances, the bond is exceptionally volatile..."
      },
      "solvency": {
        "short": "Considerable",
        "long": "The risk of default is moderate..."
      }
    },
    "profile": {
      "companyProfileDescription": {
        "short": "Reinsurance Group of America...",
        "long": "Reinsurance Group of America..."
      },
      "finStatementAnalysis": "Next call date 15-Oct-27"
    },
    "scores": {
      "marketView": 0,
      "coupon": 4,
      "valuation": 0,
      "performance": 0,
      "profitability": 4,
      "growthMom": 4,
      "other": 4,
      "countryRisk": 1,
      "liquidity": 0,
      "stressTest": 7,
      "volatility": 7,
      "solvency": 5
    },
    "keyFactors": {
      "risk": {
        "characteristic": "Considerable",
        "factors": [
          {"priority": 1, "text": "Very high price volatility", "icon": false},
          {"priority": 2, "text": "Weak & very vulnerable to price shocks", "icon": false},
          {"priority": 3, "text": "Considerable default risk", "icon": false}
        ]
      },
      "return": {
        "characteristic": "Average",
        "factors": [
          {"priority": 1, "text": "Reasonable coupons", "icon": true},
          {"priority": 2, "text": "Average margins and returns", "icon": true},
          {"priority": 3, "text": "Average growth", "icon": true}
        ]
      }
    },
    "valuation": {
      "short": "No data",
      "long": "The instrument is not actively trading..."
    },
    "marketView": {
      "description": {
        "short": "Not enough data",
        "long": "There is not enough market data to compare this bond to its peers..."
      },
      "yearSpreadHistory": [],
      "yearPriceHistory": [],
      "yearYieldHistory": [],
      "yearPeersSpreadHistory": [],
      "firstSpreadDateInArray": "2024-12-03T00:00:00",
      "lastSpreadDateInArray": "2025-12-01T00:00:00",
      "leftPeersValue": 62.0,
      "rightPeersValue": 329.0
    },
    "profitability": {
      "description": "Average",
      "roICWACC": {
        "description": {"short": "average value creation", "long": "..."},
        "score": 1.2
      }
    },
    "growthMomentum": {
      "description": "Average",
      "currencySize": "USD"
    },
    "coupon": {
      "short": "Reasonable",
      "long": "We draw your attention to the fact that the bond pays a floating coupon. The coupon formula is 7.125% from settlement date until 15.10.2027, then 5Y UST Yield + 3.456% to maturity."
    }
  }
}
```

## Notes

- **Marketplace product**: Requires a separate PRAAMS marketplace subscription, not included in main EODHD plans.
- **PRAAMS Ratio**: The flagship metric (`item.asset.ratio`) summarizes 470+ metrics into a single 1-10 score. Higher is better. For bonds with insufficient trading data, this may be `0`.
- **Bond vs Equity differences**: The bond endpoint uses `marketView` (spread/yield analysis) instead of `analystView`, `coupon` instead of `dividend`, and includes `bondType` and `cohortId`. The `assetClass` is `"bond"` and `isBond` is `true`.
- **Demo ISINs**: `US7593518852` (RGA corporate bond) and `US91282CJN20` are available with `api_token=demo`.
- **Coverage**: Part of the 120,000+ global equities and bonds coverage. Use the equity ISIN endpoint for equity analysis (see praams-risk-scoring-by-isin.md).
- **Score of 0**: A score of `0` in `item.scores` indicates insufficient data for that dimension. This is common for illiquid bonds where market data is sparse (e.g. `marketView: 0`, `valuation: 0`, `performance: 0`, `liquidity: 0`).
- **Subordinated bonds**: The `otherRisks` and `solvency` descriptions provide detailed subordination analysis, including expected recovery rates (typically 15-20% for subordinated bonds).
- **Callable bonds**: Call risk is documented in `otherRisks.long` and the next call date appears in `profile.finStatementAnalysis`.
- **Floating-rate bonds**: The `coupon` section describes the full coupon formula, including the fixed-rate period and the floating-rate formula after the reset date.
- **Peer spread range**: `marketView.leftPeersValue` and `rightPeersValue` (in basis points) define the fair value range for comparable bonds. Below the range = expensive; above = cheap.
- **Valuation format**: Unlike equities (which return structured multiples), bond valuation may return a simple `{short, long}` text object when insufficient trading data is available.
- **Profitability and growth**: These sections analyze the bond **issuer's** financial health, not the bond itself. They share the same structure as the equity endpoint.
- **Rich text descriptions**: Most sections include `short` (headline) and `long` (detailed paragraph) descriptions suitable for display to end users.
- **Related endpoints**: Use `/analyse/equity/isin/{isin}` for equity ISIN lookups and `/analyse/equity/ticker/{ticker}` for equity ticker lookups.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **415** | Wrong Token | Token format is invalid. |
| **420** | Operation Cancelled | Request was cancelled. |
| **430** | Data Not Found | ISIN not found in PRAAMS database. |

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
            print("Error: ISIN not found in PRAAMS database.")
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
