# Praams Multi-Factor Bond Report by ISIN API

Status: complete
Source: marketplace (PRAAMS API)
Docs: https://eodhd.com/marketplace/unicornbay/options/docs
Provider: PRAAMS via EODHD Marketplace
Base URL: `https://eodhd.com/api/mp/praams`
Path: `/reports/bond/{isin}`
Method: GET
Auth: `api_token` query parameter
Response: PDF file download

## Purpose

Generates and downloads a multi-page PDF investment report for a specific bond
identified by its ISIN code. The report contains concise visual and descriptive
information covering 6 return factors and 6 risk factors.

**Return factors**: valuation, performance, analyst/market view, profitability, growth, and dividends/coupons.

**Risk factors**: default, volatility, stress-test, selling difficulty, country, and other risks.

Each report is an asset class-specific analytical summary — bond reports differ from
equity reports. Reports are updated daily with new prices, financials, dividends,
and corporate actions.

**Use cases**:
- Download a PDF investment report on any bond using its ISIN
- Share bond analysis with colleagues or clients
- Get a quick visual summary of bond risk and return factors
- Analyze corporate and sovereign bonds from global markets

**Disclaimer**: The product does not constitute financial advice or investment recommendations. Trading involves risk, and users should carefully evaluate their own financial situation before engaging in any trades.

## Plans & API Calls

This is a **Marketplace product** — its rate limits are counted separately from the main EODHD plans.

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

> The 24-hour period is counted differently for Marketplace products compared to the main EODHD plans.

**Demo access**: Use `api_token=demo` with ISINs `US7593518852` or `US91282CJN20`.

## Parameters

### Path (required)

| Parameter | Type | Description |
|-----------|------|-------------|
| `isin` | string | ISIN code of the bond (e.g. `US7593518852`, `US91282CJN20`, `US59018YTM39`) |

### Query

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `api_token` | Yes | string | Your API key (or `demo` for demo ISINs) |
| `email` | Yes | string | Email address for notifications or confirmations |
| `isFull` | No | boolean | Whether to generate the full report or a partial report |

## Response

Returns a **PDF file download** on success. The response `Content-Type` is `application/pdf`.

The downloaded file is named in the format: `PRAAMS_report_{ISIN}_{timestamp}.pdf`

**Example**: `PRAAMS_report_US59018YTM39_2026-02-16 19_33_45Z.pdf`

## Example Request

```bash
# Demo access
curl -o PRAAMS_bond_report.pdf "https://eodhd.com/api/mp/praams/reports/bond/US7593518852?isFull=false&email=test@test.com&api_token=demo"

# Production access (Bank of America bond, 6.05% coupon, maturing 1 June 2034)
curl -o PRAAMS_bond_report.pdf "https://eodhd.com/api/mp/praams/reports/bond/US59018YTM39?isFull=false&email=test@test.com&api_token=YOUR_API_TOKEN"
```

### Python Example

```python
import requests

def download_bond_report_by_isin(isin, email, api_token, is_full=False, output_path=None):
    """Download a PRAAMS bond PDF report by ISIN."""
    url = f"https://eodhd.com/api/mp/praams/reports/bond/{isin}"
    params = {
        "api_token": api_token,
        "email": email,
        "isFull": str(is_full).lower()
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    if output_path is None:
        output_path = f"PRAAMS_bond_report_{isin}.pdf"

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

# Demo usage
path = download_bond_report_by_isin("US7593518852", "test@test.com", "demo")
print(f"Report saved to: {path}")
```

## Coverage

120,000+ global bonds including:
- **Corporate bonds**: US, UK, Europe, China, India, Middle East, Asia & Oceania, LatAm, and Africa (both OTC and exchange-traded)
- **Sovereign bonds**: Government debt from global markets

## Notes

- **Marketplace product**: Requires a separate PRAAMS marketplace subscription, not included in main EODHD plans.
- **PDF response**: Unlike most EODHD endpoints that return JSON, this endpoint returns a binary PDF file. Use appropriate file handling (binary write mode).
- **Demo ISINs**: `US7593518852` and `US91282CJN20` are available with `api_token=demo`.
- **Daily updates**: Reports are regenerated daily with latest prices, financials, dividends, and corporate actions.
- **Bond-specific**: Bond reports differ from equity reports — they include coupon analysis, spread comparisons, and credit risk assessment instead of dividend and analyst view sections.
- **ISIN required**: Bonds are identified by ISIN only (no ticker-based lookup for bonds).
- **Related endpoints**: Use `/reports/equity/ticker/{ticker}` for equity reports by ticker (see praams-report-equity-by-ticker.md). Use `/reports/equity/isin/{isin}` for equity reports by ISIN (see praams-report-equity-by-isin.md).

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | PDF file returned successfully. |
| **401** | Unauthorized | Invalid or missing API key. |
| **415** | Wrong Token | Token format is invalid. |
| **420** | Operation Cancelled | Request was cancelled. |
| **430** | Data Not Found | ISIN not found in PRAAMS database. |
