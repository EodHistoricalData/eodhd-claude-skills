# Praams Smart Investment Screener Bond API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/financial-apis/equity-risk-return-scoring-api
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/explore/bond`
Method: POST
Auth: `api_token` query parameter

## Purpose

Returns a filtered, paginated list of bonds matching user-defined criteria
across 12 risk-return dimensions, geography, sector, currency, yield, and
duration. This is a smart screener covering 120,000+ instruments including
corporate and sovereign bonds from US, UK, Europe, China, India, Middle East,
Asia & Oceania, LatAm, and Africa (both OTC and exchange-traded).

Users can find trade ideas like "bonds of European banks with high yields
with good growth loved by market analysts" in several seconds.

**Use cases**:
- Screen bonds by any combination of 12 risk-return scoring dimensions (1-7 scale)
- Filter by PRAAMS Ratio (mainRatio) for quick risk-return quality screening
- Filter by region, country, sector, and industry
- Filter by currency (ISO Alpha-3 codes)
- Filter by yield range and duration range
- Exclude subordinated bonds or perpetuals
- Paginate through large result sets with `skip`/`take`
- Sort results by any field using `orderBy`
- Build custom bond screening tools and watchlists

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

## Parameters

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key |

### Query (optional — pagination)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | integer | 0 | Number of records to skip |
| `take` | integer | — | Number of records to retrieve |

### Request Body (JSON) — Scoring Filters

All scoring filters use a 1-7 integer scale. Provide `*Min` and/or `*Max` to define a range. All are optional and nullable.

#### PRAAMS Ratio

| Field | Type | Description |
|-------|------|-------------|
| `mainRatioMin` | integer \| null | Minimum PRAAMS Ratio (1-7) |
| `mainRatioMax` | integer \| null | Maximum PRAAMS Ratio (1-7) |

#### Return factors (1-7)

| Field | Type | Description |
|-------|------|-------------|
| `valuationMin` / `valuationMax` | integer \| null | Valuation score range |
| `performanceMin` / `performanceMax` | integer \| null | Performance score range |
| `profitabilityMin` / `profitabilityMax` | integer \| null | Profitability score range |
| `growthMomMin` / `growthMomMax` | integer \| null | Growth momentum score range |
| `marketViewMin` / `marketViewMax` | integer \| null | Market view score range (bond-specific, replaces analystView) |
| `couponsMin` / `couponsMax` | integer \| null | Coupon score range (bond-specific, replaces dividends) |
| `analystViewMin` / `analystViewMax` | integer \| null | Analyst view score range |
| `dividendsMin` / `dividendsMax` | integer \| null | Dividends score range |

#### Risk factors (1-7)

| Field | Type | Description |
|-------|------|-------------|
| `otherMin` / `otherMax` | integer \| null | Other risks score range |
| `countryRiskMin` / `countryRiskMax` | integer \| null | Country risk score range |
| `liquidityMin` / `liquidityMax` | integer \| null | Liquidity risk score range |
| `stressTestMin` / `stressTestMax` | integer \| null | Stress test score range |
| `volatilityMin` / `volatilityMax` | integer \| null | Volatility score range |
| `solvencyMin` / `solvencyMax` | integer \| null | Solvency/default risk score range |

### Request Body (JSON) — Classification Filters

| Field | Type | Description |
|-------|------|-------------|
| `regions` | array of integers \| null | Region IDs (see Reference Tables below) |
| `countries` | array of integers \| null | Country IDs (see Reference Tables below) |
| `sectors` | array of integers \| null | Sector IDs (see Reference Tables below) |
| `industries` | array of integers \| null | Industry IDs (see Reference Tables below) |
| `capitalisation` | array of integers \| null | Market cap categories: `1`=Small, `2`=Mid, `3`=Large |
| `currency` | array of strings \| null | ISO Alpha-3 currency codes (e.g. `["EUR", "USD"]`) |

### Request Body (JSON) — Bond-Specific Filters

| Field | Type | Description |
|-------|------|-------------|
| `yieldMin` | integer \| null | Minimum yield filter |
| `yieldMax` | integer \| null | Maximum yield filter |
| `durationMin` | integer \| null | Minimum duration filter |
| `durationMax` | integer \| null | Maximum duration filter |
| `excludeSubordinated` | boolean \| null | Exclude subordinated bonds |
| `excludePerpetuals` | boolean \| null | Exclude perpetual bonds |

### Request Body (JSON) — Sorting

| Field | Type | Description |
|-------|------|-------------|
| `orderBy` | string \| null | Field name to sort results by |

## Response (shape)

JSON object with top-level envelope:

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` if request succeeded |
| `message` | string | Status message (empty on success) |
| `errors` | array | Error objects (empty on success) |
| `item` | object | The main data payload |

### `item` object

| Field | Type | Description |
|-------|------|-------------|
| `peers` | array | Array of matching bond records |
| `totalCount` | integer | Total number of matching bonds (for pagination) |

### `item.peers[]` record

Each peer record contains:

#### `assetInfo` object

| Field | Type | Description |
|-------|------|-------------|
| `assetId` | integer | Internal PRAAMS asset ID |
| `ratio` | integer | PRAAMS Ratio (1-10 scale) |
| `watchList` | boolean | Watchlist flag |
| `isBond` | boolean | Always `true` for bond screener |
| `bondType` | string | Bond classification (e.g. `"Corporate"`) |
| `isFinancial` | boolean | Whether the issuer is in the financial sector |
| `ticker` | string | Bond description (e.g. `"ACA.PA 1.3% 08-Feb-27"`) |
| `name` | string | Issuer name |
| `isin` | string | ISIN identifier |
| `companyDescription` | string | Issuer description (may be empty) |
| `isActivelyTrading` | boolean | Whether the bond is currently trading |

#### Scoring fields (top-level in peer record)

| Field | Type | Description |
|-------|------|-------------|
| `riskWatch` | string | Overall risk characterization (e.g. `"Limited"`) |
| `returnWatch` | string | Overall return characterization (e.g. `"Strong"`) |
| `amountOutstanding` | integer | Amount outstanding category |
| `marketView` | integer | Market view score (bond-specific) |
| `coupon` | integer | Coupon score (bond-specific) |
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

## Example Request

```bash
curl -X POST \
  'https://eodhd.com/api/mp/praams/explore/bond?skip=0&take=3&api_token=YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "growthMomMin": 4,
    "growthMomMax": 7,
    "regions": [3],
    "sectors": [6],
    "currency": ["EUR"],
    "marketViewMin": 4,
    "marketViewMax": 7,
    "yieldMin": 7,
    "yieldMax": 15
  }'
```

## Example Response

```json
{
  "success": true,
  "message": "",
  "errors": [],
  "item": {
    "peers": [
      {
        "assetInfo": {
          "assetId": 292529,
          "ratio": 6,
          "watchList": false,
          "isBond": true,
          "bondType": "Corporate",
          "isFinancial": false,
          "ticker": "ACA.PA 1.3% 08-Feb-27",
          "name": "Credit Agricole S.A.",
          "isin": "FR0013229259",
          "companyDescription": "",
          "isActivelyTrading": true
        },
        "riskWatch": "Limited",
        "returnWatch": "Strong",
        "amountOutstanding": 1,
        "marketView": 7,
        "coupon": 4,
        "valuation": 7,
        "performance": 2,
        "profitability": 3,
        "growthMom": 5,
        "other": 1,
        "countryRisk": 1,
        "liquidity": 5,
        "stressTest": 1,
        "volatility": 1,
        "solvency": 4
      }
    ],
    "totalCount": 9
  }
}
```

## Reference Tables

### Regions

| Code | Description |
|------|-------------|
| 1 | Other |
| 2 | North America |
| 3 | Europe |
| 4 | EMEA |
| 5 | Asia & Oceania |
| 6 | LATAM |
| 7 | Africa |
| 8 | Middle East |

### Sectors

| Code | Description |
|------|-------------|
| -1 | ETF multi-sector |
| 2 | Communication Services |
| 3 | Consumer Cyclical |
| 4 | Consumer Defensive |
| 5 | Energy |
| 6 | Financial Services |
| 7 | Healthcare |
| 8 | Industrials |
| 9 | Real Estate |
| 10 | Technology |
| 11 | Utilities |
| 12 | Basic Materials |
| 13 | Sovereign / Supranat. |

### Industries

| Code | Description |
|------|-------------|
| 2 | Aerospace & defence |
| 3 | Apparel |
| 4 | Auto |
| 5 | Banks & credit |
| 6 | Building materials |
| 7 | Capital markets |
| 8 | Chemicals |
| 9 | Consumer other |
| 10 | Engineering |
| 11 | Financials other |
| 12 | Food & beverage |
| 13 | Hardware & eqpmnt |
| 14 | Healthcare other |
| 15 | HoReCa |
| 16 | Industrials other |
| 17 | Insurance |
| 18 | Luxury & leisure |
| 19 | Media |
| 20 | Metals industrial |
| 21 | Metals precious |
| 22 | Mining |
| 23 | Oil & gas downstrm |
| 24 | Oil & gas eqpmnt |
| 25 | Oil & gas upstrm |
| 26 | Paper & packaging |
| 27 | Pharma & biotech |
| 28 | Real estate other |
| 29 | REITs |
| 30 | Retail |
| 31 | Semiconductors |
| 32 | Software & services |
| 33 | Telecoms & services |
| 34 | Transport |
| 35 | Utilities all |

### Capitalisation

| Code | Description |
|------|-------------|
| 1 | Small |
| 2 | Mid |
| 3 | Large |

### Countries

See the full list of 100+ country codes in the API documentation. Common examples:

| Code | Country |
|------|---------|
| 20 | US |
| 4 | UK |
| 30 | Germany |
| 31 | France |
| 28 | Italy |
| 25 | Spain |
| 38 | Japan |
| 23 | China |
| 37 | India |
| 14 | Canada |
| 10 | Australia |

## Notes

- **Marketplace product**: Requires a separate PRAAMS Smart Investment Screener marketplace subscription, not included in main EODHD plans.
- **POST method**: Unlike most EODHD endpoints, this is a POST endpoint with a JSON request body for filters. The `api_token` is still passed as a query parameter.
- **At least one filter required**: The request body must contain at least one filter (regions, sectors, currency, or any `*Min`/`*Max` scoring field).
- **Scoring scale**: All `*Min`/`*Max` scoring filters use a 1-7 integer scale. For risk dimensions, lower = less risky. For return dimensions, higher = better.
- **Bond-specific fields**: The bond screener includes `marketView` (instead of `analystView`), `coupon` (instead of `dividends`), `amountOutstanding`, `bondType`, and bond-specific filters (`yieldMin`/`yieldMax`, `durationMin`/`durationMax`, `excludeSubordinated`, `excludePerpetuals`).
- **Pagination**: Use `skip` and `take` query parameters. The response `totalCount` tells you how many total matches exist.
- **Coverage**: Corporate and sovereign bonds from US, UK, Europe, China, India, Middle East, Asia & Oceania, LatAm, and Africa — both OTC and exchange-traded.
- **Currency filter**: Uses ISO Alpha-3 currency codes (e.g. `"EUR"`, `"USD"`, `"GBP"`).
- **Related endpoint**: Use `/explore/equity` for equity screening (see praams-smart-investment-screener-equity.md).

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **415** | Unsupported Media Type | Wrong content type (must be `application/json`). |
| **420** | Operation Cancelled | Request was cancelled. |
| **430** | Data Not Found | No data found for the given filters. |

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

def make_api_request(url, params, json_body):
    try:
        response = requests.post(url, params=params, json=json_body)
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
            print("Error: Content-Type must be application/json.")
        elif e.response.status_code == 430:
            print("Error: No data found for the given filters.")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

**Best Practices**:
- Always check `success` field in the response before processing `item`
- Use `totalCount` for pagination logic
- Implement exponential backoff for rate limit errors
- Start with broad filters, then narrow down to find specific trade ideas
- Monitor your API usage in the user dashboard
