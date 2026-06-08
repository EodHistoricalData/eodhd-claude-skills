---
name: eodhd-screen
description: >-
  Screen stocks by fundamental and technical criteria using the EODHD screener —
  market cap, P/E, dividend yield, sector, exchange, and signals, with currency-
  aware thresholds. Invoke as /eodhd-screen <criteria>.
argument-hint: "<criteria, e.g. high dividend large cap US>"
---

Screen stocks using EODHD screener based on these criteria: $ARGUMENTS

Translate the user's criteria into EODHD screener filters.

**Filter format (critical):** `filters` is a **JSON array of `[field, operation, value]` triples**, NOT
dot-notation and NOT a JSON object. A JSON object is rejected with HTTP 422 ("must be an array").
Operations: `=`, `!=`, `>`, `>=`, `<`, `<=`, `match`.

**Sort format:** `--sort field.direction`, e.g. `market_capitalization.desc` or `pe.asc`. A bare field name
(or a separate order flag) is rejected with HTTP 422 ("sort.0.direction is required").

**Currency caveat (important):** absolute-money fields — `market_capitalization`, `revenue`, `ebitda` — are
reported in each listing's **local currency**, not normalized to USD. So a raw threshold leaks huge non-USD
companies (e.g. a Vietnam-listed firm shows "3.88T" ₫ ≈ $150M but passes a `>= 10B` filter). Each result row
carries a `currency_symbol` field telling you the currency. Therefore:
- When filtering/sorting by an absolute-money field, **scope to one market** — add `["exchange","=","us"]`
  (or the user's intended exchange) so the threshold is currency-consistent.
- For multi-market screens, you cannot compare raw caps across rows — group/label by `currency_symbol`.
- Ratio/percent fields (`pe`, `pb`, `ps`, `peg`, `roe`, `roa`, `beta`, `dividend_yield`) are currency-independent and safe to compare across markets.

**Instrument-type noise (important — the screener has NO `type` filter):** there is no field to restrict
results to common stock. Passing `["type", ...]` is rejected with HTTP 422 (`filters.0.field is invalid`).
Two kinds of junk leak into unscoped screens, especially dividend screens:
- **OTC / foreign cross-listings** — the combined `["exchange","=","us"]` virtual exchange *includes* OTC
  grey-market listings (codes ending in `F`/`Y`, e.g. `TCANF`, `RNECF`) with broken `dividend_yield`
  (55–110%). **Scope to a real venue instead** — `["exchange","=","nyse"]` or `["exchange","=","nasdaq"]`
  — to drop them. (`us` is still fine when you only need currency consistency, not clean common stock.)
- **Preferred shares / baby bonds** — these list on NYSE/NASDAQ too, carry a `-` in `code`
  (e.g. `JPM-PD`, `DLR-PJ`) and a coupon rate in `name`, and dominate high-yield screens. The API can't
  filter them, so **post-filter the results**: for a common-stock screen, drop rows whose `code` contains `-`.
- **Sanity-cap broken yields** — for any dividend screen add `["dividend_yield","<=",0.25]` (no real common
  stock yields >25%) to discard rows with corrupt data.

Common mappings (note: `dividend_yield` is a **fraction** — 0.03 = 3%):
- "large cap" → `["market_capitalization",">=",10000000000]`
- "mid cap" → `["market_capitalization",">=",2000000000],["market_capitalization","<=",10000000000]`
- "small cap" → `["market_capitalization","<=",2000000000]`
- "high dividend" → `["dividend_yield",">=",0.03],["dividend_yield","<=",0.25]` (upper cap drops broken-data OTC/preferred rows)
- "low P/E" or "cheap" → `["pe",">",0],["pe","<",15]` + `--sort pe.asc`
- "tech" → `["sector","=","Technology"]`
- "healthcare" → `["sector","=","Healthcare"]`
- US stocks → `["exchange","=","nyse"]` or `["exchange","=","nasdaq"]` for clean common stock (avoids OTC junk); use `["exchange","=","us"]` only when you need currency consistency, not a clean instrument set
- Sector names, industry names, exchange codes as additional `[field,"=",value]` triples

Example: "high dividend large cap (US)" →
`--filters '[["dividend_yield",">=",0.03],["dividend_yield","<=",0.25],["market_capitalization",">=",10000000000],["exchange","=","nyse"]]' --sort dividend_yield.desc`
(then drop result rows whose `code` contains `-` — those are preferred shares, not common stock)

Use the `stock-screener` skill workflow:
1. Run screener with translated filters (limit 20)
2. Unless the user explicitly wants preferred shares/ETFs, drop result rows whose `code` contains `-`
   (preferred shares) before presenting — the API has no instrument-type filter to do this server-side
3. For top 5-10 results, fetch fundamentals for deeper detail
4. Fetch recent price data for performance context

Present:
- **Filters Applied** — show the JSON filter used
- **Results Table** — ticker, name, sector, market cap (with its `currency_symbol`), P/E, dividend yield, price, 30d change. Show the currency next to any cap/revenue figure; never present a non-USD cap as if it were USD.
- **Top 5 Deep Dive** — expanded valuation and growth metrics for best matches
- **Summary** — key themes and patterns in results

If criteria are vague, ask for clarification or suggest reasonable defaults.

Include disclaimer: "This is not financial advice. Data is for informational purposes only."
