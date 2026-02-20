# Praams Multi-Factor Equity Report by ISIN API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/marketplace/unicornbay/options/docs
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/reports/equity/isin/{isin}`
Method: GET
Auth: `api_token` query parameter
Response: PDF file download

## Purpose

Generates and downloads a multi-page PDF investment report for a specific equity
identified by its ISIN code. The report contains concise visual and descriptive
information covering 6 return factors and 6 risk factors.

**Return factors**: valuation, performance, analyst/market view, profitability, growth, and dividends/coupons.

**Risk factors**: default, volatility, stress-test, selling difficulty, country, and other risks.

Each report is an industry-specific and asset class-specific analytical summary.
Reports for bank and corporate entities will be different. Reports are updated daily
with new prices, financials, dividends, and corporate actions.

**Use cases**:
- Download a PDF investment report for any equity using its ISIN code
- Share multi-factor analysis with colleagues or clients
- ISIN-based lookup for international equities or bonds that share the same ISIN
- Get a quick visual summary of risk and return factors

**Disclaimer**: The product does not constitute financial advice or investment recommendations. Trading involves risk, and users should carefully evaluate their own financial situation before engaging in any trades.

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with ISINs `US0378331005` (Apple), `US88160R1014` (Tesla), or `US0231351067` (Amazon).

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `isin` | string | ISIN code of the equity (e.g. `US0378331005`, `US88160R1014`, `US0231351067`) |

### Query

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `api_token` | Yes | string | Your API key (or `demo` for demo ISINs) |
| `email` | Yes | string | Email address for notifications or confirmations |
| `isFull` | No | boolean | Whether to generate the full report or a partial report |

## Response

Returns a **PDF file download** on success. The response `Content-Type` is `application/pdf`.

The downloaded file is named in the format: `PRAAMS_report_{ISIN}_{timestamp}.pdf`

## Example Request

```bash
# Demo access (Apple by ISIN)
curl -o PRAAMS_report_AAPL.pdf "https://eodhd.com/api/mp/praams/reports/equity/isin/US0378331005?isFull=false&email=test@test.com&api_token=demo"

# Production access
curl -o PRAAMS_report.pdf "https://eodhd.com/api/mp/praams/reports/equity/isin/US59018YTM39?isFull=false&email=test@test.com&api_token=YOUR_API_TOKEN"
```

### Python Example

```python
import requests

def download_equity_report_by_isin(isin, email, api_token, is_full=False, output_path=None):
    """Download a PRAAMS equity PDF report by ISIN."""
    url = f"https://eodhd.com/api/mp/praams/reports/equity/isin/{isin}"
    params = {
        "api_token": api_token,
        "email": email,
        "isFull": str(is_full).lower()
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    if output_path is None:
        output_path = f"PRAAMS_report_{isin}.pdf"

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

# Demo usage
path = download_equity_report_by_isin("US0378331005", "test@test.com", "demo")
print(f"Report saved to: {path}")
```

## Coverage

120,000+ global equities including:
- **Stocks**: US, UK, Europe, China, India, Middle East, Asia & Oceania, LatAm, and Africa (including small & micro-caps)
- **ETFs**: Key providers such as Vanguard, iShares, Invesco, Goldman Sachs, JPM, Fidelity, First Trust, etc.

## Notes

- **Marketplace product**: Requires a separate PRAAMS marketplace subscription, not included in main EODHD plans.
- **PDF response**: Unlike most EODHD endpoints that return JSON, this endpoint returns a binary PDF file. Use appropriate file handling (binary write mode).
- **Demo ISINs**: `US0378331005` (Apple), `US88160R1014` (Tesla), and `US0231351067` (Amazon) are available with `api_token=demo`.
- **Daily updates**: Reports are regenerated daily with latest prices, financials, dividends, and corporate actions.
- **Industry-specific**: Reports are tailored to the industry — a bank report will differ from a non-financial corporate report.
- **ISIN vs Ticker**: Use this endpoint when you have an ISIN code. Use `/reports/equity/ticker/{ticker}` for ticker-based lookups (see praams-report-equity-by-ticker.md).
- **Related endpoints**: Use `/reports/bond/isin/{isin}` for bond reports (see praams-report-bond-by-isin.md).

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | PDF file returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **415** | Wrong Token | Token format is invalid. |
| **420** | Operation Cancelled | Request was cancelled. |
| **430** | Data Not Found | ISIN not found in PRAAMS database. |
