# EODHD API Glossary

Quick reference for financial, technical, and EODHD-specific terms used across the API.

## Financial Data Terms

| Term | Definition |
|------|------------|
| EOD | End-of-day — closing price data after market close |
| OHLCV | Open, High, Low, Close, Volume — standard price bar format |
| Ticker | Symbol identifying a tradable security (e.g., AAPL, MSFT) |
| Exchange | Marketplace where securities are traded (NYSE, NASDAQ, LSE) |
| Fundamentals | Company financial data (balance sheet, income statement, cash flow) |
| Real-time | Live streaming data with minimal delay |
| Delayed | Data with 15-20 minute lag from real-time |
| Intraday | Price data within a single trading day |
| Historical | Past price and financial data |
| Sentiment | Market mood derived from news and social analysis |
| Options | Derivative contracts giving the right to buy/sell at a set price |
| Greeks | Options risk measures — Delta, Gamma, Theta, Vega, Rho |
| Forex | Foreign exchange — currency trading |
| Crypto | Cryptocurrency trading data |
| Index | Basket of securities representing a market segment (e.g., S&P 500) |
| Dividend | Company payment to shareholders |
| Split | Stock division increasing share count (e.g., 2:1 split) |
| Adjusted Price | Price corrected for splits and dividends |
| Market Cap | Company value = share price x shares outstanding |
| P/E Ratio | Price-to-earnings ratio — valuation metric |
| EPS | Earnings per share |
| ESG | Environmental, Social, and Governance — sustainability metrics |
| ETF | Exchange-Traded Fund |
| Mutual Fund | Pooled investment fund managed by professionals |

## Technical Terms

| Term | Definition |
|------|------------|
| API | Application Programming Interface |
| REST | Representational State Transfer — API architectural style |
| WebSocket | Persistent connection for real-time bidirectional data streaming |
| Rate Limit | Maximum API requests allowed per time period |
| API Key | Authentication token for API access (passed as `api_token`) |
| Endpoint | Specific API URL serving a particular data type |
| SDK | Software Development Kit — client library for a programming language |
| JSON | JavaScript Object Notation — default API response format |
| CSV | Comma-Separated Values — alternative response format (`fmt=csv`) |
| MCP | Model Context Protocol — standard for AI assistant tool integrations |
| CORS | Cross-Origin Resource Sharing — browser security mechanism for API access |

## EODHD-Specific Terms

| Term | Definition |
|------|------------|
| Marketplace | Third-party data provider platform on EODHD |
| All-in-One | Subscription plan bundling all main data feeds |
| Internal Use | License for data used internally (not shown to end-users) |
| Display Use | License for data shown to your end-users |
| Demo Key | Special API key (`demo`) for testing select endpoints without registration |
| Screener | Tool for filtering stocks by various criteria |
| Technical Indicators | Computed metrics based on price data (SMA, EMA, RSI, etc.) |
