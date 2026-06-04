# Fundamentals Data API

Status: complete
Source: financial-apis (Fundamental Data API)
Docs: https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /fundamentals/{SYMBOL}
Method: GET
Auth: api_token (query)

## Purpose
Return comprehensive fundamental data for a company including financial statements,
valuation metrics, earnings history, dividends, and company profile information.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | EODHD API key |
| {SYMBOL} | Yes | string | Symbol with exchange suffix (e.g., AAPL.US) |
| filter | No | string | Sections to return. Comma-separated for multiple top-level sections (e.g. `General,Highlights,Valuation`); use `::` to drill into nested paths (e.g. `Financials::Balance_Sheet::yearly`, `Earnings::Trend::Quarterly`) |
| fmt | No | string | Output format: 'json' or 'csv'. Defaults to 'json' |

## API Versions

Two endpoints are available and return the same top-level sections:

| Version | Path | Notes |
|---------|------|-------|
| **v1.1** (recommended) | `/api/v1.1/fundamentals/{SYMBOL}` | `Earnings.Trend` is split into `Quarterly` and `Annual` sub-objects, each entry adds a human-readable `fiscalQuarter` (Q1–Q4) and a `type` field, and the prior Q4-data-loss bug (quarterly and annual estimates sharing a date) is fixed |
| current/legacy | `/api/fundamentals/{SYMBOL}` | `Earnings.Trend` is a flat object keyed by period date; remains available for backward compatibility |

Both consume 10 API calls and accept the same parameters. The response shape below reflects **v1.1**.

## Response (shape)
Large nested JSON object containing multiple sections:

```json
{
  "General": {
    "Code": "AAPL",
    "Name": "Apple Inc",
    "Exchange": "NASDAQ",
    "CurrencyCode": "USD",
    "Sector": "Technology",
    "Industry": "Consumer Electronics",
    "Description": "...",
    "FullTimeEmployees": 164000,
    "IPODate": "1980-12-12",
    "WebURL": "https://www.apple.com"
  },
  "Highlights": {
    "MarketCapitalization": 2500000000000,
    "EBITDA": 130000000000,
    "PERatio": 28.5,
    "PEGRatio": 2.1,
    "WallStreetTargetPrice": 195.0,
    "BookValue": 4.25,
    "DividendShare": 0.96,
    "DividendYield": 0.005,
    "EarningsShare": 6.15,
    "EPSEstimateCurrentYear": 6.50,
    "EPSEstimateNextYear": 7.20,
    "MostRecentQuarter": "2024-09-30",
    "ProfitMargin": 0.255,
    "OperatingMarginTTM": 0.302,
    "ReturnOnAssetsTTM": 0.215,
    "ReturnOnEquityTTM": 1.475,
    "RevenueTTM": 385000000000,
    "RevenuePerShareTTM": 24.50,
    "QuarterlyRevenueGrowthYOY": 0.08,
    "GrossProfitTTM": 170000000000,
    "DilutedEpsTTM": 6.15
  },
  "Valuation": {
    "TrailingPE": 28.5,
    "ForwardPE": 26.2,
    "PriceSalesTTM": 6.5,
    "PriceBookMRQ": 41.5,
    "EnterpriseValue": 2600000000000,
    "EnterpriseValueRevenue": 6.75,
    "EnterpriseValueEbitda": 20.0
  },
  "SharesStats": {
    "SharesOutstanding": 15700000000,
    "SharesFloat": 15650000000,
    "PercentInsiders": 0.07,
    "PercentInstitutions": 60.5,
    "SharesShort": 120000000,
    "ShortRatio": 1.5,
    "ShortPercentOfFloat": 0.008
  },
  "Technicals": {
    "Beta": 1.25,
    "52WeekHigh": 260.1,
    "52WeekLow": 164.08,
    "50DayMA": 211.5,
    "200DayMA": 222.3,
    "SharesShort": 120000000,
    "ShortRatio": 1.5
  },
  "SplitsDividends": {
    "ForwardAnnualDividendRate": 1.0,
    "ForwardAnnualDividendYield": 0.0043,
    "PayoutRatio": 0.15,
    "DividendDate": "2025-02-13",
    "ExDividendDate": "2025-02-10",
    "LastSplitFactor": "4:1",
    "LastSplitDate": "2020-08-31",
    "NumberDividendsByYear": { "...": "..." }
  },
  "AnalystRatings": {
    "Rating": 4.2,
    "TargetPrice": 250.0,
    "StrongBuy": 12,
    "Buy": 20,
    "Hold": 8,
    "Sell": 1,
    "StrongSell": 0
  },
  "Holders": {
    "Institutions": { "...": "..." },
    "Funds": { "...": "..." }
  },
  "InsiderTransactions": { "...": "..." },
  "ESGScores": {
    "Disclaimer": "...",
    "RatingDate": "2024-12-01",
    "TotalEsg": 16.5,
    "EnvironmentScore": 0.6,
    "SocialScore": 7.4,
    "GovernanceScore": 8.5
  },
  "outstandingShares": { "annual": [], "quarterly": [] },
  "Earnings": {
    "History": { "2024-09-30": { "date": "2024-09-30", "epsActual": 1.64, "epsEstimate": 1.6, "epsDifference": 0.04, "surprisePercent": 2.5 } },
    "Trend": {
      "Quarterly": { "2026-09-30": { "date": "2026-09-30", "period": "+1q", "fiscalQuarter": "Q4", "type": "quarterly", "earningsEstimateAvg": "2.0107", "revenueEstimateAvg": "114207466420.00" } },
      "Annual":    { "2027-09-30": { "date": "2027-09-30", "period": "+1y", "type": "yearly", "earningsEstimateAvg": "9.6552", "revenueEstimateAvg": "517815320250.00" } }
    },
    "Annual": { "2024-09-30": { "date": "2024-09-30", "epsActual": 6.08 } }
  },
  "Financials": {
    "Balance_Sheet": { "quarterly": {}, "yearly": {} },
    "Income_Statement": { "quarterly": {}, "yearly": {} },
    "Cash_Flow": { "quarterly": {}, "yearly": {} }
  }
}
```

## Example request
```bash
# Full fundamentals for AAPL
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json"

# Only highlights and valuation
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&filter=Highlights,Valuation"

# Using the helper client
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US
```

## Notes
- Returns extensive data; use filter parameter to reduce payload size
- Financial statements include quarterly and yearly data going back several years
- Currency is in the company's reporting currency (check CurrencyCode)
- Some fields may be null for companies that don't report certain metrics
- ETFs have different structure focusing on holdings and asset allocation
- Mutual funds have NAV history and expense ratio information
- API call consumption: 10 calls per request regardless of sections filtered

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

### Error Response Format

When an error occurs, the API returns a JSON response with error details:

```json
{
  "error": "Error message description",
  "code": 403
}
```

### Handling Errors

**Python Example**:
```python
import requests

def make_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:
            print("Error: API limit exceeded. Please upgrade your plan.")
        elif e.response.status_code == 403:
            print("Error: Invalid API key. Check your credentials.")
        elif e.response.status_code == 429:
            print("Error: Rate limit exceeded. Please slow down your requests.")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

**Best Practices**:
- Always check status codes before processing response data
- Implement exponential backoff for 429 errors
- Cache responses to reduce API calls
- Monitor your API usage in the user dashboard
