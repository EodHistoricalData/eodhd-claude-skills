---
name: eodhd-analyze
description: >-
  Comprehensive single-company analysis using EODHD data — profile,
  fundamentals, price action, news sentiment, insider activity, and technicals,
  presented as a structured company brief. Invoke as /eodhd-analyze <ticker>.
argument-hint: "<ticker or company name>"
---

Perform a comprehensive analysis of the company $ARGUMENTS using EODHD data.

Use the `company-brief` skill workflow:
1. Fetch company fundamentals (profile, valuation, financials)
2. Fetch recent price history (last 90 days)
3. Fetch recent news with sentiment (last 10 articles)
4. Fetch insider transactions (last 90 days)
5. Calculate key technical indicators (RSI, SMA 50/200)

Present the results as a structured company brief with:
- Company profile and business description
- Valuation snapshot table (P/E, P/S, P/B, EV/EBITDA, dividend yield)
- Financial highlights (revenue, margins, ROE, growth)
- Price action summary with 52-week context
- Top news headlines with sentiment
- Insider activity summary
- 3-5 key takeaways

If the ticker format is ambiguous, resolve it (e.g., "Apple" → AAPL.US, "BMW" → BMW.XETRA).

Include disclaimer: "This is not financial advice. Data is for informational purposes only."
