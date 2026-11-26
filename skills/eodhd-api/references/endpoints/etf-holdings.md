# ETF Holdings API (beta)

Status: complete (beta)
Source: financial-apis (ETF Holdings API)
Docs: https://eodhd.com/financial-apis/etf-holdings-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /etf/holdings/{symbol}
Method: GET
Auth: api_token (query)

## Purpose

Full portfolio of a **US-listed ETF**, built from the fund's SEC N-PORT filing: every position with weight, shares and value, plus the ten largest holdings, asset allocation, sector and region weights, and performance. The API is in **beta**. Only US-listed ETFs are covered.

For the reverse question (which funds hold a given stock), see `etf-held-by.md`.

Available on the Fundamentals Data Feed and All-In-One plans. Each request costs **10 API calls**, including a 404. The demo token works for `VTI`. JSON is the only format; there is no `fmt` parameter and no pagination, so all positions arrive in one response (large funds are several MB; BND is about 5 MB).

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API access token |
| symbol | Yes | string (path) | US ETF ticker, with or without `.US` (`VTI` = `VTI.US`); lowercase also works. Other exchanges return 422. |

## Response (shape)

Envelope: `{"data": {...}, "meta": [], "links": []}`. `meta` and `links` are empty lists here.

```json
{
  "data": {
    "General": {
      "Code": "XLE", "Type": "ETF", "Name": "Energy Select Sector SPDR Fund",
      "Exchange": "US", "Issuer": "...", "Fund_Type": "etf",
      "Net_Assets": 0, "Report_Date": "YYYY-MM-DD", "Source": "nport",
      "Is_Complete": true, "Mapped_Weight_%": 0, "Filed_Positions_Count": 23
    },
    "Holdings": {
      "XOM.US": {
        "Code": "XOM", "Exchange": "US", "Name": "...", "Sector": "Energy",
        "Industry": "...", "Country": "United States", "Country_Code": "US",
        "Region": "North America", "Assets_%": 0, "Shares": 0, "Value_USD": 0,
        "Contract_Code": null
      }
    },
    "Top_10_Holdings": { "XOM.US": { "...": "same shape as Holdings" } },
    "Holdings_Count": 23,
    "Asset_Allocation": {
      "Cash": { "Long_%": 0, "Short_%": 0, "Net_Assets_%": 0 },
      "Bond": { "Long_%": 0, "Short_%": 0, "Net_Assets_%": 0 },
      "Stock_US": { "Long_%": 0, "Short_%": 0, "Net_Assets_%": 0 },
      "Stock_non-US": { "Long_%": 0, "Short_%": 0, "Net_Assets_%": 0 },
      "Other": { "Long_%": 0, "Short_%": 0, "Net_Assets_%": 0 }
    },
    "Sector_Weights": { "Energy": { "Equity_%": 0 } },
    "World_Regions": { "North America": { "Equity_%": 0 } },
    "Performance": {
      "Returns_YTD": null, "Returns_1Y": null, "Returns_3Y": null, "Returns_5Y": null,
      "Returns_10Y": null, "1y_Volatility": null, "3y_Volatility": null, "3y_SharpRatio": null
    }
  },
  "meta": [],
  "links": []
}
```

Values above are placeholders; the types are what matter.

### `General`

| Field | Type | Description |
|-------|------|-------------|
| Code | string | Fund ticker |
| Type | string | Always `ETF` |
| Name | string | Fund name |
| Exchange | string | Always `US` |
| Issuer | string | Fund issuer |
| Fund_Type | string | `etf` |
| Net_Assets | number | Net assets, USD |
| Report_Date | string (date) | End of the filing period, not the request date |
| Source | string | `nport` |
| Is_Complete | boolean | Whether the position list is complete |
| Mapped_Weight_% | number | Share of fund weight whose positions have a ticker |
| Filed_Positions_Count | integer | Positions in the filing itself |

### `Holdings` and `Top_10_Holdings`

`Holdings` is an object keyed by position key (`CODE.EXCHANGE`, for example `NVDA.US`, `ASML.AS`). A position without a ticker gets another opaque key, possibly with a `~` suffix; **treat keys as opaque**. `Top_10_Holdings` has the same shape (ten largest).

| Field | Type | Description |
|-------|------|-------------|
| Code | string or null | Ticker code |
| Exchange | string or null | Exchange code |
| Name | string | Security name |
| Sector | string or null | Sector |
| Industry | string or null | Industry |
| Country | string | Country name (for example United States) |
| Country_Code | string | Two-letter country code |
| Region | string or null | World region |
| Assets_% | number | Weight in percent; can be negative; the sum can be above or below 100 |
| Shares | number | Shares held |
| Value_USD | number | Position value, USD |
| Contract_Code | string or null | Option or other derivative contract identifier |

**Edge case:** for a fund with no positions (for example `GAID`) `Holdings` is an empty list `[]`, not an object. Handle both types.

`Holdings_Count` is the number of entries in `Holdings`. Lots of one security are summed, so it can be below `Filed_Positions_Count`.

### Other blocks

- `Asset_Allocation`: exactly five keys (`Cash`, `Bond`, `Stock_US`, `Stock_non-US`, `Other`), each with `Long_%`, `Short_%`, `Net_Assets_%`.
- `Sector_Weights`, `World_Regions`: name to `{ "Equity_%": number }`. Equities only; may contain an `Unclassified` entry; an empty object for funds without equities (for example `BND`).
- `Performance`: an object or null. Each field is a number or null.

## Example Requests

```bash
# Small fund, good for a first test (about 11 KB)
curl "https://eodhd.com/api/etf/holdings/XLE?api_token=YOUR_TOKEN"

# Large fund: 3,544 positions; the demo token works for VTI
curl "https://eodhd.com/api/etf/holdings/VTI.US?api_token=demo"

# Using the helper client
python eodhd_client.py --endpoint etf/holdings --symbol XLE
```

## Notes

- Beta. US-listed ETFs only; other exchanges return 422.
- Data comes from SEC N-PORT filings, so `Report_Date` lags the request date.
- Funds without N-PORT coverage (for example commodity or crypto trusts and ETNs) return 404.
- Do not use `--limit` or `--offset` with the helper client for this endpoint; it is not paginated.

## HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. |
| **401** | Unauthorized | Plain text body `Unauthenticated`: missing or invalid token. |
| **403** | Forbidden | Plain text: the plan does not include this API. |
| **404** | Not Found | Fund not covered; see the codes below. Costs 10 API calls. |
| **422** | Unprocessable | Ticker is not US-listed. |
| **429** | Too Many Requests | Rate limit of the plan. |

### 404 codes

```json
{"errors":[{"status":"404","title":"Symbol not found","code":"NOT_COVERED","detail":"This ticker is outside ETF holdings coverage."}]}
```

| `code` | Meaning |
|--------|---------|
| `FUND_NOT_FOUND` | No fund with this ticker (unknown ticker, or a renamed fund such as SPLG) |
| `NOT_COVERED` | Outside coverage (for example GLD, SLV, IBIT, ETNs; some small funds) |
| `NO_HOLDINGS_YET` | Known fund with no N-PORT filing yet (for example JINT) |

### 422 body

```json
{"errors":{"symbol":["ETF data is available for US-listed securities only."]}}
```
