#!/usr/bin/env python3
"""Static validation of skill / slash-command / agent cross-references.

Checks:
  - Each SKILL.md has valid YAML frontmatter (name, description, version).
  - Endpoints referenced in SKILL.md (e.g., references/endpoints/foo.md) exist.
  - Python client examples (`eodhd_client.py --endpoint X`) use real endpoints
    from SUPPORTED_ENDPOINTS.
  - Slash commands reference real skills/agents.
  - plugin.json `capabilities.tools`, if declared, matches actual MCP v1 tools count
    (if env var set). The field is optional and non-standard, so the check skips when absent.

Stdlib-only. No network access required (unless EODHD_API_TOKEN is set,
then the MCP tool count is cross-checked too).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / "skills"
AGENTS = REPO_ROOT / "agents"
# User-facing slash commands are now first-class skills under skills/ (v0.5.2);
# the legacy commands/ directory was removed to avoid dual-directory load ambiguity.
COMMAND_SKILLS = {
    "eodhd-analyze", "eodhd-compare", "eodhd-macro", "eodhd-market", "eodhd-screen",
}
CLIENT = SKILLS / "eodhd-api" / "scripts" / "eodhd_client.py"


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    """Minimal stdlib YAML-frontmatter parser. Returns (frontmatter_dict, body)."""
    if not text.startswith("---"):
        return None, text
    end = text.find("---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].strip()
    fm: dict = {}
    current_key = None
    current_block: list[str] = []
    for line in fm_text.splitlines():
        # Multi-line scalar (`>-` or `|`)
        if current_key is not None and (line.startswith("  ") or line.startswith("\t")):
            current_block.append(line.strip())
            continue
        if current_key is not None:
            fm[current_key] = " ".join(current_block).strip()
            current_key = None
            current_block = []
        if ":" in line:
            k, _, v = line.partition(":")
            v = v.strip()
            if v in (">", "|", ">-", "|-"):
                current_key = k.strip()
                current_block = []
            else:
                fm[k.strip()] = v.strip(' "\'')
    if current_key is not None:
        fm[current_key] = " ".join(current_block).strip()
    return fm, text[end + 3:].lstrip()


def supported_endpoints() -> set[str]:
    """Extract SUPPORTED_ENDPOINTS from eodhd_client.py without importing it."""
    text = CLIENT.read_text(encoding="utf-8")
    m = re.search(r"SUPPORTED_ENDPOINTS\s*=\s*\[(.*?)\]", text, re.DOTALL)
    if not m:
        return set()
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def check_skill_frontmatter() -> list[str]:
    """Each SKILL.md must have name/description in frontmatter."""
    fails = []
    for skill in sorted(SKILLS.glob("*/SKILL.md")):
        fm, _ = parse_frontmatter(skill.read_text(encoding="utf-8"))
        if fm is None:
            fails.append(f"{skill.relative_to(REPO_ROOT)}: no YAML frontmatter")
            continue
        for required in ("name", "description"):
            if required not in fm:
                fails.append(f"{skill.relative_to(REPO_ROOT)}: missing '{required}'")
        # Name should match directory
        expected = skill.parent.name
        if fm.get("name") != expected:
            fails.append(f"{skill.relative_to(REPO_ROOT)}: name='{fm.get('name')}' != dir='{expected}'")
    return fails


def check_endpoint_references() -> list[str]:
    """SKILL.md may reference references/endpoints/<name>.md — must exist."""
    fails = []
    ENDPOINT_PATTERN = re.compile(r"references/endpoints/([\w\-/]+\.md)")
    endpoints_dir = SKILLS / "eodhd-api" / "references" / "endpoints"
    available = {p.name for p in endpoints_dir.glob("*.md")} if endpoints_dir.exists() else set()
    for md in sorted(SKILLS.glob("**/*.md")):
        text = md.read_text(encoding="utf-8")
        for ref in ENDPOINT_PATTERN.findall(text):
            base = Path(ref).name
            if base not in available:
                fails.append(f"{md.relative_to(REPO_ROOT)}: references missing endpoint doc '{ref}'")
    return fails


def check_client_examples() -> list[str]:
    """Examples like `eodhd_client.py --endpoint foo` must use real endpoints."""
    fails = []
    supported = supported_endpoints()
    if not supported:
        return ["could not extract SUPPORTED_ENDPOINTS from eodhd_client.py"]
    pattern = re.compile(r"eodhd_client\.py.*?--endpoint\s+(\S+)")
    for md in sorted(REPO_ROOT.glob("**/*.md")):
        if ".git" in md.parts or "node_modules" in md.parts:
            continue
        for endpoint in pattern.findall(md.read_text(encoding="utf-8")):
            # Strip trailing quotes/punctuation
            endpoint = endpoint.strip('`",;)\'')
            if endpoint not in supported:
                fails.append(f"{md.relative_to(REPO_ROOT)}: --endpoint '{endpoint}' not in SUPPORTED_ENDPOINTS")
    return fails


def check_slash_commands() -> list[str]:
    """The user-facing slash commands are skills under skills/ (v0.5.2).
    Each must exist with valid frontmatter and reference only real skills."""
    fails = []
    available_skills = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}
    if not COMMAND_SKILLS.issubset(available_skills):
        missing = sorted(COMMAND_SKILLS - available_skills)
        fails.append(f"missing command skills under skills/: {missing}")
    # Guard against re-introducing the legacy dual directory.
    if (REPO_ROOT / "commands").exists():
        fails.append("legacy commands/ directory present — commands must live in skills/ (see v0.5.2)")
    for name in sorted(COMMAND_SKILLS & available_skills):
        skill_md = SKILLS / name / "SKILL.md"
        fm, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        if fm is None:
            fails.append(f"skills/{name}/SKILL.md: no frontmatter")
            continue
        for field in ("name", "description"):
            if field not in fm:
                fails.append(f"skills/{name}/SKILL.md: missing '{field}'")
        # Any skills/<name>/ references in the body must resolve.
        for skill_ref in re.findall(r"skills/([\w\-]+)/", body):
            if skill_ref not in available_skills:
                fails.append(f"skills/{name}/SKILL.md: references missing skill '{skill_ref}'")
    return fails


def check_agents() -> list[str]:
    """agents/*.md should have frontmatter."""
    fails = []
    if not AGENTS.exists():
        return ["no agents directory"]
    for agent in sorted(AGENTS.glob("*.md")):
        fm, _ = parse_frontmatter(agent.read_text(encoding="utf-8"))
        if fm is None:
            fails.append(f"{agent.relative_to(REPO_ROOT)}: no frontmatter")
            continue
        if "name" not in fm:
            fails.append(f"{agent.relative_to(REPO_ROOT)}: missing 'name'")
    return fails


def check_manifest_capabilities() -> list[str]:
    """plugin.json claims a tool count; compare with MCP if token available."""
    fails = []
    plugin_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    with plugin_path.open(encoding="utf-8") as f:
        manifest = json.load(f)
    claimed = manifest.get("capabilities", {}).get("tools")
    if claimed is None:
        print("  (skipped - plugin.json declares no static tool count; "
              "`capabilities` removed for plugin-schema compliance)")
        return fails
    token = os.getenv("EODHD_API_TOKEN")
    if not token:
        print(f"  (skipped MCP tool-count check - no EODHD_API_TOKEN)")
        print(f"  plugin.json claims {claimed} tools")
        return fails
    # Actually fetch tool count
    import urllib.request
    try:
        url = f"https://mcp.eodhd.com/v1/mcp?apikey={token}"
        # initialize
        req = urllib.request.Request(url, data=json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                       "clientInfo": {"name": "t", "version": "1"}}
        }).encode(), headers={"Content-Type": "application/json",
                              "Accept": "application/json, text/event-stream"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            session_id = None
            for k, v in resp.headers.items():
                if k.lower() == "mcp-session-id":
                    session_id = v
        # notifications/initialized
        req = urllib.request.Request(url, data=json.dumps({
            "jsonrpc": "2.0", "method": "notifications/initialized"
        }).encode(), headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": session_id or "",
        })
        try:
            urllib.request.urlopen(req, timeout=10).read()
        except Exception:
            pass
        # tools/list
        req = urllib.request.Request(url, data=json.dumps({
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
        }).encode(), headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": session_id or "",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode()
            # SSE may wrap it
            if "data:" in body:
                for line in body.splitlines():
                    if line.startswith("data:"):
                        body = line[5:].strip()
                        break
            data = json.loads(body)
            actual = len(data["result"]["tools"])
            if claimed != actual:
                fails.append(
                    f"plugin.json capabilities.tools={claimed} but MCP v1 exposes {actual} tools"
                )
    except Exception as exc:
        fails.append(f"could not fetch MCP tool count: {exc}")
    return fails


def main() -> int:
    sections = [
        ("SKILL.md frontmatter", check_skill_frontmatter),
        ("Endpoint doc references", check_endpoint_references),
        ("Python client examples in docs", check_client_examples),
        ("Slash command references", check_slash_commands),
        ("Agent frontmatter", check_agents),
        ("Manifest tool count vs MCP", check_manifest_capabilities),
    ]
    all_fails: list[str] = []
    for name, fn in sections:
        print(f"\n=== {name} ===")
        fails = fn()
        if not fails:
            print("  OK")
        else:
            for f in fails:
                print(f"  FAIL {f}")
            all_fails.extend(fails)
    print()
    print("=" * 80)
    print(f"Total failures: {len(all_fails)}")
    return 1 if all_fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
