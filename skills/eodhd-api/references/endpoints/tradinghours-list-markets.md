# TradingHours List All Markets API

Status: complete
Source: marketplace (TradingHours)
Docs: https://eodhd.com/marketplace/tradinghours/options/docs
Provider: TradingHours via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/tradinghours`
Path: `/markets`
Method: GET
Auth: `api_token` query parameter
Response: JSON

## Purpose

Returns a list of all available markets with their FinIDs, exchange names, MICs,
asset types, and holiday coverage dates. Use this endpoint to discover which markets
are available and find the correct `{FinID}` for use with other TradingHours endpoints.

Each unique trading schedule or trading calendar is identified by a unique `{FinID}`.
Most exchanges have several different trading schedules for equities, bonds, futures, etc.
If you use `{MIC}` in place of the `{FinID}`, the system will select the closest match.

To find the correct `{FinID}`, look at `exchange`, `market`, and `products` fields.

**Use cases**:
- Discover available markets and their FinIDs
- Map MIC codes to FinIDs for use with status and details endpoints
- Check holiday data coverage range for each market
- Filter markets by access tier (Core, Extended, All)

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
| `group` | No | string | `all` | Which group of markets to show. One of: `core`, `extended`, `all`, `allowed` |

The `allowed` group returns only markets your subscription has access to.

## Response

Returns a JSON object with a `data` array containing market objects.

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
# List all Core (G20+) markets
curl "https://eodhd.com/api/mp/tradinghours/markets?group=core&api_token=YOUR_API_TOKEN"

# List all available markets
curl "https://eodhd.com/api/mp/tradinghours/markets?group=all&api_token=YOUR_API_TOKEN"

# List only markets you have access to
curl "https://eodhd.com/api/mp/tradinghours/markets?group=allowed&api_token=demo"
```

### Example Response (Core group, truncated)

```json
{
  "data": [
    {
      "fin_id": "AU.ASX",
      "exchange": "ASX Australian Securities Exchange",
      "market": "Cash Market",
      "products": "Shares, ETPs, Hybrid Securities, A-REITs, etc",
      "mic": "XASX",
      "asset_type": "Equities",
      "group": "Core",
      "permanently_closed": null,
      "holidays_min_date": "2000-01-03",
      "holidays_max_date": "2028-12-29"
    },
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

def list_markets(api_token, group="all"):
    """List all available TradingHours markets."""
    url = "https://eodhd.com/api/mp/tradinghours/markets"
    params = {
        "api_token": api_token,
        "group": group
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()["data"]

# List Core (G20+) markets
markets = list_markets("YOUR_API_TOKEN", group="core")
for m in markets:
    print(f"{m['fin_id']:15} {m['exchange']:45} MIC: {m['mic']}")
```

## Core (G20+) Markets

The Core tier covers 24 markets:

| FinID | Exchange | MIC |
|-------|----------|-----|
| AU.ASX | ASX Australian Securities Exchange | XASX |
| BR.BOVESPA | B3 - Brasil Bolsa Balcão | BVMF |
| CA.XTSX | TMX Group (TSX Venture Exchange) | XTSX |
| CH.SIX | SIX Swiss Exchange | XSWX |
| CN.SSE | Shanghai Stock Exchange | XSHG |
| CN.SZSE | Shenzhen Stock Exchange | XSHE |
| DE.MUN | Munich Stock Exchange | XMUN |
| DE.STU | Stuttgart Stock Exchange | XSTU |
| DE.XETR | Xetra | XETR |
| DE.XFRA | Frankfurt Stock Exchange | XFRA |
| ES.BME | Bolsas y Mercados Españoles (BME) | BMEX |
| GB.LSE | LSE Group | XLON |
| HK.HKEX | Hong Kong Exchanges and Clearing | XHKG |
| ID.IDX | Indonesia Stock Exchange | XIDX |
| IN.BSE | BSE India Limited | XBOM |
| IN.NSE | National Stock Exchange of India | XNSE |
| IT.EURONEXT | EURONEXT Milan | MTAA |
| JP.JPX | Japan Exchange Group | XJPX |
| KR.KRX | Korea Exchange (KOSPI) | XKRX |
| MX.BMV | Mexican Stock Exchange (BMV) | XMEX |
| RU.MOEX | Moscow Exchange | MISX |
| TW.TWSE | Taiwan Stock Exchange | XTAI |
| US.NASDAQ | Nasdaq U.S. | XNAS |
| US.NYSE | New York Stock Exchange | XNYS |
| ZA.JSE | Johannesburg Stock Exchange | XJSE |

## Notes

- **Marketplace product**: Requires a separate TradingHours marketplace subscription, not included in main EODHD plans.
- **FinID vs MIC**: FinIDs are more granular than MICs — they uniquely identify distinct trading schedules. MICs alone may not be sufficient to distinguish all schedules.
- **Access tiers**: Your subscription determines which markets you can access. Use `group=allowed` to see only your accessible markets.
- **Related endpoints**: Use the FinID from this endpoint with `/markets/details` (see tradinghours-market-details.md), `/markets/status` (see tradinghours-market-status.md), and `/markets/lookup` (see tradinghours-lookup-markets.md).

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Market list returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | Access denied (subscription required). |
| **429** | Too Many Requests | Rate limit exceeded. |
