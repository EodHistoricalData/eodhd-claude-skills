# Stock Fundamentals FAQ

Common questions and answers about the EODHD Fundamentals API, covering common stocks, ETFs, and mutual funds.

---

## General Questions

### Data Sources

For fundamental data, EODHD collects data from announcements, financial news providers, investor relations, corporate websites, and published annual reports — i.e., publicly available sources. Fundamentals are not subject to approval or disapproval by any exchange.

More details: https://eodhd.com/financial-apis/our-data-sources-and-data-partners/

### Fundamentals in CSV Format

The Fundamentals API returns JSON only (due to its complex nested structure). Workarounds for CSV:

1. Use any online converter (e.g., https://www.convertcsv.com/json-to-csv.htm or https://json-csv.com/) to convert JSON to CSV.
2. Use the EODHD Excel or Google Sheets add-ins.
3. Use the **Bulk Fundamentals** endpoint, which supports CSV output (though with limited fields/periods). See: https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds/#Bulk_Fundamentals_Output

**Note**: The Bulk Fundamentals `&version=1.2` does **not** support CSV output. The complex nested data structure makes CSV impractical at this version level, and adding new fields would break existing CSV consumers by shifting columns.

### Null and Zero Values

For many exchanges, some fields are not available due to differences in reporting completeness between companies and markets. Both `0` and `null` represent the same thing: **the data is not currently available from the API**.

Whether this is temporary (e.g., a preliminary quarterly report with fields to be filled later) or permanent (e.g., the figure is not available from the company's reports) cannot be distinguished from the API response alone.

### Short Interest

There is no separate short interest API. The current snapshot of short interest data is available as a section for **US tickers** within their fundamentals response.

### ROI (Return on Investment)

ROI is a personal metric pertaining to your own investments, not a company metric. It needs to be calculated on your side using historical price data from the EOD API.

### Audited vs Unaudited Statements

There is no flag in the API to differentiate between audited and unaudited financial statements.

### Historical Fundamentals

The fundamentals output is historical in the following sections: **outstandingShares**, **Earnings**, **Financials**. All other metrics are current snapshots and are not subject to point-in-time filtering.

You can calculate historical metrics from financials and prices using the EOD API. EODHD has an Academy article for this: https://eodhd.com/financial-apis/historical-financial-ratios-market-capitalization-price-to-earnings-price-to-book/

---

## General Section Fields

### Sector and Industry Classification

The sector/industry classification used by EODHD is similar to the Morningstar classification (though not identical — there may be differences on select stocks). It is not source-specific and is used by many open sources.

A full classification list is available at: https://eodhd.com/download/SectorIndustries.csv

Reference: https://indexes.morningstar.com/resources/PDF/Methodology%20Documents/SectorArticle.pdf

### Duplicate Sectors and Industries

The sector/industry list may contain entries that appear duplicated or excessive. This is because the list includes all sectors and industries as they currently are **and** as they used to be — including classifications that remain on delisted companies as they were at the moment of delisting.

### GICS (Global Industry Classification Standard)

GICS codes are available but not filled for all tickers across all exchanges — they are primarily available for US and some other major exchanges.

GICS is not updated on a fixed weekly schedule. Updates are made as changes are announced by MSCI and S&P Dow Jones Indices. EODHD reflects these updates soon after official publication, though there may be a short delay.

Reference: https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard

### Company Location

The `countryName` field in fundamentals represents the **country of the exchange** the ticker is traded on, not the company's headquarters location. To determine a company's actual location, use the **address fields** in the General section.

Note: For international companies, defining a single "location" is inherently complex — default to the headquarters address.

### SPAC (Special Purpose Acquisition Companies)

There is no dedicated SPAC flag. You can identify SPACs by filtering for: `"Sector": "Financial Services"`, `"Industry": "Shell Companies"`.

---

## Highlights / Valuation / SharesStats

### Float Larger Than Outstanding Shares

This can happen for two reasons:

1. **Timing lag**: The `SharesFloat` figure may update before `SharesOutstanding`, creating a temporary inconsistency.
2. **Multi-class stocks**: Companies with multiple stock classes may share the same float figure, while outstanding shares are class-specific. For example, Emera Corporation has tickers `EMA.TO` and `EMA-PH.TO` — they share the same float but have different outstanding shares.

### Beta

Beta is a **5-year monthly levered beta** based on main indices for the country (e.g., GSPC for USA, CAC40 for France). It is updated weekly on average.

Levered beta measures the risk of a firm with debt and equity in its capital structure relative to market volatility. A key determinant of beta is leverage (the ratio of a company's debt to its equity).

### Beta Against Other Indices

To calculate beta against a non-default index (or even another stock), use the Technical Indicators API:

```
https://eodhd.com/financial-apis/technical-indicators-api/#BETA
```

### Analyst Ratings

`AnalystRatings` are provided for **top US and EU stocks**. The data is collected from public reports using an automatic process that gathers data from news and announcements and processes it with NLP.

The `targetPrice` is the expected price at the end of the year for a particular stock.

### Historical Float

Only historical **outstanding shares** are available in the Fundamentals API, not historical free float. Float is not a calculated field — it must be reported by the company.

---

## Outstanding Shares

### Diluted or Basic

EODHD provides **diluted outstanding shares**, adjusted for splits.

---

## Earnings

### Future Earnings Date Accuracy

Future earnings dates are **approximate estimates**. Once the actual date is confirmed and updated by data sources, the API will reflect the correct date.

### GAAP vs Non-GAAP EPS

EODHD uses **non-GAAP EPS**, consistent with many other major financial data sources (e.g., Seeking Alpha, Investing.com, Yahoo Finance). SEC.gov reports use GAAP.

**Exception**: For AAPL, MSFT, and other very major companies, every source provides GAAP diluted EPS as it is reported directly in their SEC filings.

### EPS Forecast Horizon

Only a **1-year EPS forecast** is available. Two-year forecasts are not provided.

### Earnings Trends — Missing Data

If earnings trends data is incomplete in the fundamentals response, try the **Calendar API — Trends** endpoint, which may have more complete data:

```
https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits/#Earnings_Trends_API
```

### Earnings Trends — Not Updated After 10-K

Even after a company reports its 10-K, it takes time for analysts to produce estimates based on the data. The trend section is updated once analyst estimates become available.

### Earnings Trends — Update Timestamp

The update procedure runs daily, but the exact timestamp of when a particular value changes is not recorded.

---

## Financial Statements

### Filing Date

The filing date is generally available for **US tickers** but less reliably so for non-US ones.

### Missing Fields in Financial Reports

Companies report differently. Fields available in AAPL's reports might not exist for another company — even among SEC filers. Field names may differ between companies or even between different years of the same company's reports.

The totals and major fields are present and correct, but the template is standardized and cannot accommodate every unique field a company may include.

### Sales Growth QoQ

Not provided directly. Calculate it from financial reports by comparing the relevant quarters' revenue figures.

### Semi-Annual Reporting

There is no flag indicating that a company reports semi-annually. Circumstantial evidence includes:

- 4 quarters of a year showing identical values (yearly data split evenly)
- 2 quarters showing identical values (semi-annual data split evenly)
- Only even quarters showing data; odd quarters are null
- Odd quarters missing entirely
- Odd quarters showing substantially different magnitude from even quarters

### Many Null Values

Fundamental data depends on what companies report. The template is standardized, but actual data coverage varies between companies and exchanges.

### Income Statement Trajectory

The standard relationship between income statement fields:

```
totalRevenue - costOfRevenue = grossProfit
grossProfit - totalOperatingExpenses = operatingIncome
otherOperatingExpenses = costOfRevenue + totalOperatingExpenses
totalRevenue - otherOperatingExpenses = operatingIncome
operatingIncome = ebit
ebitda = ebit + depreciationAndAmortization
depreciationAndAmortization = reconciledDepreciation
operatingIncome + totalOtherIncomeExpenseNet = incomeBeforeTax
incomeBeforeTax - taxProvision = netIncome
taxProvision = incomeTaxExpense
netIncome - minorityInterest = netIncomeApplicableToCommonShares
```

### Restatements

EODHD does not keep two versions of fundamental data. If there is a restatement, the data point may be updated at a later point — typically when the next full report is published that includes the restated figure, rather than immediately after the restatement is announced.

---

## Bulk Fundamentals

### Extended Fundamentals Subscription

The Bulk Fundamentals feature (allowing bulk requests with a stock list) requires the **Extended Fundamentals** package. This is essentially the All-in-One plan with bulk fundamentals added. Users are subscribed to this plan manually by request. See [eodhd.com](https://eodhd.com/) for current pricing.

### 504 Timeout Errors

504 errors occur when a request contains too many tickers. Use the `offset` and `limit` parameters to paginate:

```
https://eodhd.com/knowledgebase/stock-etfs-fundamental-data-feeds/
```

For large exchanges like NYSE, EODHD makes 20-30 internal requests per symbol — thousands of requests per query. Splitting into 2-3 requests (using `limit` and `offset`) may take slightly longer but allows downloading an entire exchange's data.

### Version 1.2 and CSV

`&version=1.2` does **not** support CSV output. Reasons:

1. The complex nested data structure is not suitable for CSV (designed for flat tables, not nested structures).
2. Adding new fields to CSV output would shift all subsequent columns, breaking existing consumers.
3. JSON is flexible and allows adding fields without breaking changes.

---

## ETF-Specific

### TotalAssets vs AUM

`TotalAssets` includes **all** assets held by the ETF, while AUM (Assets Under Management) only includes assets currently being managed. These figures may differ.

### EPS for ETFs

EODHD does not provide EPS for ETFs directly, but it can be calculated. For US and iShares ETFs, holdings with percentage weights are provided — use them to compute a weighted average P/E ratio or EPS for the underlying stocks.

### Fixed Income Fields

For bond ETFs (e.g., BND), the figures under `Fixed_Income` are **averages for the bonds in the ETF's portfolio**. The `Relative_to_Category` figures are comparison averages for similar ETFs. A coupon value of 0 means there is no coupon data available for the bonds in that portfolio.

### Replication Data

ETF replication information (physical vs synthetic) is not available.

### Returns Differ from Price-Calculated Returns

Returns in the Fundamentals API factor in **management fees**, so they will always be slightly lower than returns calculated purely from price changes.

### ETF Technicals

ETF technicals in the Fundamentals API are updated on a **monthly basis**. For daily technical indicators, use the Technical Indicators API endpoint instead.

### ETF — NAV

EODHD does not provide NAV directly for ETFs. The closest available metric is **Book-Value Growth** in the ETF fundamentals. For Mutual Funds, NAV is available in the Fundamentals API.

### ETF — KIID Information

Key Investor Information Document (KIID) data is not available.

### ETF — Highs and Lows (Web vs API)

On the EODHD web page, highs/lows are adjusted for **splits only**. Via the API, highs/lows are adjusted for both **splits and dividends**.

### ETF — Market Cap Classification of Holdings

Market cap classification follows standard industry definitions (see: https://www.investopedia.com/insights/understanding-small-and-big-cap-stocks/):

| Category | Market Cap Range |
|----------|-----------------|
| Mega-cap | $200 billion and greater |
| Big-cap | $10 billion and greater |
| Mid-cap | $2 billion to $10 billion |
| Small-cap | $300 million to $2 billion |
| Micro-cap | $50 million to $300 million |
| Nano-cap | Under $50 million |

### ETF — Equity Weights and Relative-to-Category

In ETF fundamentals, "equity weights" show the weight distribution of holdings. The "relative-to-category" weights compare the ETF's values against averages for similar ETFs within its category. Categories are the same as used by MorningStar (though not officially published as a complete list by EODHD).

### ETF — UCITS Compliance

EODHD does not provide a UCITS compliance flag. As a workaround, search for the word **"UCITS"** in the ETF's name string — many UCITS-compliant ETFs include this designation in their names.

### ETF — Ex-Dividends

EODHD provides ex-dividend data for ETFs (historical). However, **future ex-dividend dates** for ETFs are not currently available.

---

## Mutual Fund (FUND) Specific

### AverageMarketCap

The `Market_Capitalization` section shows the market cap distribution of a fund's holdings. `AverageMarketCap` is a subsection showing the average market cap across holdings. The remaining subsections show the breakdown by size category (large-cap, mid-cap, small-cap, etc.).

### FUND — NAV

NAV is part of the funds' fundamental data. If you need a history of prices, use the funds' EOD data endpoint instead.

### FUND — Negative Weights

Negative weights on mutual fund holdings mean there are **more short positions than long positions** on those holdings.

---

## Funds & ETFs — Common

### Reinvesting (ACC) vs Distributing (DIST)

EODHD does not provide an accumulating/distributing flag. However, some funds' and ETFs' names include `ACC` or `DIST` in the name string, which can be used for identification.

---

## Outstanding Shares — Annual vs Quarterly

Annual outstanding shares data is generated slightly later than quarterly data. In most cases, EODHD recommends using **quarterly outstanding shares** as the more precise option.

---

## Sector Distribution Standard

EODHD uses a common sector structure (similar to Reuters, Yahoo, WSJ, and others) for stocks. For funds/ETFs, a MorningStar-style sector structure is used. Different formats are used because it is not possible to apply the same standard across all asset types.

The known sector values include: "Basic Materials", "Communication Services", "Conglomerates", "Consumer Cyclical", "Consumer Defensive", "Consumer Goods", "Distribution", "Energy", "Financial", "Financial Services", "Health", "Healthcare", "Industrial Goods", "Industrials", "Other", "Property", "Real Estate", "Services", "Technology", "Utilities".

There may be variations between exchanges because data is collected from different sources and is not fully standardized worldwide.

---

## Fundamentals Data Sources

EODHD compiles fundamental data from a combination of:
- **Official financial filings** (e.g., 10-K, 10-Q) submitted to regulatory bodies like the SEC (for US companies)
- **Global financial regulators and exchanges** (for non-US companies)
- **Aggregated data vendors and data partners** who supply structured, standardized fundamental data
- **Company disclosures and investor relations pages** for supplementary details

The data is standardized across regions and company types to ensure consistency for comparison and analysis. More details: https://eodhd.com/financial-apis/our-data-sources-and-data-partners

---

**Last Updated**: February 2026
**Source**: EODHD Official Documentation
**Maintained By**: EODHD Skills Team
