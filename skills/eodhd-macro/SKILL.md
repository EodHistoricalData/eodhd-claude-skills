---
name: eodhd-macro
description: >-
  Macro-economic dashboard using EODHD data — GDP, CPI, unemployment, interest
  rates, Treasury yield curve, real yields, and the economic events calendar.
  Invoke as /eodhd-macro [country or region].
argument-hint: "[country or region, e.g. USA, EU, G7]"
---

Generate a macro-economic dashboard using EODHD data.

Use the `macro-dashboard` skill workflow:

1. Fetch key macro indicators for USA (and other countries if specified in $ARGUMENTS):
   - GDP growth (gdp_growth_annual)
   - Inflation / CPI (inflation_consumer_prices_annual)
   - Unemployment (unemployment_total_percent)
   - Real interest rate (real_interest_rate)
   - Trade balance / net exports (net_trades_goods_services — absolute USD, not % of GDP)
   - Government debt (debt_percent_gdp — central govt debt, % of GDP)

2. Fetch US Treasury yield curve:
   - Bill rates (ust/bill-rates)
   - Yield curve rates (ust/yield-rates)
   - Real yield rates (ust/real-yield-rates)

3. Fetch upcoming economic events (`economic-events`). **Always pass an explicit date window and country** —
   e.g. `--from-date <today> --to-date <today+14d> --country US` — otherwise the API returns arbitrary
   far-future events with empty fields. Field mapping (the API does NOT use `event`/`forecast` keys):
   - event name → `type`
   - forecast/consensus → `estimate`
   - previous → `previous`, actual → `actual` (null for not-yet-released)

Present:
- **Key Indicators Table** with latest value, previous, YoY change, trend arrow
- **Yield Curve Table** with all standard maturities + 2Y-10Y spread + curve shape assessment
- **Real Yields** — inflation-adjusted yields for 5Y, 10Y, 30Y
- **Upcoming Economic Events** — next 10 events with date, country, forecast, previous
- **Economic Narrative** — 3-5 bullet point summary of current economic state

If $ARGUMENTS specifies countries (e.g., "USA vs EU" or "G7"), include multi-country comparison.

Include disclaimer: "This is not financial advice. Data is for informational purposes only."
