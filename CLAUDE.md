# EODHD Claude Skills

## Overview

Plugin enabling AI agents (Claude Code, Codex) to work with the [EODHD financial data API](https://eodhd.com/). Distributed as a Claude Code plugin (`EodHistoricalData/eodhd-claude-skills`). Version: **0.5.2**.

Includes MCP Server connector (OAuth), 13 skills (1 core + 7 workflow + 5 user-facing commands), financial analyst agent, 72 endpoint docs, 28 general guides, and a stdlib-only Python client. As of v0.5.2 the user commands (`eodhd-analyze` etc.) live under `skills/` as standard skills and are invoked namespaced (e.g. `/eodhd-api:eodhd-analyze`) — the legacy `commands/` directory was removed because its flat files did not load as usable commands in a live session on newer Claude Code (verified live on 2.1.158 and 2.1.161: all 13 skills load).

## File Structure

```
.claude-plugin/
  marketplace.json              # Plugin manifest (name, version, skills list)
  plugin.json                   # Extended plugin metadata (keywords, author, license)
.mcp.json                       # MCP Server connector → mcpv2.eodhd.dev/v2/mcp
agents/
  financial-analyst.md          # Financial analyst agent definition
skills/                         # All skills incl. user commands (auto-discovered)
  eodhd-analyze/SKILL.md        # /eodhd-api:eodhd-analyze <ticker>
  eodhd-compare/SKILL.md        # /eodhd-api:eodhd-compare <ticker1> <ticker2>
  eodhd-market/SKILL.md         # /eodhd-market
  eodhd-screen/SKILL.md         # /eodhd-screen <criteria>
  eodhd-macro/SKILL.md          # /eodhd-macro
  eodhd-api/                    # Core skill — full API access (30+ client endpoints)
    SKILL.md
    references/
      general/                  # 28 general guides
      endpoints/                # 72 endpoint docs
      subscriptions/            # 7 subscription plans
      workflows.md              # 4 analysis patterns
    scripts/
      eodhd_client.py           # Python client (stdlib-only, ~495 lines)
      market_cap_series.py
      test_investverte_*.py
    templates/
      analysis_report.md
  company-brief/SKILL.md        # Company snapshot workflow
  earnings-monitor/SKILL.md     # Earnings tracking workflow
  market-overview/SKILL.md      # Market summary workflow
  portfolio-risk/SKILL.md       # Risk analysis workflow
  stock-screener/SKILL.md       # Stock screening workflow
  macro-dashboard/SKILL.md      # Macro-economic dashboard
  options-analyzer/SKILL.md     # Options analysis workflow
adapters/
  claude/eodhd-api.md
  codex/eodhd-api.md
registry/
  capabilities.json             # Single source of truth for all endpoints (75 entries)
  build.py                      # Generates support-matrix.md; --check for CI freshness
  README.md                     # Registry schema + workflow
```

## Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| marketplace.json | Plugin manifest (version, skills list) | `.claude-plugin/marketplace.json` |
| plugin.json | Extended metadata (keywords, author, license) | `.claude-plugin/plugin.json` |
| .mcp.json | MCP Server connector (OAuth HTTP) | `.mcp.json` |
| Core SKILL.md | Full API skill (triggers, workflow, guardrails) | `skills/eodhd-api/SKILL.md` |
| Workflow skills (7) | Curated analysis workflows | `skills/*/SKILL.md` |
| Financial analyst | Agent definition | `agents/financial-analyst.md` |
| Slash commands (5) | User-facing commands (standard skills, invoked `/eodhd-api:<name>`) | `skills/eodhd-{analyze,compare,market,screen,macro}/SKILL.md` |
| eodhd_client.py | Stdlib-only Python client, 31 endpoints | `skills/eodhd-api/scripts/eodhd_client.py` |
| Endpoint docs | Per-endpoint API reference | `skills/eodhd-api/references/endpoints/` |
| General guides | Cross-cutting topics | `skills/eodhd-api/references/general/` |
| Capabilities registry | Machine-readable source of truth for endpoints + support tiers | `registry/capabilities.json` |
| Support matrix | Generated agent-facing endpoint/tier table | `skills/eodhd-api/references/general/support-matrix.md` |

## Development Setup

1. Clone: `git clone https://github.com/EodHistoricalData/eodhd-claude-skills.git`
2. Set token: `export EODHD_API_TOKEN="your_token_here"`
3. Test client: `python skills/eodhd-api/scripts/eodhd_client.py --endpoint exchanges-list`

Or install as Claude Code plugin:
```bash
/plugin marketplace add EodHistoricalData/eodhd-claude-skills
/plugin install eodhd-api@eodhd-claude-skills
```

## Testing

```bash
python skills/eodhd-api/scripts/eodhd_client.py --endpoint exchanges-list
python skills/eodhd-api/scripts/eodhd_client.py --endpoint eod --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-01-31
```

Automated tests live in `tests/` (stdlib-only, no pytest dependency):
- `tests/test_python_client.py` — 30 e2e cases hitting every endpoint in `SUPPORTED_ENDPOINTS` against the live API. Requires `EODHD_API_TOKEN`.
- `tests/test_mcp_v1.py` — MCP protocol e2e: v2 OAuth challenge, v1 initialize/tools-list/tools-call.
- `tests/test_skill_references.py` — static cross-reference validation (SKILL.md frontmatter, endpoint docs, slash commands, agent frontmatter, manifest tool count vs MCP).
- `tests/test_registry.py` — static parity: registry ↔ client `SUPPORTED_ENDPOINTS`, registry ↔ endpoint docs, validated-tier ↔ e2e cases, and support-matrix freshness. Stdlib-only, runs in CI.

CI (`.github/workflows/validate.yml`) runs the static suite on every push/PR. The two e2e suites run automatically when `EODHD_API_TOKEN` is configured as a GitHub Actions secret; otherwise the e2e job emits a skip warning and the CI passes (no false negatives).

## Deployment

No runtime deployment. Distributed via GitHub releases.

- Version bumps: edit `version` in `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`
- Auto-release: `.github/workflows/release.yml` triggers on version bump
- Users install/update via Claude Code plugin system

## Conventions

### Documentation
- Endpoint docs follow standard template: Purpose, Parameters, Response, Examples, Notes
- `exchanges.md` = source of truth for exchange codes
- `symbol-format.md` = source of truth for ticker formatting

### Python Client
- `eodhd_client.py` is **stdlib-only** — no external packages
- Token from `EODHD_API_TOKEN` env var
- JSON stdout, exit codes: 0=success, 1=API error, 2=client error

### Skills
- Each workflow skill has YAML frontmatter (name, description, version)
- Skills reference endpoints from `../eodhd-api/references/endpoints/`
- Skills include output structure templates and endpoint cost tables

### Git
- Main branch: `main`
- Commit style: imperative, descriptive
- Version in marketplace.json and plugin.json must stay in sync

## Related

- GitHub: https://github.com/EodHistoricalData/eodhd-claude-skills
- EODHD API: https://eodhd.com/financial-apis/
- MCP Server: https://mcpv2.eodhd.dev/v2/mcp
