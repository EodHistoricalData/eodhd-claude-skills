#!/usr/bin/env python3
"""End-to-end tests for the EODHD MCP Server v1 (API-key auth).

Tests MCP JSONRPC protocol over HTTP at https://mcpv2.eodhd.dev/v1/mcp?apikey=...

Steps:
  1. initialize  — handshake, get server info + capabilities
  2. tools/list  — enumerate available tools
  3. tools/call  — invoke a simple tool (eodhd_eod_AAPL_US or similar)

Also probes v2 endpoint to confirm OAuth challenge (401 without bearer).

Stdlib-only. Requires EODHD_API_TOKEN env var.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

MCP_V1 = "https://mcpv2.eodhd.dev/v1/mcp"
MCP_V2 = "https://mcpv2.eodhd.dev/v2/mcp"


def jsonrpc(url: str, method: str, params: dict | None = None,
            req_id: int = 1, extra_headers: dict | None = None,
            timeout: int = 30) -> tuple[int, dict | str, dict]:
    """Send a JSONRPC request. Returns (http_status, body_dict_or_text, response_headers)."""
    payload = {"jsonrpc": "2.0", "id": req_id, "method": method}
    if params is not None:
        payload["params"] = params

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if extra_headers:
        headers.update(extra_headers)

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers=headers, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return (resp.status, parse_body(body), dict(resp.headers))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return (exc.code, parse_body(body), dict(exc.headers) if exc.headers else {})


def parse_body(body: str):
    """MCP can return application/json OR SSE (text/event-stream) with data: lines."""
    body = body.strip()
    if not body:
        return ""
    # SSE format: each event is `data: <json>\n\n`
    if body.startswith("event:") or body.startswith("data:"):
        for line in body.splitlines():
            if line.startswith("data:"):
                try:
                    return json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    pass
        return body
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return body


def test_v2_oauth_challenge() -> tuple[str, str]:
    """v2 should respond 401 with proper auth challenge."""
    status, body, _ = jsonrpc(MCP_V2, "initialize", {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "eodhd-tests", "version": "1.0.0"},
    })
    if status == 401:
        return ("pass", f"401 Unauthorized (OAuth required) - body: {str(body)[:80]}")
    if status == 200:
        return ("fail", f"v2 returned 200 without auth - should require OAuth! body: {str(body)[:80]}")
    return ("fail", f"unexpected HTTP {status}: {str(body)[:120]}")


def test_v1_initialize(token: str) -> tuple[str, str, dict | None, str | None]:
    """v1 initialize handshake with apikey. Returns (status, detail, result, session_id)."""
    url = f"{MCP_V1}?apikey={token}"
    status, body, headers = jsonrpc(url, "initialize", {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "eodhd-tests", "version": "1.0.0"},
    })
    if status != 200:
        return ("fail", f"HTTP {status}: {str(body)[:200]}", None, None)
    if not isinstance(body, dict) or "result" not in body:
        return ("fail", f"no result in response: {str(body)[:200]}", None, None)
    server_info = body["result"].get("serverInfo", {})
    # Capture session ID (case-insensitive header lookup)
    session_id = None
    for k, v in headers.items():
        if k.lower() == "mcp-session-id":
            session_id = v
            break
    return ("pass",
            f"server={server_info.get('name', '?')} v{server_info.get('version', '?')}, "
            f"protocol={body['result'].get('protocolVersion', '?')}, "
            f"session={session_id[:12] if session_id else 'none'}...",
            body["result"], session_id)


def send_initialized_notification(token: str, session_id: str) -> None:
    """After initialize + capturing session, send 'notifications/initialized' (no response expected)."""
    url = f"{MCP_V1}?apikey={token}"
    payload = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Mcp-Session-Id": session_id,
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                  headers=headers, method="POST")
    try:
        urllib.request.urlopen(req, timeout=10).read()
    except urllib.error.HTTPError:
        pass  # Server may 202/204; ignore


def test_v1_tools_list(token: str, session_id: str | None = None) -> tuple[str, str, list | None]:
    """List available MCP tools."""
    url = f"{MCP_V1}?apikey={token}"
    extra = {"Mcp-Session-Id": session_id} if session_id else None
    status, body, _ = jsonrpc(url, "tools/list", {}, req_id=2, extra_headers=extra)
    if status != 200:
        return ("fail", f"HTTP {status}: {str(body)[:200]}", None)
    if not isinstance(body, dict) or "result" not in body:
        return ("fail", f"no result: {str(body)[:200]}", None)
    tools = body["result"].get("tools", [])
    sample = ", ".join(t["name"] for t in tools[:5])
    return ("pass", f"{len(tools)} tools listed (first 5: {sample})", tools)


def pick_simple_tool(tools: list) -> dict | None:
    """Pick a simple read-only tool to test. Prefer 'eod' or 'real-time' or 'exchanges-list'."""
    priority = ["get_exchanges_list", "exchanges_list", "get_real_time_quote",
                "real_time", "get_eod_data", "eod"]
    by_name = {t["name"]: t for t in tools}
    for n in priority:
        if n in by_name:
            return by_name[n]
    return tools[0] if tools else None


def test_v1_tool_call(token: str, tool: dict, session_id: str | None = None) -> tuple[str, str]:
    """Invoke one tool with minimal args."""
    name = tool["name"]
    schema = tool.get("inputSchema", {})
    required = schema.get("required", [])
    props = schema.get("properties", {})

    # Build minimal args. For symbol-required tools, use AAPL.US; for exchange, US.
    args: dict = {}
    for req in required:
        prop = props.get(req, {})
        if "symbol" in req or "ticker" in req:
            args[req] = "AAPL.US"
        elif "exchange" in req or "code" in req:
            args[req] = "US"
        elif prop.get("type") == "integer":
            args[req] = 10
        elif prop.get("type") == "string":
            args[req] = "AAPL.US"  # safe default
        else:
            args[req] = None

    url = f"{MCP_V1}?apikey={token}"
    extra = {"Mcp-Session-Id": session_id} if session_id else None
    status, body, _ = jsonrpc(url, "tools/call",
                              {"name": name, "arguments": args},
                              req_id=3, extra_headers=extra, timeout=60)
    if status != 200:
        return ("fail", f"{name}: HTTP {status}: {str(body)[:200]}")
    if not isinstance(body, dict):
        return ("fail", f"{name}: non-dict body: {str(body)[:200]}")
    if "error" in body:
        return ("fail", f"{name}: {body['error']}")
    result = body.get("result", {})
    content = result.get("content", [])
    if not content:
        return ("fail", f"{name}: empty content")
    first = content[0]
    if first.get("type") == "text":
        text = first.get("text", "")
        preview = text[:120].replace("\n", " ")
        return ("pass", f"{name}({args}) → {len(text)} chars: {preview}...")
    return ("pass", f"{name}: {first.get('type')} content received")


def main() -> int:
    token = os.getenv("EODHD_API_TOKEN")
    if not token:
        print("ERROR: EODHD_API_TOKEN env var not set", file=sys.stderr)
        return 2

    print("\n=== MCP Server tests ===\n")
    results: list[tuple[str, str, str]] = []

    # v2 OAuth challenge
    status, detail = test_v2_oauth_challenge()
    results.append(("v2 OAuth challenge", status, detail))
    print(f"v2 OAuth challenge       {symbol(status)} {status.upper():<5}  {detail}")

    # v1 initialize
    status, detail, init_result, session_id = test_v1_initialize(token)
    results.append(("v1 initialize", status, detail))
    print(f"v1 initialize            {symbol(status)} {status.upper():<5}  {detail}")

    if status != "pass":
        print("\nv1 initialize failed - aborting remaining MCP tests")
        return 1

    # Per MCP spec: must send 'initialized' notification after handshake
    if session_id:
        send_initialized_notification(token, session_id)

    # v1 tools/list (with session)
    status, detail, tools = test_v1_tools_list(token, session_id)
    results.append(("v1 tools/list", status, detail))
    print(f"v1 tools/list            {symbol(status)} {status.upper():<5}  {detail}")

    if status != "pass" or not tools:
        print("\nv1 tools/list failed - cannot test individual tool calls")
        return 1

    # v1 tools/call — try a simple one
    tool = pick_simple_tool(tools)
    if not tool:
        print("No suitable tool to test")
    else:
        status, detail = test_v1_tool_call(token, tool, session_id)
        results.append(("v1 tools/call", status, detail))
        print(f"v1 tools/call            {symbol(status)} {status.upper():<5}  {detail}")

    fails = [r for r in results if r[1] == "fail"]
    print()
    print("=" * 80)
    print(f"Total: {len(results)} | PASS: {sum(1 for r in results if r[1]=='pass')} | FAIL: {len(fails)}")
    return 1 if fails else 0


def symbol(status: str) -> str:
    return {"pass": "PASS", "fail": "FAIL", "skip": "SKIP"}.get(status, "?")


if __name__ == "__main__":
    raise SystemExit(main())
