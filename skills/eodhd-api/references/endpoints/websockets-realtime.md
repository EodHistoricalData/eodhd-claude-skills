# WebSockets Real-Time Data API

Status: complete
Source: financial-apis
Provider: EODHD (sourced from Finage, proxied via EODHD ACDC service)
Base URL: `wss://ws.eodhistoricaldata.com`
Path: `/ws/{market}` where market is `us`, `us-quote`, `forex`, or `crypto`
Method: WebSocket (persistent connection)
Auth: `api_token` query parameter validated during handshake
API Calls Consumption: Does not consume API calls
Available In Plans: All-In-One, EOD+Intraday — All World Extended plans

---

## Table of Contents

1. [Overview](#overview)
2. [Connection Flow](#connection-flow)
3. [What is WebSocket Protocol](#what-is-websocket-protocol)
4. [Data Availability](#data-availability)
5. [Updates & Latency](#updates--latency)
6. [Endpoints](#endpoints)
7. [Subscribe / Unsubscribe](#subscribe--unsubscribe)
8. [Response Schemas](#response-schemas)
9. [Symbol Limits & Usage Notes](#symbol-limits--usage-notes)
10. [Python Implementation](#python-implementation)
11. [Testing Tools](#testing-tools)
12. [API Comparison Guide](#api-comparison-guide)
13. [Best Practices](#best-practices)
14. [Failover & Reliability](#failover--reliability)

---

## Overview

### What This API Provides

EODHD offers real-time finance data for US markets, 1100+ Forex pairs, and 1000+ Digital Currencies with **delay of less than 50ms** via WebSockets.

**Key Features**:
- Real-time streaming data (not polling)
- 50 tickers simultaneously (upgradeable via dashboard)
- US stocks: pre-market and post-market hours (4 AM - 8 PM EST)
- No API call consumption
- Persistent connection with push updates

### Plans & Access

**Production Access**: Available in All-In-One and EOD+Intraday plans

**Demo Access**: Available with API key `demo` for:
- US Stocks: AAPL, MSFT, TSLA
- Forex: EURUSD
- Crypto: ETH-USD, BTC-USD

**Global Markets**: Live (Delayed) data available with 15-minute delay for all exchanges worldwide

---

## Connection Flow

1. Client connects to EODHD WebSocket endpoint with `api_token`
2. EODHD validates the API token against the subscription
3. Client sends JSON subscribe commands for desired symbols
4. Server pushes price updates as they occur
5. Client receives a continuous stream of market data

---

## What is WebSocket Protocol

WebSockets is a communication protocol that provides **full-duplex communication** channels over a single TCP connection. It enables real-time communication between a client and a server, allowing them to exchange messages continuously without the overhead of repeatedly establishing new connections.

**Why WebSockets for Financial Data?**
- Minimal latency (~50ms transport delay)
- Continuous streaming (no polling overhead)
- Efficient bandwidth usage
- Real-time updates pushed from server

---

## Data Availability

### US Stocks

**Coverage**: Full list of US tickers (retrieve via exchange-symbol-list API with "US" exchange)

**Available Streams**:
- **Trade stream** (`/ws/us`): Last price, size, trade conditions, dark pool indicator
- **Quote stream** (`/ws/us-quote`): Bid/ask prices and sizes

**Exchanges Covered**:
- NASDAQ
- NYSE
- Other primary US exchanges

**Extended Hours**: Pre-market and post-market trading supported (4 AM - 8 PM EST)

### Forex

**Coverage**: 1100+ currency pairs (retrieve via exchange-symbol-list API with "FOREX" exchange)

**Data Fields**:
- Bid/ask prices
- Daily change (percentage and absolute)
- Ticker format: `EURUSD`, `AUDUSD` (no separator)

### Digital Currencies

**Coverage**: 1000+ cryptocurrency pairs (retrieve via exchange-symbol-list API with "CC" exchange)

**Data Fields**:
- Last price
- Trade quantity
- Daily change (percentage and absolute)
- Ticker format: `ETH-USD`, `BTC-USD` (dash-separated)

### Retrieving Available Tickers

```bash
# US Stocks
https://eodhd.com/api/exchange-symbol-list/US?api_token=YOUR_API_KEY&fmt=json

# Forex Pairs
https://eodhd.com/api/exchange-symbol-list/FOREX?api_token=YOUR_API_KEY&fmt=json

# Cryptocurrencies
https://eodhd.com/api/exchange-symbol-list/CC?api_token=YOUR_API_KEY&fmt=json
```

---

## Updates & Latency

### Performance Characteristics

| Metric | Specification |
|--------|--------------|
| **Streaming Method** | Real-time push over persistent WebSocket connection |
| **Transport Latency** | < 50 ms from gateway to client (excluding network distance) |
| **Update Frequency** | As trades/quotes occur in the market |
| **Connection Type** | Full-duplex, persistent |

### Latency Breakdown

| Segment | Typical Latency |
|---------|-----------------|
| Source → EODHD | ~1–5 ms |
| EODHD → Client | Depends on network |
| **Total end-to-end** | **< 50 ms from exchange** |

### Market Status

For US stocks, each message includes a `ms` (market status) field:
- `open` - Regular trading hours
- `closed` - Market closed
- `extended hours` - Pre-market or post-market trading

---

## Endpoints

### Connection Protocol

**Production**: Use `wss://` (WebSocket Secure)
**Local Testing**: `ws://` available (not secure)

### US Equities - Trades

**Endpoint**:
```
wss://ws.eodhistoricaldata.com/ws/us?api_token=YOUR_API_KEY
```

**Purpose**: Stream real-time trade data (last price, size, conditions)

**Example**:
```
wss://ws.eodhistoricaldata.com/ws/us?api_token=demo
```

### US Equities - Quotes

**Endpoint**:
```
wss://ws.eodhistoricaldata.com/ws/us-quote?api_token=YOUR_API_KEY
```

**Purpose**: Stream real-time bid/ask quotes with sizes

**Example**:
```
wss://ws.eodhistoricaldata.com/ws/us-quote?api_token=demo
```

### Forex

**Endpoint**:
```
wss://ws.eodhistoricaldata.com/ws/forex?api_token=YOUR_API_KEY
```

**Purpose**: Stream real-time forex bid/ask prices

**Example**:
```
wss://ws.eodhistoricaldata.com/ws/forex?api_token=demo
```

### Crypto

**Endpoint**:
```
wss://ws.eodhistoricaldata.com/ws/crypto?api_token=YOUR_API_KEY
```

**Purpose**: Stream real-time cryptocurrency prices

**Example**:
```
wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo
```

---

## Subscribe / Unsubscribe

### Command Format

After opening the WebSocket connection, send JSON commands to subscribe or unsubscribe from symbols.

### Subscribe to Single Symbol

```json
{"action": "subscribe", "symbols": "ETH-USD"}
```

### Subscribe to Multiple Symbols

Use comma-separated list (no spaces):

```json
{"action": "subscribe", "symbols": "AAPL,TSLA,MSFT"}
```

### Unsubscribe from Symbols

```json
{"action": "unsubscribe", "symbols": "ETH-USD,BTC-USD"}
```

### Complete Connection Example

```bash
# 1. Open connection
wss://ws.eodhistoricaldata.com/ws/us?api_token=demo

# 2. Send subscribe command
{"action": "subscribe", "symbols": "AMZN,TSLA"}

# 3. Receive streaming data...

# 4. Unsubscribe when done
{"action": "unsubscribe", "symbols": "AMZN"}
```

---

## Response Schemas

### US Trades (`/ws/us`)

```json
{
  "s": "AAPL",         // ticker symbol
  "p": 227.31,         // last trade price
  "v": 100,            // trade size (number of shares)
  "c": 12,             // trade condition code (numeric, see glossary)
  "dp": false,         // dark pool indicator (true/false)
  "ms": "open",        // market status: "open" | "closed" | "extended hours"
  "t": 1725198451165   // timestamp (epoch milliseconds)
}
```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `s` | string | Ticker symbol |
| `p` | float | Last trade price |
| `v` | integer | Trade size in shares |
| `c` | integer | Trade condition code (see EODHD glossary PDF) |
| `dp` | boolean | Dark pool indicator - true if off-exchange trade |
| `ms` | string | Market status: "open", "closed", or "extended hours" |
| `t` | integer | Timestamp in epoch milliseconds |

**Note**: Trade condition codes (`c` field) map to specific trade types. See the downloadable glossary in EODHD documentation.

### US Quotes (`/ws/us-quote`)

```json
{
  "s": "AAPL",          // ticker symbol
  "ap": 227.33,         // ask price
  "as": 200,            // ask size (shares)
  "bp": 227.30,         // bid price
  "bs": 100,            // bid size (shares)
  "t": 1725198451165    // timestamp (epoch milliseconds)
}
```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `s` | string | Ticker symbol |
| `ap` | float | Ask price (price to buy) |
| `as` | integer | Ask size in shares |
| `bp` | float | Bid price (price to sell) |
| `bs` | integer | Bid size in shares |
| `t` | integer | Timestamp in epoch milliseconds |

### Forex (`/ws/forex`)

```json
{
  "s": "EURUSD",        // currency pair symbol
  "a": 1.08675,         // ask price
  "b": 1.08665,         // bid price
  "dc": 0.21,           // daily change (percentage)
  "dd": 0.0023,         // daily difference (price units)
  "ppms": false,        // pre/post market status (always false for Forex)
  "t": 1725198451165    // timestamp (epoch milliseconds)
}
```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `s` | string | Currency pair symbol (e.g., EURUSD) |
| `a` | float | Ask price |
| `b` | float | Bid price |
| `dc` | float | Daily change in percentage |
| `dd` | float | Daily difference in price units |
| `ppms` | boolean | Pre/post market status (always false for Forex) |
| `t` | integer | Timestamp in epoch milliseconds |

**Example Stream Output**:

```json
{"s":"AUDUSD","a":0.70743161,"b":0.70722341,"dc":"0.552","dd":"0.0039","ppms":false,"t":1770759992063}
{"s":"AUDUSD","a":0.70743265,"b":0.70722236,"dc":"0.552","dd":"0.0039","ppms":false,"t":1770759992425}
{"s":"AUDUSD","a":0.70743034,"b":0.70722216,"dc":"0.5519","dd":"0.0039","ppms":false,"t":1770759993310}
```

### Crypto (`/ws/crypto`)

```json
{
  "s": "ETH-USD",       // cryptocurrency pair symbol
  "p": 2874.12,         // last price
  "q": 0.145,           // trade quantity
  "dc": -0.54,          // daily change (percentage)
  "dd": -15.61,         // daily difference (price units)
  "t": 1725198451165    // timestamp (epoch milliseconds)
}
```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `s` | string | Cryptocurrency pair symbol (e.g., ETH-USD) |
| `p` | float | Last trade price |
| `q` | float | Trade quantity |
| `dc` | float | Daily change in percentage |
| `dd` | float | Daily difference in price units |
| `t` | integer | Timestamp in epoch milliseconds |

---

## Symbol Limits & Usage Notes

### Concurrent Subscriptions

**Default Limit**: 50 symbols per connection
**Upgrade**: Available via user dashboard for additional fee

### Ticker Format Requirements

| Asset Type | Format | Examples |
|------------|--------|----------|
| **US Stocks** | Plain ticker (no exchange suffix) | `AAPL`, `MSFT`, `TSLA` |
| **Forex** | No separator between currencies | `EURUSD`, `AUDUSD`, `GBPJPY` |
| **Crypto** | Dash-separated | `BTC-USD`, `ETH-USD`, `ADA-USD` |

### Important Notes

1. **Reconnection Handling**: If the WebSocket connection drops and reconnects, you must re-send your subscription commands. The server does not persist subscriptions.

2. **Batch Subscriptions**: For efficiency, batch multiple symbols in a single subscribe command rather than sending individual commands:
   ```json
   // Good: Single command with multiple symbols
   {"action": "subscribe", "symbols": "AAPL,MSFT,TSLA,AMZN,GOOGL"}

   // Less efficient: Multiple individual commands
   {"action": "subscribe", "symbols": "AAPL"}
   {"action": "subscribe", "symbols": "MSFT"}
   ```

3. **Connection Limits**: Each API key is subject to rate limits on the number of simultaneous WebSocket connections.

4. **Data Compression**: Consider implementing client-side buffering if handling high-frequency updates.

---

## Python Implementation

### Basic Connection Example

```python
import asyncio
import websockets
import json

async def connect_to_websocket():
    """Basic WebSocket connection example"""
    url = "wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo"

    async with websockets.connect(url) as ws:
        # Subscribe to symbols
        subscribe_msg = {"action": "subscribe", "symbols": "BTC-USD"}
        await ws.send(json.dumps(subscribe_msg))

        # Receive and print messages
        while True:
            message = await ws.recv()
            print(message)

# Run the connection
asyncio.run(connect_to_websocket())
```

### Multi-Symbol US Stock Monitor

```python
import asyncio
import websockets
import json
from datetime import datetime

class StockMonitor:
    """Real-time US stock trade monitor"""

    def __init__(self, api_token, symbols):
        self.api_token = api_token
        self.symbols = symbols
        self.url = f"wss://ws.eodhistoricaldata.com/ws/us?api_token={api_token}"

    async def connect(self):
        """Connect and stream trade data"""
        async with websockets.connect(self.url) as ws:
            # Subscribe to all symbols
            subscribe_msg = {
                "action": "subscribe",
                "symbols": ",".join(self.symbols)
            }
            await ws.send(json.dumps(subscribe_msg))
            print(f"Subscribed to: {', '.join(self.symbols)}")

            # Process incoming trades
            while True:
                message = await ws.recv()
                data = json.loads(message)
                self.process_trade(data)

    def process_trade(self, trade):
        """Process and display trade data"""
        if 's' in trade:  # Valid trade message
            timestamp = datetime.fromtimestamp(trade['t'] / 1000)
            print(f"{timestamp.strftime('%H:%M:%S')} | "
                  f"{trade['s']:6} | "
                  f"Price: ${trade['p']:.2f} | "
                  f"Size: {trade['v']:>6} | "
                  f"Status: {trade['ms']}")

# Usage
async def main():
    monitor = StockMonitor(
        api_token="demo",
        symbols=["AAPL", "MSFT", "TSLA"]
    )
    await monitor.connect()

asyncio.run(main())
```

**Output Example**:
```
Subscribed to: AAPL, MSFT, TSLA
14:23:15 | AAPL   | Price: $227.31 | Size:    100 | Status: open
14:23:15 | TSLA   | Price: $725.45 | Size:     50 | Status: open
14:23:16 | MSFT   | Price: $412.89 | Size:    200 | Status: open
```

### Forex Quote Monitor

```python
import asyncio
import websockets
import json

class ForexMonitor:
    """Real-time Forex quote monitor"""

    def __init__(self, api_token, pairs):
        self.api_token = api_token
        self.pairs = pairs
        self.url = f"wss://ws.eodhistoricaldata.com/ws/forex?api_token={api_token}"

    async def connect(self):
        """Connect and stream forex data"""
        async with websockets.connect(self.url) as ws:
            # Subscribe to currency pairs
            subscribe_msg = {
                "action": "subscribe",
                "symbols": ",".join(self.pairs)
            }
            await ws.send(json.dumps(subscribe_msg))
            print(f"Monitoring: {', '.join(self.pairs)}\n")

            # Process incoming quotes
            while True:
                message = await ws.recv()
                data = json.loads(message)
                self.display_quote(data)

    def display_quote(self, quote):
        """Display forex quote with spread calculation"""
        if 's' in quote:
            spread = quote['a'] - quote['b']
            spread_pips = spread * 10000  # Convert to pips for major pairs

            print(f"{quote['s']:8} | "
                  f"Bid: {quote['b']:.5f} | "
                  f"Ask: {quote['a']:.5f} | "
                  f"Spread: {spread_pips:.1f} pips | "
                  f"Daily: {quote['dc']:+.2f}%")

# Usage
async def main():
    monitor = ForexMonitor(
        api_token="demo",
        pairs=["EURUSD", "AUDUSD", "GBPUSD"]
    )
    await monitor.connect()

asyncio.run(main())
```

**Output Example**:
```
Monitoring: EURUSD, AUDUSD, GBPUSD

EURUSD   | Bid: 1.08665 | Ask: 1.08675 | Spread: 1.0 pips | Daily: +0.21%
AUDUSD   | Bid: 0.70722 | Ask: 0.70743 | Spread: 2.1 pips | Daily: +0.55%
GBPUSD   | Bid: 1.26450 | Ask: 1.26470 | Spread: 2.0 pips | Daily: -0.15%
```

### Crypto Price Tracker with Alerts

```python
import asyncio
import websockets
import json

class CryptoTracker:
    """Real-time cryptocurrency tracker with price alerts"""

    def __init__(self, api_token, pairs, alert_thresholds):
        self.api_token = api_token
        self.pairs = pairs
        self.alert_thresholds = alert_thresholds  # {symbol: threshold_pct}
        self.url = f"wss://ws.eodhistoricaldata.com/ws/crypto?api_token={api_token}"
        self.initial_prices = {}

    async def connect(self):
        """Connect and track crypto prices"""
        async with websockets.connect(self.url) as ws:
            # Subscribe to crypto pairs
            subscribe_msg = {
                "action": "subscribe",
                "symbols": ",".join(self.pairs)
            }
            await ws.send(json.dumps(subscribe_msg))
            print(f"Tracking: {', '.join(self.pairs)}\n")

            # Process incoming prices
            while True:
                message = await ws.recv()
                data = json.loads(message)
                self.process_price(data)

    def process_price(self, price_data):
        """Process price update and check alerts"""
        if 's' not in price_data:
            return

        symbol = price_data['s']
        price = price_data['p']
        daily_change = price_data['dc']

        # Store initial price
        if symbol not in self.initial_prices:
            self.initial_prices[symbol] = price

        # Check alert threshold
        alert_triggered = False
        if symbol in self.alert_thresholds:
            if abs(daily_change) >= self.alert_thresholds[symbol]:
                alert_triggered = True

        # Display with alert indicator
        alert_flag = "🚨 ALERT" if alert_triggered else ""
        print(f"{symbol:10} | "
              f"${price:>10,.2f} | "
              f"Daily: {daily_change:>+6.2f}% | "
              f"Qty: {price_data['q']:.4f} {alert_flag}")

# Usage
async def main():
    tracker = CryptoTracker(
        api_token="demo",
        pairs=["BTC-USD", "ETH-USD"],
        alert_thresholds={
            "BTC-USD": 2.0,  # Alert if moves > 2%
            "ETH-USD": 3.0   # Alert if moves > 3%
        }
    )
    await tracker.connect()

asyncio.run(main())
```

### Advanced: Reconnection Handler

```python
import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResilientWebSocketClient:
    """WebSocket client with automatic reconnection"""

    def __init__(self, api_token, endpoint, symbols):
        self.api_token = api_token
        self.endpoint = endpoint  # 'us', 'us-quote', 'forex', 'crypto'
        self.symbols = symbols
        self.url = f"wss://ws.eodhistoricaldata.com/ws/{endpoint}?api_token={api_token}"
        self.reconnect_delay = 5  # seconds
        self.max_reconnect_delay = 60

    async def connect(self):
        """Connect with automatic reconnection on failure"""
        reconnect_delay = self.reconnect_delay

        while True:
            try:
                async with websockets.connect(self.url) as ws:
                    logger.info(f"Connected to {self.endpoint}")
                    reconnect_delay = self.reconnect_delay  # Reset delay on success

                    # Subscribe to symbols
                    await self.subscribe(ws)

                    # Process messages
                    await self.receive_messages(ws)

            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"Connection closed. Reconnecting in {reconnect_delay}s...")
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, self.max_reconnect_delay)

            except Exception as e:
                logger.error(f"Unexpected error: {e}. Reconnecting in {reconnect_delay}s...")
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, self.max_reconnect_delay)

    async def subscribe(self, ws):
        """Send subscription command"""
        subscribe_msg = {
            "action": "subscribe",
            "symbols": ",".join(self.symbols)
        }
        await ws.send(json.dumps(subscribe_msg))
        logger.info(f"Subscribed to: {', '.join(self.symbols)}")

    async def receive_messages(self, ws):
        """Receive and process messages"""
        while True:
            message = await ws.recv()
            data = json.loads(message)
            self.process_message(data)

    def process_message(self, data):
        """Override this method to process messages"""
        print(data)

# Usage
async def main():
    client = ResilientWebSocketClient(
        api_token="demo",
        endpoint="crypto",
        symbols=["BTC-USD", "ETH-USD"]
    )
    await client.connect()

asyncio.run(main())
```

---

## Testing Tools

### 1. Chrome Extension: Simple WebSocket Client

**Installation**: Install from Chrome Web Store

**Steps**:
1. Open extension
2. Enter URL: `wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo`
3. Click "Connect"
4. Send: `{"action":"subscribe","symbols":"BTC-USD"}`
5. View streaming data in real-time

### 2. EODHD Chrome Extension

**Installation**: [Install from EODHD website](https://eodhd.com/chrome-extension)

**Features**:
- Free mini ticker window
- Live Stocks/FX/Crypto data
- No commands needed (automatic connection)
- Perfect for monitoring EODHD real-time feed

### 3. Postman (GUI Testing)

**Steps**:
1. Create new request → **WebSocket Request**
2. Enter URL: `wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo`
3. Click **Connect**
4. In message box, enter: `{"action":"subscribe","symbols":"BTC-USD"}`
5. Click **Send**
6. View streaming responses in the message panel

### 4. Python (Minimal Script)

**Requirements**: `pip install websockets`

```python
import asyncio, websockets, json

URL = "wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo"

async def main():
    async with websockets.connect(URL) as ws:
        await ws.send(json.dumps({"action":"subscribe","symbols":"BTC-USD"}))
        while True:
            print(await ws.recv())

asyncio.run(main())
```

**Run**: `python test_websocket.py`

### 5. macOS Terminal: websocat

**Installation** (via Homebrew):
```bash
brew install websocat
```

**One-liner Command**:
```bash
printf '{"action":"subscribe","symbols":"BTC-USD"}\n' | \
websocat "wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo"
```

**Interactive Mode**:
```bash
websocat "wss://ws.eodhistoricaldata.com/ws/forex?api_token=demo"
# Then type: {"action":"subscribe","symbols":"EURUSD"}
```

### 6. Linux/Unix: wscat

**Installation**:
```bash
npm install -g wscat
```

**Usage**:
```bash
wscat -c "wss://ws.eodhistoricaldata.com/ws/us?api_token=demo"
# Then type: {"action":"subscribe","symbols":"AAPL,MSFT"}
```

---

## API Comparison Guide

### Quick Comparison: Real-Time vs. Delayed vs. Historical

| Aspect | Real-Time (WebSockets) | Live (Delayed) | Intraday Historical |
|--------|------------------------|----------------|---------------------|
| **Transport** | WebSocket (push) | HTTPS REST (pull) | HTTPS REST (pull) |
| **Latency / Freshness** | ~live (<50 ms transport) | Stocks: 15–20 min delay<br>Currencies: ~1 min | Finalized ~2–3 hours after US after-hours close |
| **Data Types** | US trades & quotes<br>FX ticks<br>Crypto ticks | Latest OHLCV snapshot<br>(1-min updates) | OHLCV bars at 1m / 5m / 1h intervals |
| **Time Ranges** | n/a (streaming only) | n/a (snapshot feed) | 1m: 120 days<br>5m: 600 days<br>1h: 7,200 days |
| **Markets & Assets** | • US stocks (pre/post supported)<br>• Forex<br>• Digital Currencies | • US & Global Stocks<br>• Forex<br>• Digital Currencies | • US & Global Stocks<br>• Forex<br>• Digital Currencies |
| **API Calls Consumed** | 0 (no consumption) | 1 per request | 1 per request |
| **Connection Type** | Persistent, bidirectional | Request/response | Request/response |
| **Best For** | • Real-time dashboards<br>• Trading signals<br>• Market-making tools<br>• Live monitoring | • Quote tickers<br>• Watchlists<br>• Lightweight UIs<br>• Snapshot displays | • Backtesting<br>• Analytics<br>• Charting<br>• Historical analysis |
| **Update Mechanism** | Server pushes updates as they occur | Client polls periodically | Client requests historical range |
| **Data Granularity** | Tick-by-tick (every trade/quote) | Latest snapshot only | Aggregated bars (1m/5m/1h) |
| **Concurrent Symbols** | 50 default (upgradeable) | Unlimited (within API limits) | Unlimited (within API limits) |
| **Pre/Post Market** | ✅ Yes (US stocks) | ✅ Yes | ✅ Yes |
| **Historical Queries** | ❌ No | ❌ No | ✅ Yes |

### When to Use Each API

#### Use Real-Time WebSockets When:
- Building live trading dashboards
- Implementing real-time alerts and signals
- Creating market-making or algorithmic trading tools
- Need sub-second latency
- Monitoring specific tickers continuously
- Building order flow analysis tools

#### Use Live (Delayed) API When:
- Building portfolio tracking apps
- Creating watchlist displays
- Need current prices with 15-min delay acceptable
- Polling periodically (not continuous streaming)
- Simple quote displays
- Lower bandwidth requirements

#### Use Intraday Historical API When:
- Backtesting trading strategies
- Performing technical analysis
- Building charting applications
- Need historical intraday patterns
- Calculating indicators on historical bars
- Analyzing price action over time ranges

### Data Flow Comparison

```
Real-Time WebSockets:
Market → EODHD Gateway → Your Client (< 50ms)
         [persistent connection]
         [push updates continuously]

Live (Delayed):
Market → EODHD Gateway → Cache → Your Client (polling)
         [15-20 min delay for stocks]
         [~1 min delay for FX]
         [pull on demand]

Intraday Historical:
Market → EODHD Database → Your Client (query)
         [finalized 2-3h after close]
         [pull historical range]
```

---

## Best Practices

### 1. Connection Management

**Implement Reconnection Logic**:
```python
# Always handle disconnections gracefully
try:
    async with websockets.connect(url) as ws:
        await process_stream(ws)
except websockets.exceptions.ConnectionClosed:
    # Reconnect with exponential backoff
    await asyncio.sleep(reconnect_delay)
    reconnect_delay = min(reconnect_delay * 2, max_delay)
```

**Re-subscribe After Reconnect**:
```python
# Server does not persist subscriptions
async def reconnect_handler():
    while True:
        try:
            async with websockets.connect(url) as ws:
                # IMPORTANT: Re-send subscriptions
                await ws.send(json.dumps(subscribe_msg))
                await process_messages(ws)
        except:
            await asyncio.sleep(5)
```

### 2. Symbol Management

**Batch Subscriptions**:
```python
# Good: Single subscribe command
{"action": "subscribe", "symbols": "AAPL,MSFT,TSLA,AMZN,GOOGL"}

# Avoid: Multiple individual commands
{"action": "subscribe", "symbols": "AAPL"}
{"action": "subscribe", "symbols": "MSFT"}
# ... creates unnecessary overhead
```

**Monitor Active Subscriptions**:
```python
class SubscriptionManager:
    def __init__(self):
        self.active_symbols = set()

    async def subscribe(self, ws, symbols):
        new_symbols = set(symbols) - self.active_symbols
        if new_symbols:
            msg = {"action": "subscribe", "symbols": ",".join(new_symbols)}
            await ws.send(json.dumps(msg))
            self.active_symbols.update(new_symbols)

    async def unsubscribe(self, ws, symbols):
        symbols_to_remove = set(symbols) & self.active_symbols
        if symbols_to_remove:
            msg = {"action": "unsubscribe", "symbols": ",".join(symbols_to_remove)}
            await ws.send(json.dumps(msg))
            self.active_symbols -= symbols_to_remove
```

### 3. Data Processing

**Use Asyncio for Non-Blocking Processing**:
```python
async def process_message(data):
    """Process message without blocking the receive loop"""
    if 's' in data:
        # Quick processing
        symbol = data['s']
        price = data['p']

        # Offload heavy processing to task
        asyncio.create_task(analyze_price_change(symbol, price))

async def analyze_price_change(symbol, price):
    """Heavy analysis in separate task"""
    # This won't block receiving new messages
    await perform_analysis(symbol, price)
```

**Buffer High-Frequency Updates**:
```python
class MessageBuffer:
    def __init__(self, flush_interval=1.0):
        self.buffer = []
        self.flush_interval = flush_interval

    async def add(self, message):
        self.buffer.append(message)
        if len(self.buffer) >= 100:  # Buffer size threshold
            await self.flush()

    async def flush(self):
        if self.buffer:
            await self.process_batch(self.buffer)
            self.buffer.clear()

    async def process_batch(self, messages):
        # Process buffered messages in batch
        pass
```

### 4. Error Handling

**Validate Message Format**:
```python
def process_message(message):
    try:
        data = json.loads(message)

        # Validate required fields
        if 's' not in data:
            logger.warning(f"Message missing symbol: {message}")
            return

        if 'p' not in data:
            logger.warning(f"Message missing price for {data['s']}")
            return

        # Process valid message
        handle_price_update(data)

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
```

**Handle Connection Errors**:
```python
async def robust_connect(url, max_retries=5):
    """Connect with retry logic"""
    for attempt in range(max_retries):
        try:
            ws = await websockets.connect(url)
            return ws
        except websockets.exceptions.InvalidStatusCode as e:
            if e.status_code == 401:
                raise ValueError("Invalid API token")
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

    raise ConnectionError("Failed to connect after retries")
```

### 5. Performance Optimization

**Use Connection Pooling for Multiple Endpoints**:
```python
class MultiEndpointClient:
    """Manage multiple WebSocket connections efficiently"""

    def __init__(self, api_token):
        self.api_token = api_token
        self.connections = {}

    async def connect_all(self):
        """Connect to multiple endpoints concurrently"""
        tasks = [
            self.connect_endpoint("us", ["AAPL", "MSFT"]),
            self.connect_endpoint("forex", ["EURUSD"]),
            self.connect_endpoint("crypto", ["BTC-USD"])
        ]
        await asyncio.gather(*tasks)

    async def connect_endpoint(self, endpoint, symbols):
        url = f"wss://ws.eodhistoricaldata.com/ws/{endpoint}?api_token={self.api_token}"
        ws = await websockets.connect(url)
        self.connections[endpoint] = ws

        # Subscribe
        msg = {"action": "subscribe", "symbols": ",".join(symbols)}
        await ws.send(json.dumps(msg))

        # Start processing
        asyncio.create_task(self.process_endpoint(endpoint, ws))
```

**Implement Rate Limiting for Subscriptions**:
```python
import asyncio
from collections import deque

class RateLimiter:
    """Prevent overwhelming the WebSocket with subscription commands"""

    def __init__(self, max_commands_per_second=10):
        self.max_commands = max_commands_per_second
        self.commands = deque()

    async def send_command(self, ws, command):
        """Send command with rate limiting"""
        now = asyncio.get_event_loop().time()

        # Remove old commands (> 1 second ago)
        while self.commands and self.commands[0] < now - 1:
            self.commands.popleft()

        # Check rate limit
        if len(self.commands) >= self.max_commands:
            wait_time = 1 - (now - self.commands[0])
            await asyncio.sleep(wait_time)

        # Send command
        await ws.send(json.dumps(command))
        self.commands.append(asyncio.get_event_loop().time())
```

### 6. Monitoring & Logging

**Track Connection Health**:
```python
import time

class ConnectionMonitor:
    """Monitor WebSocket connection health"""

    def __init__(self):
        self.last_message_time = time.time()
        self.message_count = 0
        self.reconnection_count = 0

    def on_message(self):
        """Call when message received"""
        self.last_message_time = time.time()
        self.message_count += 1

    def on_reconnect(self):
        """Call when reconnected"""
        self.reconnection_count += 1

    def check_health(self):
        """Check if connection is healthy"""
        idle_time = time.time() - self.last_message_time

        if idle_time > 60:  # No messages for 1 minute
            logger.warning(f"Connection idle for {idle_time:.1f} seconds")
            return False

        return True

    def get_stats(self):
        """Get connection statistics"""
        return {
            "messages_received": self.message_count,
            "reconnections": self.reconnection_count,
            "idle_seconds": time.time() - self.last_message_time
        }
```

**Log Message Statistics**:
```python
from collections import Counter
import time

class MessageStats:
    """Track message statistics by symbol"""

    def __init__(self, report_interval=60):
        self.symbol_counts = Counter()
        self.last_report = time.time()
        self.report_interval = report_interval

    def record_message(self, symbol):
        """Record message for symbol"""
        self.symbol_counts[symbol] += 1

        # Periodic reporting
        if time.time() - self.last_report >= self.report_interval:
            self.report()

    def report(self):
        """Print statistics report"""
        print("\n=== Message Statistics ===")
        for symbol, count in self.symbol_counts.most_common():
            print(f"{symbol}: {count} messages")
        print(f"Total: {sum(self.symbol_counts.values())} messages\n")

        self.last_report = time.time()
```

### 7. Security

**Protect API Token**:
```python
import os

# Good: Load from environment variable
api_token = os.environ.get("EODHD_API_TOKEN")
if not api_token:
    raise ValueError("EODHD_API_TOKEN not set")

# Avoid: Hardcoding in source code
# api_token = "your_token_here"  # DON'T DO THIS
```

**Use Secure Connections**:
```python
# Always use wss:// in production
production_url = "wss://ws.eodhistoricaldata.com/ws/us?api_token={token}"

# Only use ws:// for local testing
dev_url = "ws://localhost:8080/ws/us?api_token={token}"
```

### 8. Resource Cleanup

**Proper Connection Closure**:
```python
async def graceful_shutdown(ws, symbols):
    """Properly close WebSocket connection"""
    try:
        # Unsubscribe from all symbols
        unsubscribe_msg = {"action": "unsubscribe", "symbols": ",".join(symbols)}
        await ws.send(json.dumps(unsubscribe_msg))

        # Wait briefly for unsubscribe to process
        await asyncio.sleep(0.5)

        # Close connection
        await ws.close()
        logger.info("Connection closed gracefully")

    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
```

**Context Manager Pattern**:
```python
class ManagedWebSocketClient:
    """WebSocket client with automatic cleanup"""

    async def __aenter__(self):
        self.ws = await websockets.connect(self.url)
        await self.subscribe()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.unsubscribe()
        await self.ws.close()

# Usage
async with ManagedWebSocketClient(url, symbols) as client:
    async for message in client:
        process_message(message)
# Automatically cleaned up
```

---

## Failover & Reliability

- **Source disconnection**: Automatic reconnection with exponential backoff
- **Service crash**: Automatic restart and recovery
- **Client disconnection**: Server-side cleanup of subscriptions

---

## FAQ

### API Call Consumption

Due to the nature of this API, WebSockets do **not** consume API calls. The only limit is the 50-symbol subscription limit per connection, which can be increased at an additional cost via the user dashboard.

### Connection Limits

You can use **one connection per WebSocket endpoint**. The endpoints are:
- `wss://ws.eodhistoricaldata.com/ws/us` (US trades)
- `wss://ws.eodhistoricaldata.com/ws/us-quote` (US quotes)
- `wss://ws.eodhistoricaldata.com/ws/forex` (Forex)
- `wss://ws.eodhistoricaldata.com/ws/crypto` (Crypto)

Each connection can have multiple tickers subscribed, with a total of **50 symbols** per connection.

### Test Ticker

There is no test ticker for US that works 24/7. You should test WebSockets during working hours, including pre-market and post-market hours (4 AM - 8 PM EST).

### Crypto Data Source

Data for cryptocurrencies is aggregated from **100+ exchanges**. For a ticker like BTC-USD, EODHD aggregates data using a **volume-weighted average price (VWAP)** approach: real-time price and volume data is collected from exchanges, then each exchange's price is weighted by its trading volume to calculate a single, coherent feed. This method smooths out anomalies from low-liquidity exchanges, ensuring the price reflects market activity accurately without random jumps.

### Volume Discrepancy (EOD vs WebSocket)

The total volume seen in the EOD API is aggregated data from **all exchanges**, whereas the WebSocket API provides only the **IEX exchange** data. This results in partial volume compared to EOD figures.

### Index Price Feed Fields

Index data uses the following format:

```json
{"s":"IXIC","p":14106.083,"dc":"1.8972","dd":"267.6230","ppms":true,"t":1647973245}
```

| Field | Description |
|-------|-------------|
| `s` | Symbol |
| `p` | Price |
| `dc` | Daily change (percentage) |
| `dd` | Day difference (from previous day's close) |
| `ppms` | Pre-/post-market data (true/false) |
| `t` | Timestamp |

### Update Frequency

The data is **tick-based**, not frequency-based. Updates do not happen at fixed intervals — they arrive as trades/quotes occur in the market. This can be observed by the varying timestamps between messages.

### Response Codes

| Response | Meaning |
|----------|---------|
| `{"status_code":200,"message":"Authorized"}` | Successful authentication |
| `{"status_code":422,"message":"Symbols limit reached"}` | Exceeded the 50-symbol subscription limit |
| HTTP 401 | Unauthorized (invalid API token) |
| HTTP 403 | Exceeded the number of concurrent connections |

### Trade Conditions Guidelines

When creating aggregates from WebSocket trade data, the following rules apply for which trade conditions should update which fields. The `c` field in trade messages contains condition codes.

**Early Trading Hours / After Hours (Minute Aggregates):**

| Action | Eligible Condition Codes |
|--------|--------------------------|
| Update High/Low | 0, 1, 3, 4, 5, 8, 9, 10, 12, 13, 14, 22, 23, 25, 27, 28, 29, 30, 33, 34, 36, 38 |
| Do NOT Update High/Low | 2, 7, 15, 16, 20, 21, 37, 52, 53 |
| Update Last | 0, 1, 3, 4, 8, 9, 12, 13, 14, 23, 25, 27, 28, 30, 34, 36, 38 |
| Do NOT Update Last | 2, 5, 7, 10, 15, 16, 20, 21, 22, 29, 33, 37, 52, 53 |
| Update Volume | 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 20, 21, 22, 23, 25, 27, 28, 29, 30, 33, 34, 36, 37, 52, 53 |
| Do NOT Update Volume | 15, 16, 38 |

**Normal Trading Hours (Minute & Daily Aggregates):**

| Action | Eligible Condition Codes |
|--------|--------------------------|
| Update High/Low | 0, 1, 3, 4, 5, 8, 9, 10, 14, 22, 23, 25, 27, 28, 29, 30, 33, 34, 36, 38 |
| Do NOT Update High/Low | 2, 7, 12, 13, 15, 16, 20, 21, 37, 52, 53 |
| Update Last | 0, 1, 3, 4, 8, 9, 14, 23, 25, 27, 28, 30, 34, 36, 38 |
| Do NOT Update Last | 2, 5, 7, 10, 12, 13, 15, 16, 20, 21, 22, 29, 33, 37, 52, 53 |
| Update Volume | 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 20, 21, 22, 23, 25, 27, 28, 29, 30, 33, 34, 36, 37, 52, 53 |
| Do NOT Update Volume | 15, 16, 38 |

### Forex Non-Trading Periods

EODHD aggregates Forex pairs from various sources and countries through trading companies, over-the-counter markets, market makers, banks, central banks, and third-party providers. Some specific pairs may have less volume or be affected by national holidays in specific countries, resulting in periods of non-trading.

### Low-Trading Tickers

Due to low trading volume, some tickers may produce data rarely. Updates will come eventually as trades occur.

### Past Issue: Subscribing to Multiple Tickers

There was a known issue where some tickers could be lost from the subscribe command when multiple tickers were used in a single command. **Workaround**: use multiple subscribe commands — one per ticker — to ensure all tickers stream data. Note: this issue may have been resolved; test with batch subscriptions first.

### Volume as a Decimal

The `v` (volume) field may contain decimal values. This occurs due to **fractional share trading**: some brokerages allow buying and selling fractional shares (portions of a share rather than whole shares), particularly for high-priced stocks. This results in non-integer trade sizes.

### Daily Change for Forex

For Forex pairs (e.g., EURUSD), the `dd` (day difference) and `dc` (daily change percentage) fields are calculated from **exactly 24 hours ago**, not from a fixed daily reset time.

---

## Summary

The EODHD WebSockets Real-Time Data API provides:

✅ **Ultra-low latency** streaming data (<50ms transport delay)
✅ **50 concurrent symbols** (upgradeable via dashboard)
✅ **Zero API call consumption** (does not count toward API limits)
✅ **Extended hours support** for US stocks (4 AM - 8 PM EST)
✅ **1100+ Forex pairs** and **1000+ cryptocurrencies**
✅ **Trade and quote streams** for US equities
✅ **Persistent connections** with push updates

**Key Endpoints**:
- `wss://ws.eodhistoricaldata.com/ws/us` - US stock trades
- `wss://ws.eodhistoricaldata.com/ws/us-quote` - US stock quotes
- `wss://ws.eodhistoricaldata.com/ws/forex` - Forex pairs
- `wss://ws.eodhistoricaldata.com/ws/crypto` - Cryptocurrencies

**Perfect For**:
- Real-time trading dashboards
- Live market monitoring
- Algorithmic trading systems
- Signal generation tools
- Market-making applications

For historical analysis and backtesting, use the **Intraday Historical API** instead. For delayed snapshots, use the **Live (Delayed) API**.

---

## Error Handling

### WebSocket Error Messages

When an error occurs, the WebSocket connection sends error messages in JSON format:

```json
{
  "status": 422,
  "message": "Server error"
}
```

### Common Error Codes

| Status Code | Meaning | Description | Solution |
|-------------|---------|-------------|----------|
| **401** | Unauthorized | Invalid API token | Check your `api_token` parameter in the connection URL |
| **403** | Forbidden | API key does not have access to real-time data | Upgrade to a plan with real-time WebSocket access |
| **422** | Unprocessable Entity | Server error or invalid request | Check your subscribe message format and symbol syntax |
| **429** | Too Many Requests | Rate limit exceeded from rapid reconnection attempts | Implement exponential backoff for reconnections |
| **500** | Internal Server Error | Server-side error | Retry connection after a delay |

### WebSocket Close Codes

Standard WebSocket close codes you may encounter:

| Close Code | Meaning | Description |
|------------|---------|-------------|
| **1000** | Normal Closure | Connection closed normally |
| **1001** | Going Away | Server is shutting down or browser navigating away |
| **1002** | Protocol Error | WebSocket protocol error |
| **1006** | Abnormal Closure | Connection lost without close frame |
| **1008** | Policy Violation | Message violates server policy (e.g., invalid symbols) |
| **1011** | Internal Error | Server encountered unexpected condition |

### Python Error Handling Example

```python
import asyncio
import websockets
import json
import time

class ResilientWebSocketClient:
    """WebSocket client with comprehensive error handling"""

    def __init__(self, url, max_reconnect_attempts=5):
        self.url = url
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_delay = 1  # Start with 1 second
        self.max_reconnect_delay = 60  # Cap at 60 seconds

    async def connect_with_retry(self):
        """Connect with exponential backoff on failures"""
        attempt = 0

        while attempt < self.max_reconnect_attempts:
            try:
                print(f"Connection attempt {attempt + 1}/{self.max_reconnect_attempts}")

                async with websockets.connect(self.url) as ws:
                    print("✅ Connected successfully")
                    self.reconnect_delay = 1  # Reset delay on success

                    # Subscribe to symbols
                    await self.subscribe(ws)

                    # Process messages with error handling
                    await self.receive_messages(ws)

            except websockets.exceptions.InvalidStatusCode as e:
                if e.status_code == 401:
                    print("❌ Error 401: Invalid API token. Check your credentials.")
                    break  # Don't retry on auth errors
                elif e.status_code == 403:
                    print("❌ Error 403: No access to real-time data. Upgrade your plan.")
                    break  # Don't retry on permission errors
                elif e.status_code == 429:
                    print(f"⚠️ Error 429: Rate limit exceeded. Waiting {self.reconnect_delay}s...")
                    await asyncio.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                else:
                    print(f"❌ Connection failed with status {e.status_code}")

            except websockets.exceptions.ConnectionClosed as e:
                print(f"⚠️ Connection closed: code={e.code}, reason={e.reason}")

                if e.code == 1000:
                    print("Normal closure - not reconnecting")
                    break
                elif e.code == 1008:
                    print("Policy violation - check your symbols and subscription format")
                    break
                else:
                    print(f"Reconnecting in {self.reconnect_delay}s...")
                    await asyncio.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)

            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)

            attempt += 1

        print(f"Failed to connect after {self.max_reconnect_attempts} attempts")

    async def subscribe(self, ws):
        """Send subscription message"""
        subscribe_msg = {
            "action": "subscribe",
            "symbols": "AAPL,MSFT"
        }
        await ws.send(json.dumps(subscribe_msg))
        print("📡 Subscription sent")

    async def receive_messages(self, ws):
        """Receive and process messages with error handling"""
        async for message in ws:
            try:
                data = json.loads(message)

                # Check for error messages
                if "status" in data and "message" in data:
                    status = data["status"]
                    msg = data["message"]

                    if status == 422:
                        print(f"⚠️ Server error (422): {msg}")
                        print("   Check your subscribe message format")
                    elif status == 429:
                        print(f"⚠️ Rate limit (429): {msg}")
                        print("   Reduce subscription frequency or symbol count")
                    else:
                        print(f"⚠️ Error {status}: {msg}")

                    continue

                # Check for authorization message
                if "status_code" in data and data.get("status_code") == 200:
                    print("✅ Authorized")
                    continue

                # Process valid market data
                if "s" in data and "p" in data:
                    self.process_market_data(data)

            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON received: {message}")
            except Exception as e:
                print(f"⚠️ Error processing message: {e}")

    def process_market_data(self, data):
        """Process valid market data message"""
        print(f"{data['s']}: ${data.get('p', 'N/A')}")


# Usage
async def main():
    url = "wss://ws.eodhistoricaldata.com/ws/crypto?api_token=demo"
    client = ResilientWebSocketClient(url, max_reconnect_attempts=5)
    await client.connect_with_retry()

asyncio.run(main())
```

### Error Handling Best Practices

#### 1. Implement Exponential Backoff

```python
async def exponential_backoff_reconnect(url, max_delay=60):
    """Reconnect with exponential backoff"""
    delay = 1
    while True:
        try:
            async with websockets.connect(url) as ws:
                # Reset delay on successful connection
                delay = 1
                await process_stream(ws)
        except Exception as e:
            print(f"Error: {e}. Reconnecting in {delay}s...")
            await asyncio.sleep(delay)
            delay = min(delay * 2, max_delay)  # Exponential backoff with cap
```

#### 2. Handle Rate Limiting (429)

```python
async def handle_rate_limit(ws, error_message):
    """Handle rate limit errors"""
    print(f"Rate limit hit: {error_message}")

    # Unsubscribe from some symbols to reduce load
    unsubscribe_msg = {"action": "unsubscribe", "symbols": "LESS_IMPORTANT_SYMBOLS"}
    await ws.send(json.dumps(unsubscribe_msg))

    # Wait before resuming
    await asyncio.sleep(60)  # Wait 1 minute
```

#### 3. Validate Messages Before Processing

```python
def is_valid_market_data(data):
    """Validate market data message"""
    # Check for error status
    if "status" in data:
        return False

    # Check for required fields
    required_fields = ["s", "p", "t"]  # symbol, price, timestamp
    return all(field in data for field in required_fields)

async def safe_process_message(message):
    """Safely process WebSocket message"""
    try:
        data = json.loads(message)

        if is_valid_market_data(data):
            process_market_data(data)
        elif "status" in data:
            handle_error_message(data)
        else:
            print(f"Unknown message format: {data}")
    except Exception as e:
        print(f"Error processing message: {e}")
```

#### 4. Monitor Connection Health

```python
class ConnectionMonitor:
    """Monitor WebSocket connection health"""

    def __init__(self, timeout=60):
        self.last_message_time = time.time()
        self.timeout = timeout

    def update(self):
        """Call when message received"""
        self.last_message_time = time.time()

    def is_healthy(self):
        """Check if connection is healthy"""
        return (time.time() - self.last_message_time) < self.timeout

    async def health_check_loop(self, ws):
        """Periodic health check"""
        while True:
            await asyncio.sleep(10)

            if not self.is_healthy():
                print("⚠️ Connection appears stale, no messages received")
                # Attempt to reconnect
                await ws.close()
                break
```

#### 5. Graceful Shutdown

```python
async def graceful_shutdown(ws, symbols):
    """Properly close WebSocket connection"""
    try:
        # Unsubscribe from all symbols
        unsubscribe_msg = {
            "action": "unsubscribe",
            "symbols": ",".join(symbols)
        }
        await ws.send(json.dumps(unsubscribe_msg))

        # Wait for unsubscribe to process
        await asyncio.sleep(0.5)

        # Close with normal closure code
        await ws.close(code=1000, reason="Normal shutdown")
        print("✅ Connection closed gracefully")

    except Exception as e:
        print(f"Error during shutdown: {e}")
```

### Quick Error Reference

**Connection Errors**:
- ❌ 401/403 → Check API key and plan access
- ⚠️ 429 → Slow down reconnection attempts (exponential backoff)
- ⚠️ 422 → Verify subscribe message format and symbol syntax

**Message Errors**:
```json
{"status": 422, "message": "Invalid symbol format"}
{"status": 429, "message": "Too many subscription requests"}
```

**Close Codes**:
- 1000 → Normal (don't reconnect)
- 1006 → Connection lost (reconnect with backoff)
- 1008 → Policy violation (fix subscription, then reconnect)

---

**Related Documentation**:
- [Intraday Historical API](./intraday-data.md)
- [Live (Delayed) API](./live-delayed.md)
- [Exchange Symbol List API](./exchange-symbol-list.md)

**External Resources**:
- [EODHD Product Landing Page](https://eodhd.com/real-time-api)
- [Coding Libraries (Python, etc)](https://github.com/eodhd)
- [WebSocket Protocol RFC](https://tools.ietf.org/html/rfc6455)
