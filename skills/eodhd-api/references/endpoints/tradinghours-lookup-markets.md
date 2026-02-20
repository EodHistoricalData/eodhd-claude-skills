# TradingHours Lookup Markets API

Status: complete
Source: marketplace (TradingHours)
Docs: https://eodhd.com/marketplace/tradinghours/options/docs
Provider: TradingHours via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/tradinghours`
Path: `/markets/lookup`
Method: GET
Auth: `api_token` query parameter
Response: JSON

## Purpose

Searches for markets based on any attribute such as exchange name, market name,
security description, MIC, or country. Returns matching markets with their FinIDs
and metadata.

Each unique trading schedule or trading calendar is identified by a unique `{FinID}`.
Most exchanges have several different trading schedules for equities, bonds, futures, etc.
In total, TradingHours tracks over 900 different trading schedules.

This endpoint allows you to easily search for the exact trading calendar you need.

**Use cases**:
- Search for markets by exchange name, country, or MIC code
- Find the correct FinID for a specific trading venue
- Discover available trading schedules for a particular exchange
- Filter search results by access tier

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Access tiers**: This API has three tiers corresponding to TradingHours products:

| Tier | Group Value | Product |
|------|-------------|---------|
| Core | `core` | G20+ Markets (24 markets) |
| Extended | `extended` | Global Equities |
| All | `all` | Global Equities & Derivatives |

**Demo access**: Use `api_token=demo` with `group=allowed`.

## Parameters

### Query

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `api_token` | Yes | string | — | Your API key (or `demo` for demo access) |
| `q` | No | string | — | Free-form search term (exchange name, market name, MIC, country, etc.) |
| `group` | No | string | `all` | Which group of markets to search. One of: `core`, `extended`, `all`, `allowed` |

## Response

Returns a JSON object with a `data` array containing matching market objects.

### Market Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `fin_id` | string | Unique identifier for the trading schedule (e.g. `US.NYSE`, `JP.JPX`) |
| `exchange` | string | Exchange name (e.g. `New York Stock Exchange`) |
| `market` | string\|null | Market segment name (e.g. `Cash Market`, `Equity Market`) |
| `products` | string\|null | Products traded (e.g. `Shares, ETPs, Hybrid Securities`) |
| `mic` | string | Market Identifier Code (ISO 10383) |
| `asset_type` | string | Asset type (e.g. `Securities`, `Equities`) |
| `group` | string | Access tier: `Core`, `Extended`, or `All` |
| `permanently_closed` | string\|null | Date the market permanently closed, or null if active |
| `holidays_min_date` | string | Earliest holiday data available (YYYY-MM-DD) |
| `holidays_max_date` | string | Latest holiday data available (YYYY-MM-DD) |

## Example Request

```bash
# Search for Japanese markets
curl "https://eodhd.com/api/mp/tradinghours/markets/lookup?q=japan&api_token=YOUR_API_TOKEN"

# Search for markets by MIC code
curl "https://eodhd.com/api/mp/tradinghours/markets/lookup?q=XNYS&api_token=YOUR_API_TOKEN"

# Search within Core tier only
curl "https://eodhd.com/api/mp/tradinghours/markets/lookup?q=NYSE&group=core&api_token=YOUR_API_TOKEN"

# Demo access
curl "https://eodhd.com/api/mp/tradinghours/markets/lookup?q=name&group=allowed&api_token=demo"
```

### Example Response

```json
{
  "data": [
    {
      "fin_id": "US.NYSE",
      "exchange": "New York Stock Exchange",
      "market": "Canonical",
      "products": null,
      "mic": "XNYS",
      "asset_type": "Securities",
      "group": "Core",
      "permanently_closed": null,
      "holidays_min_date": "2000-01-17",
      "holidays_max_date": "2033-12-26"
    }
  ]
}
```

### Python Example

```python
import requests

def lookup_markets(query, api_token, group="all"):
    """Search for TradingHours markets by name, MIC, country, etc."""
    url = "https://eodhd.com/api/mp/tradinghours/markets/lookup"
    params = {
        "api_token": api_token,
        "q": query,
        "group": group
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()["data"]

# Search for German markets
markets = lookup_markets("germany", "YOUR_API_TOKEN", group="core")
for m in markets:
    print(f"{m['fin_id']:15} {m['exchange']:45} MIC: {m['mic']}")
```

## Notes

- **Marketplace product**: Requires a separate TradingHours marketplace subscription, not included in main EODHD plans.
- **Free-form search**: The `q` parameter searches across all market attributes — exchange name, market name, product description, MIC, and country.
- **No query returns all**: If `q` is omitted, behaves like the List All Markets endpoint (see tradinghours-list-markets.md).
- **FinID vs MIC**: FinIDs are more granular than MICs. Use FinIDs with other TradingHours endpoints for precise results.
- **Related endpoints**: Use the FinID from search results with `/markets/details` (see tradinghours-market-details.md) and `/markets/status` (see tradinghours-market-status.md).

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Search results returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | Access denied (subscription required). |
| **429** | Too Many Requests | Rate limit exceeded. |
