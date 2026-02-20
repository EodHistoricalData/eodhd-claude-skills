# EODHD Data Update Times & Frequencies

This document describes when various data types are updated in the EODHD API, based on official EODHD documentation.

## Overview

EODHD provides different update frequencies depending on:
- Data type (EOD, intraday, real-time, fundamentals, etc.)
- Exchange and market hours
- Asset class (stocks, forex, crypto, etc.)
- Data complexity and quality checks

**Important**: All times mentioned are based on official EODHD schedules and may vary slightly due to data quality checks or exchange-specific factors. Much of the data in this document, such as update times and processing delays, is empirical in nature and is provided for guidance only. The EODHD API is constantly changing and evolving, so actual behavior may differ. For any questions, please email supportlevel1@eodhistoricaldata.com

## End-of-Day (EOD) Data

### US Major Exchanges (NYSE, NASDAQ)

**Update Time**: 15 minutes after market close (16:00 EST)

- Regular trading closes: **16:00 EST**
- Data typically available: **16:15 EST**
- Adjusted for corporate actions: **Same day**

**Note**: ETFs traded on NYSE ARCA may update within the 2-3 hours timeframe (not the 15-minute window).

### US Special Categories

#### US Mutual Funds, PINK, OTCBB, Some Indices

**Update Window**: Next morning, 3:00-6:00 AM EST

- Update starts: **3:00-4:00 AM EST**
- Update completes: **5:00-6:00 AM EST**
- Some adjustments continue until: **12:00 PM EST**

**Reason**: Data quality issues, especially for Mutual Funds and Pink Stocks. "Updated prices" continue to arrive until 3-4 AM EST.

**Price Source Evolution**:
- First prices: NOCP (National Odd-Lot Clearance Provider)
- Later updates: Aggregated SIP (Securities Information Processor) data
- Low-volume tickers not traded on NASDAQ may show small differences

#### OTC Markets

**Update Time**: Variable, until 5:00-6:00 AM EST

**Recent Observations**: Complete dataset typically available by **3:00 AM EST**

**Note**: First prices are NOCP, but later updates use aggregated SIP data. For low-volume tickers not traded on NASDAQ, there could be small differences.

### International Exchanges

**Standard Update Time**: 2-3 hours after market close

**Coverage**:
- Major exchanges: Most international exchanges
- Update timing: Consistent 2-3 hour delay
- See exchange-specific times in table below

### INDX (Indices Exchange)

**Multiple Updates Per Day**:

| Update Time (New York Time) | Purpose |
|----------------------------|---------|
| 00:30 AM EST | First update |
| 04:30 AM EST | Morning update |
| 07:00 AM EST | Pre-market update |
| 04:30 PM EST | Post-close update |
| 08:30 PM EST | Evening update |

**Recommended Update Time**: 10-15 minutes after each scheduled update

**Reason**: INDX accumulates indices traded around the world, requiring multiple daily updates.

### Detailed Update Schedule by Exchange

| Exchange/Region | Market Close (Local) | Update Available | Notes |
|----------------|---------------------|------------------|-------|
| **US - NYSE/NASDAQ** | 16:00 EST | 16:15 EST | 15-minute delay |
| **US - ARCA ETFs** | 16:00 EST | 18:00-19:00 EST | 2-3 hour delay |
| **US - Mutual Funds** | N/A | 03:00-06:00 AM EST next day | Quality checks |
| **US - PINK/OTCBB** | 16:00 EST | 03:00-06:00 AM EST next day | Quality checks |
| **US - OTC** | 16:00 EST | By 03:00 AM EST next day | Variable |
| **LSE (London)** | 16:30 GMT | ~18:30-19:30 GMT | 2-3 hours |
| **XETRA (Germany)** | 17:30 CET | ~19:30-20:30 CET | 2-3 hours |
| **Euronext (Paris)** | 17:30 CET | ~19:30-20:30 CET | 2-3 hours |
| **Hong Kong** | 16:00 HKT | ~18:00-19:00 HKT | 2-3 hours |
| **Shanghai/Shenzhen** | 15:00 CST | ~17:00-18:00 CST | 2-3 hours |
| **EUFUND** | N/A | 19:00 GMT | Check 1 hour later (20:00 GMT) |

## Intraday Data

### Update Frequencies

| Interval | Update Time | Coverage | Notes |
|----------|-------------|----------|-------|
| **5-minute bars** | 2-3 hours after close | Regular hours only | Standard delay |
| **1-minute bars** | 2-3 hours after after-hours close | Includes pre/post-market | US markets |

**1-Minute Data Details**:
- Includes pre-market and post-market prices (for US stocks)
- Update: 2-3 hours after after-hours trading ends (~20:00 EST)

**5-Minute Data Details**:
- Regular trading hours only
- Update: 2-3 hours after market close
- No post-market included

### Historical Intraday Retention

| Interval | Maximum Range |
|----------|---------------|
| 1m | 120 days |
| 5m | 600 days |
| 1h | 7200 days |

- **Intervals**: 1m, 5m, 1h
- **Format**: OHLCV bars with timestamps

## Options Data (Marketplace)

### EOD Options Data

**Update Time**: 10:00 PM-12:00 AM EST

**Recommended Check**: After midnight EST for complete data

**Data Type**: Historical data only (not real-time)

**Frequency**: Every trading day

**Coverage**:
- All US options chains
- Greeks calculations
- Implied volatility
- Open interest and volume

**Access**: Via Marketplace API endpoints (`/api/mp/unicornbay/options/...`).

## Forex (FOREX)

### EOD Updates

**Update Frequency**: Every 4 hours, starting at 00:00 GMT

**Update Schedule**:
- 00:00 GMT
- 04:00 GMT
- 08:00 GMT
- 12:00 GMT
- 16:00 GMT
- 20:00 GMT

**Recommended Fetch Time**: 1-2 hours after each update

**Reason**: Integrity checks are performed on EOD data after initial update.

**Preliminary Data**: Some currencies may get preliminary EOD data during the day, but receive corrected data after the day is over.

### Real-Time Forex

**Market Hours**: 24/5 (Sunday 17:00 EST - Friday 17:00 EST)

**Update Frequency**: Real-time (continuous)

**Latency**: < 100ms for real-time plans, 15-20 minutes for standard plans

## Cryptocurrencies (CC)

### EOD Updates

**Update Frequency**: Every 4 hours, starting at 00:00 GMT

**Update Schedule**: Same as Forex (every 4 hours)

**Recommended Fetch Time**: 1-2 hours after each update

**Data Quality**: Preliminary data during the day, corrected data after day ends

### Real-Time Crypto

**Market Hours**: 24/7/365

**Update Frequency**: Real-time (continuous)

**Data Sources**: Multiple cryptocurrency exchanges

## Fundamentals Data

### General Update Schedule

**Update Frequency**: Daily (various times throughout the day)

**Primary Update Window**: 02:00-04:00 UTC (nightly batch)

**Reason for Varied Times**: Multiple data sources with different update schedules

### Component-Specific Update Frequencies

| Component | Update Frequency | Typical Delay | Notes |
|-----------|-----------------|---------------|-------|
| **Highlights** | Daily | Same day | Always current |
| **Financial Statements** | Quarterly | 24-48 hours | After company filing |
| **Valuation** | Weekly | End of week | Calculated metrics |
| **Earnings** | Quarterly | 1 hour | After release |
| **Analyst Estimates** | Daily | Same day | As analysts revise |
| **Analyst Ratings** | Quarterly | Per quarter | Quarterly updates |
| **Ownership Data** | Monthly | 1-2 weeks | After month end |
| **Insider Transactions** | Weekly | Within 24 hours | SEC Form 4 filings |
| **Officers** | Weekly | End of week | Management changes |
| **ESG Scores** | Monthly/Quarterly | Varies | Provider dependent |
| **FullTimeEmployees** | Quarterly | Per quarter | From public reports |
| **ETF Holdings** | Twice weekly | 3-4 days | Tuesday, Friday updates |
| **ETF Asset Allocation** | Monthly | 1 week | Monthly refresh |
| **ETF Sector Weights** | Monthly | Up to 1 week | Monthly refresh |
| **SharesStats** | Daily (US) | 2-3 days (US), 1 week (non-US) | May lag splits |
| **Outstanding Shares** | Daily | 2-3 days | May lag split adjustments |
| **Short Interest** | Bi-weekly | 2 weeks | NASDAQ schedule |
| **Index Components** | Weekly | Up to 2 weeks | Current constituents |

### Regional Delays for Fundamentals

**US Companies**:
- Filing to API: **Next day**
- Example: Report filed Monday, available Tuesday

**Major EU Companies**:
- Filing to API: **2-3 days**
- Example: Report filed Monday, available Wednesday-Thursday

**Other Exchanges**:
- Filing to API: **Within 1 week**
- Example: Report filed Monday, available by next Monday

### Financial Statements Processing

**Sources**:
- US: SEC EDGAR filings (10-K, 10-Q, 8-K)
- International: Local regulatory filings

**Processing Time**:
- Automated extraction: 1-4 hours after filing
- Manual verification: 24-48 hours for complex cases
- Historical corrections: Ongoing as needed

## Calendar Events

### Calendar API Updates

**US Exchanges**: Next day

**Other Exchanges**: During the following week

**Update Timing**: Continuous throughout the day for US, batch for international

### Earnings Calendar

**Update Frequency**: Real-time for announcements, next day for results

**Data Freshness**:
- Upcoming earnings: Continuous updates
- Actual results: Next day
- Estimates: Daily updates
- **Surprise Difference**: Next day after earnings

**Coverage**:
- Lookback: Historical earnings
- Lookahead: Up to 3-6 months

### Dividends Calendar & History

**Update Frequency**: Daily

**Update Time**: 02:00-04:00 UTC (nightly batch)

**Coverage**:
- Announcement dates
- Ex-dividend dates
- Payment dates
- Historical dividends from 2000+

### Splits Calendar & History

**Update Frequency**: Daily

**Update Time**: 02:00-04:00 UTC (nightly batch)

**Split Data Timing**:
- Split announcement: Same day
- Historical price adjustment: After market close same day (rarely next day)
- API availability: Within 1 hour

**Note**: Outstanding shares section may take 2-3 days to sync with split data.

**Coverage**:
- Announced splits (future)
- Historical splits from 2000+
- Reverse splits included

### IPOs Calendar

**Update Frequency**: Multiple times per day

**Coverage**:
- Filed IPOs: As announced
- Priced IPOs: Same day
- Expected dates: Subject to change
- Withdrawn IPOs: Same day

**Historical Range**:
- Lookback: From January 2015
- Lookahead: Up to 2-3 weeks

## News & Sentiment

### Financial News API

**Update Frequency by Symbol**:

| Symbol Type | Update Frequency | Examples |
|------------|-----------------|----------|
| **Major stocks** (highest market cap) | Every 15 minutes | AAPL, MSFT, GOOGL |
| **Popular symbols** | Every 30 minutes | Large-cap stocks |
| **Other tickers** | Every 4 hours | Mid/small-cap |

**News Recalculation**: On each update cycle

### Sentiment API

**Update Frequency**:
- **Major stocks**: Every 15 minutes (AAPL, MSFT, etc.)
- **Other symbols**: Every 30 minutes

**Calculation Trigger**: Each time news is updated

**Sentiment Recalculation**: Real-time with news updates

**Data Processing**: AI-based sentiment analysis on each news article

## Economic Events Data API

### Update Timing

**Standard Updates**: As published by government agencies

**FED Announcements**: Up to **1.5 hours delay** (not real-time)

**Typical Release Frequency**:
- GDP: Quarterly
- Inflation (CPI): Monthly
- Unemployment: Monthly
- Interest rates: As changed by central banks

**EODHD Processing**: Within 1 hour of official release (except FED)

**Coverage**: 50+ countries

## Institutional & Ownership Data

### Holders / Institutional Ownership

**Data Source**: Quarterly reports (13F filings)

**Update Frequency**: Quarterly

**Filing Deadline**: 45 days after quarter-end

**Change Percentage**: Quarter-to-quarter changes

**Example Timeline**:
- Q1 ends: March 31
- Filing deadline: May 15 (45 days)
- Data available: Mid-May to early June

### Mutual Fund Portfolio Data

**Update Frequency**: Quarterly

**Data Lag**: Similar to 13F filings (45 days after quarter)

## Daily API Call Reset

### Quota Reset Time

**Reset Time**: Midnight GMT (00:00 GMT)

**What Resets**:
- Daily API call limits
- Daily rate limit counters
- Usage statistics for the day

**Monthly Reset**: 1st of each month at 00:00 GMT

## Historical Data Coverage

### End-of-Day (EOD) Data

**US Exchanges**:
- Coverage: From inception for most symbols
- Example: Ford Motor Company data from June 1972
- Major US stocks: 1970s-1980s and later
- Total coverage: 45,000+ US stocks, ETFs, and Mutual Funds

**International Exchanges**:
- Standard coverage: From January 2000
- Major companies: Further back (1990s)
- Regional variations: Depends on exchange

**Data Granularity**: Daily and weekly data available

### Fundamentals Data

**US Exchanges**:
- Major symbols: Back to 2000 (some earlier)
- Coverage: 19+ years of data
- NYSE, NASDAQ, ARCA: 7,000+ symbols with 10+ years
- Minor companies: At least 7-8 years yearly data
- Quarterly data: Previous 20 quarters for most symbols

**International Exchanges**:
- Major companies: Back to 2000
- Coverage: Most world exchanges
- Growing dataset: Continually expanding

**Supported Exchanges**: See [exchanges.md](exchanges.md) for complete list

### Index Components

**Current Constituents**: Available for all indices

**Historical Constituents**:
- **S&P 500**: From 2000 onwards
- **Other indices**: Current constituents only

### News Data

**Standard Coverage**: From March 2021

**Major Tickers** (AAPL, MSFT, etc.): 3-4 years of historical news

**Data Retention**: Typically 12-24 months for most symbols

### Sentiment Data

**Coverage**: From 2018

**Historical Range**: 3+ years of sentiment scores

**Granularity**: Daily sentiment scores

### Economic Events

**Coverage**: From 2020

**Historical Data**: 4+ years of economic event history

**Data Types**: GDP, inflation, unemployment, interest rates, etc.

## Best Practices for Data Fetching

### Timing Your Requests

**EOD Data - US Markets**:
```python
# NYSE/NASDAQ: Wait 20 minutes after close
fetch_time = market_close + timedelta(minutes=20)  # 16:20 EST

# Mutual Funds/PINK/OTCBB: Fetch in the morning
fetch_time = next_day + timedelta(hours=6)  # 6:00 AM EST next day

# OTC: Early morning fetch
fetch_time = next_day + timedelta(hours=3, minutes=30)  # 3:30 AM EST
```

**EOD Data - International**:
```python
# Standard: Wait 3 hours after close
fetch_time = market_close + timedelta(hours=3)

# Safe buffer: Add 30 minutes
fetch_time = market_close + timedelta(hours=3, minutes=30)
```

**Intraday Data**:
```python
# 5-minute bars: 3 hours after close
fetch_time = market_close + timedelta(hours=3)

# 1-minute bars (with pre/post-market): 2-3 hours after after-hours close (20:00 EST)
fetch_time = after_hours_close + timedelta(hours=3)  # ~23:00 EST
```

**Forex/Crypto**:
```python
# Wait 2 hours after scheduled update for integrity checks
fetch_time = scheduled_update + timedelta(hours=2)

# Example: 00:00 GMT update -> fetch at 02:00 GMT
```

**Fundamentals**:
```python
# US companies: Next day after filing
fetch_time = filing_date + timedelta(days=1)

# Major EU companies: 3 days after filing
fetch_time = filing_date + timedelta(days=3)

# Other exchanges: 1 week after filing
fetch_time = filing_date + timedelta(days=7)
```

### Scheduling Considerations

1. **Avoid immediate fetches**: Don't request data at exact market close time
2. **Add buffer time**: Account for processing delays
3. **Handle missing data gracefully**: Data might not be available yet
4. **Check timestamps**: Verify data freshness in responses
5. **Use appropriate intervals**: Match update frequency to your needs

### Caching Strategy by Data Type

| Data Type | Cache Duration | Reason |
|-----------|---------------|--------|
| EOD prices | Until next trading day | Updated once per day |
| Intraday (5-min) | 5 minutes | Update frequency |
| Intraday (1-min) | 1 minute | Update frequency |
| Real-time quotes | 15-60 seconds | Based on plan |
| Fundamentals (Highlights) | 24 hours | Updated daily |
| Fundamentals (Financials) | 7 days | Updated quarterly |
| News | 30-60 minutes | Update frequency varies |
| Sentiment | 30-60 minutes | Updates with news |
| Calendar events | 24 hours | Updated daily |

## Monitoring Data Freshness

### Checking Data Timestamps

Always check timestamp fields in API responses:

```python
def is_data_fresh(response, max_age_hours=24):
    """Check if data is within acceptable age."""
    if 'timestamp' in response:
        data_time = datetime.fromisoformat(response['timestamp'])
        age = datetime.now(timezone.utc) - data_time
        return age.total_seconds() / 3600 < max_age_hours
    return False
```

### Handling Delayed Data

```python
def fetch_with_retry(symbol, max_retries=3, retry_delay=300):
    """Retry fetch if data isn't available yet."""
    for attempt in range(max_retries):
        data = fetch_eod_data(symbol)
        if data and is_data_fresh(data):
            return data

        if attempt < max_retries - 1:
            print(f"Data not ready, waiting {retry_delay}s...")
            time.sleep(retry_delay)

    raise Exception("Data not available after retries")
```

## Time Zone Reference

Key time zones used by EODHD:

| Time Zone | Abbreviation | UTC Offset | Notes |
|-----------|-------------|------------|-------|
| Coordinated Universal Time | UTC/GMT | +0:00 | Reference time |
| US Eastern | EST/EDT | -5:00/-4:00 | NYSE, NASDAQ |
| Central European | CET/CEST | +1:00/+2:00 | European exchanges |
| Hong Kong | HKT | +8:00 | No DST |
| Australian Eastern | AEST/AEDT | +10:00/+11:00 | Sydney |

**Important**: All timestamps in API responses are typically in UTC unless otherwise specified.

## Summary Table: When to Fetch Data

| Data Type | Best Fetch Time | Update Frequency | Notes |
|-----------|----------------|------------------|-------|
| US Stocks (Major) | 16:20 EST | Daily | 15-min after close |
| US Stocks (ARCA ETFs) | 18:30 EST | Daily | 2-3 hours |
| US Mutual Funds | 06:00 AM EST (next day) | Daily | Quality checks |
| US OTC | 03:30 AM EST (next day) | Daily | Variable timing |
| International Stocks | 3 hours after close | Daily | Standard delay |
| INDX Exchange | 10-15 min after updates | 5x daily | Multiple updates |
| Intraday (5-min) | 3 hours after close | Real-time | Regular hours |
| Intraday (1-min) | 2-3 hrs after after-hours | Real-time | Includes pre/post-market |
| Options (Marketplace) | After midnight EST | Daily | 10 PM-midnight update |
| Forex | 2 hours after GMT updates | Every 4 hours | Integrity checks |
| Crypto | 2 hours after GMT updates | Every 4 hours | Integrity checks |
| Fundamentals (general) | 04:00-05:00 UTC | Daily | Nightly batch |
| Fundamentals (financials) | Next day (US) | Quarterly | Filing dependent |
| News (major stocks) | Every 15-30 min | Real-time | Market hours |
| Sentiment | Every 15-30 min | Real-time | With news updates |
| Calendar Events | 05:00 UTC | Daily | Next day for US |
| Economic Events | 2 hours after release | As published | FED: 1.5hr delay |

---

**Last Updated**: February 2026
**Source**: Official EODHD documentation and support responses
**Maintained By**: EODHD Skills Team
