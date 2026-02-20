# Stock Market Logos API

Status: complete
Source: marketplace (Unicorn Data Services)
Docs: https://eodhd.com/financial-apis/stock-market-logos-api
Provider: Unicorn Data Services via EODHD Marketplace
Base URL: `https://eodhd.com/api`
Path: `/logo/{symbol}`
Method: GET
Auth: `api_token` query parameter
Response: PNG image file (200x200px with transparency)

## Purpose

Returns the logo image for a specified stock exchange ticker symbol as a 200x200px
PNG file with transparency. The largest collection of 40,000+ stock market company
logos available via a single API endpoint, covering 60+ exchanges worldwide.

**Use cases**:
- Display company logos alongside stock information in applications
- Build visually rich financial dashboards and portfolio trackers
- Enhance stock screener or watchlist UIs with company branding
- Generate reports or presentations with company logos

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
| `symbol` | string | Ticker symbol in `{ticker}.{exchange}` format (e.g. `AAPL.US`, `BMW.XETRA`, `0700.HK`) |

### Query (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | string | Your API key (or `demo` for demo access) |

## Response

Returns a **PNG image file** on success (200x200px with transparency). The response `Content-Type` is `image/png`.

## Example Request

```bash
# Download Apple logo
curl -o AAPL_logo.png "https://eodhd.com/api/logo/AAPL.US?api_token=demo"

# Download BMW logo (XETRA)
curl -o BMW_logo.png "https://eodhd.com/api/logo/BMW.XETRA?api_token=demo"

# Download Tencent logo (Hong Kong)
curl -o Tencent_logo.png "https://eodhd.com/api/logo/0700.HK?api_token=demo"
```

### Python Example

```python
import requests

def download_logo(symbol, api_token, output_path=None):
    """Download a company logo as PNG."""
    url = f"https://eodhd.com/api/logo/{symbol}"
    params = {"api_token": api_token}

    response = requests.get(url, params=params)
    response.raise_for_status()

    if output_path is None:
        ticker = symbol.replace(".", "_")
        output_path = f"{ticker}_logo.png"

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

# Demo usage
path = download_logo("AAPL.US", "demo")
print(f"Logo saved to: {path}")
```

### Batch Download Example

```python
import requests
import time

def download_logos_batch(symbols, api_token, output_dir="."):
    """Download logos for multiple symbols."""
    for symbol in symbols:
        url = f"https://eodhd.com/api/logo/{symbol}"
        params = {"api_token": api_token}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            ticker = symbol.replace(".", "_")
            path = f"{output_dir}/{ticker}_logo.png"
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {symbol}")
        except requests.exceptions.HTTPError as e:
            print(f"Failed: {symbol} - {e}")

        time.sleep(0.1)  # Rate limiting

# Usage
symbols = ["AAPL.US", "MSFT.US", "TSLA.US", "AMZN.US", "GOOGL.US"]
download_logos_batch(symbols, "YOUR_API_TOKEN")
```

## Coverage

40,000+ company logos across 60+ exchanges:

AS, AT, AU, BA, BK, BR, BSE, CN, CO, CSE, DU, F, HE, HK, HM, IC, IR, IS, JK, JSE, KLSE, KO, KQ, LS, LSE, MC, MCX, MI, MU, MX, NEO, NSE, NZ, OL, PA, RG, SA, SG, SHE, SHG, SN, SR, ST, STU, SW, TA, TO, TSE, TW, TWO, US, V, VI, VS, VX, XETRA

## Notes

- **Marketplace product**: Requires a separate Unicorn Data Services marketplace subscription, not included in main EODHD plans.
- **PNG response**: Unlike most EODHD endpoints that return JSON, this endpoint returns a binary PNG image. Use appropriate file handling (binary write mode).
- **Image format**: All logos are 200x200px PNG files with transparency.
- **Symbol format**: Use the standard `{ticker}.{exchange}` format (e.g. `AAPL.US`, `BMW.XETRA`).
- **Full ticker list**: Available as an Excel file (logos_list.xlsx) from the Marketplace product page.
- **Caching**: Logo images change infrequently. Cache aggressively to reduce API calls.
- **Demo access**: The demo API key works with any supported ticker.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | PNG image returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **403** | Forbidden | Access denied (subscription required). |
| **404** | Not Found | Logo not available for the specified ticker. |
| **429** | Too Many Requests | Rate limit exceeded. |
