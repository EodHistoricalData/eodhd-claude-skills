# Stock Market Logos API (SVG Extension)

Status: complete
Source: marketplace (Unicorn Data Services)
Docs: https://eodhd.com/financial-apis/stock-market-logos-api
Provider: Unicorn Data Services via EODHD Marketplace
Base URL: `https://eodhd.com/api`
Path: `/logo-svg/{symbol}`
Method: GET
Auth: `api_token` query parameter
Response: SVG image file (XML-based scalable vector graphics)

## Purpose

Returns the logo image in SVG format for a specified stock exchange ticker symbol.
SVG format is only available for US and TO (Toronto) exchanges. This endpoint is
useful for applications that need scalable vector graphics for high-resolution
displays, printing, or responsive layouts where logos need to scale without
quality loss.

This is an extended version of the Stock Market Logos API (see stock-market-logos.md
for the PNG version covering 60+ exchanges).

**Use cases**:
- Display company logos at any resolution without quality loss
- Build high-DPI / Retina-ready financial dashboards
- Generate print-quality reports and presentations with company logos
- Use in responsive web designs where logos need to scale dynamically

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with any supported ticker (e.g. `AAPL.US`).

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | Ticker symbol in `{ticker}.{exchange}` format. SVG is only available for US and TO exchanges (e.g. `AAPL.US`, `MSFT.US`, `SHOP.TO`) |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key (or `demo` for demo access) |

## Response

Returns an **SVG image file** on success. The response `Content-Type` is `image/svg+xml`.

The SVG is a standard XML document starting with `<?xml version="1.0"?>` followed by an `<svg>` element.

## Example Request

```bash
# Download Apple logo (SVG)
curl -o AAPL_logo.svg "https://eodhd.com/api/logo-svg/AAPL.US?api_token=demo"

# Download Microsoft logo (SVG)
curl -o MSFT_logo.svg "https://eodhd.com/api/logo-svg/MSFT.US?api_token=demo"

# Download Shopify logo (Toronto)
curl -o SHOP_logo.svg "https://eodhd.com/api/logo-svg/SHOP.TO?api_token=demo"
```

### Python Example

```python
import requests

def download_logo_svg(symbol, api_token, output_path=None):
    """Download a company logo as SVG."""
    url = f"https://eodhd.com/api/logo-svg/{symbol}"
    params = {"api_token": api_token}

    response = requests.get(url, params=params)
    response.raise_for_status()

    if output_path is None:
        ticker = symbol.replace(".", "_")
        output_path = f"{ticker}_logo.svg"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    return output_path

# Demo usage
path = download_logo_svg("AAPL.US", "demo")
print(f"Logo saved to: {path}")
```

### Batch Download Example

```python
import requests
import time

def download_logos_svg_batch(symbols, api_token, output_dir="."):
    """Download SVG logos for multiple symbols."""
    for symbol in symbols:
        url = f"https://eodhd.com/api/logo-svg/{symbol}"
        params = {"api_token": api_token}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            ticker = symbol.replace(".", "_")
            path = f"{output_dir}/{ticker}_logo.svg"
            with open(path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Downloaded: {symbol}")
        except requests.exceptions.HTTPError as e:
            print(f"Failed: {symbol} - {e}")

        time.sleep(0.1)  # Rate limiting

# Usage (US and TO exchanges only)
symbols = ["AAPL.US", "MSFT.US", "TSLA.US", "AMZN.US", "SHOP.TO"]
download_logos_svg_batch(symbols, "YOUR_API_TOKEN")
```

## Coverage

SVG logos are available for **US and TO exchanges only**:

| Exchange | Description |
|----------|-------------|
| US | United States (NYSE, NASDAQ, OTC combined) |
| TO | Toronto Stock Exchange (Canada) |

For PNG logos covering 60+ exchanges, see the standard Stock Market Logos API (stock-market-logos.md).

## Notes

- **Marketplace product**: Requires a separate Unicorn Data Services marketplace subscription, not included in main EODHD plans.
- **SVG response**: Unlike most EODHD endpoints that return JSON, this endpoint returns an SVG XML document. Use text mode for writing (not binary).
- **Limited exchange coverage**: SVG format is only available for US and TO exchanges. For other exchanges, use the PNG endpoint (`/logo/{symbol}`).
- **Scalable**: SVG logos can be scaled to any size without quality loss, unlike the fixed 200x200px PNG logos.
- **Symbol format**: Use the standard `{ticker}.{exchange}` format (e.g. `AAPL.US`, `SHOP.TO`).
- **Demo access**: The demo API key works with any supported ticker.
- **Related endpoint**: Use `/logo/{symbol}` for PNG logos covering 60+ exchanges (see stock-market-logos.md).

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | SVG image returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | Access denied (subscription required). |
| **404** | Not Found | Logo not available for the specified ticker. |
| **429** | Too Many Requests | Rate limit exceeded. |
