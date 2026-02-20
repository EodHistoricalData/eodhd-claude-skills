# EODHD API Versioning & Changes

This document describes the EODHD API's versioning policy and stability guarantees.

## Current Approach

EODHD follows a **backwards-compatible update** approach. All changes to the API preserve existing functionality. There is no formal URL-based versioning scheme (e.g., `/v1/`, `/v2/`).

This means:

- **Existing integrations are not broken** by updates
- New fields may be added to response objects over time
- New endpoints may be introduced
- Existing fields and endpoints are not removed or renamed

## What This Means for Your Code

- Tolerate **new fields** appearing in JSON responses — do not fail on unknown fields
- Existing fields will not change type or be removed
- Endpoint URLs remain stable
- Query parameters remain stable

## Breaking Changes (If They Occur)

In the rare event that a breaking change becomes necessary, the following process is intended:

1. **Impact analysis** — Identification of all affected endpoints and data fields
2. **Customer impact assessment** — Identification of affected users
3. **Migration path** — Design of a backward-compatible option or migration guide
4. **Customer notification** — Minimum 30 days advance notice
5. **Support period** — 90 days typical for migration assistance
6. **Deprecation headers** — Added to old version responses

## Recommendations

- Parse JSON responses flexibly — do not fail on unknown fields
- Subscribe to EODHD communications for change announcements
- Test with the `demo` API key when evaluating new features
- Contact support if you encounter unexpected response changes
