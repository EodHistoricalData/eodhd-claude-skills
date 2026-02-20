# Sentiment Data API

Status: complete
Source: financial-apis (Financial News Feed and Stock News Sentiment data API)
Docs: https://eodhd.com/financial-apis/financial-news-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /sentiments
Method: GET
Auth: api_token (query)

## Purpose

Get aggregated daily sentiment scores for one or more financial instruments (stocks, ETFs, crypto, forex).
Sentiment scores are calculated from news and social media, normalized on a scale from -1 (very negative)
to +1 (very positive). Useful for sentiment trend analysis, trading signals, and market mood tracking.

**API Call Consumption**: 5 API calls per request + 5 API calls per ticker.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| s | Yes | string | One or more comma-separated tickers (e.g., AAPL.US,BTC-USD.CC) |
| from | No | string (YYYY-MM-DD) | Start date for filtering sentiment data |
| to | No | string (YYYY-MM-DD) | End date for filtering sentiment data |
| api_token | Yes | string | Your API access token |
| fmt | No | string | Response format: json (default) |

## Response (shape)

Sentiment data is grouped by ticker symbol. Each entry represents one day's aggregated sentiment:

```json
{
  "BTC-USD.CC": [
    {
      "date": "2022-02-22",
      "count": 8,
      "normalized": -0.1811
    },
    {
      "date": "2022-02-21",
      "count": 5,
      "normalized": 0.2824
    }
  ],
  "AAPL.US": [
    {
      "date": "2022-02-22",
      "count": 23,
      "normalized": 0.6152
    },
    {
      "date": "2022-02-21",
      "count": 23,
      "normalized": 0.3668
    }
  ]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| date | string (YYYY-MM-DD) | Date of sentiment aggregation |
| count | integer | Number of articles used for sentiment calculation |
| normalized | float | Sentiment score between -1 (very negative) and +1 (very positive) |

### Sentiment Score Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 0.6 to 1.0 | Very positive sentiment |
| 0.2 to 0.6 | Positive sentiment |
| -0.2 to 0.2 | Neutral sentiment |
| -0.6 to -0.2 | Negative sentiment |
| -1.0 to -0.6 | Very negative sentiment |

## Example Requests

```bash
# Single ticker sentiment
curl "https://eodhd.com/api/sentiments?s=AAPL.US&from=2025-01-01&to=2025-01-31&api_token=demo&fmt=json"

# Multiple tickers sentiment
curl "https://eodhd.com/api/sentiments?s=btc-usd.cc,aapl.us&from=2022-01-01&to=2022-02-22&api_token=demo&fmt=json"

# Crypto sentiment
curl "https://eodhd.com/api/sentiments?s=BTC-USD.CC,ETH-USD.CC&from=2025-01-01&to=2025-01-15&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint sentiment --symbol AAPL.US --from-date 2025-01-01 --to-date 2025-01-31

# Multiple symbols
python eodhd_client.py --endpoint sentiment --symbol "AAPL.US,MSFT.US,GOOGL.US" --from-date 2025-01-01
```

## Response Example (Full)

```json
{
  "BTC-USD.CC": [
    {"date": "2022-04-22", "count": 31, "normalized": 0.1835},
    {"date": "2022-04-21", "count": 41, "normalized": 0.2555},
    {"date": "2022-04-20", "count": 34, "normalized": 0.2068},
    {"date": "2022-04-19", "count": 35, "normalized": 0.4781},
    {"date": "2022-04-18", "count": 29, "normalized": 0.1618},
    {"date": "2022-04-17", "count": 12, "normalized": 0.0056}
  ],
  "AAPL.US": [
    {"date": "2022-02-22", "count": 23, "normalized": 0.6152},
    {"date": "2022-02-21", "count": 23, "normalized": 0.3668},
    {"date": "2022-02-20", "count": 11, "normalized": 0.2995},
    {"date": "2022-02-19", "count": 4, "normalized": 0.1753},
    {"date": "2022-02-18", "count": 24, "normalized": 0.2938}
  ]
}
```

## Use Cases

1. **Sentiment Trend Analysis**: Track how market sentiment changes over time for a symbol
2. **Correlation Analysis**: Compare sentiment trends with price movements
3. **Trading Signals**: Use sentiment shifts as potential buy/sell indicators
4. **Multi-Asset Comparison**: Compare sentiment across related assets (e.g., tech stocks)
5. **Risk Assessment**: Monitor sentiment deterioration as a risk indicator

## Demo Tickers

For testing with the "demo" API key:
- AAPL.US, TSLA.US, VTI.US, AMZN.US (US Stocks/ETFs)
- BTC-USD.CC (Cryptocurrency)
- EURUSD.FOREX (Forex)

## Notes

- Sentiment is aggregated daily from news articles and social media mentions
- `count` indicates data quality - higher counts mean more reliable sentiment scores
- Days with no news coverage may be missing from the response
- Sentiment scores are normalized: -1 = very negative, 0 = neutral, +1 = very positive
- Works for stocks, ETFs, cryptocurrencies, and forex pairs
- Results are sorted by date (most recent first)
- Available in: Standalone package, All-In-One, EOD Historical Data, Fundamentals Data Feed, Free plan
- **Symbols limit**: Maximum **100 symbols** per request.
- **News sources**: Built upon news collected by EODHD. The news is English-language based but not limited to US-only sources.
- **Data depth**: Sentiment data is available from **2018** onwards.
- **Analysis technique**: Sentiment analysis uses NLP-based techniques similar to NLTK sentiment analysis (see: https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk).

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
