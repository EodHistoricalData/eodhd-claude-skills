# Claude Adapter: eodhd-api

Use this adapter when operating in Claude-style environments with local skills support.

## Registration

| Setting | Value |
|---------|-------|
| Skill name | `eodhd-api` |
| Entry file | `skills/eodhd-api/SKILL.md` |
| Helper script | `skills/eodhd-api/scripts/eodhd_client.py` |
| Token env var | `EODHD_API_TOKEN` |

## Setup

1. Set the API token environment variable:
   ```bash
   export EODHD_API_TOKEN="your_token_here"
   ```

2. Register the skill in your Claude environment by referencing the SKILL.md file.

## Prompting patterns

### Basic data retrieval
```
Use the `eodhd-api` skill. Pull daily prices for AAPL.US from 2025-01-01 to 2025-01-31.
```

### Fundamentals analysis
```
Use the `eodhd-api` skill. Get fundamentals for MSFT.US and summarize key valuation metrics.
```

### Multi-symbol comparison
```
Use the `eodhd-api` skill. Compare AAPL.US, MSFT.US, and GOOGL.US on P/E ratio,
revenue growth, and YTD performance. Present in a table.
```

### Technical analysis
```
Use the `eodhd-api` skill. Calculate 50-day and 200-day SMA for NVDA.US
and identify any crossover signals in the past month.
```

### Screening
```
Use the `eodhd-api` skill. Screen for US tech stocks with market cap > $100B,
P/E < 30, and positive YTD returns. Show top 10 by market cap.
```

### Event study
```
Use the `eodhd-api` skill. Pull intraday data for TSLA.US around the last
earnings announcement. Analyze price movement in the 2 hours before and after.
```

## Operational guidelines

1. **Start narrow**: Validate symbol and date range with a small initial pull
2. **Be explicit**: Specify exact parameters rather than relying on defaults
3. **Document everything**: Include commands used and note any data limitations
4. **Respect guardrails**: Never fabricate data; report failures with exact error
5. **Use templates**: Follow `templates/analysis_report.md` for consistent output

## Endpoint reference

Quick reference for common endpoints:

| Task | Endpoint | Example |
|------|----------|---------|
| Historical prices | `eod` | `--endpoint eod --symbol AAPL.US` |
| Intraday data | `intraday` | `--endpoint intraday --symbol AAPL.US --interval 5m` |
| Real-time quote | `real-time` | `--endpoint real-time --symbol AAPL.US` |
| Fundamentals | `fundamentals` | `--endpoint fundamentals --symbol AAPL.US` |
| News | `news` | `--endpoint news --symbol AAPL.US --limit 10` |
| Technical indicators | `technical` | `--endpoint technical --symbol AAPL.US --function sma --period 50` |
| Screening | `screener` | `--endpoint screener --limit 20` |
| Macro data | `macro-indicator` | `--endpoint macro-indicator --symbol USA` |

## Error handling

When API calls fail, Claude should:
1. Report the exact command that was attempted
2. Include the error message received
3. Suggest possible causes (invalid symbol, date range, missing token)
4. Offer alternative approaches if applicable

## References

- Full skill definition: `skills/eodhd-api/SKILL.md`
- Endpoint specifications: `skills/eodhd-api/references/endpoints/`
- Workflow recipes: `skills/eodhd-api/references/workflows.md`
- Output template: `skills/eodhd-api/templates/analysis_report.md`
