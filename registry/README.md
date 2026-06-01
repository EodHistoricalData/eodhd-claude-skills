# Endpoint Capabilities Registry

`capabilities.json` is the single source of truth for every EODHD endpoint this plugin
knows about. Tooling and CI read it; do not let the client, docs, or tests drift from it.

## Entry schema

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable kebab id (unique). |
| `path` | string | API path template, e.g. `/eod/{symbol}`. |
| `transport` | `rest` \| `websocket` | How the endpoint is called. |
| `support_tier` | `validated` \| `fallback` \| `documented` | See tiers below. |
| `client_endpoint` | string \| null | `--endpoint` value in `eodhd_client.py`, or `null` if curl-only. |
| `required_params` | string[] | API params always required (excludes `api_token`, `fmt`). |
| `optional_params` | string[] | API params accepted but optional. |
| `aliases` | string[] | Alternate names (doc slug, API-name variants). |
| `response_family` | enum | Response-shape grouping. |
| `doc_path` | string | Doc path relative to `skills/eodhd-api/`. |

## Support tiers

- **validated** — in `eodhd_client.py` `SUPPORTED_ENDPOINTS` and covered by a passing case in
  `tests/test_python_client.py`. Prefer these.
- **fallback** — in the client but not e2e-verified (e.g. subscription-gated). Works; verify
  the response shape.
- **documented** — `client_endpoint: null`; call via `curl` per the endpoint doc.

## Workflow

1. Edit `capabilities.json`.
2. Run `python registry/build.py` to regenerate
   `skills/eodhd-api/references/general/support-matrix.md`.
3. Run `python tests/test_registry.py` until green.

CI (`.github/workflows/validate.yml`) runs `test_registry.py` on every push/PR.
