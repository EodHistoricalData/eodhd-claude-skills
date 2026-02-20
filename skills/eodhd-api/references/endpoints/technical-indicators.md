# Technical Indicators API - Complete Reference

**Status**: Complete
**Source**: EODHD Technical Analysis Indicators API
**Docs**: https://eodhd.com/financial-apis/technical-indicators-api
**Provider**: EODHD
**Base URL**: https://eodhd.com/api
**Path**: /technical/{SYMBOL}
**Method**: GET
**Auth**: api_token (query parameter)

---

## Overview

The Technical Indicators API provides detailed technical analysis data for equities, offering pre-calculated technical indicators for stocks, cryptocurrencies, and forex markets. This API eliminates the need to compute indicators locally from raw price data.

**Key Features**:
- **21+ technical indicators** including moving averages, oscillators, trend indicators
- **Pre-calculated values** ready to use in trading strategies
- **Flexible date ranges** with custom periods
- **Multiple output formats** (JSON, CSV, AmiBroker)
- **Filter capabilities** to get only the latest value
- **Split-adjusted data** option for accurate historical analysis

---

## Plan Availability

**Available Plans**:
- All-In-One Plan
- EOD+Intraday — All World Extended plans

**API Consumption**: Each request consumes **5 API calls** (not 1).

---

## Integration Options

Technical indicators are integrated with:
- **Google Sheets add-on** - Use indicators directly in spreadsheets
- **Excel add-on** - Import indicators into Excel
- **Python library** - EODHD Python SDK
- **ChatGPT assistant** - Natural language queries

---

## Quick Start

### Base URL Format

```
https://eodhd.com/api/technical/{SYMBOL}?function={FUNCTION}&api_token={API_TOKEN}&fmt=json
```

### Simple Example

```bash
# 50-period SMA for Apple Inc (AAPL)
curl "https://eodhd.com/api/technical/AAPL.US?function=sma&period=50&api_token=demo&fmt=json"
```

### Example with Date Range

```bash
# SMA from August 2017 to January 2020
curl "https://eodhd.com/api/technical/AAPL.US?order=d&from=2017-08-01&to=2020-01-01&function=sma&period=50&api_token=demo&fmt=json"
```

---

## API Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `{SYMBOL}` | string | Symbol with exchange suffix (e.g., `AAPL.US`, `BTC-USD.CC`, `EURUSD.FOREX`) |
| `api_token` | string | Your EODHD API key (get one by signing up) |
| `function` | string | Indicator function name (see [Supported Functions](#supported-functions)) |

**Symbol Format**: `{TICKER}.{EXCHANGE}`
- `AAPL.US` - Apple Inc on NASDAQ
- `AAPL.MX` - Apple Inc on Mexican Stock Exchange
- `BTC-USD.CC` - Bitcoin to USD cryptocurrency
- `EURUSD.FOREX` - EUR/USD forex pair

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `period` | integer | 50 (varies) | Number of data points for calculation. Valid range: 2-100000 |
| `from` | date | - | Start date in YYYY-MM-DD format (e.g., `2017-01-05`) |
| `to` | date | - | End date in YYYY-MM-DD format (e.g., `2020-01-01`) |
| `order` | string | `a` | Sort order: `a` (ascending, old to new) or `d` (descending, new to old) |
| `fmt` | string | `json` | Output format: `json` or `csv` |
| `splitadjusted_only` | integer | `0` | `0` = adjust for splits & dividends, `1` = adjust for splits only |
| `filter` | string | - | Filter to get only specific values (e.g., `last_ema`, `last_volume`) |

### Special Function Parameters

Some functions have additional parameters:

| Function | Additional Parameters |
|----------|----------------------|
| `stochastic` | `fast_kperiod`, `slow_kperiod`, `slow_dperiod` |
| `stochrsi` | `fast_kperiod`, `fast_dperiod` |
| `macd` | `fast_period`, `slow_period`, `signal_period` |
| `sar` | `acceleration`, `maximum` |
| `beta` | `code2` (comparison ticker) |
| `splitadjusted` | `agg_period` (aggregation: d/w/m) |

---

## Filter Fields

The API supports filtering to retrieve only the **last calculated value** instead of the entire time series.

### Usage

Add `filter=last_{function_name}` with `fmt=json`:

```bash
# Get only the last EMA value
curl "https://eodhd.com/api/technical/AAPL.US?function=ema&filter=last_ema&api_token=demo&fmt=json"
```

**Output**: Single numeric value
```json
185.42
```

### Available Filters

You can use `filter=last_{field}` for any output field:
- `filter=last_sma` - Last SMA value
- `filter=last_ema` - Last EMA value
- `filter=last_rsi` - Last RSI value
- `filter=last_volume` - Last average volume
- `filter=last_macd` - Last MACD value
- etc.

**Use Case**: Perfect for real-time dashboards or alerts where you only need the current indicator value.

---

## Supported Functions

### Complete Function List

| Function | Description | Default Period | Multi-Value |
|----------|-------------|----------------|-------------|
| `splitadjusted` | Split-adjusted OHLC data | N/A | Yes |
| `avgvol` | Average Trading Volume | 50 | No |
| `avgvolccy` | Average Volume by Price | 50 | No |
| `sma` | Simple Moving Average | 50 | No |
| `ema` | Exponential Moving Average | 50 | No |
| `wma` | Weighted Moving Average | 50 | No |
| `volatility` | Historical Volatility | 50 | No |
| `stochastic` | Stochastic Oscillator | 14 | Yes (K, D) |
| `rsi` | Relative Strength Index | 50 | No |
| `stddev` | Standard Deviation | 50 | No |
| `stochrsi` | Stochastic RSI | 14 | Yes (K, D) |
| `slope` | Linear Regression Slope | 50 | No |
| `dmi` | Directional Movement Index | 50 | Yes |
| `adx` | Average Directional Index | 50 | No |
| `macd` | MACD | 12/26/9 | Yes (MACD, Signal, Hist) |
| `atr` | Average True Range | 50 | No |
| `cci` | Commodity Channel Index | 50 | No |
| `sar` | Parabolic SAR | 0.02/0.2 | No |
| `beta` | Beta (vs benchmark) | 50 | No |
| `bbands` | Bollinger Bands | 50 | Yes (Upper, Middle, Lower) |
| `format_amibroker` | AmiBroker format | N/A | Yes |

---

## Technical Indicator Functions

### 1. Split Adjusted Data

Returns OHLC data adjusted only for stock splits (not dividends).

**Function**: `splitadjusted`

**Parameters**:
- `agg_period` (optional) - Aggregation period:
  - `d` - daily (default)
  - `w` - weekly
  - `m` - monthly

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=splitadjusted&from=2023-01-01&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2023-01-03",
    "open": 130.28,
    "high": 130.90,
    "low": 124.17,
    "close": 125.07,
    "volume": 112117471
  },
  {
    "date": "2023-01-04",
    "open": 126.89,
    "high": 128.66,
    "low": 125.08,
    "close": 126.36,
    "volume": 89113619
  }
]
```

**Use Case**: When you need price history adjusted for splits but want to preserve dividend-related price drops.

**Note**: By default, EODHD provides raw OHLC (no adjustments) and `adjusted_close` (both splits & dividends). Use this function for split-only adjusted data.

---

### 2. Average Volume (avgvol)

Returns the average trading volume over a specified period.

**Function**: `avgvol`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.

**Formula**:
```
Average Volume = Sum(Volume for N periods) / N
```

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=avgvol&period=20&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "avgvol": 58234567.5
  },
  {
    "date": "2024-01-16",
    "avgvol": 59123456.8
  }
]
```

**Use Case**: Identify liquidity and unusual volume spikes.

---

### 3. Average Volume by Price (avgvolccy)

Returns average trading volume multiplied by price (volume in currency units).

**Function**: `avgvolccy`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.

**Formula**:
```
Average Volume by Price = Sum(Volume × Price for N periods) / N
```

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=avgvolccy&period=20&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "avgvolccy": 10567234567.89
  }
]
```

**Use Case**: Measure actual dollar volume traded (useful for institutional traders).

---

### 4. Simple Moving Average (SMA)

Returns the Simple Moving Average - arithmetic mean of prices over N periods.

**Function**: `sma`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
- `splitadjusted_only` (optional) - Set to `1` for split-only adjustment.

**Formula**:
```
SMA = (P1 + P2 + ... + Pn) / n
```

**Example Request**:
```bash
# 50-day SMA
curl "https://eodhd.com/api/technical/AAPL.US?function=sma&period=50&api_token=demo&fmt=json"

# 200-day SMA with split-adjusted data only
curl "https://eodhd.com/api/technical/AAPL.US?function=sma&period=200&splitadjusted_only=1&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "sma": 185.42
  },
  {
    "date": "2024-01-16",
    "sma": 185.67
  }
]
```

**Common Periods**:
- 20-day - Short-term trend
- 50-day - Intermediate trend
- 200-day - Long-term trend

**Use Case**: Identify trend direction, support/resistance levels.

**Wikipedia**: [Simple Moving Average](https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average)

---

### 5. Exponential Moving Average (EMA)

Returns the Exponential Moving Average - gives more weight to recent prices.

**Function**: `ema`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
- `splitadjusted_only` (optional) - Set to `1` for split-only adjustment.

**Formula**:
```
EMA = Price(t) × k + EMA(y) × (1 - k)
where k = 2 / (N + 1)
```

**Example Request**:
```bash
# 12-day EMA
curl "https://eodhd.com/api/technical/AAPL.US?function=ema&period=12&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "ema": 186.23
  },
  {
    "date": "2024-01-16",
    "ema": 186.45
  }
]
```

**Common Periods**:
- 12-day & 26-day - MACD components
- 9-day - MACD signal line
- 50-day & 200-day - Long-term trend

**Use Case**: More responsive to recent price changes than SMA.

**Wikipedia**: [Exponential Moving Average](https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average)

---

### 6. Weighted Moving Average (WMA)

Returns the Weighted Moving Average - linear weighting with most recent data weighted highest.

**Function**: `wma`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
- `splitadjusted_only` (optional) - Set to `1` for split-only adjustment.

**Formula**:
```
WMA = (P1 × n + P2 × (n-1) + ... + Pn × 1) / (n × (n+1) / 2)
```

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=wma&period=20&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "wma": 185.89
  }
]
```

**Use Case**: Middle ground between SMA (equal weights) and EMA (exponential decay).

**Wikipedia**: [Weighted Moving Average](https://en.wikipedia.org/wiki/Moving_average#Weighted_moving_average)

---

### 7. Volatility

Returns historical volatility - statistical measure of price dispersion.

**Function**: `volatility`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
- `splitadjusted_only` (optional) - Set to `1` for split-only adjustment.

**Formula**:
```
Volatility = Standard Deviation of log returns × √(trading days per year)
```

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=volatility&period=30&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "volatility": 28.45
  },
  {
    "date": "2024-01-16",
    "volatility": 29.12
  }
]
```

**Interpretation**:
- **< 20%**: Low volatility
- **20-40%**: Moderate volatility
- **> 40%**: High volatility

**Use Case**: Risk assessment, options pricing, position sizing.

**Investopedia**: [Volatility](https://www.investopedia.com/terms/v/volatility.asp)

---

### 8. Stochastic Oscillator

Returns Stochastic Oscillator values (K and D lines) - momentum indicator comparing closing price to price range.

**Function**: `stochastic`

**Parameters**:
- `fast_kperiod` (optional) - Fast K period. Default: 14. Range: 2-100000.
- `slow_kperiod` (optional) - Slow K period. Default: 3. Range: 2-100000.
- `slow_dperiod` (optional) - Slow D period. Default: 3. Range: 2-100000.

**Formula**:
```
%K = 100 × (Current Close - Lowest Low) / (Highest High - Lowest Low)
%D = 3-period SMA of %K
```

**Example Request**:
```bash
# Default 14,3,3
curl "https://eodhd.com/api/technical/AAPL.US?function=stochastic&api_token=demo&fmt=json"

# Custom parameters
curl "https://eodhd.com/api/technical/AAPL.US?function=stochastic&fast_kperiod=14&slow_kperiod=3&slow_dperiod=3&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "stochastic_k": 82.34,
    "stochastic_d": 78.56
  },
  {
    "date": "2024-01-16",
    "stochastic_k": 85.67,
    "stochastic_d": 81.23
  }
]
```

**Interpretation**:
- **> 80**: Overbought (potential sell signal)
- **< 20**: Oversold (potential buy signal)
- **K crosses above D**: Bullish signal
- **K crosses below D**: Bearish signal

**Use Case**: Identify overbought/oversold conditions, momentum changes.

**Wikipedia**: [Stochastic Oscillator](https://en.wikipedia.org/wiki/Stochastic_oscillator)

---

### 9. Relative Strength Index (RSI)

Returns the RSI - momentum oscillator measuring speed and magnitude of price changes.

**Function**: `rsi`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
  - **Note**: Standard RSI uses 14 periods, but API defaults to 50. Use `period=14` for traditional RSI.
- `splitadjusted_only` (optional) - Set to `1` for split-only adjustment.

**Formula**:
```
RSI = 100 - [100 / (1 + RS)]
where RS = Average Gain / Average Loss
```

**Example Request**:
```bash
# Standard 14-period RSI
curl "https://eodhd.com/api/technical/AAPL.US?function=rsi&period=14&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "rsi": 67.34
  },
  {
    "date": "2024-01-16",
    "rsi": 69.12
  }
]
```

**Interpretation**:
- **> 70**: Overbought (potential reversal down)
- **< 30**: Oversold (potential reversal up)
- **50**: Neutral

**Use Case**: Identify overbought/oversold conditions, divergences with price.

**Wikipedia**: [RSI](https://en.wikipedia.org/wiki/Relative_strength_index)

---

### 10. Standard Deviation (stddev)

Returns the standard deviation of prices - measure of volatility.

**Function**: `stddev`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.

**Formula**:
```
StdDev = √[Σ(Xi - μ)² / N]
```

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=stddev&period=20&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "stddev": 3.45
  },
  {
    "date": "2024-01-16",
    "stddev": 3.52
  }
]
```

**Use Case**: Component of Bollinger Bands, risk measurement.

**Wikipedia**: [Standard Deviation](https://en.wikipedia.org/wiki/Standard_deviation)

---

### 11. Stochastic RSI

Returns Stochastic RSI values (K and D lines) - applies stochastic oscillator to RSI values.

**Function**: `stochrsi`

**Parameters**:
- `fast_kperiod` (optional) - Fast K period. Default: 14. Range: 2-100000.
- `fast_dperiod` (optional) - Fast D period. Default: 14. Range: 2-100000.

**Formula**:
```
Stochastic RSI = (RSI - Lowest RSI) / (Highest RSI - Lowest RSI)
%K = 100 × Stochastic RSI
%D = 3-period SMA of %K
```

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=stochrsi&fast_kperiod=14&fast_dperiod=14&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "stochrsi_k": 78.45,
    "stochrsi_d": 72.34
  },
  {
    "date": "2024-01-16",
    "stochrsi_k": 82.67,
    "stochrsi_d": 76.89
  }
]
```

**Interpretation**:
- **> 80**: Overbought
- **< 20**: Oversold
- More sensitive than regular Stochastic or RSI alone

**Use Case**: Identify short-term overbought/oversold conditions.

**Investopedia**: [Stochastic RSI](https://www.investopedia.com/terms/s/stochrsi.asp)

---

### 12. Slope (Linear Regression)

Returns the slope of linear regression line - rate of price change.

**Function**: `slope`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
- `splitadjusted_only` (optional) - Set to `1` for split-only adjustment.

**Formula**:
```
Slope = Σ[(Xi - X̄)(Yi - Ȳ)] / Σ[(Xi - X̄)²]
```

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=slope&period=20&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "slope": 0.45
  },
  {
    "date": "2024-01-16",
    "slope": 0.52
  }
]
```

**Interpretation**:
- **Positive slope**: Uptrend
- **Negative slope**: Downtrend
- **Magnitude**: Strength of trend

**Use Case**: Quantify trend strength and direction.

**Wikipedia**: [Linear Regression](https://en.wikipedia.org/wiki/Linear_regression)

---

### 13. Directional Movement Index (DMI / DX)

Returns the Directional Movement Index - identifies trend direction and strength.

**Function**: `dmi` (or `dx`)

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.

**Components**:
- **+DI**: Positive Directional Indicator
- **-DI**: Negative Directional Indicator
- **DX**: Directional Movement Index

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=dmi&period=14&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "dmi_plus": 28.45,
    "dmi_minus": 15.67,
    "dx": 35.23
  }
]
```

**Interpretation**:
- **+DI > -DI**: Uptrend
- **-DI > +DI**: Downtrend
- **DX > 25**: Strong trend

**Use Case**: Trend identification, filter for trend-following strategies.

**Investopedia**: [DMI](https://www.investopedia.com/terms/d/dmi.asp)

---

### 14. Average Directional Movement Index (ADX)

Returns the ADX - measures trend strength (not direction).

**Function**: `adx`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.

**Formula**:
```
ADX = 100 × EMA of DX
```

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=adx&period=14&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "adx": 32.45
  },
  {
    "date": "2024-01-16",
    "adx": 33.67
  }
]
```

**Interpretation**:
- **< 20**: Weak trend (range-bound)
- **20-25**: Emerging trend
- **25-50**: Strong trend
- **> 50**: Very strong trend

**Use Case**: Filter trades to only take positions in trending markets.

**Investopedia**: [ADX](https://www.investopedia.com/terms/a/adx.asp)

---

### 15. Moving Average Convergence/Divergence (MACD)

Returns MACD values - trend-following momentum indicator.

**Function**: `macd`

**Parameters**:
- `fast_period` (optional) - Fast EMA period. Default: 12. Range: 2-100000.
- `slow_period` (optional) - Slow EMA period. Default: 26. Range: 2-100000.
- `signal_period` (optional) - Signal line period. Default: 9. Range: 2-100000.
- `splitadjusted_only` (optional) - Set to `1` for split-only adjustment.

**Formula**:
```
MACD Line = EMA(12) - EMA(26)
Signal Line = EMA(9) of MACD Line
Histogram = MACD Line - Signal Line
```

**Example Request**:
```bash
# Default 12,26,9
curl "https://eodhd.com/api/technical/AAPL.US?function=macd&api_token=demo&fmt=json"

# Custom parameters
curl "https://eodhd.com/api/technical/AAPL.US?function=macd&fast_period=12&slow_period=26&signal_period=9&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "macd": 2.35,
    "macd_signal": 1.89,
    "macd_hist": 0.46
  },
  {
    "date": "2024-01-16",
    "macd": 2.67,
    "macd_signal": 2.12,
    "macd_hist": 0.55
  }
]
```

**Interpretation**:
- **MACD > Signal**: Bullish
- **MACD < Signal**: Bearish
- **MACD crosses above Signal**: Buy signal
- **MACD crosses below Signal**: Sell signal
- **Histogram expanding**: Trend strengthening
- **Histogram contracting**: Trend weakening

**Use Case**: Identify trend changes, momentum shifts.

**Wikipedia**: [MACD](https://en.wikipedia.org/wiki/MACD)

---

### 16. Average True Range (ATR)

Returns the ATR - measures market volatility.

**Function**: `atr`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
  - **Note**: Standard ATR uses 14 periods.

**Formula**:
```
True Range = max[(High - Low), |High - Previous Close|, |Low - Previous Close|]
ATR = Average of True Range over N periods
```

**Example Request**:
```bash
# Standard 14-period ATR
curl "https://eodhd.com/api/technical/AAPL.US?function=atr&period=14&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "atr": 3.45
  },
  {
    "date": "2024-01-16",
    "atr": 3.52
  }
]
```

**Interpretation**:
- **Higher ATR**: More volatile (wider stop losses needed)
- **Lower ATR**: Less volatile (tighter stop losses possible)

**Use Case**: Position sizing, stop loss placement, volatility filtering.

**Investopedia**: [ATR](https://www.investopedia.com/terms/a/atr.asp)

---

### 17. Commodity Channel Index (CCI)

Returns the CCI - momentum oscillator identifying overbought/oversold conditions.

**Function**: `cci`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
  - **Note**: Standard CCI uses 20 periods.

**Formula**:
```
CCI = (Typical Price - SMA of Typical Price) / (0.015 × Mean Deviation)
where Typical Price = (High + Low + Close) / 3
```

**Example Request**:
```bash
# Standard 20-period CCI
curl "https://eodhd.com/api/technical/AAPL.US?function=cci&period=20&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "cci": 142.34
  },
  {
    "date": "2024-01-16",
    "cci": 156.78
  }
]
```

**Interpretation**:
- **> +100**: Overbought
- **< -100**: Oversold
- **Crossing above -100**: Buy signal
- **Crossing below +100**: Sell signal

**Use Case**: Identify cyclical trends, overbought/oversold extremes.

**Investopedia**: [CCI](https://www.investopedia.com/terms/c/commoditychannelindex.asp)

---

### 18. Parabolic SAR

Returns Parabolic SAR values - trailing stop and reverse indicator.

**Function**: `sar`

**Parameters**:
- `acceleration` (optional) - Acceleration Factor. Default: 0.02.
- `maximum` (optional) - Maximum Acceleration Factor. Default: 0.20.

**Formula**:
```
SAR(tomorrow) = SAR(today) + AF × [EP - SAR(today)]
where:
  EP = Extreme Point (highest high or lowest low)
  AF = Acceleration Factor (starts at 0.02, increases by 0.02, max 0.20)
```

**Example Request**:
```bash
# Default 0.02, 0.20
curl "https://eodhd.com/api/technical/AAPL.US?function=sar&api_token=demo&fmt=json"

# Custom parameters
curl "https://eodhd.com/api/technical/AAPL.US?function=sar&acceleration=0.02&maximum=0.20&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "sar": 182.45
  },
  {
    "date": "2024-01-16",
    "sar": 183.12
  }
]
```

**Interpretation**:
- **Price > SAR**: Uptrend (SAR below price acts as support)
- **Price < SAR**: Downtrend (SAR above price acts as resistance)
- **Price crosses SAR**: Trend reversal signal

**Use Case**: Trailing stop loss, trend reversal identification.

**Wikipedia**: [Parabolic SAR](https://en.wikipedia.org/wiki/Parabolic_SAR)

---

### 19. BETA

Returns Beta values - measures volatility relative to a benchmark (default: S&P 500).

**Function**: `beta`

**Parameters**:
- `code2` (optional) - Benchmark ticker. Default: `GSPC.INDX` (S&P 500).
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.

**Formula**:
```
Beta = Covariance(Stock Returns, Market Returns) / Variance(Market Returns)
```

**Example Request**:
```bash
# Beta vs S&P 500 (default)
curl "https://eodhd.com/api/technical/AAPL.US?function=beta&api_token=demo&fmt=json"

# Beta vs NASDAQ Composite
curl "https://eodhd.com/api/technical/AAPL.US?function=beta&code2=IXIC.INDX&period=60&api_token=demo&fmt=json"

# Beta vs another stock
curl "https://eodhd.com/api/technical/TSLA.US?function=beta&code2=AAPL.US&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "beta": 1.23
  },
  {
    "date": "2024-01-16",
    "beta": 1.25
  }
]
```

**Interpretation**:
- **Beta = 1.0**: Moves with the market
- **Beta > 1.0**: More volatile than market (e.g., 1.5 = 50% more volatile)
- **Beta < 1.0**: Less volatile than market (e.g., 0.5 = 50% less volatile)
- **Beta < 0**: Moves opposite to market (rare)

**Use Case**: Portfolio risk assessment, diversification, CAPM calculations.

**Wikipedia**: [Beta (Finance)](https://en.wikipedia.org/wiki/Beta_(finance))

---

### 20. Bollinger Bands

Returns Bollinger Bands - volatility bands placed above and below a moving average.

**Function**: `bbands`

**Parameters**:
- `period` (optional) - Number of data points. Default: 50. Range: 2-100000.
  - **Note**: Standard Bollinger Bands use 20 periods.

**Formula**:
```
Middle Band = SMA(20)
Upper Band = SMA(20) + (2 × Standard Deviation)
Lower Band = SMA(20) - (2 × Standard Deviation)
```

**Example Request**:
```bash
# Standard 20-period Bollinger Bands
curl "https://eodhd.com/api/technical/AAPL.US?function=bbands&period=20&api_token=demo&fmt=json"
```

**Example Response**:
```json
[
  {
    "date": "2024-01-15",
    "bbands_upper": 195.50,
    "bbands_middle": 185.42,
    "bbands_lower": 175.34
  },
  {
    "date": "2024-01-16",
    "bbands_upper": 196.23,
    "bbands_middle": 185.89,
    "bbands_lower": 175.55
  }
]
```

**Interpretation**:
- **Price near Upper Band**: Overbought
- **Price near Lower Band**: Oversold
- **Bands contracting**: Low volatility (potential breakout coming)
- **Bands expanding**: High volatility (trending move)
- **Price breaks above/below bands**: Strong momentum

**Use Case**: Identify overbought/oversold conditions, volatility, mean reversion opportunities.

**Wikipedia**: [Bollinger Bands](https://en.wikipedia.org/wiki/Bollinger_Bands)

---

## Special Formats

### AmiBroker File Format

Returns data in AmiBroker format for importing into AmiBroker software.

**Function**: `format_amibroker`

**Parameters**:
- Standard date range parameters (`from`, `to`)

**Example Request**:
```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=format_amibroker&from=2023-01-01&to=2023-12-31&api_token=demo"
```

**Example Response**:
```
$FORMAT Ticker, Date_YMD, Open, High, Low, Close, Volume
AAPL,2023-01-03,130.28,130.90,124.17,125.07,112117471
AAPL,2023-01-04,126.89,128.66,125.08,126.36,89113619
AAPL,2023-01-05,127.13,127.77,124.76,125.02,80962690
```

**Note**:
- OHLC fields are **split-adjusted only** (not adjusted for dividends)
- Format designed for direct import into AmiBroker
- Use this for technical analysis software integration

**Use Case**: Import EODHD data into AmiBroker for technical analysis and backtesting.

---

## Response Format Examples

### Single-Value Indicator (SMA, EMA, RSI)

```json
[
  {
    "date": "2024-01-15",
    "sma": 185.42
  },
  {
    "date": "2024-01-16",
    "sma": 185.67
  }
]
```

### Multi-Value Indicator (MACD)

```json
[
  {
    "date": "2024-01-15",
    "macd": 2.35,
    "macd_signal": 1.89,
    "macd_hist": 0.46
  }
]
```

### Multi-Value Indicator (Bollinger Bands)

```json
[
  {
    "date": "2024-01-15",
    "bbands_upper": 195.50,
    "bbands_middle": 185.42,
    "bbands_lower": 175.34
  }
]
```

### Multi-Value Indicator (Stochastic)

```json
[
  {
    "date": "2024-01-15",
    "stochastic_k": 82.34,
    "stochastic_d": 78.56
  }
]
```

### Filtered Response (Last Value Only)

```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=rsi&period=14&filter=last_rsi&api_token=demo&fmt=json"
```

Response:
```json
67.34
```

### CSV Format

```bash
curl "https://eodhd.com/api/technical/AAPL.US?function=sma&period=50&fmt=csv&api_token=demo"
```

Response:
```csv
date,sma
2024-01-15,185.42
2024-01-16,185.67
2024-01-17,185.89
```

---

## Important Notes

### Data Adjustment

1. **Default Behavior**: Most functions calculate using close prices adjusted for **both splits and dividends**
2. **Split-Only Adjustment**: Set `splitadjusted_only=1` for the following functions:
   - `sma`, `ema`, `wma`, `volatility`, `rsi`, `slope`, `macd`
3. **Raw OHLC**: Use the main EOD API for unadjusted data
4. **adjusted_close**: Available in EOD API for dividend+split adjusted closes

### Calculation Requirements

- **Minimum Data**: Each indicator requires at least `period` data points before returning values
- **Initial NaN Values**: First N values (where N = period) may be NaN or missing
- **Sufficient History**: Ensure ticker has enough historical data for your requested period

### Period Defaults

**API Default vs Standard Practice**:
| Function | API Default | Standard Default | Recommended |
|----------|-------------|------------------|-------------|
| `rsi` | 50 | 14 | Use `period=14` |
| `atr` | 50 | 14 | Use `period=14` |
| `cci` | 50 | 20 | Use `period=20` |
| `bbands` | 50 | 20 | Use `period=20` |
| `adx` | 50 | 14 | Use `period=14` |
| `stochastic` | N/A | 14,3,3 | Use defaults |

**Always specify `period` explicitly** to match standard technical analysis practices.

### Performance Considerations

- **API Consumption**: Each request = 5 API calls
- **Response Size**: Longer date ranges = larger responses
- **Use Filters**: `filter=last_*` reduces bandwidth when you only need current value
- **Date Ranges**: Limit to needed timeframe with `from` and `to`

### Common Pitfalls

1. **Wrong Period**: Using API defaults instead of standard periods (e.g., RSI should be 14, not 50)
2. **Insufficient Data**: Requesting 200-period SMA on a ticker with only 100 days of history
3. **Missing Adjustment**: Not setting `splitadjusted_only=1` when analyzing around split dates
4. **Ignoring NaN**: Not handling initial NaN/missing values in first N data points

---

## Integration Examples

### Python Example - Complete Technical Analysis

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt

class TechnicalAnalysis:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://eodhd.com/api/technical"

    def get_indicator(self, ticker, function, **params):
        """Fetch technical indicator data."""
        url = f"{self.base_url}/{ticker}"
        params['api_token'] = self.api_token
        params['function'] = function
        params['fmt'] = 'json'

        response = requests.get(url, params=params)
        return response.json()

    def multi_indicator_analysis(self, ticker, from_date, to_date):
        """Get multiple indicators for comprehensive analysis."""

        # Fetch multiple indicators
        sma_50 = self.get_indicator(ticker, 'sma', period=50, **{'from': from_date, 'to': to_date})
        sma_200 = self.get_indicator(ticker, 'sma', period=200, **{'from': from_date, 'to': to_date})
        rsi = self.get_indicator(ticker, 'rsi', period=14, **{'from': from_date, 'to': to_date})
        macd = self.get_indicator(ticker, 'macd', **{'from': from_date, 'to': to_date})
        bbands = self.get_indicator(ticker, 'bbands', period=20, **{'from': from_date, 'to': to_date})

        return {
            'sma_50': pd.DataFrame(sma_50),
            'sma_200': pd.DataFrame(sma_200),
            'rsi': pd.DataFrame(rsi),
            'macd': pd.DataFrame(macd),
            'bbands': pd.DataFrame(bbands)
        }

    def get_current_signals(self, ticker):
        """Get current (last) values for all indicators."""
        indicators = {
            'SMA_50': self.get_indicator(ticker, 'sma', period=50, filter='last_sma'),
            'SMA_200': self.get_indicator(ticker, 'sma', period=200, filter='last_sma'),
            'RSI_14': self.get_indicator(ticker, 'rsi', period=14, filter='last_rsi'),
            'MACD': self.get_indicator(ticker, 'macd', filter='last_macd'),
        }

        # Generate signals
        signals = {
            'trend': 'Bullish' if indicators['SMA_50'] > indicators['SMA_200'] else 'Bearish',
            'rsi_signal': 'Overbought' if indicators['RSI_14'] > 70 else 'Oversold' if indicators['RSI_14'] < 30 else 'Neutral',
            'macd_signal': 'Bullish' if indicators['MACD'] > 0 else 'Bearish'
        }

        return indicators, signals

# Usage
analyzer = TechnicalAnalysis(api_token="your_api_token")

# Get comprehensive analysis
data = analyzer.multi_indicator_analysis('AAPL.US', '2023-01-01', '2024-01-01')

# Get current signals
current, signals = analyzer.get_current_signals('AAPL.US')
print(f"Current Trend: {signals['trend']}")
print(f"RSI Signal: {signals['rsi_signal']}")
print(f"MACD Signal: {signals['macd_signal']}")
```

### Python Example - Trading Strategy Backtest

```python
def simple_sma_crossover_strategy(ticker, api_token, from_date, to_date):
    """
    Simple SMA crossover strategy:
    - Buy when SMA(50) crosses above SMA(200) (Golden Cross)
    - Sell when SMA(50) crosses below SMA(200) (Death Cross)
    """
    base_url = "https://eodhd.com/api/technical"

    # Fetch SMA data
    sma_50 = requests.get(f"{base_url}/{ticker}", params={
        'api_token': api_token,
        'function': 'sma',
        'period': 50,
        'from': from_date,
        'to': to_date,
        'fmt': 'json'
    }).json()

    sma_200 = requests.get(f"{base_url}/{ticker}", params={
        'api_token': api_token,
        'function': 'sma',
        'period': 200,
        'from': from_date,
        'to': to_date,
        'fmt': 'json'
    }).json()

    # Convert to DataFrames
    df_50 = pd.DataFrame(sma_50).set_index('date')
    df_200 = pd.DataFrame(sma_200).set_index('date')

    # Merge and find crossovers
    df = pd.merge(df_50, df_200, left_index=True, right_index=True, suffixes=('_50', '_200'))
    df['signal'] = 0
    df.loc[df['sma_50'] > df['sma_200'], 'signal'] = 1  # Bullish
    df.loc[df['sma_50'] < df['sma_200'], 'signal'] = -1  # Bearish
    df['crossover'] = df['signal'].diff()

    # Find buy/sell signals
    buy_signals = df[df['crossover'] == 2].index.tolist()  # Bullish crossover
    sell_signals = df[df['crossover'] == -2].index.tolist()  # Bearish crossover

    return {
        'buy_dates': buy_signals,
        'sell_dates': sell_signals,
        'data': df
    }
```

### curl Examples

```bash
# Complete technical analysis for AAPL
# 1. Get current RSI
curl "https://eodhd.com/api/technical/AAPL.US?function=rsi&period=14&filter=last_rsi&api_token=YOUR_TOKEN&fmt=json"

# 2. Get MACD for last 6 months
curl "https://eodhd.com/api/technical/AAPL.US?function=macd&from=2023-07-01&to=2024-01-01&api_token=YOUR_TOKEN&fmt=json"

# 3. Get Bollinger Bands
curl "https://eodhd.com/api/technical/AAPL.US?function=bbands&period=20&api_token=YOUR_TOKEN&fmt=json"

# 4. Get 50-day and 200-day SMA for Golden Cross analysis
curl "https://eodhd.com/api/technical/AAPL.US?function=sma&period=50&filter=last_sma&api_token=YOUR_TOKEN&fmt=json"
curl "https://eodhd.com/api/technical/AAPL.US?function=sma&period=200&filter=last_sma&api_token=YOUR_TOKEN&fmt=json"

# 5. Get Beta vs S&P 500
curl "https://eodhd.com/api/technical/AAPL.US?function=beta&period=60&api_token=YOUR_TOKEN&fmt=json"

# 6. Get volatility for risk assessment
curl "https://eodhd.com/api/technical/AAPL.US?function=volatility&period=30&api_token=YOUR_TOKEN&fmt=json"

# 7. CSV output for spreadsheet import
curl "https://eodhd.com/api/technical/AAPL.US?function=sma&period=50&fmt=csv&api_token=YOUR_TOKEN" > aapl_sma50.csv
```

---

## Common Use Cases

### 1. Trend Identification
```python
# Golden Cross / Death Cross detection
sma_50 = get_indicator('AAPL.US', 'sma', period=50, filter='last_sma')
sma_200 = get_indicator('AAPL.US', 'sma', period=200, filter='last_sma')

if sma_50 > sma_200:
    print("Bullish Trend (Golden Cross)")
else:
    print("Bearish Trend (Death Cross)")
```

### 2. Overbought/Oversold Detection
```python
# RSI-based signals
rsi = get_indicator('AAPL.US', 'rsi', period=14, filter='last_rsi')

if rsi > 70:
    print("Overbought - Consider selling")
elif rsi < 30:
    print("Oversold - Consider buying")
else:
    print("Neutral")
```

### 3. Momentum Trading
```python
# MACD crossover
macd_data = get_indicator('AAPL.US', 'macd')
latest = macd_data[-1]

if latest['macd'] > latest['macd_signal']:
    print("Bullish Momentum")
elif latest['macd'] < latest['macd_signal']:
    print("Bearish Momentum")
```

### 4. Volatility-Based Position Sizing
```python
# ATR for stop loss placement
atr = get_indicator('AAPL.US', 'atr', period=14, filter='last_atr')
stop_loss_distance = 2 * atr  # 2 ATR stop loss

print(f"Suggested stop loss distance: ${stop_loss_distance:.2f}")
```

### 5. Mean Reversion Strategy
```python
# Bollinger Bands mean reversion
bbands = get_indicator('AAPL.US', 'bbands', period=20)
latest = bbands[-1]
current_price = 185.50  # From real-time API

if current_price <= latest['bbands_lower']:
    print("Price at lower band - potential buy")
elif current_price >= latest['bbands_upper']:
    print("Price at upper band - potential sell")
```

---

## Error Handling

### Common Errors

**1. Insufficient Data**
```
Error: Not enough data points for calculation
```
Solution: Reduce `period` or use ticker with longer history

**2. Invalid Ticker**
```
Error: Symbol not found
```
Solution: Check ticker format (must include exchange: `AAPL.US`, not just `AAPL`)

**3. Invalid Date Range**
```
Error: Invalid date format
```
Solution: Use YYYY-MM-DD format for `from` and `to` parameters

**4. Invalid Period**
```
Error: Period out of range
```
Solution: Period must be 2-100000

---

## Related APIs

Combine Technical Indicators API with other EODHD endpoints:

1. **End-of-Day Historical Data API** - Get raw OHLCV data
2. **Live Stock Prices API** - Real-time price to compare with indicators
3. **Fundamentals API** - Combine technical and fundamental analysis
4. **Calendar API** - Earnings dates to avoid trading around events

---

## Best Practices

1. **Use Standard Periods**: Override API defaults to match industry standards
   - RSI: 14 periods
   - ATR: 14 periods
   - Bollinger Bands: 20 periods
   - MACD: 12,26,9

2. **Filter for Performance**: Use `filter=last_*` when you only need current values

3. **Date Range Optimization**: Only request data you need to reduce API calls

4. **Handle NaN Values**: First N values may be missing due to insufficient lookback data

5. **Combine Indicators**: Use multiple indicators together for confirmation
   - Trend (SMA) + Momentum (RSI) + Volatility (BBands)
   - Don't rely on single indicator

6. **Adjust for Splits**: Use `splitadjusted_only=1` when analyzing around split dates

7. **Document Your Strategy**: Track which parameters and combinations work for your use case

---

## Support and Documentation

- **API Documentation**: https://eodhd.com/financial-apis/technical-indicators-api
- **Support**: Contact EODHD support for technical issues
- **Community**: Join EODHD community for trading strategy discussions

---

**Last Updated**: 2024-11-27
**API Version**: EODHD Technical Indicators API v1

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
