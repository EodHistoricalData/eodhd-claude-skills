# Changelog

All notable changes to this plugin are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed
- **Insider Transactions reference** rewritten to document the SEC **Form 4** endpoint
  `/api/sec-filings/{symbol}/form4` (nested non-derivative/derivative/footnote schema, EDGAR-sourced,
  pagination, 10 calls) as the recommended source, alongside the legacy flat `/api/insider-transactions`
  feed. Verified live: the two feeds differ in coverage (e.g. `AAPL.US` is empty on the legacy feed
  but populated via Form 4). Closes community report on stale endpoint references.
- **Fundamentals reference** updated for the **v1.1** endpoint (`/api/v1.1/fundamentals/{SYMBOL}`):
  `Earnings.Trend` is now split into `Quarterly`/`Annual` with `fiscalQuarter` and `type` fields;
  added the previously-undocumented top-level sections (`Technicals`, `SplitsDividends`,
  `AnalystRatings`, `Holders`, `InsiderTransactions`, `ESGScores`) to the response shape; documented
  the `::` nested-filter syntax. Both v1.1 and the legacy `/api/fundamentals` shapes are shown.

## [0.5.2] — 2026-06-03

### Fixed
- **Plugin loaded only 5 skills and slash commands did not register on newer Claude Code (2.1.16x)** (EODHD-1524, surfaced by QA). Root cause: the plugin shipped BOTH a legacy `commands/` directory (5 flat files) and a modern `skills/` directory (8). `claude plugin details` merges them (reports 13), but the in-session loader on newer Claude Code resolved only the flat `commands/` files (5) and did not register them as `/`-commands — so `/eodhd-analyze` returned "Unknown command".

### Changed
- Consolidated all components into `skills/`. Migrated the 5 slash commands (`eodhd-analyze`, `eodhd-compare`, `eodhd-macro`, `eodhd-market`, `eodhd-screen`) from flat `commands/*.md` into `skills/<name>/SKILL.md` as standard skills with YAML frontmatter (`name`, `description`, `argument-hint`), and removed the legacy `commands/` directory. Per the Claude Code plugin docs, `skills/` is the supported directory for new plugins; consolidating removes the dual-directory ambiguity that broke loading.
- **Verified in a live session** (not just `claude plugin details`): on Claude Code **2.1.158 AND 2.1.161** all **13 skills load** (namespaced `eodhd-api:<name>`), including the 5 `eodhd-*` commands. On v0.5.1 the same live probe loaded only the 8 `skills/` entries — the flat `commands/*.md` files did **not** load as usable commands, which is why `/eodhd-analyze` returned "Unknown command". Commands are now invoked namespaced, e.g. `/eodhd-api:eodhd-analyze`.

## [0.5.1] — 2026-06-03

### Fixed
- **Plugin loaded 0 skills and 0 slash commands** despite a clean `/doctor` (surfaced in v0.5.0 QA, EODHD-1524). Two packaging bugs:
  - **Name mismatch** — `plugin.json` declared `name: "eodhd-claude-skills"` while the marketplace entry declared the plugin as `eodhd-api`. The mismatch broke component binding, so convention-based discovery of `skills/` never ran. `plugin.json` `name` is now `eodhd-api` (matches the install identifier `eodhd-api@eodhd-claude-skills`); added `displayName: "EODHD Claude Skills"` to the marketplace entry for the UI label.
  - **Slash commands in the wrong directory** — commands lived in `.claude/commands/`, which is project-local config and is NOT discovered inside a plugin. Moved all 5 to `commands/` at the plugin root. `/eodhd-analyze` and the rest now register.
- Verified locally with `claude plugin details eodhd-api`: 13 skills (8 workflow + 5 commands) + 1 agent + 1 MCP server all load.

### Changed
- `tests/test_skill_references.py` now validates commands at `commands/` (was `.claude/commands/`); `CLAUDE.md` and `README.md` file-structure diagrams updated to match.

## [0.5.0] — 2026-06-01

### Fixed
- Plugin install failure (`conflicting manifests: both plugin.json and marketplace entry specify components`). The marketplace entry used `strict: false` while declaring a `skills` component array, conflicting with the components declared by `plugin.json` and directory conventions. Set the entry to `strict: true` and removed the redundant `skills` array — all skills, commands, the agent, and the MCP server now load via convention-based discovery.
## [0.4.5] — 2026-06-01

Repo-side fixes from the v0.4.2 manual QA pass (EODHD-1524), verified live against the production API.

### Fixed
- **Screener filters** — documented the correct request shape: `filters` must be a JSON array of `[field, operation, value]` triples (a JSON object is rejected with HTTP 422) and `sort` must be `field.direction` (e.g. `market_capitalization.desc`; a bare field name → HTTP 422). Corrected the wrong dot-notation/object mappings in the `eodhd-screen` command, `stock-screener` skill, and the endpoint reference. `dividend_yield` clarified as a fraction (0.03 = 3%).
- **macro-indicator** — the Python client now lowercases the API's PascalCase keys (`Date`/`Value`/`CountryCode` → `date`/`value`/`countrycode`) for consistency with every other endpoint.
- **UST rates** (`ust/*`) — the Python client now unwraps the `{meta, data, links}` envelope to the bare `data` array, so indexing like `data[-1]` works.
- **economic-events** — documented that the event name field is `type` (not `event`) and the forecast field is `estimate` (not `forecast`); workflows now pass an explicit date window and country to avoid empty far-future results.
- **Commodities** — `market-overview` switched gold/oil from the unreliable `GC.COMEX`/`CL.COMEX` futures symbols to liquid ETF proxies `GLD.US`/`USO.US`.
- **options-analyzer** — removed the misleading "requires Marketplace subscription" note; US options endpoints are reachable on many paid plans.

### Changed
- **Currency handling in screener** — documented that absolute-money fields (`market_capitalization`, `revenue`, `ebitda`) are in each listing's local currency (rows carry a `currency_symbol`); skills now scope money thresholds to one market (`exchange=us`), label currency in output, and avoid cross-currency comparison.
- **README** — added a Troubleshooting section (macOS SSL certificate install, OAuth fallback via `EODHD_API_TOKEN`).

### Notes
- The MCP v2 OAuth login flow (PKCE) is fixed server-side (EODHD-1536) — unrelated to this plugin release.
- `eodhd_client.py` gains client-side response normalization; pass `--raw` to bypass it and see the exact API payload.

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
