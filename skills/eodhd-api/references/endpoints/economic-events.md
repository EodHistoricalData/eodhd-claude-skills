# Economic Events API

Status: complete
Source: financial-apis (Economic Events Data API)
Docs: https://eodhd.com/financial-apis/economic-events-data-api
Provider: EODHD
Base URL: https://eodhd.com/api
Path: /economic-events
Method: GET
Auth: api_token (query)

## Purpose

Fetches economic events and indicators by date range, country, and comparison type.
Includes actual values, estimates, and changes for events like GDP releases, employment data,
inflation reports, and central bank decisions. Useful for macro analysis and event-driven trading.

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| api_token | Yes | string | Your API key for authentication |
| from | No | string (YYYY-MM-DD) | Start date for data retrieval |
| to | No | string (YYYY-MM-DD) | End date for data retrieval |
| country | No | string | ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB', 'DE') |
| comparison | No | string | Comparison type: 'mom' (month-over-month), 'qoq' (quarter-over-quarter), 'yoy' (year-over-year) |
| offset | No | integer | Data offset (0-1000). Default: 0 |
| limit | No | integer | Number of results (0-1000). Default: 50 |

## Response (shape)

Array of economic event objects:

```json
[
  {
    "type": "Nonfarm Payrolls",
    "comparison": null,
    "period": "May",
    "country": "US",
    "date": "2025-06-03 16:30:00",
    "actual": 275,
    "previous": 256,
    "estimate": 250,
    "change": 19,
    "change_percentage": 7.42
  },
  {
    "type": "CPI",
    "comparison": "yoy",
    "period": "May",
    "country": "US",
    "date": "2025-06-12 12:30:00",
    "actual": 3.2,
    "previous": 3.4,
    "estimate": 3.3,
    "change": -0.2,
    "change_percentage": -5.88
  }
]
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| type | string | Event type (e.g., 'Nonfarm Payrolls', 'CPI', 'GDP') |
| comparison | string/null | Comparison type: 'mom', 'qoq', 'yoy', or null |
| period | string/null | Period for the data (e.g., 'May', 'Q1') |
| country | string | ISO 3166 country code |
| date | string (datetime) | Event date and time (YYYY-MM-DD HH:MM:SS) |
| actual | number/null | Actual reported value |
| previous | number/null | Previous period's value |
| estimate | number/null | Consensus estimate |
| change | number/null | Change from previous value |
| change_percentage | number/null | Percentage change from previous |

### Common Event Types

- Employment: Nonfarm Payrolls, Unemployment Rate, Initial Jobless Claims
- Inflation: CPI, PPI, PCE Price Index
- Growth: GDP, Industrial Production, Retail Sales
- Manufacturing: ISM Manufacturing PMI, Durable Goods Orders
- Housing: Existing Home Sales, Building Permits, Housing Starts
- Central Bank: Fed Interest Rate Decision, ECB Rate Decision

## Federal Reserve Interest Rate Events

### Overview

**Fed Interest Rate** events represent Federal Open Market Committee (FOMC) meetings where the Federal Reserve decides to **raise, lower, or hold** the federal funds rate target.

**What This Represents**:
- FOMC monetary policy decisions (8 scheduled meetings per year)
- Federal funds rate target (overnight lending rate between banks)
- Changes of typically 0.25% (25 basis points) or 0.50% (50 basis points)
- Critical for financial markets - affects borrowing costs, currency values, stock prices

**Event Type**: `"Fed Interest Rate"` or `"Fed Interest Rate Decision"`

### Querying Fed Rate Events

**Filter by Type**:
```bash
# Get recent Fed rate decisions
curl "https://eodhd.com/api/economic-events?country=US&from=2023-01-01&to=2024-12-31&api_token=YOUR_API_KEY&fmt=json" | jq '.[] | select(.type | contains("Fed Interest Rate"))'
```

**Search by Date Range** (FOMC meeting dates):
```bash
# Get Fed events for specific date range
curl "https://eodhd.com/api/economic-events?country=US&from=2024-01-01&to=2024-12-31&api_token=YOUR_API_KEY&fmt=json"
```

### Example Response

**Rate Increase (Hiking Cycle)**:
```json
{
  "type": "Fed Interest Rate",
  "comparison": null,
  "period": null,
  "country": "US",
  "date": "2023-07-26 18:00:00",
  "actual": 5.50,
  "previous": 5.25,
  "estimate": 5.50,
  "change": 0.25,
  "change_percentage": 4.76
}
```

**Rate Hold (Pause)**:
```json
{
  "type": "Fed Interest Rate",
  "comparison": null,
  "period": null,
  "country": "US",
  "date": "2024-06-12 18:00:00",
  "actual": 5.50,
  "previous": 5.50,
  "estimate": 5.50,
  "change": 0.00,
  "change_percentage": 0.00
}
```

**Rate Decrease (Cutting Cycle)**:
```json
{
  "type": "Fed Interest Rate",
  "comparison": null,
  "period": null,
  "country": "US",
  "date": "2024-09-18 18:00:00",
  "actual": 5.00,
  "previous": 5.50,
  "estimate": 5.25,
  "change": -0.50,
  "change_percentage": -9.09
}
```

### Field Interpretation for Fed Rate Events

| Field | Meaning for Fed Rate Events |
|-------|----------------------------|
| `actual` | **New federal funds rate** target (in percentage) after FOMC decision |
| `previous` | Federal funds rate before this meeting |
| `estimate` | Market consensus expectation before the meeting |
| `change` | Change in rate (percentage points): positive = hike, negative = cut, zero = hold |
| `change_percentage` | Percentage change in the rate itself |
| `date` | FOMC meeting announcement time (typically 2:00 PM ET / 18:00:00 UTC) |

### Python Example: Track Fed Rate History

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

def get_fed_rate_history(api_token, from_date=None, to_date=None):
    """
    Get historical Federal Reserve interest rate decisions.

    Args:
        api_token: EODHD API token
        from_date: Start date (YYYY-MM-DD), defaults to 2 years ago
        to_date: End date (YYYY-MM-DD), defaults to today

    Returns:
        DataFrame with Fed rate history
    """
    # Default date range: last 2 years
    if not to_date:
        to_date = datetime.now().strftime('%Y-%m-%d')
    if not from_date:
        from_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')

    url = "https://eodhd.com/api/economic-events"
    params = {
        "api_token": api_token,
        "country": "US",
        "from": from_date,
        "to": to_date,
        "fmt": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    events = response.json()

    # Filter for Fed Interest Rate events only
    fed_events = [
        event for event in events
        if "Fed Interest Rate" in event.get("type", "")
    ]

    # Convert to DataFrame
    df = pd.DataFrame(fed_events)

    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        # Add action column
        df['action'] = df['change'].apply(lambda x:
            'HIKE' if x > 0 else ('CUT' if x < 0 else 'HOLD')
        )

    return df


def summarize_fed_actions(df):
    """Summarize Fed rate actions"""
    if df.empty:
        print("No Fed rate data found")
        return

    print("\n" + "=" * 70)
    print("Federal Reserve Interest Rate History")
    print("=" * 70)

    for _, row in df.iterrows():
        action = row['action']
        symbol = {'HIKE': '📈', 'CUT': '📉', 'HOLD': '⏸️'}.get(action, '')

        print(f"\n{row['date'].strftime('%Y-%m-%d')} {symbol} {action}")
        print(f"  Rate: {row['previous']:.2f}% → {row['actual']:.2f}% (change: {row['change']:+.2f}%)")

        if row['estimate'] and row['estimate'] != row['actual']:
            surprise = "higher" if row['actual'] > row['estimate'] else "lower"
            print(f"  Market expected: {row['estimate']:.2f}% (actual was {surprise})")

    # Summary statistics
    total_meetings = len(df)
    hikes = len(df[df['action'] == 'HIKE'])
    cuts = len(df[df['action'] == 'CUT'])
    holds = len(df[df['action'] == 'HOLD'])

    total_change = df['actual'].iloc[-1] - df['actual'].iloc[0]

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Total FOMC meetings: {total_meetings}")
    print(f"  Rate hikes: {hikes} 📈")
    print(f"  Rate cuts: {cuts} 📉")
    print(f"  Rate holds: {holds} ⏸️")
    print(f"Net change: {total_change:+.2f} percentage points")
    print(f"Current rate: {df['actual'].iloc[-1]:.2f}%")


# Usage Example
if __name__ == "__main__":
    api_token = "YOUR_API_KEY"

    # Get Fed rate history for last 2 years
    fed_history = get_fed_rate_history(api_token)

    # Display summary
    summarize_fed_actions(fed_history)

    # Export to CSV
    fed_history.to_csv('fed_rate_history.csv', index=False)
    print("\nData exported to fed_rate_history.csv")
```

**Output Example**:
```
======================================================================
Federal Reserve Interest Rate History
======================================================================

2023-02-01 📈 HIKE
  Rate: 4.50% → 4.75% (change: +0.25%)
  Market expected: 4.75% (actual matched)

2023-03-22 📈 HIKE
  Rate: 4.75% → 5.00% (change: +0.25%)

2023-05-03 📈 HIKE
  Rate: 5.00% → 5.25% (change: +0.25%)

2023-07-26 📈 HIKE
  Rate: 5.25% → 5.50% (change: +0.25%)

2023-09-20 ⏸️ HOLD
  Rate: 5.50% → 5.50% (change: +0.00%)

2024-09-18 📉 CUT
  Rate: 5.50% → 5.00% (change: -0.50%)
  Market expected: 5.25% (actual was lower - surprise cut!)

======================================================================
Summary
======================================================================
Total FOMC meetings: 6
  Rate hikes: 4 📈
  Rate cuts: 1 📉
  Rate holds: 1 ⏸️
Net change: +0.50 percentage points
Current rate: 5.00%
```

### Use Cases for Fed Rate Data

#### 1. Trading Strategy Backtesting
```python
def analyze_market_reaction_to_fed(fed_df, stock_prices_df):
    """Analyze how markets react to Fed rate changes"""
    reactions = []

    for _, meeting in fed_df.iterrows():
        meeting_date = meeting['date'].date()
        action = meeting['action']

        # Get price before and after Fed decision
        try:
            price_before = stock_prices_df[stock_prices_df['date'] < meeting_date].iloc[-1]['close']
            price_after = stock_prices_df[stock_prices_df['date'] > meeting_date].iloc[0]['close']

            reaction = ((price_after - price_before) / price_before) * 100

            reactions.append({
                'date': meeting_date,
                'action': action,
                'rate_change': meeting['change'],
                'market_reaction_pct': reaction
            })
        except:
            continue

    return pd.DataFrame(reactions)
```

#### 2. Economic Cycle Identification
```python
def identify_rate_cycles(fed_df):
    """Identify hiking and cutting cycles"""
    cycles = []
    current_cycle = None
    cycle_start = None

    for _, row in fed_df.iterrows():
        if row['action'] in ['HIKE', 'CUT']:
            if current_cycle != row['action']:
                if current_cycle:
                    cycles.append({
                        'type': current_cycle,
                        'start': cycle_start,
                        'end': row['date']
                    })
                current_cycle = row['action']
                cycle_start = row['date']

    return pd.DataFrame(cycles)
```

#### 3. Rate Expectation vs Reality
```python
def analyze_fed_surprises(fed_df):
    """Identify when Fed surprised markets"""
    surprises = []

    for _, row in fed_df.iterrows():
        if row['estimate'] and row['actual'] != row['estimate']:
            surprise_direction = "hawkish" if row['actual'] > row['estimate'] else "dovish"
            surprise_magnitude = abs(row['actual'] - row['estimate'])

            surprises.append({
                'date': row['date'],
                'expected': row['estimate'],
                'actual': row['actual'],
                'surprise': surprise_magnitude,
                'direction': surprise_direction
            })

    return pd.DataFrame(surprises)
```

### Important Notes

⚠️ **FOMC Meeting Schedule**: Federal Reserve holds 8 regularly scheduled meetings per year (approximately every 6 weeks)

⚠️ **Emergency Meetings**: Occasionally, the Fed holds unscheduled meetings in response to economic crises

⚠️ **Announcement Time**: Fed rate decisions typically announced at 2:00 PM ET (18:00 UTC)

⚠️ **Market Impact**: Fed rate decisions are among the most significant market-moving events

⚠️ **Forward Guidance**: FOMC statements and press conferences provide guidance on future rate path (not included in this API, but important context)

### Related Central Bank Events

The Economic Events API also includes interest rate decisions from other major central banks:

- **ECB** (European Central Bank): `"ECB Rate Decision"`
- **BOE** (Bank of England): `"BOE Rate Decision"`
- **BOJ** (Bank of Japan): `"BOJ Rate Decision"`
- **BOC** (Bank of Canada): `"BOC Rate Decision"`
- **RBA** (Reserve Bank of Australia): `"RBA Rate Decision"`

These can be queried using the same approach with appropriate country codes (e.g., `country=GB` for BOE).

## Example Requests

```bash
# Economic events for the next week
curl "https://eodhd.com/api/economic-events?api_token=demo&fmt=json"

# US events for specific date range
curl "https://eodhd.com/api/economic-events?country=US&from=2025-01-01&to=2025-01-31&api_token=demo&fmt=json"

# Year-over-year comparisons only
curl "https://eodhd.com/api/economic-events?comparison=yoy&limit=20&api_token=demo&fmt=json"

# German events with pagination
curl "https://eodhd.com/api/economic-events?country=DE&limit=50&offset=0&api_token=demo&fmt=json"

# Using the helper client
python eodhd_client.py --endpoint economic-events --from-date 2025-01-01 --to-date 2025-01-31
```

## Notes

- `actual` is null for upcoming events not yet released
- Times are in the format 'YYYY-MM-DD HH:MM:SS' (typically UTC)
- Country codes use ISO 3166-1 alpha-2 (US, GB, DE, JP, CN, etc.)
- Use `comparison` filter to get only specific comparison types
- Maximum 1000 results per request; use offset for pagination
- API call consumption: 1 call per request
- **Timezone**: All event timestamps are in **UTC**.
- **From/to parameters and limit**: By default, the API returns only 50 events per response. To access older events, use the `&limit=` parameter and specify `from` and `to` dates precisely. For example, to retrieve events from the year 2020, use both `&from=2020-01-01&to=2020-12-31` along with an appropriate limit.
- **Offset beyond 1000**: If the maximum offset of 1000 is not enough, use the `from` and `to` parameters in conjunction with `offset` to paginate deeper into history by narrowing the date range.
- **Data depth**: Economic events data is available from **2020** onwards.

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
