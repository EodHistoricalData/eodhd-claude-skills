# Macro Indicator API

Status: complete
Source: financial-apis (Macroeconomics Data API)
Docs: https://eodhd.com/financial-apis/macroeconomics-data-and-macro-indicators-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /macro-indicator/{COUNTRY}
Method: GET
Auth: api_token (query)

## Purpose
Retrieve macroeconomic indicators for countries including GDP, inflation, unemployment,
interest rates, trade balance, and other economic metrics from sources like the World Bank.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | EODHD API key |
| {COUNTRY} | Yes | string | ISO 3166-1 alpha-3 country code (e.g., USA, GBR, DEU, JPN, CHN) |
| indicator | No | string | Specific indicator code (see list below) |
| fmt | No | string | Output format: 'csv' or 'json' (default csv) |

## Common Indicators
| Code | Description |
|------|-------------|
| gdp_current_usd | GDP (current US$) |
| gdp_growth_annual | GDP growth (annual %) |
| inflation_consumer_prices_annual | Inflation, consumer prices (annual %) |
| unemployment_total_percent | Unemployment, total (% of labor force) |
| real_interest_rate | Real interest rate (%) — EODHD has no nominal policy-rate indicator |
| population_total | Total population |
| population_growth_annual | Population growth (annual %) |
| merchandise_trade_percent_gdp | Merchandise trade (% of GDP) — trade volume, not balance |
| net_trades_goods_services | Trade balance / net exports (absolute USD, not % of GDP) |
| debt_percent_gdp | Central government debt (% of GDP) |

## Response (shape)
Array of time-series data points:

```json
[
  {
    "CountryCode": "USA",
    "CountryName": "United States",
    "Indicator": "gdp_current_usd",
    "Date": "2023-12-31",
    "Period": "2023",
    "Value": 25462700000000
  }
]
```

When no specific indicator is provided, returns all available indicators as an object with arrays per indicator:
```json
{
  "CountryCode": "USA",
  "CountryName": "United States",
  "gdp_current_usd": [
    {"CountryCode": "USA", "Date": "2023-12-31", "Period": "2023", "Value": 25462700000000},
    {"CountryCode": "USA", "Date": "2022-12-31", "Period": "2022", "Value": 25744100000000}
  ],
  "inflation_consumer_prices_annual": [
    {"CountryCode": "USA", "Date": "2023-12-31", "Period": "2023", "Value": 4.1178}
  ]
}
```

## Example request
```bash
# All macro indicators for USA
curl "https://eodhd.com/api/macro-indicator/USA?api_token=demo&fmt=json"

# Specific indicator: GDP growth
curl "https://eodhd.com/api/macro-indicator/USA?api_token=demo&fmt=json&indicator=gdp_growth_annual"

# Inflation for Germany
curl "https://eodhd.com/api/macro-indicator/DEU?api_token=demo&fmt=json&indicator=inflation_consumer_prices_annual"

# Using the helper client
python eodhd_client.py --endpoint macro-indicator --symbol USA --indicator gdp_current_usd
```

## Notes
- **Invalid indicator codes fail silently**: an unrecognized `indicator` value returns plain text
  `Indicator or Country are Not Found.` (not JSON), and a bare call without `indicator` returns only the
  GDP series — so a wrong code can look like "GDP came back instead". Only use codes from the table above;
  they are verified against the live API. Common traps: `interest_rate` (use `real_interest_rate`),
  `trade_balance_percent_gdp`/`trade_percent_gdp` (use `net_trades_goods_services` or
  `merchandise_trade_percent_gdp`), `government_debt_percent_gdp` (use `debt_percent_gdp`).
- Country codes use ISO 3166-1 alpha-3 format (USA, GBR, DEU, JPN, CHN, etc.)
- Data is typically annual, with varying historical depth by indicator
- Some indicators may have gaps or missing years
- Values are in the units specified by the indicator (%, USD, count, etc.)
- Data sourced from World Bank and other official sources
- API call consumption: 1 call per request
- **Helper client normalization**: the raw API returns PascalCase keys (`Date`, `Value`, `CountryCode`,
  `CountryName`, `Indicator`, `Period`). `eodhd_client.py` recursively lowercases all keys (→ `date`,
  `value`, `countrycode`, ...) so they match every other endpoint and `d.get("date")`/`d.get("value")`
  work. Pass `--raw` to see the original PascalCase keys.
- **Data sources**: EODHD uses more than 5 sources for macroeconomic data and compiles it internally. The primary source is the [World Bank](https://www.worldbank.org/en/home), supplemented by government news and publications.
- **Fertility indicator**: The `fertility_rate` indicator represents the **birth rate** (total fertility rate per woman).

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
