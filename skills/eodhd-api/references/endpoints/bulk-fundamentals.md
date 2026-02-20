# Bulk Fundamentals API

Status: complete
Source: financial-apis (Fundamentals API)
Docs: https://eodhd.com/financial-apis/bulk-fundamentals-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /bulk-fundamentals/{EXCHANGE}
Method: GET
Auth: api_token (query)

## Purpose

Download fundamental data for hundreds of companies in a single request. Returns General info, Highlights, Valuation, Technicals, Splits/Dividends, Earnings (last 4 quarters), and full Financials (Balance Sheet, Cash Flow, Income Statement) with last 4 quarters and last 4 years of history. Available only via the Extended Fundamentals subscription plan (contact support@eodhistoricaldata.com).

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API access token |
| {EXCHANGE} | Yes | path | Exchange code (e.g., NASDAQ, NYSE, US, LSE). US exchanges can be addressed separately: NASDAQ, NYSE, BATS, AMEX |
| symbols | No | string | Comma-separated list of specific symbols (e.g., AAPL.US,MSFT.US). When specified, the exchange code in the path is ignored |
| offset | No | integer | Starting symbol position for pagination (default: 0) |
| limit | No | integer | Number of symbols to return (default: 500, max: 500) |
| fmt | No | string | Response format: json (recommended) or csv (default) |
| version | No | string | Set to "1.2" for output closer to the single-symbol Fundamentals API template (includes Earnings Trends). JSON only |

## Response (shape)

```json
{
  "0": {
    "General": {
      "Code": "AAPL",
      "Type": "Common Stock",
      "Name": "Apple Inc",
      "Exchange": "NASDAQ",
      "CurrencyCode": "USD",
      "CountryName": "USA",
      "CountryISO": "US",
      "ISIN": "US0378331005",
      "PrimaryTicker": "AAPL.US",
      "CUSIP": "037833100",
      "Sector": "Technology",
      "Industry": "Consumer Electronics",
      "Description": "Apple Inc. designs, manufactures...",
      "FullTimeEmployees": 150000,
      "UpdatedAt": "2026-02-15"
    },
    "Highlights": {
      "MarketCapitalization": 3759435415552,
      "MarketCapitalizationMln": 3759435.4156,
      "EBITDA": 152901992448,
      "PERatio": 32.3772,
      "PEGRatio": 2.3096,
      "WallStreetTargetPrice": 292.1462,
      "BookValue": 5.998,
      "DividendShare": 1.03,
      "DividendYield": 0.0039,
      "EarningsShare": 7.9,
      "EPSEstimateCurrentYear": 8.4911,
      "EPSEstimateNextYear": 9.313,
      "MostRecentQuarter": "2025-12-31",
      "ProfitMargin": 0.2704,
      "OperatingMarginTTM": 0.3537,
      "ReturnOnAssetsTTM": 0.2438,
      "ReturnOnEquityTTM": 1.5202,
      "RevenueTTM": 435617005568,
      "DilutedEpsTTM": 7.9,
      "QuarterlyEarningsGrowthYOY": 0.183
    },
    "Valuation": {
      "TrailingPE": 32.3772,
      "ForwardPE": 30.2115,
      "PriceSalesTTM": 8.6301,
      "PriceBookMRQ": 42.5801,
      "EnterpriseValueRevenue": 8.6745,
      "EnterpriseValueEbitda": 24.7135
    },
    "Technicals": {
      "Beta": 1.107,
      "52WeekHigh": 288.3502,
      "52WeekLow": 168.4757,
      "50DayMA": 267.4752,
      "200DayMA": 240.0591,
      "SharesShort": 116854414,
      "ShortRatio": 2.36,
      "ShortPercent": 0.008
    },
    "SplitsDividends": {
      "ForwardAnnualDividendRate": 1.04,
      "ForwardAnnualDividendYield": 0.0041,
      "PayoutRatio": 0.1315,
      "DividendDate": "2026-02-12",
      "ExDividendDate": "2026-02-09",
      "LastSplitFactor": "4:1",
      "LastSplitDate": "2020-08-31"
    },
    "Earnings": {
      "Last_0": {
        "reportDate": "2026-01-29",
        "date": "2025-12-31",
        "epsActual": 2.84,
        "epsEstimate": 2.67,
        "epsDifference": 0.17,
        "surprisePercent": 6.367
      },
      "Last_1": { "..." : "..." },
      "Last_2": { "..." : "..." },
      "Last_3": { "..." : "..." }
    },
    "Financials": {
      "Balance_Sheet": {
        "currency_symbol": "USD",
        "quarterly_last_0": { "date": "2025-12-31", "totalAssets": "379297000000.00", "..." : "..." },
        "quarterly_last_1": { "..." : "..." },
        "quarterly_last_2": { "..." : "..." },
        "quarterly_last_3": { "..." : "..." },
        "yearly_last_0": { "..." : "..." },
        "yearly_last_1": { "..." : "..." },
        "yearly_last_2": { "..." : "..." },
        "yearly_last_3": { "..." : "..." }
      },
      "Cash_Flow": { "..." : "..." },
      "Income_Statement": { "..." : "..." }
    }
  },
  "1": { "..." : "..." }
}
```

### Output Format

The response is a JSON object keyed by numeric index ("0", "1", ...). Each entry contains the following sections:

**General fields:**

| Field | Type | Description |
|-------|------|-------------|
| Code | string | Ticker symbol |
| Type | string | Instrument type (e.g., Common Stock) |
| Name | string | Company name |
| Exchange | string | Exchange name |
| CurrencyCode | string | Trading currency (ISO alpha-3) |
| CountryName | string | Country name |
| CountryISO | string | Country ISO code |
| OpenFigi | string | OpenFIGI identifier |
| ISIN | string | International Securities Identification Number |
| LEI | string | Legal Entity Identifier |
| PrimaryTicker | string | Primary ticker in EODHD format |
| CUSIP | string | CUSIP identifier |
| Sector | string | Company sector |
| Industry | string | Company industry |
| Description | string | Company description |
| FullTimeEmployees | integer | Number of full-time employees |
| UpdatedAt | string (YYYY-MM-DD) | Last update date |

**Highlights fields:**

| Field | Type | Description |
|-------|------|-------------|
| MarketCapitalization | integer | Market cap in currency units |
| MarketCapitalizationMln | float | Market cap in millions |
| EBITDA | integer | EBITDA |
| PERatio | float | Price-to-earnings ratio |
| PEGRatio | float | Price/earnings-to-growth ratio |
| WallStreetTargetPrice | float | Analyst consensus target price |
| BookValue | float | Book value per share |
| DividendShare | float | Dividend per share |
| DividendYield | float | Dividend yield (decimal) |
| EarningsShare | float | Earnings per share (TTM) |
| EPSEstimateCurrentYear | float | EPS estimate for current fiscal year |
| EPSEstimateNextYear | float | EPS estimate for next fiscal year |
| EPSEstimateNextQuarter | float | EPS estimate for next quarter |
| MostRecentQuarter | string (YYYY-MM-DD) | Most recent quarter end date |
| ProfitMargin | float | Net profit margin (decimal) |
| OperatingMarginTTM | float | Operating margin TTM (decimal) |
| ReturnOnAssetsTTM | float | Return on assets TTM (decimal) |
| ReturnOnEquityTTM | float | Return on equity TTM (decimal) |
| RevenueTTM | integer | Revenue TTM |
| RevenuePerShareTTM | float | Revenue per share TTM |
| QuarterlyRevenueGrowthYOY | float | Quarterly revenue growth YoY (decimal) |
| GrossProfitTTM | integer | Gross profit TTM |
| DilutedEpsTTM | float | Diluted EPS TTM |
| QuarterlyEarningsGrowthYOY | float | Quarterly earnings growth YoY (decimal) |

**Valuation fields:**

| Field | Type | Description |
|-------|------|-------------|
| TrailingPE | float | Trailing P/E ratio |
| ForwardPE | float | Forward P/E ratio |
| PriceSalesTTM | float | Price-to-sales TTM |
| PriceBookMRQ | float | Price-to-book MRQ |
| EnterpriseValueRevenue | float | EV/Revenue |
| EnterpriseValueEbitda | float | EV/EBITDA |

**Technicals fields:**

| Field | Type | Description |
|-------|------|-------------|
| Beta | float | Beta coefficient |
| 52WeekHigh | float | 52-week high price |
| 52WeekLow | float | 52-week low price |
| 50DayMA | float | 50-day moving average |
| 200DayMA | float | 200-day moving average |
| SharesShort | integer | Shares sold short |
| SharesShortPriorMonth | integer | Shares short prior month |
| ShortRatio | float | Short ratio (days to cover) |
| ShortPercent | float | Short interest as percent of float |

**Earnings fields (Last_0 through Last_3):**

| Field | Type | Description |
|-------|------|-------------|
| reportDate | string (YYYY-MM-DD) | Earnings report date |
| date | string (YYYY-MM-DD) | Quarter end date |
| epsActual | float | Actual EPS |
| epsEstimate | float | Estimated EPS |
| epsDifference | float | EPS surprise (actual - estimate) |
| surprisePercent | float | Surprise percentage |

**Financials (Balance_Sheet, Cash_Flow, Income_Statement):**

Each section contains `quarterly_last_0` through `quarterly_last_3` and `yearly_last_0` through `yearly_last_3`. Fields match the standard Fundamentals API with values as stringified numbers.

## Example Requests

```bash
# All NASDAQ stocks (first 500)
curl "https://eodhd.com/api/bulk-fundamentals/NASDAQ?api_token=YOUR_TOKEN&fmt=json"

# Specific symbols (exchange code in path is ignored)
curl "https://eodhd.com/api/bulk-fundamentals/NASDAQ?symbols=AAPL.US,MSFT.US&api_token=YOUR_TOKEN&fmt=json"

# Paginated: 100 symbols starting from position 500
curl "https://eodhd.com/api/bulk-fundamentals/NASDAQ?offset=500&limit=100&api_token=YOUR_TOKEN&fmt=json"

# Version 1.2 output (closer to single-symbol fundamentals template)
curl "https://eodhd.com/api/bulk-fundamentals/NASDAQ?symbols=AAPL.US&version=1.2&api_token=YOUR_TOKEN&fmt=json"

# Using the helper client (exchange-based)
python eodhd_client.py --endpoint bulk-fundamentals --symbol NASDAQ --limit 100

# Using the helper client (specific symbols via --symbols)
python eodhd_client.py --endpoint bulk-fundamentals --symbol NASDAQ --symbols AAPL.US,MSFT.US
```

## Notes

- **Plan requirement**: Requires the Extended Fundamentals subscription plan (contact support@eodhistoricaldata.com)
- **API call cost**: 100 API calls per request. When `symbols` parameter is used, cost is 100 + number of symbols (e.g., 3 symbols = 103 calls)
- **Stocks only**: ETFs and Mutual Funds are not supported
- **Pagination**: Default offset=0, limit=500. Maximum limit is 500 (values above are reset to 500)
- **US exchanges**: NASDAQ, NYSE (or NYSE MKT), BATS, AMEX can be addressed separately in addition to the general "US" code
- **Default format**: CSV. Always add `fmt=json` for JSON output (strongly recommended)
- **Historical data**: Limited to last 4 quarters and last 4 years
- **Version 1.2**: Add `version=1.2` for output closer to single-symbol Fundamentals API (includes Earnings Trends). JSON only
- **When `symbols` is specified**: The exchange code in the path is ignored
- The response is an object keyed by numeric index ("0", "1", ...), not an array

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
- Use `fmt=json` for all requests
- Use `symbols` parameter to minimize API call cost when you need specific companies
- Paginate large exchanges with `offset` and `limit` to manage response size
