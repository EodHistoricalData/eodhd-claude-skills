# Changelog

All notable changes to this plugin are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [0.4.4] — 2026-05-29

### Added
- `CHANGELOG.md` documenting the full release history.

### Changed
- `CLAUDE.md` "No test framework" note replaced with an explicit description of the three test suites in `tests/` and the conditional CI execution model.
- GitHub repository metadata: description, homepage, and topic tags set for marketplace discoverability.

## [0.4.3] — 2026-05-29

### Changed
- README disclaimer rewritten — replaced "may differ from API behavior, Claude may interpret incorrectly" with a scoped "Not financial advice; verify against eodhd.com" notice.
- README gains an **Access Tiers** section explaining what works on Free vs each EODHD paid plan vs Marketplace add-ons, so users can match workflows to their subscription before installing.

## [0.4.2] — 2026-05-29

### Added
- Test suite (`tests/`, stdlib-only):
  - `test_python_client.py` — 30 e2e cases against every endpoint in `SUPPORTED_ENDPOINTS`. Subscription-gated endpoints classified as SKIP, not FAIL.
  - `test_mcp_v1.py` — full MCP protocol e2e: v2 OAuth challenge, v1 `initialize` → `notifications/initialized` → `tools/list` → `tools/call`.
  - `test_skill_references.py` — static cross-reference validation.
- CI now runs the static validation suite on every push/PR; e2e runs when `EODHD_API_TOKEN` secret is configured.
- YAML frontmatter on `agents/financial-analyst.md` so the agent loader recognises it (same class of bug as the SKILL.md fix in PR #5).

### Fixed
- `skills/eodhd-api/scripts/eodhd_client.py`: `--endpoint intraday` now converts `YYYY-MM-DD` to Unix timestamps. EODHD's intraday endpoint rejects ISO dates with HTTP 422; this was a silent bug for every workflow that touched intraday data.
- `skills/eodhd-api/scripts/market_cap_series.py`:
  - `SharesOutstanding` is read from `SharesStats::*`, not `Highlights::*` (the latter returns `"NA"`).
  - Handles scalar return from `Field::Subfield` filter (was assuming a dict).
- `plugin.json` `capabilities.tools` and README claim updated from 75 → 80 to match the actual MCP v1 tool count (verified via `tools/list`).

## [0.4.1] — 2026-05-29

### Added
- `.github/workflows/validate.yml` — schema-validates `plugin.json` / `marketplace.json` / `.mcp.json` on push/PR; checks `plugin.json.repository` is a string (regression guard against issue #7), enforces version sync between manifests, validates SKILL.md frontmatter, and probes the MCP URL (`401`/`405` = ok, `404` = wrong domain → fail).
- `.github/workflows/release.yml` — on version bump in either manifest, auto-creates the matching git tag and GitHub Release with a changelog from commits since the previous tag.

### Fixed
- **MCP URL** in `.mcp.json`, `plugin.json`, README, and CLAUDE.md changed from `https://mcp.eodhd.dev/v2/mcp` (Cloudflare 404) to `https://mcpv2.eodhd.dev/v2/mcp` (live endpoint per EODHD docs). With the wrong URL the plugin installed but every MCP call failed.
- **Plugin manifest schema** (Issue [#7](https://github.com/EodHistoricalData/eodhd-claude-skills/issues/7)): `repository` field changed from npm-style object `{type, url}` to a plain URL string. The object form fails Claude Code's plugin schema validator and blocked `/plugin install eodhd-api@eodhd-claude-skills` entirely.

## [0.4.0] — 2026-05-09

Initial public release.

- `.claude-plugin/plugin.json` + `marketplace.json` manifests.
- MCP Server v2 connector (OAuth) — 75 tools claimed (actually 80, see 0.4.2).
- 8 skills: 1 core `eodhd-api` + 7 curated workflows (`company-brief`, `earnings-monitor`, `market-overview`, `portfolio-risk`, `stock-screener`, `macro-dashboard`, `options-analyzer`).
- 1 agent: `financial-analyst`.
- 5 slash commands: `/eodhd-analyze`, `/eodhd-compare`, `/eodhd-market`, `/eodhd-screen`, `/eodhd-macro`.
- Stdlib-only Python client (`eodhd_client.py`), 72 endpoint docs, 28 general guides.
- Claude and Codex adapters in `adapters/`.
