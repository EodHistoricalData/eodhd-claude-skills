# News Word Weights API

Status: complete
Source: financial-apis (Financial News Feed and Stock News Sentiment data API)
Docs: https://eodhd.com/financial-apis/financial-news-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /news-word-weights
Method: GET
Auth: api_token (query)

## Purpose

Provides a weighted list of the most relevant words found in financial news articles about a specific
stock ticker over a defined date range. Each word is scored based on its frequency and significance
across the processed news. Useful for trend analysis, NLP input, thematic clustering, and identifying
key topics driving market narratives.

**Note**: This endpoint uses AI to process hundreds or thousands of articles, which may result in
longer response times. If you encounter timeouts, narrow the date range or focus on specific tickers.

**API Call Consumption**: 5 API calls per request + 5 API calls per ticker.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| s | Yes | string | Ticker symbol to analyze (e.g., AAPL.US) |
| filter[date_from] | No | string (YYYY-MM-DD) | Start date for filtering news |
| filter[date_to] | No | string (YYYY-MM-DD) | End date for filtering news |
| page[limit] | No | integer | Number of top words to return |
| api_token | Yes | string | Your API access token |
| fmt | No | string | Response format: json (default) |

## Response (shape)

```json
{
  "data": {
    "appl": 0.01933,
    "tariff": 0.01893,
    "stock": 0.01889,
    "trump": 0.01114,
    "companies": 0.00989,
    "market": 0.00927,
    "china": 0.00792,
    "trade": 0.00719,
    "ai": 0.00607,
    "price": 0.00579
  },
  "meta": {
    "news_processed": 300,
    "news_found": 5860
  },
  "links": {
    "next": null
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| data | object | Key-value pairs of words and their weights |
| meta.news_found | integer | Total number of articles matched |
| meta.news_processed | integer | Number of articles successfully processed |
| links.next | string or null | URL to next page of results (if available) |

### Word Weight Interpretation

- Weights are relative scores (typically 0.001 to 0.02 range)
- Higher weights indicate more frequent and significant terms
- Words are stemmed/normalized (e.g., "apple" → "appl")
- Stop words and common terms are filtered out

## Example Requests

```bash
# Top 10 words for AAPL over a week
curl "https://eodhd.com/api/news-word-weights?s=AAPL&filter[date_from]=2025-04-08&filter[date_to]=2025-04-16&page[limit]=10&api_token=demo&fmt=json"

# Top 20 words for TSLA over a month
curl "https://eodhd.com/api/news-word-weights?s=TSLA.US&filter[date_from]=2025-01-01&filter[date_to]=2025-01-31&page[limit]=20&api_token=demo&fmt=json"

# Top 50 words for crypto
curl "https://eodhd.com/api/news-word-weights?s=BTC-USD.CC&filter[date_from]=2025-01-01&filter[date_to]=2025-01-15&page[limit]=50&api_token=demo&fmt=json"
```

## Response Example (Full)

```json
{
  "data": {
    "appl": 0.01922,
    "tariff": 0.01889,
    "stock": 0.01884,
    "trump": 0.01115,
    "companies": 0.00983,
    "market": 0.00919,
    "china": 0.0079,
    "trade": 0.00723,
    "ai": 0.00605,
    "price": 0.00577,
    "iphone": 0.00542,
    "revenue": 0.00498,
    "sales": 0.00467,
    "earnings": 0.00423,
    "growth": 0.00398
  },
  "meta": {
    "news_processed": 300,
    "news_found": 5748
  },
  "links": {
    "next": null
  }
}
```

## Use Cases

1. **Trend Detection**: Identify emerging themes and topics in news coverage
2. **NLP/ML Input**: Use word weights as features for machine learning models
3. **Thematic Analysis**: Understand what's driving stock narrative
4. **Keyword Monitoring**: Track specific terms over time
5. **Comparative Analysis**: Compare word weights across different stocks
6. **Market Narrative**: Identify macro themes affecting a stock (e.g., tariffs, AI, regulation)

## Processing Patterns

### Extract top themes with jq
```bash
# Get top 5 words
curl "https://eodhd.com/api/news-word-weights?s=AAPL&filter[date_from]=2025-01-01&filter[date_to]=2025-01-31&page[limit]=5&api_token=demo&fmt=json" | jq '.data'

# Get metadata
curl "..." | jq '.meta'
```

### Compare themes across stocks
```bash
# Compare AAPL vs MSFT word weights for same period
for ticker in AAPL MSFT; do
  echo "=== $ticker ==="
  curl -s "https://eodhd.com/api/news-word-weights?s=$ticker&filter[date_from]=2025-01-01&filter[date_to]=2025-01-15&page[limit]=10&api_token=demo&fmt=json" | jq '.data'
done
```

## Demo Tickers

For testing with the "demo" API key:
- AAPL.US, TSLA.US, VTI.US, AMZN.US (US Stocks/ETFs)
- BTC-USD.CC (Cryptocurrency)
- EURUSD.FOREX (Forex)

## Notes

- **Performance**: AI processing may cause longer response times; narrow date ranges for faster responses
- **Word Stemming**: Words are normalized (e.g., "companies" → "compani", "trading" → "trade")
- **Coverage**: `news_found` vs `news_processed` indicates processing coverage
- Weights are relative within a response; compare rankings, not absolute values
- Empty periods or tickers with no news will return minimal data
- Useful for building word clouds, topic models, and sentiment dashboards
- Available in: Standalone package, All-In-One, EOD Historical Data, Fundamentals Data Feed, Free plan

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
