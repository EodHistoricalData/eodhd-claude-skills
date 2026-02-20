# TradingHours Get Market Details API

Status: complete
Source: marketplace (TradingHours)
Docs: https://eodhd.com/marketplace/tradinghours/options/docs
Provider: TradingHours via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/tradinghours`
Path: `/markets/details`
Method: GET
Auth: `api_token` query parameter
Response: JSON

## Purpose

Returns detailed information about one or more markets identified by their FinID,
including country code, timezone, weekend definition, MIC codes, and more. Use this
endpoint to get the full profile of a market or trading venue.

**Use cases**:
- Get timezone and weekend definition for a specific market
- Identify the country and MIC codes for a trading venue
- Look up exchange acronyms and product descriptions
- Check if a market has been permanently closed

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with `fin_id=us.nyse`.

## Parameters

### Query

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `api_token` | Yes | string | Your API key (or `demo` for demo access) |
| `fin_id` | Yes | string | Market FinID(s) to get details for (e.g. `us.nyse`). Case-insensitive. |

## Response

Returns a JSON object with a `data` array containing market detail objects.

### Market Detail Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `fin_id` | string | Unique identifier for the trading schedule (e.g. `US.NYSE`) |
| `country_code` | string | ISO 3166-1 alpha-2 country code (e.g. `US`, `JP`, `GB`) |
| `exchange` | string | Exchange name (e.g. `New York Stock Exchange`) |
| `market` | string\|null | Market segment name (e.g. `Canonical`, `Cash Market`) |
| `products` | string\|null | Products traded (e.g. `DAX, TecDAX, MDAX, SDAX listed`) |
| `mic` | string | Market Identifier Code (ISO 10383) |
| `mic_extended` | string | Extended MIC code |
| `acronym` | string | Exchange acronym (e.g. `NYSE`, `JPX`, `LSE`) |
| `asset_type` | string\|null | Asset type (e.g. `Securities`, `Equities`) |
| `memo` | string\|null | Additional notes about the market |
| `permanently_closed` | string\|null | Date the market permanently closed, or null if active |
| `timezone` | string | IANA timezone identifier (e.g. `America/New_York`, `Asia/Tokyo`) |
| `weekend_definition` | string | Weekend days (e.g. `Sat-Sun`, `Fri-Sat`) |
| `holidays_min_date` | string | Earliest holiday data available (YYYY-MM-DD) |
| `holidays_max_date` | string | Latest holiday data available (YYYY-MM-DD) |

## Example Request

```bash
# Get details for NYSE
curl "https://eodhd.com/api/mp/tradinghours/markets/details?fin_id=us.nyse&api_token=demo"

# Get details for Tokyo Stock Exchange
curl "https://eodhd.com/api/mp/tradinghours/markets/details?fin_id=jp.jpx&api_token=YOUR_API_TOKEN"
```

### Example Response

```json
{
  "data": [
    {
      "fin_id": "US.NYSE",
      "country_code": "US",
      "exchange": "New York Stock Exchange",
      "market": "Canonical",
      "products": null,
      "mic": "XNYS",
      "mic_extended": "XNYS",
      "acronym": "NYSE",
      "asset_type": "Securities",
      "memo": "Canonical",
      "permanently_closed": null,
      "timezone": "America/New_York",
      "weekend_definition": "Sat-Sun",
      "holidays_min_date": "2000-01-17",
      "holidays_max_date": "2033-12-26"
    }
  ]
}
```

### Python Example

```python
import requests

def get_market_details(fin_id, api_token):
    """Get detailed information about a market by FinID."""
    url = "https://eodhd.com/api/mp/tradinghours/markets/details"
    params = {
        "api_token": api_token,
        "fin_id": fin_id
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()["data"]

# Get NYSE details
details = get_market_details("us.nyse", "demo")
for market in details:
    print(f"Exchange:  {market['exchange']}")
    print(f"FinID:     {market['fin_id']}")
    print(f"Timezone:  {market['timezone']}")
    print(f"MIC:       {market['mic']}")
    print(f"Weekend:   {market['weekend_definition']}")
```

## Notes

- **Marketplace product**: Requires a separate TradingHours marketplace subscription, not included in main EODHD plans.
- **Case-insensitive**: The `fin_id` parameter is case-insensitive (`us.nyse` and `US.NYSE` both work).
- **Timezone**: The `timezone` field uses IANA timezone identifiers, useful for converting market times to local time.
- **Weekend definition**: Most markets use `Sat-Sun`, but some Middle Eastern markets may use `Fri-Sat`.
- **Related endpoints**: Use `/markets` (see tradinghours-list-markets.md) or `/markets/lookup` (see tradinghours-lookup-markets.md) to find FinIDs. Use `/markets/status` (see tradinghours-market-status.md) for real-time open/closed status.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Market details returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | Access denied (subscription required). |
| **429** | Too Many Requests | Rate limit exceeded. |
