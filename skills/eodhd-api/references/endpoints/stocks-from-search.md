# Stocks From Search API

Status: complete
Source: financial-apis
Docs: https://eodhd.com/financial-apis/search-api-for-stocks-etfs-mutual-funds-bonds-and-indices
Provider: EODHD
Base URL: `https://eodhd.com/api`
Path: `/search/{query_string}`
Method: GET
Auth: `api_token` query parameter

## Purpose

Searches for financial instruments by ticker symbol, company name, or ISIN.
Returns a list of matching assets including stocks, ETFs, mutual funds, bonds,
and indices across all supported exchanges.

The search engine automatically adjusts behavior based on the input string and
considers asset popularity using metrics like market capitalization and trading
volume. Results can be filtered by asset type or exchange.

**Use cases**:
- Look up assets by ticker code (e.g. `AAPL`)
- Search by company name (e.g. `Apple Inc`)
- Resolve an ISIN to all exchange listings (e.g. `US0378331005`)
- Build autocomplete/typeahead for asset selection UIs
- Filter search results by asset type (stock, etf, fund, bond, index, crypto)
- Filter search results by exchange code (US, XETRA, LSE, etc.)
- Find all cross-listed instances of a security across exchanges

## Plans & API Calls

Available in: **All-In-One**, **EOD Historical Data — All World**, **EOD+Intraday — All World Extended**, **Fundamentals Data Feed**, and **Free** plans.

| Limit | Value |
|-------|-------|
| API calls per request | 1 |

> The demo API key does **not** work for the Search API. You must register to get a free API token.

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `query_string` | string | The search input. Can be a ticker symbol, company name, or ISIN (e.g. `AAPL`, `Apple Inc`, `US0378331005`) |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key |
| `fmt` | string | Response format. Use `json` |

### Query (optional)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 15 | Maximum number of results to return (max 500) |
| `bonds_only` | integer | 0 | Set to `1` to include only bonds in the results |
| `exchange` | string | — | Filter results by exchange code (e.g. `US`, `PA`, `FOREX`, `NYSE`, `NASDAQ`) |
| `type` | string | — | Filter by asset type: `all`, `stock`, `etf`, `fund`, `bond`, `index`, `crypto` |

## Response (shape)

JSON array of matching instrument objects:

### Instrument object

| Field | Type | Description |
|-------|------|-------------|
| `Code` | string | Ticker symbol of the asset (e.g. `"AAPL"`, `"APC"`, `"0R2V"`) |
| `Exchange` | string | Exchange code where the asset is listed (e.g. `"US"`, `"XETRA"`, `"LSE"`) |
| `Name` | string | Full name of the instrument (e.g. `"Apple Inc"`) |
| `Type` | string | Type of asset (e.g. `"Common Stock"`, `"ETF"`, `"Fund"`, `"Bond"`) |
| `Country` | string | Country of the exchange (e.g. `"USA"`, `"Germany"`, `"UK"`) |
| `Currency` | string | Currency in which the asset is traded (e.g. `"USD"`, `"EUR"`, `"CAD"`) |
| `ISIN` | string \| null | ISIN code if available, `null` otherwise |
| `previousClose` | number | Previous closing price |
| `previousCloseDate` | string | Date of the previous close price (e.g. `"2026-02-13"`) |
| `isPrimary` | boolean | `true` if this is the primary exchange for the asset |

## Example Requests

Search by ticker code:
```bash
curl "https://eodhd.com/api/search/AAPL?api_token=YOUR_API_TOKEN&fmt=json"
```

Search by company name:
```bash
curl "https://eodhd.com/api/search/Apple%20Inc?api_token=YOUR_API_TOKEN&fmt=json"
```

Search by ISIN:
```bash
curl "https://eodhd.com/api/search/US0378331005?api_token=YOUR_API_TOKEN&fmt=json"
```

Search with a limit of 1 result:
```bash
curl "https://eodhd.com/api/search/Apple%20Inc?limit=1&api_token=YOUR_API_TOKEN&fmt=json"
```

Search for bonds only:
```bash
curl "https://eodhd.com/api/search/AAPL?bonds_only=1&api_token=YOUR_API_TOKEN&fmt=json"
```

Filter by exchange:
```bash
curl "https://eodhd.com/api/search/AAPL?exchange=US&api_token=YOUR_API_TOKEN&fmt=json"
```

Filter by asset type:
```bash
curl "https://eodhd.com/api/search/AAPL?type=stock&api_token=YOUR_API_TOKEN&fmt=json"
```

## Example Response

```json
[
  {
    "Code": "AAPL",
    "Exchange": "US",
    "Name": "Apple Inc",
    "Type": "Common Stock",
    "Country": "USA",
    "Currency": "USD",
    "ISIN": "US0378331005",
    "previousClose": 255.78,
    "previousCloseDate": "2026-02-13",
    "isPrimary": true
  },
  {
    "Code": "AAPL",
    "Exchange": "BA",
    "Name": "Apple Inc DRC",
    "Type": "Common Stock",
    "Country": "Argentina",
    "Currency": "ARS",
    "ISIN": "US0378331005",
    "previousClose": 19010,
    "previousCloseDate": "2026-02-13",
    "isPrimary": false
  },
  {
    "Code": "0R2V",
    "Exchange": "LSE",
    "Name": "Apple Inc.",
    "Type": "Common Stock",
    "Country": "UK",
    "Currency": "USD",
    "ISIN": "US0378331005",
    "previousClose": 258.832,
    "previousCloseDate": "2026-02-13",
    "isPrimary": false
  },
  {
    "Code": "APC",
    "Exchange": "XETRA",
    "Name": "Apple Inc",
    "Type": "Common Stock",
    "Country": "Germany",
    "Currency": "EUR",
    "ISIN": "US0378331005",
    "previousClose": 218.3,
    "previousCloseDate": "2026-02-13",
    "isPrimary": false
  },
  {
    "Code": "AAPL",
    "Exchange": "NEO",
    "Name": "Apple Inc CDR",
    "Type": "Common Stock",
    "Country": "Canada",
    "Currency": "CAD",
    "ISIN": "US0378331005",
    "previousClose": 36.53,
    "previousCloseDate": "2026-02-13",
    "isPrimary": false
  },
  {
    "Code": "AAPL",
    "Exchange": "MX",
    "Name": "Apple Inc",
    "Type": "Common Stock",
    "Country": "Mexico",
    "Currency": "MXN",
    "ISIN": "US0378331005",
    "previousClose": 4395.7202,
    "previousCloseDate": "2026-02-13",
    "isPrimary": false
  }
]
```

## Notes

- **Active tickers only**: The API searches among active (currently trading) tickers only.
- **Demo key not supported**: The demo API key does not work for the Search API. You must register for a free API token.
- **Response is a JSON array**: Unlike many EODHD endpoints, the response is a raw JSON array (not wrapped in an envelope object).
- **Bonds excluded by default**: When using `type=all` or no type filter, bonds are excluded from results. Use `type=bond` or `bonds_only=1` to include bonds.
- **ISIN returns all listings**: Searching by ISIN returns all exchange listings for that security. Use the `isPrimary` field to identify the primary listing, or filter with `exchange` to narrow results.
- **Cross-listed tickers**: The same security may appear with different ticker codes on different exchanges (e.g. `AAPL` on US, `APC` on XETRA, `0R2V` on LSE).
- **Search engine**: EODHD uses a professional search engine ([SphinxSearch](http://sphinxsearch.com/)) with sophisticated search rules that take into account market capitalization (converted to USD) and average trading volume over the past 10 days. The ticker code is the primary ranking parameter. For example, searching "VISA" returns that ticker first because it is a valid ticker code on some markets, even though Visa Inc.'s primary ticker is `V`.
- **Search by ISIN**: Tickers are searchable by their ISINs via the Search API and the main page search tool. However, ISINs are not unique — the same ISIN can exist on different exchanges (e.g., `AAPL.US` and `AAPL.MX`). EODHD uses `TICKER + EXCHANGE` as the unique identifier, consistent with other data providers.
- **Special characters in names**: Some company names contain characters that are difficult for the search engine to interpret (e.g., the apostrophe in "Lowe's Companies"). In most cases the search works perfectly, but such names may produce unexpected results.
- **Multiple tickers**: The search input is a single string. It returns results relevant to that string as a whole. Entering two different ticker codes will not return two separate results — it will likely return no results. Search is one query at a time.
- **Related endpoint**: There is a separate ID mapping endpoint to retrieve common identifiers (CUSIP, ISIN, OpenFigi, LEI, and CIK) for a symbol or by a specific identifier.

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
- Use `isPrimary` to identify the main listing when searching by ISIN
- Monitor your API usage in the user dashboard
