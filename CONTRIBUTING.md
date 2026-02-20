# Contributing to EODHD Skills Adapter

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Ways to Contribute

### 1. Fill in Endpoint Documentation Stubs

Many endpoint files in `skills/eodhd-api/references/endpoints/` are currently stubs (marked `Status: stub`). Priority endpoints needing documentation:

**High Priority:**
- `sentiment-data.md` - Sentiment analysis API
- `us-options-contracts.md` - Options contracts listing
- `websockets-realtime.md` - WebSocket streaming
- `us-tick-data.md` - Tick-level data

**Medium Priority:**
- ESG endpoints (`investverte-*.md`)
- Banking/Bond endpoints (`praams-*.md`)
- Illio analytics endpoints (`illio-*.md`)

**Documentation format:**
```markdown
# Endpoint Name API

Status: draft
Source: financial-apis (API Category)
Docs: https://eodhd.com/financial-apis/...
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /endpoint/{SYMBOL}
Method: GET
Auth: api_token (query)

## Purpose
Brief description of what this endpoint does.

## Parameters
- Required:
  - api_token: EODHD API key
  - {SYMBOL}: Symbol format description
- Optional:
  - param1: Description
  - param2: Description

## Response (shape)
JSON example showing response structure.

## Example request
curl and Python client examples.

## Notes
- Important usage notes
- Rate limits, data availability, etc.
```

### 2. Expand the Python Client

The helper script `skills/eodhd-api/scripts/eodhd_client.py` can be extended to support more endpoints. Requirements:

- **Keep it stdlib-only**: No external dependencies (no `requests`, `pandas`, etc.)
- **Follow existing patterns**: See how current endpoints are implemented
- **Add to SUPPORTED_ENDPOINTS**: Register new endpoint in the list
- **Update build_path()**: Add path construction logic
- **Handle special parameters**: Some endpoints use different query params

Example addition:
```python
# In SUPPORTED_ENDPOINTS list
"new-endpoint",

# In build_path()
if endpoint == "new-endpoint":
    if not symbol:
        raise ClientError("--symbol is required for endpoint=new-endpoint")
    return f"/new-endpoint/{symbol}"
```

### 3. Add Workflow Examples

Contribute new workflow recipes to `skills/eodhd-api/references/workflows.md`:

- Sector analysis patterns
- Portfolio construction workflows
- Risk analysis recipes
- Backtesting patterns

### 4. Improve Templates

The output template `skills/eodhd-api/templates/analysis_report.md` can be enhanced:

- Add specialized templates for different analysis types
- Include more structured data sections
- Add visualization placeholders

### 5. Testing and Validation

Help validate endpoint documentation against the actual API:

- Test example requests with a demo or real API token
- Verify response shapes match documentation
- Report discrepancies as issues

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/eodhd-claude-skills.git
   cd eodhd-claude-skills
   ```

2. Set up your API token:
   ```bash
   export EODHD_API_TOKEN="your_token_here"
   ```

3. Test the client:
   ```bash
   python skills/eodhd-api/scripts/eodhd_client.py --endpoint exchanges-list
   ```

## Code Style

### Python
- Follow PEP 8
- Use type hints (Python 3.8+ style)
- Keep functions focused and documented
- Handle errors gracefully with meaningful messages

### Markdown
- Use consistent heading hierarchy
- Include code examples with syntax highlighting
- Keep lines under 100 characters where possible
- Use tables for structured information

## Pull Request Process

1. **Create a branch**: `feature/add-endpoint-xyz` or `fix/client-error-handling`

2. **Make your changes**: Follow the guidelines above

3. **Test your changes**: Verify with actual API calls if possible

4. **Update documentation**: If adding features, update relevant docs

5. **Submit PR**: Include:
   - Clear description of changes
   - Any testing performed
   - Related issues (if any)

## Commit Messages

Use clear, descriptive commit messages:

```
Add sentiment endpoint documentation

- Document /sentiments API parameters
- Add response shape examples
- Include usage notes for sentiment scores
```

## Reporting Issues

When reporting issues, include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- API response (if applicable, redact tokens)

## Questions?

Open an issue with the `question` label for any questions about contributing.

## Priority Areas

Current priority areas for contribution:

1. **Endpoint documentation**: Fill in TBD stubs for commonly used endpoints
2. **Client expansion**: Add more endpoints to the Python helper
3. **Real-world examples**: Workflow recipes with actual use cases
4. **Error handling**: Improve client error messages and recovery

Thank you for contributing!
