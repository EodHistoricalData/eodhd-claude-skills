# Codex Adapter: eodhd-api

Use this adapter in Codex environments that support tool-assisted or script-assisted workflows.

## Registration

| Setting | Value |
|---------|-------|
| Skill folder | `skills/eodhd-api` |
| Primary guide | `skills/eodhd-api/SKILL.md` |
| Helper script | `skills/eodhd-api/scripts/eodhd_client.py` |
| Token env var | `EODHD_API_TOKEN` |

## Setup

1. Set the API token:
   ```bash
   export EODHD_API_TOKEN="your_token_here"
   ```

2. Verify the client works:
   ```bash
   python skills/eodhd-api/scripts/eodhd_client.py --endpoint exchanges-list
   ```

## Execution flow

1. **Read skill definition**: `skills/eodhd-api/SKILL.md`
2. **Identify endpoint**: Reference `references/endpoints.md` or individual endpoint docs
3. **Execute API call**: Use helper script or construct curl command
4. **Process response**: Parse JSON, handle errors
5. **Format output**: Use `templates/analysis_report.md` for structure

## Example commands

### Historical prices
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint eod \
  --symbol AAPL.US \
  --from-date 2025-01-01 \
  --to-date 2025-01-31
```

### Intraday data
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint intraday \
  --symbol NVDA.US \
  --interval 5m \
  --from-date 2025-01-15
```

### Company fundamentals
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint fundamentals \
  --symbol MSFT.US
```

### Technical indicators
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint technical \
  --symbol AAPL.US \
  --function rsi \
  --period 14
```

### Company news
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint news \
  --symbol TSLA.US \
  --limit 10
```

### Stock screening
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint screener \
  --limit 20
```

### Macro indicators
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint macro-indicator \
  --symbol USA \
  --indicator gdp_growth_annual
```

### Earnings calendar
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint calendar/earnings \
  --from-date 2025-01-01 \
  --to-date 2025-01-31
```

### Exchange listings
```bash
python skills/eodhd-api/scripts/eodhd_client.py \
  --endpoint exchange-symbol-list \
  --symbol US
```

## Script arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `--endpoint` | API endpoint to query | Yes |
| `--symbol` | Ticker (e.g., AAPL.US) or exchange code | Depends on endpoint |
| `--from-date` | Start date (YYYY-MM-DD) | Optional |
| `--to-date` | End date (YYYY-MM-DD) | Optional |
| `--interval` | Intraday interval (1m, 5m, 1h) | For intraday |
| `--function` | Technical indicator (sma, ema, rsi, etc.) | For technical |
| `--period` | Indicator period | For technical |
| `--indicator` | Macro indicator code | For macro-indicator |
| `--limit` | Result limit | Optional |
| `--offset` | Pagination offset | Optional |
| `--filter` | Filter parameter | Optional |
| `--timeout` | HTTP timeout seconds | Optional (default 30) |
| `--raw` | Output raw response | Optional |

## Processing patterns

### Extract specific fields with jq
```bash
# Get just the closing prices
python eodhd_client.py --endpoint eod --symbol AAPL.US | jq '.[].close'

# Get fundamentals highlights
python eodhd_client.py --endpoint fundamentals --symbol AAPL.US | jq '.Highlights'

# Get news headlines
python eodhd_client.py --endpoint news --symbol AAPL.US --limit 5 | jq '.[].title'
```

### Combine multiple calls
```bash
# Compare multiple symbols
for symbol in AAPL.US MSFT.US GOOGL.US; do
  echo "=== $symbol ==="
  python eodhd_client.py --endpoint fundamentals --symbol $symbol | \
    jq '{symbol: .General.Code, pe: .Highlights.PERatio, marketCap: .Highlights.MarketCapitalization}'
done
```

## Error codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | API error (HTTP error, network failure) |
| 2 | Client error (missing token, invalid arguments) |

## References

- Full endpoint docs: `skills/eodhd-api/references/endpoints/`
- Workflow recipes: `skills/eodhd-api/references/workflows.md`
- Output template: `skills/eodhd-api/templates/analysis_report.md`
