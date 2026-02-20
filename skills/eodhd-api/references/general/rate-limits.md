# EODHD API Limits: Calls, Requests & Consumption

This document explains the API call system, rate limits, and consumption rules for the EODHD API.

## Key Concept: API Calls vs API Requests

An **API request** is not the same as an **API call**. API calls are a form of "currency" used to make requests. Different data requests consume different numbers of API calls. For example, a Fundamental data request costs 10 API calls, while a Live data request for 1 ticker costs 1 API call.

## Daily API Limit (Calls)

The daily limit is set by default to **100,000 API calls** per user for every paid plan or marketplace product.

### Daily Limit Reset

- **Subscription plans**: The daily limit resets at **midnight GMT**. However, the counter itself is not reset automatically — it is refreshed on the **first API request made after midnight GMT**. Before that, the counter displays the number of API calls from the last active day.
- **Marketplace products**: See the [Marketplace Product Limits](#marketplace-product-limits) section below for details on how Marketplace limits and reset times work.

### Daily Limit Increase

To increase the API call daily limit (100,000 by default) for a subscription plan:

1. Navigate to the **"Daily Usage"** section in the dashboard
2. Select the **"Increase Daily Limit"** option
3. View the price of the upgrade and submit a request to support

Daily limit increases are **not currently available** for marketplace products. Contact support for specific cases.

## API Call Consumption by Endpoint

### Summary Table

| Endpoint Type | Calls Consumed | Example |
|---------------|----------------|---------|
| Most endpoints (EOD, Splits, Dividends, Calendar, Exchange lists, etc.) | 1 call | EOD prices for 1 symbol = 1 call |
| Multi-ticker endpoints (1 call per symbol) | 1 call per symbol | Live API with 10 symbols = 10 calls |
| Technical API | 5 calls | SMA for 1 symbol = 5 calls |
| Intraday API | 5 calls | 5-minute bars for 1 symbol = 5 calls |
| News API | 5 calls | News for 1 symbol = 5 calls |
| Sentiment API | 5 + (5 x tickers) | Sentiment for 2 tickers = 15 calls |
| News Word Weights API | 5 + (5 x tickers) | Word weights for 3 tickers = 20 calls |
| Fundamental API | 10 calls | Fundamentals for 1 symbol = 10 calls |
| Marketplace products | 10 calls (unless otherwise stated) | Per product documentation |
| Bulk API (entire exchange) | 100 calls | Bulk EOD for entire exchange = 100 calls |
| Bulk API (with `symbols` parameter) | 100 + N calls | Bulk with 3 symbols = 103 calls |
| Failed requests (HTTP errors) | 0 calls | Server errors don't count against quota |
| Invalid symbol requests | 1 call | Wrong symbols still return a response and count |

### 1-Call Endpoints

The following endpoints consume **1 API call** per request:

**Market Data**:
- End-of-day prices (`/eod/{TICKER}`)
- Live (delayed) quotes (`/real-time/{TICKER}`) — 1 call per ticker
- US extended quotes (`/us-quote-delayed`) — 1 call per ticker

**Corporate Events**:
- Dividends (`/div/{TICKER}`)
- Splits (`/splits/{TICKER}`)
- Insider transactions (`/insider-transactions`)

**Calendar & Events**:
- Earnings calendar (`/calendar/earnings`)
- Earnings trends (`/calendar/trends`)
- IPOs calendar (`/calendar/ipos`)
- Splits calendar (`/calendar/splits`)
- Dividends calendar (`/calendar/dividends`)
- Economic events (`/economic-events`)

**Exchange Data**:
- Exchange list (`/exchanges-list`)
- Exchange details (`/exchanges/{CODE}`)
- Exchange symbols (`/exchange-symbol-list/{CODE}`)
- Symbol search (`/search/{QUERY}`)

**Screening**:
- Stock screener (`/screener`)

**Account**:
- User details (`/internal-user`)

**US Treasury**:
- Bill rates (`/ust/bill-rates`)
- Long-term rates (`/ust/long-term-rates`)
- Yield rates (`/ust/yield-rates`)
- Real yield rates (`/ust/real-yield-rates`)

**Multi-ticker note**: For any multi-ticker API endpoint that costs 1 API call per request, each symbol costs 1 API call. For example, a Live API request with 10 symbols costs 10 API calls.

### 5-Call Endpoints

The following endpoints consume **5 API calls** per request:

- Technical indicators (`/technical/{TICKER}`)
- Intraday data (`/intraday/{TICKER}`)
- Company news (`/news`)
- Sentiment data (`/sentiments`) — 5 + (5 x tickers)
- News word weights (`/news-word-weights`) — 5 + (5 x tickers)

**News/Sentiment formula**: `5 + (5 x number_of_tickers)`

| Request | Tickers | Calculation | Total Calls |
|---------|---------|-------------|-------------|
| `/news?s=AAPL.US` | 1 | 5 + (5 x 1) | 10 calls |
| `/news?s=AAPL.US,MSFT.US` | 2 | 5 + (5 x 2) | 15 calls |
| `/sentiments?s=AAPL.US` | 1 | 5 + (5 x 1) | 10 calls |
| `/news-word-weights?s=AAPL.US,MSFT.US,GOOGL.US` | 3 | 5 + (5 x 3) | 20 calls |

### 10-Call Endpoints

The following endpoints consume **10 API calls** per request:

- Company fundamentals (`/fundamentals/{TICKER}`)
- Marketplace products (unless otherwise stated in product documentation)

### 100-Call Endpoints (Bulk)

Bulk API endpoints consume **100 API calls** for the entire exchange:

- Bulk EOD data (`/eod-bulk-last-day/{EXCHANGE}`) — 100 calls
- Bulk fundamentals (`/bulk-fundamentals/{EXCHANGE}`) — 100 calls

When the `symbols` parameter is used, the cost is **100 + N API calls**, where N is the number of symbols. For example, requesting bulk fundamentals for 3 symbols costs 103 API calls.

## Marketplace Product Limits

Marketplace products (endpoints with `/mp/` in the path) have their own **separate** rate limits, independent from the main EODHD subscription plan.

### Common Limits for All Marketplace Products

Every Marketplace product shares the same limit structure:

| Limit | Value |
|-------|-------|
| API calls per 24 hours | 100,000 |
| API requests per minute | 1,000 |
| API calls per request | 10 (1 request = 10 API calls) |

### Separate Limit Pools

Each Marketplace subscription has its **own separate** API call limit pool of 100,000 calls per 24 hours. These are also separate from the main EODHD subscription plan limit. For example, if you subscribe to both the US Stock Options Data API and the Stock Market Logos API, each has its own 100,000-call daily limit independently.

### Marketplace Reset Time

All Marketplace subscriptions for a given user share a **single reset time**. This reset time is determined by when the user first made **any** Marketplace API request — all Marketplace subscriptions then reset at that same time every 24 hours.

The reset time can be found in the Internal User API (`/api/internal-user`) response under the `availableMarketplaceDataFeeds.timeToReset` field:

```json
{
  "availableMarketplaceDataFeeds": {
    "dailyRateLimit": 100000,
    "requestsSpent": 80,
    "timeToReset": "19:01 GMT+0000",
    "subscriptions": ["US Stock Options Data API"]
  }
}
```

- `timeToReset` — The exact time (in GMT) when all Marketplace subscription call limits reset. This is the same time for all Marketplace products on the account.
- `requestsSpent` — Number of Marketplace API calls used in the current period.
- `subscriptions` — List of active Marketplace subscription names.

### Marketplace Products List

The following Marketplace products are available (all use `/mp/` in the API path):

| Product | Endpoints | Provider |
|---------|-----------|----------|
| **US Stock Options Data API** | `/mp/unicornbay/options/contracts`, `/mp/unicornbay/options/eod`, `/mp/unicornbay/options/underlyings` | Unicorn Bay |
| **Tick Data API: US Stock Market** | `/mp/unicornbay/tickdata/ticks` | Unicorn Bay |
| **Indices Historical Constituents Data API** | `/mp/unicornbay/spglobal/list`, `/mp/unicornbay/spglobal/comp/{symbol}` | Unicorn Bay / S&P Global |
| **Investverte ESG API** | `/mp/investverte/esg/list-companies`, `/mp/investverte/esg/list-countries`, `/mp/investverte/esg/list-sectors`, `/mp/investverte/esg/view-company`, `/mp/investverte/esg/view-country`, `/mp/investverte/esg/view-sector` | Investverte |
| **Praams Equity Risk & Return Scoring API** | `/mp/praams/scoring/ticker/{ticker}`, `/mp/praams/scoring/isin/{isin}`, `/mp/praams/bond/{isin}` | PRAAMS |
| **Praams Bank Financials API** | `/mp/praams/bank/income-statement/ticker/{ticker}`, `/mp/praams/bank/income-statement/isin/{isin}`, `/mp/praams/bank/balance-sheet/ticker/{ticker}`, `/mp/praams/bank/balance-sheet/isin/{isin}` | PRAAMS |
| **Praams Smart Investment Screener API** | `/mp/praams/screener/equity`, `/mp/praams/screener/bond` | PRAAMS |
| **Multi-Factor Investment Reports API** | `/mp/praams/reports/equity/ticker/{ticker}`, `/mp/praams/reports/equity/isin/{isin}`, `/mp/praams/reports/bond/{isin}` | PRAAMS |
| **illio Performance Insights** | `/mp/illio/performance-insights` | illio |
| **illio Risk Insights** | `/mp/illio/risk-insights` | illio |
| **illio Market Insights** | `/mp/illio/market-insights/performance`, `/mp/illio/market-insights/best-worst`, `/mp/illio/market-insights/volatility`, `/mp/illio/market-insights/risk-return`, `/mp/illio/market-insights/largest-volatility`, `/mp/illio/market-insights/beta-bands` | illio |
| **Stock Market Logos API** | `/logo/{symbol}` | Unicorn Data Services |
| **Stock Market Logos API (SVG)** | `/logo-svg/{symbol}` | Unicorn Data Services |
| **Market Status API (TradingHours)** | `/mp/tradinghours/markets`, `/mp/tradinghours/markets/lookup`, `/mp/tradinghours/markets/details`, `/mp/tradinghours/markets/status` | TradingHours |

> **Note**: The Stock Market Logos endpoints (`/logo/` and `/logo-svg/`) do not use the `/mp/` path prefix but are still Marketplace products with the same separate rate limits.

## Minute Limit (Requests)

The API is restricted to no more than **1,000 requests per minute**. This is a limit on HTTP requests, not API calls.

You can check this limit via response headers included with every request:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
```

Requests exceeding the rate limit receive an **HTTP 429 (Too Many Requests)** response. Excess requests are rejected immediately (not queued).

**Best practice**: Spread requests evenly throughout the minute rather than sending them all at once, to avoid "Too Many Requests" errors.

**Note**: The per-minute request limit does **not** increase when you purchase additional daily API calls or increase your daily call limit.

## Extra API Calls

You can purchase additional API calls that function as a **buffer** — they are only consumed once your daily API limit is exhausted.

Key details:
- Extra API calls **do not expire** and can be accumulated by purchasing more as needed
- They **do not increase your daily limit** — they provide overflow capacity
- Purchase via the **"Buy Extra API Calls"** form on your dashboard page
- If you want to increase your daily limit instead, contact support: support@eodhistoricaldata.com

**PayPal subscribers**: You can purchase an additional subscription of the same type and contact support to increase your limit.

## API Usage Statistics

### User Details Endpoint

Check your current usage via the API:

```bash
curl "https://eodhd.com/api/internal-user?api_token=YOUR_TOKEN"
```

**Response** (with Marketplace subscriptions):
```json
{
  "name": "John Doe",
  "email": "john.doe@gmx.de",
  "subscriptionType": "monthly",
  "paymentMethod": "PayPal",
  "apiRequests": 5301,
  "apiRequestsDate": "2026-01-25",
  "dailyRateLimit": 100000,
  "extraLimit": 500,
  "subscriptionMode": "paid",
  "availableDataFeeds": ["EOD Historical Data", "News API", "..."],
  "availableMarketplaceDataFeeds": {
    "dailyRateLimit": 100000,
    "requestsSpent": 80,
    "timeToReset": "19:01 GMT+0000",
    "subscriptions": ["US Stock Options Data API"]
  }
}
```

**Main subscription fields**:
- `apiRequests` — Number of API calls on the latest day of API usage (resets at midnight GMT, but shows the previous day's count until a new request is made after reset)
- `apiRequestsDate` — Date of the latest API request
- `dailyRateLimit` — Maximum number of API calls allowed per day for the main subscription
- `extraLimit` — Remaining amount of additionally purchased API calls

**Marketplace fields** (in `availableMarketplaceDataFeeds`):
- `dailyRateLimit` — Maximum daily API calls per Marketplace subscription (100,000)
- `requestsSpent` — Marketplace API calls used in the current 24-hour period
- `timeToReset` — Time when all Marketplace limits reset (e.g., `19:01 GMT+0000`)
- `subscriptions` — List of active Marketplace subscription names

### Dashboard

Monitor usage through your account dashboard at https://eodhd.com/cp/api:

- Select the period and type of API requests to adjust the chart view
- The chart shows how many times you called the API
- To calculate impact on your API limit, multiply the call count by the cost per API request (e.g., each intraday API call consumes 5 limit units)

## Rate Limit Errors

### Exceeded Daily Limit

**HTTP Status**: 402 Payment Required

**Solutions** (main subscription):
1. Wait until midnight GMT (daily reset)
2. Increase your daily limit via the dashboard
3. Purchase Extra API Calls as a buffer
4. Optimize requests to use fewer calls

**Solutions** (Marketplace products):
1. Wait until the `timeToReset` time shown in `/api/internal-user` response
2. Optimize requests to use fewer calls
3. Contact support for specific Marketplace limit increase cases

### Exceeded Minute Limit

**HTTP Status**: 429 Too Many Requests

**Solutions**:
1. Spread requests evenly throughout the minute
2. Implement rate limiting in your code
3. Add delays between requests
4. Use exponential backoff for retries
5. Consider batch/bulk endpoints

### Symbols Per Request

| Request Type                            | Recommended | Maximum | Notes |
|-----------------------------------------|-------------|---------|-------|
| **Bulk end of day download**            | Entire exchange | Entire exchange | 100 calls. US = 45,000+ tickers |
| **Standard request with `s` parameter** | 15-20 symbols | ~100 symbols | URL becomes extremely long at high counts |
| **Batch real-time**                     | 15-20 symbols | ~100 symbols | Same URL length constraint |

### No Push API

EODHD provides a **REST API only** (pull-based). There is no push API that sends data to your endpoints. For real-time streaming, use the WebSocket API.

### API Request History

EODHD does **not** keep user request history data — only the latest usage counters. With hundreds of millions of requests per day across all users, storing per-request history is not feasible.

### 502 Error During Maintenance

EODHD performs technical maintenance between **5:30 and 6:00 GMT** daily. Requests during this window have an increased risk of encountering **502 errors**. Avoid scheduling automated data fetches during this period.

### EODHD Service Status

Check the current status of the EODHD service at the EODHD status page.

### WebSocket Limits

WebSocket streaming does **not** have per-request rate limits. Instead, limits apply to:

- **Concurrent connections** — Based on subscription tier
- **Symbols per connection** — Based on subscription tier (default 50, upgradeable)

See `pricing-and-plans.md` for WebSocket tier details.

## Optimization Strategies

### 1. Use Bulk Endpoints

Instead of fetching EOD data for 100 symbols individually to get last data:

**Inefficient** (100 calls):
```bash
for symbol in AAPL.US MSFT.US GOOGL.US ...; do
  curl "https://eodhd.com/api/eod/${symbol}?api_token=TOKEN"
done
```

**Efficient** (100 calls for entire exchange):
```bash
curl "https://eodhd.com/api/eod-bulk-last-day/US?api_token=TOKEN"
```

### 2. Cache Responses

Cache data that doesn't change frequently:

**EOD Data**: Cache until next trading day
```python
from datetime import datetime, time

def should_refresh_eod():
    """Refresh EOD cache after 5 PM EST."""
    now = datetime.now()
    return now.time() > time(17, 0)  # After 5 PM
```

**Fundamentals**: Cache for 24 hours
```python
import time

class FundamentalsCache:
    def __init__(self):
        self.cache = {}
        self.ttl = 86400  # 24 hours

    def get(self, symbol):
        if symbol in self.cache:
            data, timestamp = self.cache[symbol]
            if time.time() - timestamp < self.ttl:
                return data
        return None

    def set(self, symbol, data):
        self.cache[symbol] = (data, time.time())
```

### 3. Batch Requests

For calendar endpoints, request ranges instead of individual dates:

**Inefficient** (7 calls):
```python
for date in date_range:
    get_earnings(date)
```

**Efficient** (1 call):
```python
get_earnings(from_date, to_date)
```

### 4. Use Appropriate Intervals

For intraday data (5 calls each), choose the interval that matches your needs:

- **1-minute**: Most granular, largest response
- **5-minute**: Good balance for intraday analysis
- **1-hour**: Sufficient for daily patterns

### 5. Limit Historical Range

Only request the date range you actually need:

**Excessive**:
```python
# Getting 20 years when you only need 1 year
get_eod("AAPL.US", from_date="2004-01-01", to_date="2024-01-01")
```

**Appropriate**:
```python
# Only request what you need
get_eod("AAPL.US", from_date="2023-01-01", to_date="2024-01-01")
```

### 6. Minimize Expensive Endpoint Usage

**10-call endpoints** (Fundamentals): Cache aggressively, request only when needed.

**5-call endpoints** (News, Intraday, Technical): Batch tickers in one call where possible.

**News/Sentiment formula** (5 + 5*N): Request multiple symbols in one call rather than individually.

## Implementing Rate Limiting

### Python Example

```python
import time
from functools import wraps

class RateLimiter:
    def __init__(self, calls_per_second=5):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0

    def wait(self):
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.wait()
            return func(*args, **kwargs)
        return wrapper

# Usage
limiter = RateLimiter(calls_per_second=5)

@limiter
def fetch_data(symbol):
    # Your API call here
    pass
```

### Exponential Backoff

Handle 429 errors with exponential backoff:

```python
import time
import requests

def fetch_with_retry(url, max_retries=5):
    """Fetch with exponential backoff on rate limit."""
    for attempt in range(max_retries):
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            # Rate limited
            retry_after = int(response.headers.get('Retry-After', 2 ** attempt))
            print(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            continue

        # Other error
        response.raise_for_status()

    raise Exception(f"Max retries ({max_retries}) exceeded")
```

### Request Queue

Implement a request queue for multiple operations:

```python
import queue
import threading
import time

class RequestQueue:
    def __init__(self, requests_per_second=5):
        self.queue = queue.Queue()
        self.interval = 1.0 / requests_per_second
        self.worker = threading.Thread(target=self._process_queue, daemon=True)
        self.worker.start()

    def add_request(self, func, *args, **kwargs):
        """Add request to queue."""
        future = queue.Queue()
        self.queue.put((func, args, kwargs, future))
        return future

    def _process_queue(self):
        """Process queued requests at controlled rate."""
        while True:
            func, args, kwargs, future = self.queue.get()
            try:
                result = func(*args, **kwargs)
                future.put(('success', result))
            except Exception as e:
                future.put(('error', e))
            time.sleep(self.interval)
            self.queue.task_done()

# Usage
request_queue = RequestQueue(requests_per_second=5)

def fetch_symbol(symbol):
    # Your fetch logic
    pass

# Queue requests
futures = []
for symbol in symbols:
    future = request_queue.add_request(fetch_symbol, symbol)
    futures.append(future)

# Collect results
results = [f.get() for f in futures]
```

## Monitoring & Alerts

### Track Usage

Implement usage tracking:

```python
class UsageTracker:
    def __init__(self):
        self.daily_count = 0

    def increment(self, calls=1):
        """Increment usage counter."""
        self.daily_count += calls

    def check_limits(self, daily_limit=100000):
        """Check if approaching daily limit."""
        daily_pct = (self.daily_count / daily_limit) * 100

        if daily_pct > 90:
            print(f"Warning: {daily_pct:.1f}% of daily limit used")

        return daily_pct
```

### Set Up Alerts

Configure alerts when approaching limits:

```python
def send_alert(message):
    """Send alert (email, Slack, etc.)."""
    # Implement your alert mechanism
    print(f"ALERT: {message}")

def check_quota(token):
    """Check quota and alert if necessary."""
    response = requests.get(f"https://eodhd.com/api/internal-user?api_token={token}")
    data = response.json()

    # Main subscription quota
    used = data.get('apiRequests', 0)
    limit = data.get('dailyRateLimit', 100000)
    extra = data.get('extraLimit', 0)
    pct_used = (used / limit) * 100

    if pct_used > 90:
        send_alert(f"{pct_used:.1f}% of daily API limit used ({used}/{limit})!")
        if extra > 0:
            print(f"Extra API calls available as buffer: {extra}")

    # Marketplace quota
    mp = data.get('availableMarketplaceDataFeeds', [])
    if isinstance(mp, dict):
        mp_used = mp.get('requestsSpent', 0)
        mp_limit = mp.get('dailyRateLimit', 100000)
        mp_pct = (mp_used / mp_limit) * 100
        if mp_pct > 90:
            send_alert(f"Marketplace: {mp_pct:.1f}% used ({mp_used}/{mp_limit})! Resets at {mp['timeToReset']}")
```

## Best Practices

1. **Understand the cost**: Know how many API calls each endpoint consumes before building workflows
2. **Monitor usage regularly**: Check dashboard at https://eodhd.com/cp/api or use `/internal-user` endpoint
3. **Implement caching**: Reduce redundant API calls, especially for 10-call endpoints
4. **Use bulk endpoints**: 100 calls for an entire exchange vs 1 call per symbol individually
5. **Rate limit your requests**: Stay within 1,000 requests per minute
6. **Handle 429 errors gracefully**: Implement retry logic with exponential backoff
7. **Request only what you need**: Avoid over-fetching data ranges
8. **Cache expensive endpoints**: Fundamentals (10 calls), News/Sentiment (5 + 5*N)
9. **Spread requests evenly**: Don't burst all requests at once within a minute
10. **Consider Extra API Calls**: Purchase as a buffer if you occasionally exceed daily limits
11. **Monitor Marketplace quotas separately**: Each Marketplace subscription has its own 100,000-call limit. Check `availableMarketplaceDataFeeds.requestsSpent` in the `/internal-user` response.

## Upgrading & Increasing Limits

### Signs You Need More Capacity

- Regularly hitting the 100,000 daily call limit
- Frequently receiving 402 or 429 errors
- Need to process more symbols per day

### Options

1. **Increase daily limit**: Via dashboard "Increase Daily Limit" option (subscription plans only)
2. **Buy Extra API Calls**: Buffer for overflow, purchased via dashboard, never expire
3. **Upgrade subscription plan**: Contact support for enterprise-level needs

### Contact

- Support: support@eodhistoricaldata.com
- Dashboard: https://eodhd.com/cp/api

## HTTP Error Codes

| HTTP Code | Meaning |
|-----------|---------|
| 200 | Success |
| 402 | Payment Required — daily API call limit exhausted |
| 403 | Unauthorized — invalid or missing API key |
| 429 | Too Many Requests — minute request limit exceeded |
| 500 | Server Error — retry after a short delay |

## SDK Quota Management

Some official SDKs include built-in quota management:

- **R package (eodhdR2)**: Local caching and quota tracking
- **MCP Server**: Rate limiting and retry logic built in

See `sdks-and-integrations.md` for full SDK details.

## Related Resources

- **Authentication**: See `authentication.md`
- **Pricing & Plans**: See `pricing-and-plans.md` for subscription tier details
- **User endpoint**: `/api/internal-user` for quota checking (main + Marketplace) — see `../endpoints/user-details.md`
- **Account dashboard**: https://eodhd.com/cp/api
- **Support**: support@eodhistoricaldata.com
