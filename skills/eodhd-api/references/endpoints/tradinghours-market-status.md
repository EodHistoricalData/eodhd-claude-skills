# TradingHours Market Status Details API

Status: complete
Source: marketplace (TradingHours)
Docs: https://eodhd.com/marketplace/tradinghours/options/docs
Provider: TradingHours via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/tradinghours`
Path: `/markets/status`
Method: GET
Auth: `api_token` query parameter
Response: JSON

## Purpose

Returns the real-time current status of one or more markets, including whether the
market is open or closed, when it opens or closes next, the current trading phase
(pre-trading, post-trading, etc.), and any holidays or irregular schedules in effect.

**Use cases**:
- Build real-time market status dashboards
- Add countdowns or market status indicators to websites or applications
- Activate trading algorithms when markets open
- Detect market holidays and half-days programmatically
- Cache-friendly polling with the `until` field

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
| `fin_id` | Yes | string | Market FinID(s) to check status for (e.g. `us.nyse`). Case-insensitive. |

## Response

Returns a JSON object with a `data` object. Unlike other TradingHours endpoints that
return an array, this endpoint returns an object keyed by FinID.

### Status Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `fin_id` | string | Unique identifier for the trading schedule (e.g. `US.NYSE`) |
| `exchange` | string | Exchange name (e.g. `New York Stock Exchange`) |
| `market` | string\|null | Market segment name (e.g. `Canonical`, `Tokyo Stock Exchange`) |
| `products` | string\|null | Products traded |
| `timezone` | string | IANA timezone identifier (e.g. `America/New_York`) |
| `status` | string | Current market status: `Open` or `Closed` |
| `reason` | string\|null | Reason for current status (e.g. `Washington's Birthday`, `Market Holiday - Primary Trading Session (Partial)`, or null for normal open/close) |
| `until` | string | ISO 8601 datetime when the current status will change. Safe to cache results until this time. |
| `next_bell` | string | ISO 8601 datetime of the next market open or close bell |

### Important Notes on `until` vs `next_bell`

- `until` indicates when the current status will change — it is safe to cache results until this time.
- `next_bell` indicates when the market officially opens or closes next.
- These are not always the same. For example, during a post-trading session, `until` indicates the end of the post-trading session, while `next_bell` will be the following morning when markets officially open.

## Example Request

```bash
# Check NYSE status
curl "https://eodhd.com/api/mp/tradinghours/markets/status?fin_id=us.nyse&api_token=demo"

# Check Tokyo Stock Exchange status
curl "https://eodhd.com/api/mp/tradinghours/markets/status?fin_id=jp.jpx&api_token=YOUR_API_TOKEN"
```

### Example Response (Market Closed — Holiday)

```json
{
  "data": {
    "US.NYSE": {
      "fin_id": "US.NYSE",
      "exchange": "New York Stock Exchange",
      "market": "Canonical",
      "products": null,
      "timezone": "America/New_York",
      "status": "Closed",
      "reason": "Washington's Birthday",
      "until": "2026-02-17T04:00:00-05:00",
      "next_bell": "2026-02-17T09:30:00-05:00"
    }
  }
}
```

### Example Response (Market Open)

```json
{
  "data": {
    "US.NYSE": {
      "fin_id": "US.NYSE",
      "exchange": "New York Stock Exchange",
      "market": "Canonical",
      "products": null,
      "timezone": "America/New_York",
      "status": "Open",
      "reason": null,
      "until": "2026-02-18T16:00:00-05:00",
      "next_bell": "2026-02-18T16:00:00-05:00"
    }
  }
}
```

### Example Response (Half-Day / Partial Holiday)

```json
{
  "data": {
    "US.NYSE": {
      "fin_id": "US.NYSE",
      "exchange": "New York Stock Exchange",
      "market": "Canonical",
      "products": null,
      "timezone": "America/New_York",
      "status": "Open",
      "reason": "Market Holiday - Primary Trading Session (Partial)",
      "until": "2020-11-27T12:45:00-05:00",
      "next_bell": "2020-11-27T13:00:00-05:00"
    }
  }
}
```

### Python Example

```python
import requests
from datetime import datetime

def get_market_status(fin_id, api_token):
    """Get real-time market status by FinID."""
    url = "https://eodhd.com/api/mp/tradinghours/markets/status"
    params = {
        "api_token": api_token,
        "fin_id": fin_id
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()["data"]

# Check NYSE status
status_data = get_market_status("us.nyse", "demo")
nyse = status_data["US.NYSE"]

print(f"Market:    {nyse['exchange']}")
print(f"Status:    {nyse['status']}")
print(f"Reason:    {nyse['reason'] or 'Normal schedule'}")
print(f"Until:     {nyse['until']}")
print(f"Next Bell: {nyse['next_bell']}")
```

### Caching Example

```python
import requests
from datetime import datetime, timezone

def get_market_status_cached(fin_id, api_token, cache={}):
    """Get market status with caching based on 'until' field."""
    cache_key = fin_id.upper()

    if cache_key in cache:
        cached = cache[cache_key]
        until = datetime.fromisoformat(cached["until"])
        if datetime.now(timezone.utc) < until:
            return cached

    url = "https://eodhd.com/api/mp/tradinghours/markets/status"
    params = {"api_token": api_token, "fin_id": fin_id}

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()["data"]
    status = data[cache_key]
    cache[cache_key] = status

    return status
```

## Notes

- **Marketplace product**: Requires a separate TradingHours marketplace subscription, not included in main EODHD plans.
- **Caching**: Results will not change until the `until` timestamp. Cache aggressively using this field to minimize API calls and avoid rate limits.
- **Holidays only**: This API accounts for previously-scheduled holidays and half-days but does **not** factor in circuit breakers or trading halts.
- **No time parameter**: The current endpoint does not support a `time` query parameter for historical status lookups. Contact tradinghours.com for enterprise offers.
- **Response structure**: Unlike other TradingHours endpoints that return `data` as an array, this endpoint returns `data` as an object keyed by FinID.
- **Related endpoints**: Use `/markets` (see tradinghours-list-markets.md) or `/markets/lookup` (see tradinghours-lookup-markets.md) to find FinIDs. Use `/markets/details` (see tradinghours-market-details.md) for static market information like timezone and weekend definition.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Market status returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | Access denied (subscription required). |
| **429** | Too Many Requests | Rate limit exceeded. |
