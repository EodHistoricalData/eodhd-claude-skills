# CLAUDE.md

## Project Overview

EODHD Claude Skills — a skill adapter enabling AI agents (Claude Code, Codex) to work with the [EODHD financial data API](https://eodhd.com/). Distributed as a Claude Code plugin (`Enlavan/eodhd-claude-skills`).

The project is primarily documentation: markdown reference files covering 70+ API endpoints, general guides, and analysis workflows. It also includes a lightweight Python client and adapter configs.

## Structure

```
skills/eodhd-api/
  SKILL.md                    # Skill definition — triggers, workflow, supported endpoints
  references/
    general/                  # General guides (symbol format, exchanges, rate limits, etc.)
    endpoints/                # One .md per API endpoint (~73 files)
    workflows.md              # Analysis patterns
  scripts/
    eodhd_client.py           # Python API client (stdlib-only, no external deps)
  templates/
    analysis_report.md        # Output template
adapters/
  claude/eodhd-api.md         # Claude adapter guide
  codex/eodhd-api.md          # Codex adapter guide
```

## Key References

- `skills/eodhd-api/references/general/exchanges.md` — canonical list of supported exchange codes
- `skills/eodhd-api/references/general/symbol-format.md` — ticker format rules
- `skills/eodhd-api/references/general/rate-limits.md` — API quotas, Marketplace limits
- `skills/eodhd-api/references/general/update-times.md` — data update schedules
- `skills/eodhd-api/references/endpoints/README.md` — endpoint index

## Conventions

### Documentation

- Endpoint docs follow a standard template: Status header, Purpose, Parameters, Response shape, Example Requests, Notes, HTTP Status Codes
- When updating a fact, check consistency across related files (the same info may appear in general guides, endpoint docs, and examples)
- `exchanges.md` is the source of truth for valid exchange codes
- `symbol-format.md` is the source of truth for ticker formatting rules

### Python Client

- `eodhd_client.py` is **stdlib-only** — no `requests`, `pandas`, or other external packages
- API token comes from `EODHD_API_TOKEN` environment variable
- Outputs JSON to stdout

### Git

- Main branch: `main`
- Version bumps in `.claude-plugin/marketplace.json`
