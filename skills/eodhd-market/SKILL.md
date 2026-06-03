---
name: eodhd-market
description: >-
  Comprehensive market overview using EODHD data — major indices, sector
  performance, Treasury yield curve, macro snapshot, and commodities.
  Invoke as /eodhd-market [region].
argument-hint: "[optional region, e.g. Europe, Asia]"
---

Generate a comprehensive market overview using EODHD data.

Use the `market-overview` skill workflow:

1. Fetch major US indices: S&P 500 (GSPC.INDX), Nasdaq (IXIC.INDX), Dow (DJI.INDX), Russell 2000 (RUT.INDX)
2. Fetch sector ETF performance: XLK, XLF, XLV, XLE, XLI, XLY, XLP, XLU, XLRE, XLB, XLC
3. Fetch US Treasury yield curve (ust/yield-rates) — latest data
4. Fetch key macro indicators for USA — GDP growth, CPI, unemployment
5. Fetch commodity prices via liquid ETF proxies — Gold (GLD.US), Crude Oil (USO.US). The COMEX futures
   symbols (GC.COMEX, CL.COMEX) are unreliable on standard plans (empty array / error), so prefer the ETF
   proxies and note them as proxies in the output.

Present:
- **Major Indices** table with last price, daily change, % change
- **Sector Performance** table ranked by today's performance
- **Treasury Yield Curve** table with key maturities (1M, 3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y) + 2Y-10Y spread
- **Commodities** table
- **Macro Snapshot** with latest GDP, CPI, unemployment
- **Key Takeaways** — 3-5 bullet points on market themes

If $ARGUMENTS contains specific requests (e.g., "Europe" or "Asia"), include relevant international indices.

Include disclaimer: "This is not financial advice. Data is for informational purposes only."
