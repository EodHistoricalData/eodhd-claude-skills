# Praams Smart Investment Screener Equity API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/financial-apis/equity-risk-return-scoring-api
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/explore/equity`
Method: POST
Auth: `api_token` query parameter

## Purpose

Returns a filtered, paginated list of equities matching user-defined criteria
across 12 risk-return dimensions, geography, sector, currency, and market
capitalization. This is a smart screener covering 120,000+ instruments
including stocks from US, UK, Europe, China, India, Middle East, Asia & Oceania,
LatAm, and Africa (including small & micro-caps).

Users can find trade ideas like "undervalued Chinese IT stocks with high
dividends and low credit risk" in several seconds.

**Use cases**:
- Screen equities by any combination of 12 risk-return scoring dimensions (1-7 scale)
- Filter by PRAAMS Ratio (mainRatio) for quick risk-return quality screening
- Filter by region, country, sector, and industry
- Filter by market capitalization (small, mid, large)
- Filter by currency (ISO Alpha-3 codes)
- Paginate through large result sets with `skip`/`take`
- Sort results by any field using `orderBy`
- Build custom equity screening tools and watchlists

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
| `currency` | array of strings \| null | ISO Alpha-3 currency codes (e.g. `["USD", "CNY"]`) |

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
| `peers` | array | Array of matching equity records |
| `totalCount` | integer | Total number of matching equities (for pagination) |

### `item.peers[]` record

Each peer record contains:

#### `assetInfo` object

| Field | Type | Description |
|-------|------|-------------|
| `assetId` | integer | Internal PRAAMS asset ID |
| `ratio` | integer | PRAAMS Ratio (1-10 scale) |
| `watchList` | boolean | Watchlist flag |
| `isBond` | boolean | Always `false` for equity screener |
| `isFinancial` | boolean | Whether the company is in the financial sector |
| `ticker` | string | Ticker symbol (e.g. `"688618.SS"`, `"AACAF"`) |
| `name` | string | Company name |
| `isin` | string | ISIN identifier |
| `companyDescription` | string | Company description (may be empty) |
| `isActivelyTrading` | boolean | Whether the stock is currently trading |

#### Scoring fields (top-level in peer record)

| Field | Type | Description |
|-------|------|-------------|
| `riskWatch` | string | Overall risk characterization (e.g. `"High"`, `"Moderate"`) |
| `returnWatch` | string | Overall return characterization (e.g. `"Average"`, `"Favourable"`) |
| `marketCap` | integer | Market cap category (1=Small, 2=Mid, 3=Large) |
| `analystView` | integer | Analyst view score (0 = no data) |
| `dividends` | integer | Dividends score |
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

## Example Request

```bash
curl -X POST \
  'https://eodhd.com/api/mp/praams/explore/equity?skip=0&take=3&api_token=YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "solvencyMin": 1,
    "solvencyMax": 4,
    "countries": [23],
    "sectors": [10],
    "dividendsMin": 4,
    "dividendsMax": 7
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
          "assetId": 82825,
          "ratio": 3,
          "watchList": false,
          "isBond": false,
          "isFinancial": false,
          "ticker": "688618.SS",
          "name": "3onedata Co., Ltd.",
          "isin": "CNE1000077R2",
          "companyDescription": "",
          "isActivelyTrading": true
        },
        "riskWatch": "High",
        "returnWatch": "Average",
        "marketCap": 1,
        "analystView": 0,
        "dividends": 4,
        "valuation": 3,
        "performance": 6,
        "profitability": 5,
        "growthMom": 2,
        "other": 1,
        "countryRisk": 2,
        "liquidity": 3,
        "stressTest": 7,
        "volatility": 7,
        "solvency": 4
      },
      {
        "assetInfo": {
          "assetId": 99345,
          "ratio": 3,
          "watchList": false,
          "isBond": false,
          "isFinancial": false,
          "ticker": "AACAF",
          "name": "AAC Technologies Holdings Inc.",
          "isin": "KYG2953R1149",
          "companyDescription": "",
          "isActivelyTrading": true
        },
        "riskWatch": "High",
        "returnWatch": "Favourable",
        "marketCap": 1,
        "analystView": 6,
        "dividends": 4,
        "valuation": 5,
        "performance": 4,
        "profitability": 3,
        "growthMom": 4,
        "other": 1,
        "countryRisk": 2,
        "liquidity": 6,
        "stressTest": 7,
        "volatility": 7,
        "solvency": 4
      }
    ],
    "totalCount": 71
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
| 9 | Korea |
| 16 | Hong Kong |
| 3 | Taiwan |

## Notes

- **Marketplace product**: Requires a separate PRAAMS Smart Investment Screener marketplace subscription, not included in main EODHD plans.
- **POST method**: Unlike most EODHD endpoints, this is a POST endpoint with a JSON request body for filters. The `api_token` is still passed as a query parameter.
- **At least one filter required**: The request body must contain at least one filter (countries, sectors, currency, or any `*Min`/`*Max` scoring field).
- **Scoring scale**: All `*Min`/`*Max` scoring filters use a 1-7 integer scale. For risk dimensions, lower = less risky. For return dimensions, higher = better.
- **Equity-specific fields**: The equity screener uses `analystView` (instead of `marketView`), `dividends` (instead of `coupon`), and `marketCap` (instead of `amountOutstanding`). It does not have bond-specific filters like yield, duration, excludeSubordinated, or excludePerpetuals.
- **Score of 0**: A score of `0` in the response (e.g. `analystView: 0`) indicates insufficient data for that dimension.
- **Pagination**: Use `skip` and `take` query parameters. The response `totalCount` tells you how many total matches exist. For example, with `totalCount: 71`, you can page through with `skip=0&take=20`, `skip=20&take=20`, etc.
- **Coverage**: Stocks from US, UK, Europe, China, India, Middle East, Asia & Oceania, LatAm, and Africa, including small & micro-caps.
- **Currency filter**: Uses ISO Alpha-3 currency codes (e.g. `"USD"`, `"EUR"`, `"CNY"`).
- **Related endpoint**: Use `/explore/bond` for bond screening (see praams-smart-investment-screener-bond.md).

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
