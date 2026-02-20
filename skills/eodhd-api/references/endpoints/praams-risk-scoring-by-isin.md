# Praams Equity Risk & Return Scoring by ISIN API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/financial-apis/equity-risk-return-scoring-api
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/analyse/equity/isin/{isin}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Returns comprehensive risk and return analytics for a specific equity
identified by its ISIN code. The response includes the proprietary PRAAMS
Ratio, individual risk and return scores across 12 dimensions, valuation
multiples, profitability metrics, growth momentum, dividend data, analyst
views, performance history, company profile, and detailed textual descriptions
— providing CFA-level analysis in a single API call.

This is the ISIN-based variant of the PRAAMS Equity Risk & Return Scoring API.
It returns the same data structure as the ticker-based endpoint but accepts
an ISIN identifier instead. The response resolves the ISIN to its associated
ticker(s) and returns analysis for the primary listing.

**Use cases**:
- Instant risk-return assessment of any equity using the PRAAMS Ratio (1-10 scale)
- ISIN-based lookups for international equities where ticker symbols vary by exchange
- Detailed breakdown of 12 scoring dimensions (valuation, profitability, volatility, solvency, etc.)
- Valuation analysis with TTM and NTM multiples (P/E, PEG, P/B, P/S, P/FCF, EV/EBITDA)
- Performance tracking vs sector/industry peers
- Profitability analysis with margins, RoE, RoA, RoCE, and RoIC/WACC
- Growth momentum analysis (Revenue, EPS, EBITDA, FCF trends)
- Dividend history and yield analysis
- Analyst consensus price targets and recommendations
- Risk profiling: volatility, stress testing, liquidity, solvency, country risk
- Cross-listing discovery via the `profile.parentAsset` field

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with ISINs `US0378331005` (AAPL), `US88160R1014` (TSLA), or `US0231351067` (AMZN).

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `isin` | string | ISIN code of the equity (e.g. `US88160R1014`, `US0378331005`, `US0231351067`) |

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
| `ticker` | string | Resolved ticker symbol (e.g. `TL0.DE` for TSLA's German listing) |
| `name` | string | Company name |
| `isin` | string | ISIN identifier |
| `companyDescription` | string | Brief company description |
| `isActivelyTrading` | boolean | Whether the stock is currently trading |
| `assetId` | integer | Internal PRAAMS asset ID |
| `ratio` | integer | The PRAAMS Ratio (1-10 scale; higher = better risk-return) |
| `watchList` | boolean | Watchlist flag |
| `isBond` | boolean | Always `false` for equities |
| `isFinancial` | boolean | Whether the company is in the financial sector |

> **Note**: The `ticker` field may resolve to a non-US listing (e.g. `TL0.DE` for Tesla on the German exchange) depending on which exchange the ISIN maps to.

#### `item.description`

| Field | Type | Description |
|-------|------|-------------|
| `assetClass` | string | Always `"equity"` |
| `country` | string | Country code (e.g. `"US"`) |
| `sector` | string | Sector name (e.g. `"Consumer Cyclical"`) |
| `regionIds` | array of integers | Region identifiers |
| `countryId` | integer | Country identifier |
| `sectorId` | integer | Sector identifier |
| `industryId` | integer | Industry identifier |
| `currencyId` | string | Currency code (e.g. `"EUR"`, `"USD"`) |
| `otherRisks` | object | `{short, long}` — other risk assessment |
| `countryRisks` | object | `{short, long}` — country risk assessment |
| `liquidityRisk` | object | `{short, long}` — liquidity risk assessment |
| `stressTest` | object | `{short, long}` — stress test assessment |
| `volatility` | object | `{short, long}` — volatility assessment |
| `solvency` | object | `{short, long}` — solvency/default risk assessment |

Each risk object contains `short` (one-word rating like "Negligible", "Very low", "Small", "Modest", "Meaningful", "Limited") and `long` (detailed explanation).

#### `item.profile`

| Field | Type | Description |
|-------|------|-------------|
| `companyProfileDescription` | object | `{short, long}` — company profile descriptions |
| `parentNote` | string | Note about primary listing association (e.g. "This stock is associated with Tesla, Inc.. The primary listing...is TSLA.") |
| `finStatementAnalysisShort` | string | Short financial statement analysis (may be empty) |
| `finStatementAnalysis` | string | Full financial statement analysis (may be empty) |
| `parentAsset` | object | Parent/primary listing information |

##### `item.profile.parentAsset`

| Field | Type | Description |
|-------|------|-------------|
| `keyId` | integer | Internal key ID |
| `rank` | integer | Ranking value |
| `isin` | string | ISIN of the parent/primary listing |
| `assetName` | string | Ticker of the primary listing (e.g. `"TSLA"`) |
| `issuerName` | string | Issuer/company name |
| `mainRatio` | integer | PRAAMS Ratio for the primary listing |
| `watchList` | boolean | Watchlist flag |
| `isBond` | boolean | Bond flag |
| `isSovereign` | boolean | Sovereign entity flag |
| `isUncategorized` | boolean | Uncategorized flag |
| `isETF` | boolean | ETF flag |
| `isCustom` | boolean | Custom asset flag |
| `isParent` | boolean | Whether this is the parent listing |
| `groupSize` | integer | Number of listings in the group |
| `children` | array | Child listings (usually empty) |
| `searchOrder` | number | Search ordering value |
| `etfAssetWeight` | number | ETF weight (0.0 for non-ETFs) |

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
| `risk.characteristic` | string | Overall risk characterization (e.g. `"Limited"`) |
| `risk.factors[]` | array | Key risk factors with `priority`, `text`, and `icon` (true=positive) |
| `return.characteristic` | string | Overall return characterization (e.g. `"Modest"`) |
| `return.factors[]` | array | Key return factors with `priority`, `text`, and `icon` (true=positive) |

#### `item.valuation`

| Field | Type | Description |
|-------|------|-------------|
| `descriptionShort` | object | `{short, long}` — valuation summary |
| `wams` | integer | Weighted average multiple score |
| `valuations[]` | array | Individual multiples with `name`, `score`, `ttm`, `ntm` |

Multiples include: P/E, PEG, P/B, P/S, P/FCF, EV/EBITDA. Note that `ntm` may be absent for some multiples (e.g. PEG, P/B, P/FCF).

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
| `analystViewYearPriceHistory[]` | array | Analyst target price history `{id, value}` |
| `currency` | string | Currency of price history (may differ from `priceTarget.currency`) |
| `analystViewCurrency` | string | Currency of analyst price targets |

> **Note**: The ISIN endpoint may return `currency` and `analystViewCurrency` as different values (e.g. `"EUR"` for price history and `"USD"` for analyst targets) when the resolved listing trades in a different currency than the primary market.

#### `item.profitability`

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Profitability summary (e.g. `"Good"`) |
| `profitability[]` | array | Metrics (RoE, RoA, RoCE) with `name`, `description`, `assets` and `peers` objects containing TTM/NTM values and scores |
| `profitabilityGraph[]` | array | Margin graphs (Net margin, EBITDA margin) with `name`, `shortDesc`, and `graph[]` containing historical data points |
| `roICWACC` | object | RoIC/WACC analysis with `description` `{short, long}` and `score` |
| `profitabilityPeerMargins[]` | array | Peer margin comparison with `name`, `scoreTTM`, `scoreNTM` |

#### `item.growthMomentum`

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Growth summary (e.g. `"Average"`) |
| `absDescription` | string | Absolute growth description |
| `chgDescription` | string | Growth rate change description |
| `currencySize` | string | Currency for size metrics |
| `growthMomentum[]` | array | Metrics (EPS, Revenue, EBITDA, FCF) with `name`, `graph[]` and `growthRatesGraph[]` |

Each metric's `graph[]` contains `{order, label, value, isPrediction}` data points. The `growthRatesGraph[]` contains the same structure with year-over-year growth rates as decimals.

#### `item.dividend`

| Field | Type | Description |
|-------|------|-------------|
| `description` | object | `{short, long}` — dividend summary |
| `currency` | string | Dividend currency |
| `dividendPaid[]` | array | DPS history `{order, label, isPrediction}` — `value` field present only when dividends are paid |
| `annualDividendPayments[]` | array | Annual payments history `{order, label, isPrediction}` — `value` field present only when dividends are paid |
| `dividendYield[]` | array | Yield history `{order, label, isPrediction}` — `value` field present only when dividends are paid |
| `dividendsLast3Y` | number | Cumulative DPS over last 3 years (0.0 if no dividends) |
| `dividendsLast5Y` | number | Cumulative DPS over last 5 years (0.0 if no dividends) |

> **Note**: For non-dividend-paying stocks, the `dividendPaid`, `annualDividendPayments`, and `dividendYield` arrays contain entries with `order`, `label`, and `isPrediction` but no `value` field.

## Example Request

```bash
curl "https://eodhd.com/api/mp/praams/analyse/equity/isin/US88160R1014?api_token=YOUR_API_TOKEN"
```

### Demo access

```bash
curl "https://eodhd.com/api/mp/praams/analyse/equity/isin/US88160R1014?api_token=demo"
```

## Example Response (abbreviated)

```json
{
  "success": true,
  "message": "",
  "errors": [],
  "item": {
    "asset": {
      "ticker": "TL0.DE",
      "name": "Tesla, Inc.",
      "isin": "US88160R1014",
      "companyDescription": "Tesla, Inc. designs, develops, manufactures...",
      "isActivelyTrading": true,
      "assetId": 30429,
      "ratio": 4,
      "isBond": false,
      "isFinancial": false
    },
    "description": {
      "assetClass": "equity",
      "country": "US",
      "sector": "Consumer Cyclical",
      "currencyId": "EUR",
      "volatility": {
        "short": "Meaningful",
        "long": "In normal market circumstances, TL0.DE is volatile..."
      },
      "solvency": {
        "short": "Limited",
        "long": "The risk of default is minimal..."
      }
    },
    "profile": {
      "companyProfileDescription": {
        "short": "Tesla, Inc. designs, develops, manufactures...",
        "long": "Tesla, Inc. designs, develops, manufactures..."
      },
      "parentNote": "This stock is associated with Tesla, Inc.. The primary listing...is TSLA.",
      "parentAsset": {
        "keyId": 15215,
        "isin": "US88160R1014",
        "assetName": "TSLA",
        "issuerName": "Tesla, Inc.",
        "mainRatio": 3,
        "isBond": false,
        "isETF": false
      }
    },
    "scores": {
      "valuation": 1,
      "performance": 5,
      "profitability": 5,
      "growthMom": 4,
      "other": 1,
      "countryRisk": 1,
      "liquidity": 3,
      "stressTest": 3,
      "volatility": 5,
      "solvency": 3,
      "analystView": 4,
      "dividends": 1
    },
    "keyFactors": {
      "risk": {
        "characteristic": "Limited",
        "factors": [
          {"priority": 1, "text": "Meaningful price volatility", "icon": false}
        ]
      },
      "return": {
        "characteristic": "Modest",
        "factors": [
          {"priority": 1, "text": "Greatly overvalued vs peers", "icon": false}
        ]
      }
    },
    "valuation": {
      "descriptionShort": {
        "short": "Greatly overvalued",
        "long": "Based on key historical and expected multiples..."
      },
      "wams": 1,
      "valuations": [
        {"name": "P/E", "score": 1, "ttm": 254.9, "ntm": 226.2},
        {"name": "EV/EBITDA", "score": 1, "ttm": 101.8}
      ]
    },
    "profitability": {
      "description": "Good",
      "roICWACC": {
        "description": {"short": "average value creation", "long": "..."},
        "score": 1.3
      }
    },
    "dividend": {
      "description": {"short": "Very low or none", "long": "..."},
      "currency": "USD",
      "dividendsLast3Y": 0.0,
      "dividendsLast5Y": 0.0
    }
  }
}
```

## Notes

- **Marketplace product**: Requires a separate PRAAMS marketplace subscription, not included in main EODHD plans.
- **PRAAMS Ratio**: The flagship metric (`item.asset.ratio`) summarizes 470+ metrics into a single 1-10 score. Higher is better.
- **ISIN resolution**: The ISIN may resolve to a non-primary listing (e.g. `US88160R1014` resolves to `TL0.DE` rather than `TSLA`). The `profile.parentAsset` field indicates the primary listing. The `mainRatio` on the parent may differ from the `ratio` on the resolved listing.
- **Demo ISINs**: `US0378331005` (AAPL), `US88160R1014` (TSLA), and `US0231351067` (AMZN) are available with `api_token=demo`.
- **Coverage**: 120,000+ global equities. Use the ticker-based endpoint for direct ticker lookups (see praams-risk-scoring-by-ticker.md).
- **Profile section**: The ISIN endpoint includes an `item.profile` section (with `parentAsset`, `parentNote`, `companyProfileDescription`) that provides cross-listing information. This section may not be present in the ticker-based endpoint.
- **Currency differences**: When the ISIN resolves to a non-US listing, `description.currencyId` and `analystView.currency` may report in the local exchange currency (e.g. `EUR`), while `analystView.analystViewCurrency` and `profitability` metrics report in `USD`.
- **Score scale**: All 12 dimension scores in `item.scores` are integers. For risk dimensions (volatility, stressTest, liquidity, solvency, countryRisk, other), lower scores indicate lower risk. For return dimensions (valuation, performance, profitability, growthMom, analystView, dividends), higher scores indicate better return prospects.
- **Rich text descriptions**: Most sections include `short` (headline) and `long` (detailed paragraph) descriptions suitable for display to end users.
- **Peer comparisons**: Profitability and performance sections include peer benchmark data for the same sector/industry.
- **TTM vs NTM**: Valuation and profitability metrics include both trailing twelve months (TTM) and next twelve months (NTM, consensus estimates). Some multiples may lack NTM values.
- **Non-dividend stocks**: For companies that do not pay dividends, dividend arrays contain entries without `value` fields, and `dividendsLast3Y`/`dividendsLast5Y` are `0.0`.
- **Related endpoint**: Use `/analyse/equity/ticker/{ticker}` for ticker-based lookups (see praams-risk-scoring-by-ticker.md).

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
