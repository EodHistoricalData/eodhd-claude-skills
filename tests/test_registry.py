#!/usr/bin/env python3
"""Parity + self-consistency checks for registry/capabilities.json.

Stdlib-only, no network. Asserts the registry stays in sync with the Python
client (SUPPORTED_ENDPOINTS), the e2e test (CASES), and the endpoint docs.
Exit 0 if clean, 1 on any failure.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "registry" / "capabilities.json"
EODHD_DIR = REPO_ROOT / "skills" / "eodhd-api"
CLIENT = EODHD_DIR / "scripts" / "eodhd_client.py"
E2E = REPO_ROOT / "tests" / "test_python_client.py"
ENDPOINTS_DIR = EODHD_DIR / "references" / "endpoints"
BUILD = REPO_ROOT / "registry" / "build.py"

REQUIRED_FIELDS = ["id", "path", "transport", "support_tier", "client_endpoint",
                   "required_params", "optional_params", "aliases",
                   "response_family", "doc_path"]
TRANSPORTS = {"rest", "websocket"}
TIERS = {"validated", "fallback", "documented"}
RESPONSE_FAMILIES = {"time-series", "fundamentals", "calendar", "listing", "quote",
                     "rates", "news", "sentiment", "esg", "risk-report", "options",
                     "macro", "reference", "account"}


def load_registry() -> list:
    return json.loads(REGISTRY.read_text())


def supported_endpoints() -> set:
    text = CLIENT.read_text()
    m = re.search(r"SUPPORTED_ENDPOINTS\s*=\s*\[(.*?)\]", text, re.DOTALL)
    return set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()


def e2e_tested_endpoints() -> set:
    """Names of client endpoints exercised by CASES (strips the '(sma)' suffix)."""
    text = E2E.read_text()
    names = re.findall(r'\(\s*"([^"]+)"\s*,\s*\[', text)
    return {n.split("(")[0] for n in names}


def client_sets() -> dict:
    """Extract the client's endpoint-family sets (param-style classification)."""
    text = CLIENT.read_text()

    def extract(name: str) -> set:
        m = re.search(name + r"\s*=\s*\{(.*?)\}", text, re.DOTALL)
        return set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()

    return {
        "filter": extract("FILTER_API_ENDPOINTS"),
        "filter_no_page": extract("FILTER_NO_PAGINATION_ENDPOINTS"),
        "sanctions": extract("SANCTIONS_API_ENDPOINTS"),
        "sanctions_no_param": extract("SANCTIONS_NO_PARAM_ENDPOINTS"),
    }


def check_well_formed(reg) -> list:
    fails = []
    seen = set()
    for i, e in enumerate(reg):
        where = e.get("id", f"index {i}")
        for f in REQUIRED_FIELDS:
            if f not in e:
                fails.append(f"{where}: missing field '{f}'")
        if e.get("transport") not in TRANSPORTS:
            fails.append(f"{where}: transport '{e.get('transport')}' invalid")
        if e.get("support_tier") not in TIERS:
            fails.append(f"{where}: support_tier '{e.get('support_tier')}' invalid")
        if e.get("response_family") not in RESPONSE_FAMILIES:
            fails.append(f"{where}: response_family '{e.get('response_family')}' invalid")
        for lf in ("required_params", "optional_params", "aliases"):
            if not isinstance(e.get(lf), list):
                fails.append(f"{where}: '{lf}' must be a list")
        ce = e.get("client_endpoint", "__MISSING__")
        if ce != "__MISSING__" and ce is not None and not isinstance(ce, str):
            fails.append(f"{where}: client_endpoint must be a string or null")
        eid = e.get("id")
        if eid in seen:
            fails.append(f"{where}: duplicate id '{eid}'")
        seen.add(eid)
    return fails


def check_client_parity(reg) -> list:
    fails = []
    supported = supported_endpoints()
    if not supported:
        return ["could not extract SUPPORTED_ENDPOINTS from eodhd_client.py"]
    reg_client = {e["client_endpoint"] for e in reg if e.get("client_endpoint")}
    for ep in sorted(supported - reg_client):
        fails.append(f"SUPPORTED_ENDPOINTS '{ep}' has no registry entry")
    for ep in sorted(reg_client - supported):
        fails.append(f"registry client_endpoint '{ep}' not in SUPPORTED_ENDPOINTS")
    counts = {}
    for e in reg:
        ce = e.get("client_endpoint")
        if ce:
            counts[ce] = counts.get(ce, 0) + 1
    for ce, n in sorted(counts.items()):
        if n > 1:
            fails.append(f"client_endpoint '{ce}' mapped by {n} entries (must be exactly 1)")
    return fails


def check_doc_parity(reg) -> list:
    fails = []
    available = {p.name for p in ENDPOINTS_DIR.glob("*.md")} - {"README.md"}
    referenced = set()
    for e in reg:
        doc = e.get("doc_path", "")
        if not doc or not (EODHD_DIR / doc).exists():
            fails.append(f"{e.get('id')}: doc_path '{doc}' does not exist")
        else:
            referenced.add(Path(doc).name)
    for orphan in sorted(available - referenced):
        fails.append(f"endpoint doc '{orphan}' is not referenced by any registry entry")
    return fails


def check_tiers(reg) -> list:
    fails = []
    tested = e2e_tested_endpoints()
    for e in reg:
        where = e.get("id")
        tier = e.get("support_tier")
        ce = e.get("client_endpoint")
        if tier == "documented" and ce is not None:
            fails.append(f"{where}: tier 'documented' but client_endpoint='{ce}' (must be null)")
        if tier in ("validated", "fallback") and not ce:
            fails.append(f"{where}: tier '{tier}' requires a non-null client_endpoint")
        if tier == "validated" and ce and ce not in tested:
            fails.append(f"{where}: tier 'validated' but no e2e case for '{ce}'")
    return fails


def check_client_registry_style(reg) -> list:
    """Guard against drift between the client's param-style sets and the
    registry's optional_params (the exact drift that produced the original
    cds-market and programs/sources defects)."""
    fails = []
    sets = client_sets()
    if not (sets["filter"] or sets["sanctions"]):
        return ["could not extract endpoint-family sets from eodhd_client.py"]
    by_ce = {e["client_endpoint"]: e for e in reg if e.get("client_endpoint")}

    stray = sets["filter_no_page"] - sets["filter"]
    if stray:
        fails.append(f"FILTER_NO_PAGINATION_ENDPOINTS not subset of FILTER_API_ENDPOINTS: {sorted(stray)}")
    stray_s = sets["sanctions_no_param"] - sets["sanctions"]
    if stray_s:
        fails.append(f"SANCTIONS_NO_PARAM_ENDPOINTS not subset of SANCTIONS_API_ENDPOINTS: {sorted(stray_s)}")

    for ce in sorted(sets["filter"] | sets["sanctions"]):
        e = by_ce.get(ce)
        if not e:
            fails.append(f"client family set contains '{ce}' with no registry entry")
            continue
        opt = e.get("optional_params", [])
        non_page = [p for p in opt if not p.startswith("page[")]
        has_page = any(p.startswith("page[") for p in opt)
        if ce in sets["sanctions_no_param"]:
            if opt:
                fails.append(f"{ce}: no-param endpoint but registry optional_params={opt} (expected [])")
        elif ce in sets["filter"]:
            if non_page and not all(p.startswith("filter[") for p in non_page):
                fails.append(f"{ce}: FILTER_API endpoint but registry has non-filter params {non_page}")
            no_page = ce in sets["filter_no_page"]
            if no_page and has_page:
                fails.append(f"{ce}: FILTER_NO_PAGINATION but registry lists page[...]")
            if not no_page and not has_page:
                fails.append(f"{ce}: filter endpoint expected page[...] in registry, found none")
        elif ce in sets["sanctions"]:  # entities/vessels — bare params
            if any(p.startswith("filter[") for p in non_page):
                fails.append(f"{ce}: sanctions bare endpoint but registry uses filter[...] {non_page}")
            if not has_page:
                fails.append(f"{ce}: sanctions entities/vessels expected page[...] in registry, found none")
    return fails


def check_matrix_fresh(reg) -> list:
    result = subprocess.run([sys.executable, str(BUILD), "--check"],
                            capture_output=True, text=True)
    if result.returncode != 0:
        return [(result.stderr or result.stdout).strip() or "support-matrix.md is stale"]
    return []


def main() -> int:
    reg = load_registry()
    sections = [
        ("Registry well-formed", check_well_formed),
        ("Client parity (SUPPORTED_ENDPOINTS)", check_client_parity),
        ("Doc parity (references/endpoints)", check_doc_parity),
        ("Tier earns its label", check_tiers),
        ("Client↔registry param-style consistency", check_client_registry_style),
        ("Support matrix freshness", check_matrix_fresh),
    ]
    all_fails = []
    for name, fn in sections:
        print(f"\n=== {name} ===")
        fails = fn(reg)
        if not fails:
            print("  ✓ OK")
        else:
            for f in fails:
                print(f"  ✗ {f}")
            all_fails.extend(fails)
    print("\n" + "=" * 80)
    print(f"Total failures: {len(all_fails)}")
    return 1 if all_fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
