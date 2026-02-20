# Workflow Recipes

## A) Single-ticker historical + fundamentals snapshot
1. Pull EOD data for a bounded date range.
2. Pull fundamentals for the same symbol.
3. Compute simple descriptive metrics:
   - period return,
   - realized volatility proxy from close-to-close returns,
   - latest valuation fields present in fundamentals.
4. Summarize risks and limitations.

## B) Cross-sectional screener -> short list
1. Define universe (exchange or pre-specified list).
2. Call screener with valuation/profitability filters.
3. Pull lightweight quote/EOD context for top candidates.
4. Present ranked table + one-line rationale per symbol.

## C) Event window check with intraday bars
1. Identify event date/time.
2. Pull intraday bars in pre/post windows.
3. Aggregate response metrics (move, volatility, volume shift).
4. Highlight anomalies and missing intervals.

## D) Macro overlay (if endpoint/plan allows)
1. Pull instrument history.
2. Pull macro series for matching date range.
3. Align frequencies and missing dates.
4. Report directional co-movement only unless deeper stats requested.

## Quality checklist
- Symbol suffix/exchange correctness confirmed.
- Timezone assumptions explicitly stated.
- Missing values handled (drop, forward-fill, or mark unknown).
- Output includes exact calls/parameters for reproducibility.
