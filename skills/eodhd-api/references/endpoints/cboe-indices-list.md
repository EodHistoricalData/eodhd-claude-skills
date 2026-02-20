# Cboe Indices List API

Status: complete
Source: financial-apis (CBOE Europe Indices API beta)
Docs: https://eodhd.com/financial-apis/cboe-europe-indices-api-beta
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /cboe/indices
Method: GET
Auth: api_token (query)

## Purpose
Return the full list of CBOE indices available via EODHD, including the latest
close and divisor plus basic metadata needed to select an index code for the
feed endpoint.

## Parameters
- Required:
  - api_token: EODHD API key.
- Optional:
  - fmt: json or xml (default json).
  - pagination: follow the URL in links.next until null (no manual params).

## Response (shape)
- meta.total: integer total returned in this response.
- data[]: array of index entries.
  - data[].id: EODHD index identifier (often same as index_code).
  - data[].type: "cboe-index".
  - data[].attributes.region: country/region.
  - data[].attributes.index_code: CBOE index code.
  - data[].attributes.feed_type: latest feed type.
  - data[].attributes.date: YYYY-MM-DD.
  - data[].attributes.index_close: number.
  - data[].attributes.index_divisor: number.
- links.next: string or null pagination URL.

## Example request
```bash
curl "https://eodhd.com/api/cboe/indices?api_token=YOUR_API_KEY&fmt=json"
```

## Notes
- API call consumption: 10 calls per request.
- Use this endpoint to discover supported indices and the index_code for
  the detailed feed endpoint.

## HTTP Status Codes

The API returns standard HTTP status codes to indicate success or failure:

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | OK | Request succeeded. Data returned successfully. |
| **402** | Payment Required | API limit used up. Upgrade plan or wait for limit reset. |
| **403** | Unauthorized | Invalid API key. Check your `api_token` parameter. |
| **429** | Too Many Requests | Exceeded rate limit (requests per minute). Slow down requests. |

### Error Response Format

When an error occurs, the API returns a JSON response with error details:

```json
{
  "error": "Error message description",
  "code": 403
}
```

### Handling Errors

**Python Example**:
```python
import requests

def make_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:
            print("Error: API limit exceeded. Please upgrade your plan.")
        elif e.response.status_code == 403:
            print("Error: Invalid API key. Check your credentials.")
        elif e.response.status_code == 429:
            print("Error: Rate limit exceeded. Please slow down your requests.")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

**Best Practices**:
- Always check status codes before processing response data
- Implement exponential backoff for 429 errors
- Cache responses to reduce API calls
- Monitor your API usage in the user dashboard
