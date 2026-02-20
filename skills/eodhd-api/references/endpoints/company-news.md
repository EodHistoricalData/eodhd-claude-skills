# Financial News API

Status: complete
Source: financial-apis (Financial News Feed and Stock News Sentiment data API)
Docs: https://eodhd.com/financial-apis/financial-news-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /news
Method: GET
Auth: api_token (query)

## Purpose

Returns the latest financial news headlines and full articles for a given ticker symbol or topic tag.
Includes sentiment analysis scores for each article. Useful for news monitoring, sentiment analysis,
event detection, and market context.

**API Call Consumption**: 5 API calls per request + 5 API calls per ticker.
Example: 10 API calls for one request with two tickers.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| s | Yes (if t not set) | string | Ticker code (e.g., AAPL.US) |
| t | Yes (if s not set) | string | Topic tag (e.g., technology, earnings) |
| from | No | string (YYYY-MM-DD) | Start date for filtering news |
| to | No | string (YYYY-MM-DD) | End date for filtering news |
| limit | No | integer | Number of results (default: 50, min: 1, max: 1000) |
| offset | No | integer | Offset for pagination (default: 0) |
| fmt | No | string | Response format: json or xml (default: json) |
| api_token | Yes | string | Your API access token |

**Note**: At least one of `s` (ticker) or `t` (tag) is required.

## Response (shape)

Array of news article objects:

```json
[
  {
    "date": "2026-02-09T17:09:51+00:00",
    "title": "Stock Market Today: Dow Firm As Nvidia, Microsoft Jump",
    "content": "Full article body text...",
    "link": "https://finance.yahoo.com/...",
    "symbols": ["AAPL.US", "MSFT.US", "NVDA.US"],
    "tags": ["ENERGY", "STOCK-MARKET", "TECH"],
    "sentiment": {
      "polarity": -0.026,
      "neg": 0.084,
      "neu": 0.837,
      "pos": 0.08
    }
  }
]
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| date | string (ISO 8601) | Publication date and time |
| title | string | Headline of the news article |
| content | string | Full article body |
| link | string | Direct URL to the article |
| symbols | array | Ticker symbols mentioned in the article |
| tags | array | Topic tags (may be empty) |
| sentiment | object | Sentiment scores (see below) |

### Sentiment Object

| Field | Type | Description |
|-------|------|-------------|
| polarity | float | Overall sentiment score (-1 to +1) |
| neg | float | Negative sentiment probability (0 to 1) |
| neu | float | Neutral sentiment probability (0 to 1) |
| pos | float | Positive sentiment probability (0 to 1) |

## Example Requests

```bash
# News for a specific symbol
curl "https://eodhd.com/api/news?s=AAPL.US&offset=0&limit=10&api_token=demo&fmt=json"

# News for multiple symbols
curl "https://eodhd.com/api/news?s=AAPL.US,MSFT.US&limit=20&api_token=demo&fmt=json"

# News by topic tag
curl "https://eodhd.com/api/news?t=technology&limit=10&api_token=demo&fmt=json"

# News with date range
curl "https://eodhd.com/api/news?s=AAPL.US&from=2025-01-01&to=2025-01-31&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint news --symbol AAPL.US --limit 10

# With date filtering
python eodhd_client.py --endpoint news --symbol TSLA.US --from-date 2025-01-01 --to-date 2025-01-31 --limit 20
```

## Available Tags

### Standard Tags (50)

`balance sheet`, `capital employed`, `class action`, `company announcement`, `consensus eps estimate`,
`consensus estimate`, `credit rating`, `discounted cash flow`, `dividend payments`, `earnings estimate`,
`earnings growth`, `earnings per share`, `earnings release`, `earnings report`, `earnings results`,
`earnings surprise`, `estimate revisions`, `european regulatory news`, `financial results`, `fourth quarter`,
`free cash flow`, `future cash flows`, `growth rate`, `initial public offering`, `insider ownership`,
`insider transactions`, `institutional investors`, `institutional ownership`, `intrinsic value`,
`market research reports`, `net income`, `operating income`, `present value`, `press releases`,
`price target`, `quarterly earnings`, `quarterly results`, `ratings`, `research analysis and reports`,
`return on equity`, `revenue estimates`, `revenue growth`, `roce`, `roe`, `share price`, `shareholder rights`,
`shareholder`, `shares outstanding`, `split`, `strong buy`, `total revenue`, `zacks investment research`, `zacks rank`

### AI-Powered Auto-Detected Tags (Examples)

`GROWTH RATE`, `TOBACCO`, `MERGERS AND ACQUISITIONS`, `CATERING`, `ARTIFICIAL INTELLIGENCE`, `AGRITECH`,
`FINTECH`, `TECH`, `STOCK-MARKET`, `ENERGY`, `VALUATION`, `COMPETITION`, `MARKET-SENTIMENT`, `PAYMENTS`, etc.

## Demo Tickers

For testing with the "demo" API key, these tickers are available:
- AAPL.US, TSLA.US, VTI.US, AMZN.US (US Stocks/ETFs)
- BTC-USD.CC (Cryptocurrency)
- EURUSD.FOREX (Forex)

## Notes

- Sentiment `polarity` ranges from -1 (very negative) to +1 (very positive)
- `neg`, `neu`, `pos` probabilities sum to approximately 1.0
- News is aggregated from multiple financial news portals
- AI-powered tags make search more flexible beyond standard 50 tags
- Content may be truncated for some sources
- Use pagination (`offset`, `limit`) for large result sets
- Available in: Standalone package, All-In-One, EOD Historical Data, Fundamentals Data Feed, Free plan
- **One topic per request**: You can request only one tag/topic per API request.
- **Timezone**: All news timestamps are in **UTC**.
- **Sentiment thresholds**: In general, if the polarity is positive it is "good" news, and if negative it is "bad" news. There is no fixed threshold — polarity sign indicates direction.

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
