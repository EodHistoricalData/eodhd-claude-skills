# Earnings Trends API

Status: complete
Source: financial-apis (Calendar API)
Docs: https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /calendar/trends
Method: GET
Auth: api_token (query)

## Purpose

Returns forward-looking and historical earnings trend points for one or more symbols. Each symbol returns a list of dated items that indicate whether that point is an estimate or an actual. The endpoint is JSON-only. Available in All-In-One, Fundamentals Data Feed plans and via "Financial Events (Calendar) & News Feed" plans.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key |
| symbols | Yes | string | One or more tickers, comma-separated (example: AAPL.US,MSFT.US,AI.PA) |
| fmt | No | string | json only |

## Response (shape)

```json
{
  "type": "Trends",
  "description": "Historical and upcoming earning trends",
  "symbols": "AAPL.US,MSFT.US,AI.PA",
  "trends": [
    [
      {
        "code": "AAPL.US",
        "date": "2026-09-30",
        "period": "+1y",
        "growth": "0.0846",
        "earningsEstimateAvg": "7.9816",
        "earningsEstimateLow": "7.1300",
        "earningsEstimateHigh": "9.0000",
        "earningsEstimateYearAgoEps": "7.3676",
        "earningsEstimateNumberOfAnalysts": "40.0000",
        "earningsEstimateGrowth": "0.0833",
        "revenueEstimateAvg": "437035017610.00",
        "revenueEstimateLow": "408100000000.00",
        "revenueEstimateHigh": "477463000000.00",
        "revenueEstimateYearAgoEps": null,
        "revenueEstimateNumberOfAnalysts": "41.00",
        "revenueEstimateGrowth": "0.0527",
        "epsTrendCurrent": "7.9816",
        "epsTrend7daysAgo": "7.9628",
        "epsTrend30daysAgo": "7.9665",
        "epsTrend60daysAgo": "7.8069",
        "epsTrend90daysAgo": "7.8143",
        "epsRevisionsUpLast7days": "1.0000",
        "epsRevisionsUpLast30days": "4.0000",
        "epsRevisionsDownLast30days": "2.0000"
      }
    ]
  ]
}
```

### Output Format

**Top-level fields:**

| Field | Type | Description |
|-------|------|-------------|
| type | string | Constant label of the payload (example: Trends) |
| description | string | Human-readable description of the dataset |
| symbols | string | Comma-separated list of requested tickers |
| trends | array of arrays | For each symbol, an array of trend records. The i-th inner array corresponds to the i-th symbol in the symbols list. Each record is a trend item (see fields below) |

**Trend item fields:**

| Field | Type | Description |
|-------|------|-------------|
| code | string | Ticker code for this record (EODHD format) |
| date | string (YYYY-MM-DD) | Anchor date of the estimate window (quarter or year end) |
| period | string | Relative horizon: 0q (current quarter), +1q (next quarter), 0y (current FY), +1y (next FY) |
| growth | number (stringified) or null | Overall EPS growth vs prior comparable period |
| earningsEstimateAvg | number (stringified) | Consensus EPS |
| earningsEstimateLow | number (stringified) | Low EPS estimate |
| earningsEstimateHigh | number (stringified) | High EPS estimate |
| earningsEstimateYearAgoEps | number (stringified) or null | EPS for the comparable prior period |
| earningsEstimateNumberOfAnalysts | number (stringified) | Analyst count for EPS estimate |
| earningsEstimateGrowth | number (stringified) or null | EPS growth vs prior comparable period |
| revenueEstimateAvg | number (stringified) | Consensus revenue |
| revenueEstimateLow | number (stringified) | Low revenue estimate |
| revenueEstimateHigh | number (stringified) | High revenue estimate |
| revenueEstimateYearAgoEps | number (stringified) or null | Revenue for the comparable prior period (if available) |
| revenueEstimateNumberOfAnalysts | number (stringified) | Analyst count for revenue estimate |
| revenueEstimateGrowth | number (stringified) or null | Revenue growth vs prior comparable period |
| epsTrendCurrent | number (stringified) | Current EPS consensus for this period |
| epsTrend7daysAgo | number (stringified) | EPS consensus 7 days ago |
| epsTrend30daysAgo | number (stringified) | EPS consensus 30 days ago |
| epsTrend60daysAgo | number (stringified) | EPS consensus 60 days ago |
| epsTrend90daysAgo | number (stringified) | EPS consensus 90 days ago |
| epsRevisionsUpLast7days | number (stringified) | Upward EPS revisions in last 7 days |
| epsRevisionsUpLast30days | number (stringified) | Upward EPS revisions in last 30 days |
| epsRevisionsDownLast30days | number (stringified) or null | Downward EPS revisions in last 30 days |

## Example Requests

```bash
# Trends for multiple symbols
curl "https://eodhd.com/api/calendar/trends?symbols=AAPL.US,MSFT.US,AI.PA&api_token=demo&fmt=json"

# Trends for specific symbols
curl "https://eodhd.com/api/calendar/trends?symbols=F.US,AI.PA&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint calendar/trends --symbols F.US,AI.PA
```

## Notes

- JSON-only due to nested structure
- If a provided symbol has no data, it may be omitted from the response
- To paginate large symbol sets, split your symbols into batches (for example, 50–100 per call)
- Each symbol gets its own array in the `trends` array
- Period values: 0q (current quarter), +1q (next quarter), 0y (current fiscal year), +1y (next fiscal year)
- All numeric values are returned as stringified numbers
- API call consumption: 1 call per request

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
