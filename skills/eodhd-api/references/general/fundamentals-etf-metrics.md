# ETF Metrics and Calculations Reference

This guide provides comprehensive formulas, calculations, and interpretations for analyzing Exchange-Traded Funds (ETFs) using the EODHD Fundamentals API.

**Target Audience**: Developers, quantitative analysts, financial application builders

**Scope**: ETF-specific metrics including holdings analysis, asset allocation, valuation, performance, risk, and cost metrics.

---

## Table of Contents

1. [Expense and Cost Metrics](#1-expense-and-cost-metrics)
2. [Holdings Concentration Metrics](#2-holdings-concentration-metrics)
3. [Asset Allocation Analysis](#3-asset-allocation-analysis)
4. [Market Capitalization Distribution](#4-market-capitalization-distribution)
5. [Sector Analysis Metrics](#5-sector-analysis-metrics)
6. [Geographic Diversification](#6-geographic-diversification)
7. [Valuation Metrics](#7-valuation-metrics)
8. [Growth Metrics](#8-growth-metrics)
9. [Performance Metrics](#9-performance-metrics)
10. [Risk Metrics](#10-risk-metrics)
11. [Income Metrics](#11-income-metrics)
12. [Fixed Income Metrics](#12-fixed-income-metrics)
13. [Efficiency Metrics](#13-efficiency-metrics)

---

## Overview

### Data Access Pattern

All ETF metrics are accessed through the Fundamentals API:

```
https://eodhd.com/api/fundamentals/{TICKER}?api_token={API_TOKEN}&fmt=json&filter={FILTER}
```

**Key Filters**:
- `General` - Basic ETF information
- `Technicals` - Aggregate technical metrics
- `ETF_Data` - ETF-specific data (holdings, allocations, performance)
- `ETF_Data::{SUBSECTION}` - Specific subsections

### Important Notes

1. **String Types**: Most numeric values are returned as strings and must be converted to float for calculations
2. **Percentage Formats**: Some are decimals (e.g., "0.00030" = 0.03%), others are percentages (e.g., "0.03" = 0.03%)
3. **API Consumption**: Each request consumes 10 API calls
4. **Response Size**: Full ETF data can exceed 100 KB; use filters to reduce payload

---

## 1. Expense and Cost Metrics

### 1.1 Net Expense Ratio

**Description**: Annual fee charged to investors, expressed as a percentage of assets.

**Formula**:
```
Net Expense Ratio = Annual Expenses / Average Net Assets
```

**Fields Used**:
- `ETF_Data::NetExpenseRatio` (provided directly)

**Data Type**: String (decimal format, e.g., "0.00030" = 0.03%)

**API Request**:
```bash
curl "https://eodhd.com/api/fundamentals/VTI.US?api_token=demo&fmt=json&filter=ETF_Data"
```

**Python Example**:
```python
import requests

def get_expense_ratio(ticker, api_token):
    """Get net expense ratio for an ETF."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data"
    }

    response = requests.get(url, params=params).json()
    net_expense_ratio = float(response["NetExpenseRatio"])

    # Convert to percentage
    expense_ratio_pct = net_expense_ratio * 100

    return {
        "net_expense_ratio": net_expense_ratio,
        "expense_ratio_pct": expense_ratio_pct,
        "annual_cost_per_10k": expense_ratio_pct * 100  # Cost per $10,000 invested
    }

# Example usage
result = get_expense_ratio("VTI.US", "demo")
print(f"Expense Ratio: {result['expense_ratio_pct']:.3f}%")
print(f"Annual cost per $10,000: ${result['annual_cost_per_10k']:.2f}")
```

**Interpretation**:
- **< 0.20%**: Very low cost (excellent)
- **0.20% - 0.50%**: Low cost (good)
- **0.50% - 1.00%**: Moderate cost (acceptable for specialized ETFs)
- **> 1.00%**: High cost (expensive, should provide significant value)

**Benchmark Comparisons**:
- Broad market index ETFs: 0.03% - 0.15%
- Sector ETFs: 0.10% - 0.50%
- International ETFs: 0.05% - 0.75%
- Active ETFs: 0.50% - 1.50%

---

### 1.2 Ongoing Charge

**Description**: Total annual cost including management fees and operating expenses.

**Fields Used**:
- `ETF_Data::Ongoing_Charge` (provided directly)
- `ETF_Data::Date_Ongoing_Charge` (date of data)

**Data Type**: String (decimal format)

**Note**: For many US ETFs, this may be "0.0000" or identical to NetExpenseRatio. More commonly used for European ETFs.

---

### 1.3 Annual Holdings Turnover

**Description**: Percentage of portfolio holdings that changed over the past year. Higher turnover may indicate higher trading costs.

**Formula**:
```
Annual Turnover = (Value of Securities Sold or Purchased) / Average Net Assets
```

**Fields Used**:
- `ETF_Data::AnnualHoldingsTurnover` (provided directly)

**Data Type**: String (decimal format, e.g., "0.02000" = 2%)

**Python Example**:
```python
def analyze_turnover(ticker, api_token):
    """Analyze ETF turnover and its implications."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data"
    }

    response = requests.get(url, params=params).json()
    turnover = float(response["AnnualHoldingsTurnover"])
    turnover_pct = turnover * 100

    # Categorize turnover
    if turnover_pct < 5:
        category = "Very Low (Buy and Hold)"
    elif turnover_pct < 20:
        category = "Low (Index Fund)"
    elif turnover_pct < 50:
        category = "Moderate"
    elif turnover_pct < 100:
        category = "High (Active)"
    else:
        category = "Very High (Aggressive Trading)"

    return {
        "turnover_pct": turnover_pct,
        "category": category,
        "tax_efficiency": "High" if turnover_pct < 10 else "Moderate" if turnover_pct < 50 else "Low"
    }
```

**Interpretation**:
- **< 5%**: Very low turnover, highly tax-efficient
- **5% - 20%**: Low turnover, typical for index funds
- **20% - 50%**: Moderate turnover
- **50% - 100%**: High turnover, potential tax consequences
- **> 100%**: Very high turnover, active trading strategy

**Impact on Returns**:
- Higher turnover → Higher transaction costs
- Higher turnover → Potential capital gains distributions
- Higher turnover → Lower tax efficiency

---

### 1.4 Total Cost of Ownership

**Description**: Comprehensive cost including expense ratio and estimated trading costs.

**Formula**:
```
Total Cost = Net Expense Ratio + Estimated Trading Costs

Estimated Trading Costs ≈ (Annual Turnover × Bid-Ask Spread) / 2
```

**Python Example**:
```python
def estimate_total_cost(ticker, api_token, avg_bid_ask_spread=0.001):
    """
    Estimate total annual cost of owning an ETF.

    Args:
        ticker: ETF ticker (e.g., "VTI.US")
        api_token: API token
        avg_bid_ask_spread: Average bid-ask spread (default 0.1%)
    """
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data"
    }

    response = requests.get(url, params=params).json()

    expense_ratio = float(response["NetExpenseRatio"])
    turnover = float(response["AnnualHoldingsTurnover"])

    # Estimate trading costs from turnover
    estimated_trading_costs = (turnover * avg_bid_ask_spread) / 2

    total_cost = expense_ratio + estimated_trading_costs
    total_cost_pct = total_cost * 100

    return {
        "expense_ratio_pct": expense_ratio * 100,
        "estimated_trading_costs_pct": estimated_trading_costs * 100,
        "total_cost_pct": total_cost_pct,
        "cost_per_10k": total_cost_pct * 100
    }
```

---

## 2. Holdings Concentration Metrics

### 2.1 Top 10 Holdings Weight

**Description**: Percentage of total assets held in the top 10 positions. Indicates concentration risk.

**Formula**:
```
Top 10 Weight = Σ(Assets_% for top 10 holdings)
```

**Fields Used**:
- `ETF_Data::Top_10_Holdings::{TICKER}::Assets_%`

**Python Example**:
```python
def calculate_top10_concentration(ticker, api_token):
    """Calculate concentration in top 10 holdings."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Top_10_Holdings"
    }

    response = requests.get(url, params=params).json()

    top_10_weight = sum(
        holding["Assets_%"]
        for holding in response.values()
    )

    # Concentration risk assessment
    if top_10_weight < 15:
        concentration_risk = "Very Low (Highly Diversified)"
    elif top_10_weight < 30:
        concentration_risk = "Low (Well Diversified)"
    elif top_10_weight < 50:
        concentration_risk = "Moderate"
    elif top_10_weight < 70:
        concentration_risk = "High"
    else:
        concentration_risk = "Very High (Concentrated)"

    return {
        "top_10_weight_pct": top_10_weight,
        "remaining_holdings_pct": 100 - top_10_weight,
        "concentration_risk": concentration_risk
    }

# Example usage
result = calculate_top10_concentration("VTI.US", "demo")
print(f"Top 10 Holdings: {result['top_10_weight_pct']:.2f}%")
print(f"Concentration Risk: {result['concentration_risk']}")
```

**Interpretation**:
- **< 15%**: Very diversified (broad market ETFs)
- **15% - 30%**: Well diversified
- **30% - 50%**: Moderate concentration
- **50% - 70%**: Concentrated (sector/thematic ETFs)
- **> 70%**: Highly concentrated (single stock risk)

---

### 2.2 Holdings Count

**Description**: Total number of holdings in the ETF.

**Fields Used**:
- `ETF_Data::Holdings_Count` (provided directly)

**Data Type**: Integer

**Python Example**:
```python
def analyze_diversification(ticker, api_token):
    """Analyze ETF diversification through holdings count."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data"
    }

    response = requests.get(url, params=params).json()
    holdings_count = response["Holdings_Count"]

    # Classify by holdings count
    if holdings_count < 30:
        classification = "Concentrated"
    elif holdings_count < 100:
        classification = "Moderately Diversified"
    elif holdings_count < 500:
        classification = "Well Diversified"
    else:
        classification = "Broadly Diversified"

    # Estimate average holding weight (simplified)
    avg_weight = 100 / holdings_count if holdings_count > 0 else 0

    return {
        "holdings_count": holdings_count,
        "classification": classification,
        "avg_weight_pct": avg_weight
    }
```

**Typical Ranges**:
- **Broad Market ETFs**: 500+ holdings (e.g., VTI has ~3,268)
- **Large-Cap ETFs**: 100-500 holdings
- **Sector ETFs**: 30-100 holdings
- **Thematic/Niche ETFs**: 20-50 holdings
- **Leveraged/Inverse ETFs**: May hold derivatives, not stocks

---

### 2.3 Average Market Capitalization

**Description**: Weighted average market cap of holdings (in millions).

**Fields Used**:
- `ETF_Data::Average_Mkt_Cap_Mil` (provided directly)

**Data Type**: String (market cap in millions)

**Python Example**:
```python
def analyze_market_cap_focus(ticker, api_token):
    """Determine market cap focus of ETF."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data"
    }

    response = requests.get(url, params=params).json()
    avg_mkt_cap_mil = float(response["Average_Mkt_Cap_Mil"])
    avg_mkt_cap_bil = avg_mkt_cap_mil / 1000

    # Classify by average market cap
    if avg_mkt_cap_bil < 2:
        cap_focus = "Small-Cap"
    elif avg_mkt_cap_bil < 10:
        cap_focus = "Mid-Cap"
    elif avg_mkt_cap_bil < 200:
        cap_focus = "Large-Cap"
    else:
        cap_focus = "Mega-Cap"

    return {
        "avg_mkt_cap_millions": avg_mkt_cap_mil,
        "avg_mkt_cap_billions": avg_mkt_cap_bil,
        "cap_focus": cap_focus
    }
```

---

### 2.4 Sector Concentration (Herfindahl-Hirschman Index)

**Description**: Measure of portfolio concentration across sectors using HHI.

**Formula**:
```
HHI = Σ(Sector_Weight²) for all sectors

Where:
- 10,000 = Perfect concentration (one sector)
- < 1,500 = Not concentrated
- 1,500 - 2,500 = Moderately concentrated
- > 2,500 = Highly concentrated
```

**Fields Used**:
- `ETF_Data::Sector_Weights::{SECTOR}::Equity_%`

**Python Example**:
```python
def calculate_sector_hhi(ticker, api_token):
    """Calculate Herfindahl-Hirschman Index for sector concentration."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Sector_Weights"
    }

    response = requests.get(url, params=params).json()

    # Calculate HHI
    hhi = sum(
        (float(sector_data["Equity_%"]) ** 2)
        for sector_data in response.values()
        if "Equity_%" in sector_data
    )

    # Interpret concentration
    if hhi < 1500:
        concentration = "Not Concentrated (Diversified)"
    elif hhi < 2500:
        concentration = "Moderately Concentrated"
    else:
        concentration = "Highly Concentrated"

    # Find dominant sector
    sectors_sorted = sorted(
        [(sector, float(data["Equity_%"])) for sector, data in response.items() if "Equity_%" in data],
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "hhi": hhi,
        "concentration_level": concentration,
        "top_sector": sectors_sorted[0][0] if sectors_sorted else "N/A",
        "top_sector_weight": sectors_sorted[0][1] if sectors_sorted else 0
    }
```

---

## 3. Asset Allocation Analysis

### 3.1 Equity Allocation

**Description**: Percentage of assets invested in stocks (US + non-US).

**Formula**:
```
Total Equity = Stock US (Net_Assets_%) + Stock non-US (Net_Assets_%)
```

**Fields Used**:
- `ETF_Data::Asset_Allocation::Stock US::Net_Assets_%`
- `ETF_Data::Asset_Allocation::Stock non-US::Net_Assets_%`

**Python Example**:
```python
def analyze_asset_allocation(ticker, api_token):
    """Analyze ETF asset allocation across asset classes."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Asset_Allocation"
    }

    response = requests.get(url, params=params).json()

    # Extract allocations
    stock_us = float(response.get("Stock US", {}).get("Net_Assets_%", "0"))
    stock_non_us = float(response.get("Stock non-US", {}).get("Net_Assets_%", "0"))
    bond = float(response.get("Bond", {}).get("Net_Assets_%", "0"))
    cash = float(response.get("Cash", {}).get("Net_Assets_%", "0"))
    other = float(response.get("Other", {}).get("Net_Assets_%", "0"))

    total_equity = stock_us + stock_non_us

    # Calculate US equity home bias
    us_equity_ratio = (stock_us / total_equity * 100) if total_equity > 0 else 0

    # Determine allocation strategy
    if total_equity > 95:
        strategy = "Pure Equity"
    elif total_equity > 70 and bond > 20:
        strategy = "Aggressive Balanced"
    elif total_equity > 50 and bond > 30:
        strategy = "Moderate Balanced"
    elif total_equity > 30 and bond > 50:
        strategy = "Conservative Balanced"
    elif bond > 95:
        strategy = "Pure Fixed Income"
    else:
        strategy = "Mixed"

    return {
        "stock_us_pct": stock_us,
        "stock_non_us_pct": stock_non_us,
        "total_equity_pct": total_equity,
        "bond_pct": bond,
        "cash_pct": cash,
        "other_pct": other,
        "us_equity_ratio_pct": us_equity_ratio,
        "allocation_strategy": strategy
    }

# Example usage
result = analyze_asset_allocation("VTI.US", "demo")
print(f"Total Equity: {result['total_equity_pct']:.2f}%")
print(f"US Stocks: {result['stock_us_pct']:.2f}%")
print(f"International Stocks: {result['stock_non_us_pct']:.2f}%")
print(f"Bonds: {result['bond_pct']:.2f}%")
print(f"Strategy: {result['allocation_strategy']}")
```

**Interpretation**:
- **Pure Equity (>95% stocks)**: High growth potential, high volatility
- **Balanced (40-70% stocks)**: Growth with downside protection
- **Conservative (<40% stocks)**: Capital preservation focus
- **US Home Bias**: US market is ~60% of global market cap; >70% may indicate home bias

---

### 3.2 Long vs Short Positions

**Description**: Analysis of long and short positions in each asset class.

**Formula**:
```
Net Position = Long_% - Short_%
Gross Exposure = Long_% + Short_%
Leverage Ratio = Gross Exposure / Net Position
```

**Fields Used**:
- `ETF_Data::Asset_Allocation::{ASSET_CLASS}::Long_%`
- `ETF_Data::Asset_Allocation::{ASSET_CLASS}::Short_%`
- `ETF_Data::Asset_Allocation::{ASSET_CLASS}::Net_Assets_%`

**Python Example**:
```python
def analyze_long_short_positions(ticker, api_token):
    """Analyze long/short positioning in ETF."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Asset_Allocation"
    }

    response = requests.get(url, params=params).json()

    results = {}
    total_gross_exposure = 0
    total_net_exposure = 0

    for asset_class, positions in response.items():
        if isinstance(positions, dict):
            long_pct = float(positions.get("Long_%", "0"))
            short_pct = float(positions.get("Short_%", "0"))
            net_pct = float(positions.get("Net_Assets_%", "0"))

            gross_exposure = long_pct + short_pct

            results[asset_class] = {
                "long_pct": long_pct,
                "short_pct": short_pct,
                "net_pct": net_pct,
                "gross_exposure": gross_exposure
            }

            total_gross_exposure += gross_exposure
            total_net_exposure += net_pct

    # Calculate overall leverage
    leverage_ratio = total_gross_exposure / total_net_exposure if total_net_exposure != 0 else 1

    # Determine ETF type
    if leverage_ratio > 1.5:
        etf_type = "Leveraged/Hedged"
    elif any(pos["short_pct"] > 5 for pos in results.values()):
        etf_type = "Market Neutral/Long-Short"
    else:
        etf_type = "Long-Only"

    return {
        "asset_positions": results,
        "total_gross_exposure": total_gross_exposure,
        "total_net_exposure": total_net_exposure,
        "leverage_ratio": leverage_ratio,
        "etf_type": etf_type
    }
```

**Interpretation**:
- **Long-Only ETFs**: Short_% ≈ 0 for all asset classes
- **Hedged ETFs**: Significant short positions to offset currency/market risk
- **Leveraged ETFs**: Gross exposure > 100%
- **Market Neutral**: Long and short positions approximately equal

---

## 4. Market Capitalization Distribution

### 4.1 Market Cap Breakdown

**Description**: Distribution of holdings across market cap segments.

**Fields Used**:
- `ETF_Data::Market_Capitalisation::Mega` (>$200B)
- `ETF_Data::Market_Capitalisation::Big` ($10B-$200B)
- `ETF_Data::Market_Capitalisation::Medium` ($2B-$10B)
- `ETF_Data::Market_Capitalisation::Small` ($300M-$2B)
- `ETF_Data::Market_Capitalisation::Micro` (<$300M)

**Python Example**:
```python
def analyze_market_cap_distribution(ticker, api_token):
    """Analyze market cap distribution and style tilt."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Market_Capitalisation"
    }

    response = requests.get(url, params=params).json()

    mega = float(response.get("Mega", "0"))
    big = float(response.get("Big", "0"))
    medium = float(response.get("Medium", "0"))
    small = float(response.get("Small", "0"))
    micro = float(response.get("Micro", "0"))

    # Calculate large-cap (Mega + Big) vs small-cap (Small + Micro)
    large_cap = mega + big
    small_cap = small + micro

    # Determine style
    if large_cap > 80:
        style = "Large-Cap"
    elif large_cap > 60:
        style = "Large-Cap Blend"
    elif medium > 50:
        style = "Mid-Cap"
    elif small_cap > 50:
        style = "Small-Cap"
    else:
        style = "Multi-Cap Blend"

    # Calculate diversification score (lower HHI = more diversified)
    hhi = mega**2 + big**2 + medium**2 + small**2 + micro**2

    return {
        "mega_cap_pct": mega,
        "large_cap_pct": big,
        "mid_cap_pct": medium,
        "small_cap_pct": small,
        "micro_cap_pct": micro,
        "total_large_cap": large_cap,
        "total_small_cap": small_cap,
        "style": style,
        "cap_diversification_hhi": hhi
    }

# Example usage
result = analyze_market_cap_distribution("VTI.US", "demo")
print(f"Style: {result['style']}")
print(f"Large-Cap: {result['total_large_cap']:.2f}%")
print(f"Mid-Cap: {result['mid_cap_pct']:.2f}%")
print(f"Small-Cap: {result['total_small_cap']:.2f}%")
```

**Interpretation**:
- **Large-Cap Focused**: Mega + Big > 80% (lower volatility, higher liquidity)
- **Mid-Cap Focused**: Medium > 50% (balance of growth and stability)
- **Small-Cap Focused**: Small + Micro > 50% (higher growth potential, higher risk)
- **Broad Market**: Diversified across all segments

---

### 4.2 Market Cap Style Score

**Description**: Quantitative score indicating large-cap vs small-cap tilt.

**Formula**:
```
Style Score = (Mega × 5 + Big × 4 + Medium × 3 + Small × 2 + Micro × 1) / 100

Interpretation:
- > 4.0: Large-Cap
- 3.0 - 4.0: Large-Mid Blend
- 2.5 - 3.0: Mid-Cap
- 1.5 - 2.5: Small-Mid Blend
- < 1.5: Small-Cap
```

**Python Example**:
```python
def calculate_style_score(ticker, api_token):
    """Calculate quantitative market cap style score."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Market_Capitalisation"
    }

    response = requests.get(url, params=params).json()

    mega = float(response.get("Mega", "0"))
    big = float(response.get("Big", "0"))
    medium = float(response.get("Medium", "0"))
    small = float(response.get("Small", "0"))
    micro = float(response.get("Micro", "0"))

    # Calculate weighted style score
    style_score = (mega * 5 + big * 4 + medium * 3 + small * 2 + micro * 1) / 100

    # Interpret score
    if style_score > 4.0:
        interpretation = "Large-Cap"
    elif style_score > 3.0:
        interpretation = "Large-Mid Blend"
    elif style_score > 2.5:
        interpretation = "Mid-Cap"
    elif style_score > 1.5:
        interpretation = "Small-Mid Blend"
    else:
        interpretation = "Small-Cap"

    return {
        "style_score": style_score,
        "interpretation": interpretation
    }
```

---

## 5. Sector Analysis Metrics

### 5.1 Sector Weights

**Description**: Percentage allocation to each sector.

**Fields Used**:
- `ETF_Data::Sector_Weights::{SECTOR}::Equity_%`

**Available Sectors**:
- Basic Materials
- Communication Services
- Consumer Cyclical
- Consumer Defensive
- Energy
- Financial Services
- Healthcare
- Industrials
- Real Estate
- Technology
- Utilities

**Python Example**:
```python
def analyze_sector_weights(ticker, api_token):
    """Analyze sector allocation and identify concentrations."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Sector_Weights"
    }

    response = requests.get(url, params=params).json()

    sectors = {}
    for sector_name, sector_data in response.items():
        if isinstance(sector_data, dict) and "Equity_%" in sector_data:
            weight = float(sector_data["Equity_%"])
            sectors[sector_name] = weight

    # Sort sectors by weight
    sorted_sectors = sorted(sectors.items(), key=lambda x: x[1], reverse=True)

    # Identify overweight sectors (>20%)
    overweight_sectors = [(name, weight) for name, weight in sorted_sectors if weight > 20]

    # Calculate sector diversification (inverse of HHI)
    sector_hhi = sum(weight ** 2 for weight in sectors.values())
    diversification_score = 10000 / sector_hhi if sector_hhi > 0 else 0

    return {
        "sectors": sectors,
        "top_3_sectors": sorted_sectors[:3],
        "overweight_sectors": overweight_sectors,
        "sector_hhi": sector_hhi,
        "diversification_score": diversification_score
    }

# Example usage
result = analyze_sector_weights("VTI.US", "demo")
print("Top 3 Sectors:")
for sector, weight in result["top_3_sectors"]:
    print(f"  {sector}: {weight:.2f}%")
```

---

### 5.2 Sector Relative Positioning

**Description**: Compare ETF sector weights to category average to identify tilts.

**Formula**:
```
Sector Tilt = ETF Sector Weight - Category Sector Weight
Relative Weight = (ETF Sector Weight / Category Sector Weight) - 1
```

**Fields Used**:
- `ETF_Data::Sector_Weights::{SECTOR}::Equity_%` (ETF weight)
- `ETF_Data::Sector_Weights::{SECTOR}::Relative_to_Category` (Category weight)

**Python Example**:
```python
def analyze_sector_tilts(ticker, api_token):
    """
    Identify sector over/underweights relative to category.

    Returns sectors where ETF deviates significantly from category average.
    """
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Sector_Weights"
    }

    response = requests.get(url, params=params).json()

    sector_analysis = {}

    for sector_name, sector_data in response.items():
        if isinstance(sector_data, dict):
            etf_weight = float(sector_data.get("Equity_%", "0"))
            category_weight = float(sector_data.get("Relative_to_Category", "0"))

            # Calculate absolute and relative difference
            absolute_tilt = etf_weight - category_weight
            relative_tilt = ((etf_weight / category_weight) - 1) * 100 if category_weight != 0 else 0

            # Categorize tilt
            if abs(absolute_tilt) > 5:
                if absolute_tilt > 0:
                    tilt_category = "Significantly Overweight"
                else:
                    tilt_category = "Significantly Underweight"
            elif abs(absolute_tilt) > 2:
                if absolute_tilt > 0:
                    tilt_category = "Moderately Overweight"
                else:
                    tilt_category = "Moderately Underweight"
            else:
                tilt_category = "Neutral"

            sector_analysis[sector_name] = {
                "etf_weight": etf_weight,
                "category_weight": category_weight,
                "absolute_tilt": absolute_tilt,
                "relative_tilt_pct": relative_tilt,
                "tilt_category": tilt_category
            }

    # Identify most significant tilts
    significant_tilts = {
        name: data for name, data in sector_analysis.items()
        if data["tilt_category"] in ["Significantly Overweight", "Significantly Underweight"]
    }

    return {
        "sector_analysis": sector_analysis,
        "significant_tilts": significant_tilts
    }

# Example usage
result = analyze_sector_tilts("VTI.US", "demo")
print("\nSignificant Sector Tilts:")
for sector, data in result["significant_tilts"].items():
    print(f"{sector}: {data['tilt_category']}")
    print(f"  ETF: {data['etf_weight']:.2f}% vs Category: {data['category_weight']:.2f}%")
    print(f"  Difference: {data['absolute_tilt']:+.2f}% ({data['relative_tilt_pct']:+.1f}%)")
```

**Interpretation**:
- **Overweight (>+5%)**: ETF has intentional bias toward sector
- **Underweight (<-5%)**: ETF avoids or minimizes sector exposure
- **Neutral (±2%)**: ETF mirrors category/market weight
- **Active Share**: Sum of absolute tilts / 2 = measure of active management

---

## 6. Geographic Diversification

### 6.1 Regional Allocation

**Description**: Distribution of equity holdings across global regions.

**Fields Used**:
- `ETF_Data::World_Regions::{REGION}::Equity_%`
- `ETF_Data::World_Regions::{REGION}::Relative_to_Category`

**Available Regions**:
- North America
- United Kingdom
- Europe Developed
- Europe Emerging
- Africa/Middle East
- Japan
- Australasia
- Asia Developed
- Asia Emerging
- Latin America

**Python Example**:
```python
def analyze_geographic_diversification(ticker, api_token):
    """Analyze geographic exposure and home bias."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::World_Regions"
    }

    response = requests.get(url, params=params).json()

    regions = {}
    for region_name, region_data in response.items():
        if isinstance(region_data, dict):
            equity_pct = float(region_data.get("Equity_%", "0"))
            category_pct = float(region_data.get("Relative_to_Category", "0"))
            regions[region_name] = {
                "equity_pct": equity_pct,
                "category_pct": category_pct
            }

    # Calculate developed vs emerging
    developed = sum([
        regions.get("North America", {}).get("equity_pct", 0),
        regions.get("United Kingdom", {}).get("equity_pct", 0),
        regions.get("Europe Developed", {}).get("equity_pct", 0),
        regions.get("Japan", {}).get("equity_pct", 0),
        regions.get("Australasia", {}).get("equity_pct", 0),
        regions.get("Asia Developed", {}).get("equity_pct", 0)
    ])

    emerging = sum([
        regions.get("Europe Emerging", {}).get("equity_pct", 0),
        regions.get("Africa/Middle East", {}).get("equity_pct", 0),
        regions.get("Asia Emerging", {}).get("equity_pct", 0),
        regions.get("Latin America", {}).get("equity_pct", 0)
    ])

    # Home bias assessment (for US-domiciled ETFs)
    north_america_pct = regions.get("North America", {}).get("equity_pct", 0)
    home_bias = "Yes" if north_america_pct > 70 else "No"

    return {
        "regions": regions,
        "developed_markets_pct": developed,
        "emerging_markets_pct": emerging,
        "north_america_pct": north_america_pct,
        "home_bias": home_bias
    }

# Example usage
result = analyze_geographic_diversification("VTI.US", "demo")
print(f"Developed Markets: {result['developed_markets_pct']:.2f}%")
print(f"Emerging Markets: {result['emerging_markets_pct']:.2f}%")
print(f"North America: {result['north_america_pct']:.2f}%")
print(f"Home Bias: {result['home_bias']}")
```

**Interpretation**:
- **US Home Bias**: US market is ~60% of global market cap; >70% indicates home bias
- **Developed Markets**: Lower volatility, higher liquidity
- **Emerging Markets**: Higher growth potential, higher risk, currency risk
- **Global Diversification**: Reduces country-specific risk

---

### 6.2 Geographic Concentration

**Description**: Measure concentration using Herfindahl-Hirschman Index for regions.

**Formula**:
```
Geographic HHI = Σ(Region_Weight²) for all regions
```

**Python Example**:
```python
def calculate_geographic_hhi(ticker, api_token):
    """Calculate geographic concentration using HHI."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::World_Regions"
    }

    response = requests.get(url, params=params).json()

    # Calculate HHI
    hhi = sum(
        float(region_data.get("Equity_%", "0")) ** 2
        for region_data in response.values()
        if isinstance(region_data, dict)
    )

    # Interpret concentration
    if hhi > 7000:
        concentration = "Highly Concentrated (Single Region)"
    elif hhi > 4000:
        concentration = "Moderately Concentrated"
    else:
        concentration = "Globally Diversified"

    # Find dominant region
    regions_sorted = sorted(
        [(region, float(data.get("Equity_%", "0")))
         for region, data in response.items()
         if isinstance(data, dict)],
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "geographic_hhi": hhi,
        "concentration_level": concentration,
        "dominant_region": regions_sorted[0][0] if regions_sorted else "N/A",
        "dominant_region_pct": regions_sorted[0][1] if regions_sorted else 0
    }
```

---

## 7. Valuation Metrics

### 7.1 Price-to-Earnings (P/E) Ratio

**Description**: Weighted average P/E ratio of portfolio holdings.

**Fields Used**:
- `ETF_Data::Valuations_Growth::Valuations_Rates_Portfolio::Price/Prospective Earnings` (Portfolio P/E)
- `ETF_Data::Valuations_Growth::Valuations_Rates_To_Category::Price/Prospective Earnings` (Category P/E)

**Python Example**:
```python
def analyze_valuation_metrics(ticker, api_token):
    """Analyze portfolio valuation relative to category."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Valuations_Growth"
    }

    response = requests.get(url, params=params).json()

    portfolio = response["Valuations_Rates_Portfolio"]
    category = response["Valuations_Rates_To_Category"]

    # Extract valuation metrics
    pe_portfolio = float(portfolio.get("Price/Prospective Earnings", "0"))
    pb_portfolio = float(portfolio.get("Price/Book", "0"))
    ps_portfolio = float(portfolio.get("Price/Sales", "0"))
    pcf_portfolio = float(portfolio.get("Price/Cash Flow", "0"))

    pe_category = float(category.get("Price/Prospective Earnings", "0"))
    pb_category = float(category.get("Price/Book", "0"))
    ps_category = float(category.get("Price/Sales", "0"))
    pcf_category = float(category.get("Price/Cash Flow", "0"))

    # Calculate relative valuations
    pe_relative = ((pe_portfolio / pe_category) - 1) * 100 if pe_category != 0 else 0
    pb_relative = ((pb_portfolio / pb_category) - 1) * 100 if pb_category != 0 else 0
    ps_relative = ((ps_portfolio / ps_category) - 1) * 100 if ps_category != 0 else 0
    pcf_relative = ((pcf_portfolio / pcf_category) - 1) * 100 if pcf_category != 0 else 0

    # Overall valuation assessment
    avg_relative = (pe_relative + pb_relative + ps_relative + pcf_relative) / 4

    if avg_relative < -10:
        valuation_assessment = "Undervalued vs Category"
    elif avg_relative < -5:
        valuation_assessment = "Slightly Undervalued vs Category"
    elif avg_relative < 5:
        valuation_assessment = "Fairly Valued vs Category"
    elif avg_relative < 10:
        valuation_assessment = "Slightly Overvalued vs Category"
    else:
        valuation_assessment = "Overvalued vs Category"

    return {
        "portfolio": {
            "pe_ratio": pe_portfolio,
            "pb_ratio": pb_portfolio,
            "ps_ratio": ps_portfolio,
            "pcf_ratio": pcf_portfolio
        },
        "category": {
            "pe_ratio": pe_category,
            "pb_ratio": pb_category,
            "ps_ratio": ps_category,
            "pcf_ratio": pcf_category
        },
        "relative_valuation": {
            "pe_relative_pct": pe_relative,
            "pb_relative_pct": pb_relative,
            "ps_relative_pct": ps_relative,
            "pcf_relative_pct": pcf_relative,
            "average_relative_pct": avg_relative
        },
        "valuation_assessment": valuation_assessment
    }

# Example usage
result = analyze_valuation_metrics("VTI.US", "demo")
print(f"Portfolio P/E: {result['portfolio']['pe_ratio']:.2f}")
print(f"Category P/E: {result['category']['pe_ratio']:.2f}")
print(f"Relative Valuation: {result['relative_valuation']['pe_relative_pct']:+.2f}%")
print(f"Assessment: {result['valuation_assessment']}")
```

**Interpretation**:
- **P/E < 15**: Value-oriented portfolio
- **P/E 15-25**: Market valuation
- **P/E > 25**: Growth-oriented portfolio
- **Relative Valuation**:
  - < -10%: Significantly cheaper than category
  - ±10%: Similar valuation to category
  - > +10%: Significantly more expensive than category

---

### 7.2 Price-to-Book (P/B) Ratio

**Description**: Portfolio's price relative to book value.

**Fields Used**:
- `ETF_Data::Valuations_Growth::Valuations_Rates_Portfolio::Price/Book`

**Interpretation**:
- **P/B < 1**: Trading below book value (value stocks)
- **P/B 1-3**: Moderate valuation
- **P/B > 3**: Growth/quality premium

---

### 7.3 Composite Valuation Score

**Description**: Normalized score combining multiple valuation metrics.

**Formula**:
```
Valuation Score = Average of normalized (inverted) metrics:
- Normalized P/E = (Market Median P/E) / (Portfolio P/E)
- Normalized P/B = (Market Median P/B) / (Portfolio P/B)
- Normalized P/S = (Market Median P/S) / (Portfolio P/S)

Higher score = Better value
```

**Python Example**:
```python
def calculate_valuation_score(ticker, api_token, market_pe=20, market_pb=3, market_ps=2):
    """
    Calculate composite valuation score.

    Args:
        market_pe, market_pb, market_ps: Market median multiples for normalization
    """
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Valuations_Growth"
    }

    response = requests.get(url, params=params).json()
    portfolio = response["Valuations_Rates_Portfolio"]

    pe_portfolio = float(portfolio.get("Price/Prospective Earnings", market_pe))
    pb_portfolio = float(portfolio.get("Price/Book", market_pb))
    ps_portfolio = float(portfolio.get("Price/Sales", market_ps))

    # Normalize (invert so higher = cheaper)
    pe_score = market_pe / pe_portfolio if pe_portfolio > 0 else 0
    pb_score = market_pb / pb_portfolio if pb_portfolio > 0 else 0
    ps_score = market_ps / ps_portfolio if ps_portfolio > 0 else 0

    # Composite score (1.0 = market average)
    composite_score = (pe_score + pb_score + ps_score) / 3

    # Interpret
    if composite_score > 1.15:
        interpretation = "Undervalued"
    elif composite_score > 1.05:
        interpretation = "Slightly Undervalued"
    elif composite_score > 0.95:
        interpretation = "Fairly Valued"
    elif composite_score > 0.85:
        interpretation = "Slightly Overvalued"
    else:
        interpretation = "Overvalued"

    return {
        "valuation_score": composite_score,
        "interpretation": interpretation,
        "components": {
            "pe_score": pe_score,
            "pb_score": pb_score,
            "ps_score": ps_score
        }
    }
```

---

## 8. Growth Metrics

### 8.1 Earnings Growth

**Description**: Expected and historical earnings growth rates.

**Fields Used**:
- `ETF_Data::Valuations_Growth::Growth_Rates_Portfolio::Long-Term Projected Earnings Growth`
- `ETF_Data::Valuations_Growth::Growth_Rates_Portfolio::Historical Earnings Growth`
- `ETF_Data::Valuations_Growth::Growth_Rates_To_Category::Long-Term Projected Earnings Growth`

**Python Example**:
```python
def analyze_growth_metrics(ticker, api_token):
    """Analyze portfolio growth characteristics."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Valuations_Growth"
    }

    response = requests.get(url, params=params).json()

    portfolio_growth = response["Growth_Rates_Portfolio"]
    category_growth = response["Growth_Rates_To_Category"]

    # Extract growth metrics
    earnings_growth_projected = float(portfolio_growth.get("Long-Term Projected Earnings Growth", "0"))
    earnings_growth_historical = float(portfolio_growth.get("Historical Earnings Growth", "0"))
    sales_growth = float(portfolio_growth.get("Sales Growth", "0"))
    cashflow_growth = float(portfolio_growth.get("Cash-Flow Growth", "0"))
    bookvalue_growth = float(portfolio_growth.get("Book-Value Growth", "0"))

    # Category comparisons
    earnings_growth_category = float(category_growth.get("Long-Term Projected Earnings Growth", "0"))

    # Calculate relative growth
    earnings_relative = earnings_growth_projected - earnings_growth_category

    # Growth consistency score (lower variance = more consistent)
    growth_rates = [earnings_growth_historical, sales_growth, cashflow_growth, bookvalue_growth]
    avg_growth = sum(growth_rates) / len(growth_rates)
    variance = sum((g - avg_growth) ** 2 for g in growth_rates) / len(growth_rates)
    consistency_score = 100 / (1 + variance)  # Higher = more consistent

    # Growth classification
    if earnings_growth_projected > 15:
        growth_style = "High Growth"
    elif earnings_growth_projected > 10:
        growth_style = "Growth"
    elif earnings_growth_projected > 5:
        growth_style = "Moderate Growth"
    else:
        growth_style = "Low Growth/Value"

    return {
        "portfolio_growth": {
            "earnings_projected_pct": earnings_growth_projected,
            "earnings_historical_pct": earnings_growth_historical,
            "sales_growth_pct": sales_growth,
            "cashflow_growth_pct": cashflow_growth,
            "bookvalue_growth_pct": bookvalue_growth,
            "average_growth_pct": avg_growth
        },
        "relative_to_category": {
            "earnings_difference": earnings_relative,
            "vs_category": "Higher" if earnings_relative > 2 else "Similar" if earnings_relative > -2 else "Lower"
        },
        "growth_style": growth_style,
        "consistency_score": consistency_score
    }

# Example usage
result = analyze_growth_metrics("VTI.US", "demo")
print(f"Growth Style: {result['growth_style']}")
print(f"Projected Earnings Growth: {result['portfolio_growth']['earnings_projected_pct']:.2f}%")
print(f"Sales Growth: {result['portfolio_growth']['sales_growth_pct']:.2f}%")
print(f"vs Category: {result['relative_to_category']['vs_category']}")
```

**Interpretation**:
- **High Growth (>15%)**: Aggressive growth stocks, higher risk
- **Growth (10-15%)**: Growth-oriented, market outperformance potential
- **Moderate (5-10%)**: Balanced growth, lower volatility
- **Low (<5%)**: Value-oriented, mature companies

---

### 8.2 Growth at a Reasonable Price (GARP) Score

**Description**: Combines growth and valuation to identify quality growth at reasonable prices.

**Formula**:
```
GARP Score = Projected Earnings Growth / (P/E Ratio)

Higher score = better value growth opportunity
```

**Python Example**:
```python
def calculate_garp_score(ticker, api_token):
    """Calculate Growth at a Reasonable Price (GARP) score."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Valuations_Growth"
    }

    response = requests.get(url, params=params).json()

    # Get P/E ratio
    pe_ratio = float(response["Valuations_Rates_Portfolio"].get("Price/Prospective Earnings", "0"))

    # Get projected earnings growth
    earnings_growth = float(response["Growth_Rates_Portfolio"].get("Long-Term Projected Earnings Growth", "0"))

    # Calculate GARP score (similar to PEG ratio)
    garp_score = earnings_growth / pe_ratio if pe_ratio > 0 else 0

    # Interpret
    if garp_score > 1.5:
        interpretation = "Excellent Value Growth"
    elif garp_score > 1.0:
        interpretation = "Good Value Growth"
    elif garp_score > 0.7:
        interpretation = "Fair Value Growth"
    else:
        interpretation = "Expensive Growth"

    return {
        "garp_score": garp_score,
        "interpretation": interpretation,
        "pe_ratio": pe_ratio,
        "earnings_growth_pct": earnings_growth
    }

# Peter Lynch's interpretation:
# GARP Score > 1.0: Stock/Portfolio is undervalued relative to growth
# GARP Score = 1.0: Fair value
# GARP Score < 1.0: Overvalued relative to growth
```

---

## 9. Performance Metrics

### 9.1 Total Returns

**Description**: Historical returns over various periods.

**Fields Used**:
- `ETF_Data::Performance::Returns_YTD` (Year-to-date)
- `ETF_Data::Performance::Returns_1Y` (1-year)
- `ETF_Data::Performance::Returns_3Y` (3-year annualized)
- `ETF_Data::Performance::Returns_5Y` (5-year annualized)
- `ETF_Data::Performance::Returns_10Y` (10-year annualized)

**Python Example**:
```python
def analyze_performance(ticker, api_token):
    """Analyze historical performance across multiple timeframes."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Performance"
    }

    response = requests.get(url, params=params).json()

    ytd = float(response.get("Returns_YTD", "0"))
    one_year = float(response.get("Returns_1Y", "0"))
    three_year = float(response.get("Returns_3Y", "0"))
    five_year = float(response.get("Returns_5Y", "0"))
    ten_year = float(response.get("Returns_10Y", "0"))

    # Calculate consistency
    long_term_avg = (three_year + five_year + ten_year) / 3

    # Performance grade
    if long_term_avg > 15:
        grade = "Excellent"
    elif long_term_avg > 10:
        grade = "Good"
    elif long_term_avg > 7:
        grade = "Average"
    else:
        grade = "Below Average"

    return {
        "returns": {
            "ytd_pct": ytd,
            "one_year_pct": one_year,
            "three_year_annualized_pct": three_year,
            "five_year_annualized_pct": five_year,
            "ten_year_annualized_pct": ten_year
        },
        "long_term_average_pct": long_term_avg,
        "performance_grade": grade
    }

# Example usage
result = analyze_performance("VTI.US", "demo")
print(f"YTD Return: {result['returns']['ytd_pct']:.2f}%")
print(f"3-Year Annualized: {result['returns']['three_year_annualized_pct']:.2f}%")
print(f"5-Year Annualized: {result['returns']['five_year_annualized_pct']:.2f}%")
print(f"Performance Grade: {result['performance_grade']}")
```

**Interpretation**:
- **Multi-year returns**: More reliable than short-term performance
- **Annualized returns**: Allow comparison across different time periods
- **Consistency**: Similar returns across 3Y/5Y/10Y indicate stable performance

---

### 9.2 Compound Annual Growth Rate (CAGR)

**Description**: Calculate CAGR from performance data.

**Formula**:
```
CAGR = [(Ending Value / Beginning Value)^(1/Years)] - 1

For returns data:
Ending Value = 1 + (Total Return / 100)
Beginning Value = 1
```

**Note**: The Returns_3Y, Returns_5Y, and Returns_10Y fields are already annualized (i.e., they represent CAGR), so no additional calculation is needed.

**Python Example**:
```python
def verify_cagr(ticker, api_token):
    """
    The API already provides annualized returns (CAGR).
    This function demonstrates the relationship.
    """
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Performance"
    }

    response = requests.get(url, params=params).json()

    # These are already annualized
    three_year_cagr = float(response.get("Returns_3Y", "0"))
    five_year_cagr = float(response.get("Returns_5Y", "0"))
    ten_year_cagr = float(response.get("Returns_10Y", "0"))

    # Calculate growth of $10,000 investment
    def future_value(initial, rate, years):
        return initial * ((1 + rate/100) ** years)

    investment = 10000

    return {
        "cagr_3y_pct": three_year_cagr,
        "cagr_5y_pct": five_year_cagr,
        "cagr_10y_pct": ten_year_cagr,
        "growth_of_10k": {
            "after_3y": future_value(investment, three_year_cagr, 3),
            "after_5y": future_value(investment, five_year_cagr, 5),
            "after_10y": future_value(investment, ten_year_cagr, 10)
        }
    }

# Example
result = verify_cagr("VTI.US", "demo")
print(f"10-Year CAGR: {result['cagr_10y_pct']:.2f}%")
print(f"$10,000 invested 10 years ago is now worth: ${result['growth_of_10k']['after_10y']:,.2f}")
```

---

## 10. Risk Metrics

### 10.1 Volatility (Standard Deviation)

**Description**: Measure of return variability. Higher volatility = higher risk.

**Fields Used**:
- `ETF_Data::Performance::1y_Volatility` (1-year standard deviation)
- `ETF_Data::Performance::3y_Volatility` (3-year annualized standard deviation)

**Python Example**:
```python
def analyze_risk(ticker, api_token):
    """Analyze ETF risk characteristics."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Performance"
    }

    response = requests.get(url, params=params).json()

    volatility_1y = float(response.get("1y_Volatility", "0"))
    volatility_3y = float(response.get("3y_Volatility", "0"))

    # Risk classification (based on 3-year volatility)
    if volatility_3y < 10:
        risk_level = "Low Risk"
    elif volatility_3y < 15:
        risk_level = "Below Average Risk"
    elif volatility_3y < 20:
        risk_level = "Average Risk"
    elif volatility_3y < 25:
        risk_level = "Above Average Risk"
    else:
        risk_level = "High Risk"

    # Estimate 95% confidence interval for annual returns
    # Assuming normal distribution: 95% of returns within ±2 standard deviations
    three_year_return = float(response.get("Returns_3Y", "0"))
    lower_bound = three_year_return - (2 * volatility_3y)
    upper_bound = three_year_return + (2 * volatility_3y)

    return {
        "volatility_1y_pct": volatility_1y,
        "volatility_3y_pct": volatility_3y,
        "risk_level": risk_level,
        "expected_return_range_95pct": {
            "lower_bound": lower_bound,
            "expected": three_year_return,
            "upper_bound": upper_bound
        }
    }

# Example usage
result = analyze_risk("VTI.US", "demo")
print(f"3-Year Volatility: {result['volatility_3y_pct']:.2f}%")
print(f"Risk Level: {result['risk_level']}")
print(f"95% Confidence Range: {result['expected_return_range_95pct']['lower_bound']:.1f}% to {result['expected_return_range_95pct']['upper_bound']:.1f}%")
```

**Interpretation**:
- **< 10%**: Low volatility (bonds, defensive stocks)
- **10-15%**: Below average volatility (large-cap stocks)
- **15-20%**: Average volatility (S&P 500 historical average ~15%)
- **20-25%**: High volatility (small-cap, emerging markets)
- **> 25%**: Very high volatility (leveraged ETFs, sector bets)

---

### 10.2 Sharpe Ratio

**Description**: Risk-adjusted return metric. Measures excess return per unit of risk.

**Formula**:
```
Sharpe Ratio = (Portfolio Return - Risk-Free Rate) / Portfolio Standard Deviation
```

**Fields Used**:
- `ETF_Data::Performance::3y_SharpRatio` (provided directly)

**Python Example**:
```python
def analyze_sharpe_ratio(ticker, api_token):
    """Analyze risk-adjusted returns using Sharpe Ratio."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Performance"
    }

    response = requests.get(url, params=params).json()

    sharpe_ratio = float(response.get("3y_SharpRatio", "0"))
    three_year_return = float(response.get("Returns_3Y", "0"))
    three_year_volatility = float(response.get("3y_Volatility", "0"))

    # Interpret Sharpe Ratio
    if sharpe_ratio > 2.0:
        interpretation = "Excellent (Very High Risk-Adjusted Return)"
    elif sharpe_ratio > 1.0:
        interpretation = "Good (Above Average Risk-Adjusted Return)"
    elif sharpe_ratio > 0.5:
        interpretation = "Fair (Acceptable Risk-Adjusted Return)"
    elif sharpe_ratio > 0:
        interpretation = "Poor (Low Risk-Adjusted Return)"
    else:
        interpretation = "Very Poor (Negative Risk-Adjusted Return)"

    # Calculate implied risk-free rate (reverse engineering)
    # Sharpe = (Return - RFR) / Volatility
    # RFR = Return - (Sharpe × Volatility)
    implied_rfr = three_year_return - (sharpe_ratio * three_year_volatility)

    return {
        "sharpe_ratio": sharpe_ratio,
        "interpretation": interpretation,
        "return_pct": three_year_return,
        "volatility_pct": three_year_volatility,
        "implied_risk_free_rate_pct": implied_rfr
    }

# Example usage
result = analyze_sharpe_ratio("VTI.US", "demo")
print(f"Sharpe Ratio: {result['sharpe_ratio']:.2f}")
print(f"Interpretation: {result['interpretation']}")
```

**Interpretation**:
- **> 2.0**: Excellent risk-adjusted returns
- **1.0 - 2.0**: Good risk-adjusted returns
- **0.5 - 1.0**: Acceptable risk-adjusted returns
- **0 - 0.5**: Poor risk-adjusted returns
- **< 0**: Negative risk-adjusted returns (underperforming risk-free rate)

**Note**: Higher Sharpe ratio = more return per unit of risk taken.

---

### 10.3 Risk-Return Scatter Analysis

**Description**: Compare ETFs on risk-return profile.

**Python Example**:
```python
def compare_risk_return_profile(tickers, api_token):
    """
    Compare multiple ETFs on risk-return dimensions.

    Args:
        tickers: List of ETF tickers (e.g., ["VTI.US", "VOO.US", "QQQ.US"])
    """
    results = []

    for ticker in tickers:
        url = f"https://eodhd.com/api/fundamentals/{ticker}"
        params = {
            "api_token": api_token,
            "fmt": "json",
            "filter": "ETF_Data::Performance"
        }

        response = requests.get(url, params=params).json()

        results.append({
            "ticker": ticker,
            "return_3y": float(response.get("Returns_3Y", "0")),
            "volatility_3y": float(response.get("3y_Volatility", "0")),
            "sharpe_ratio": float(response.get("3y_SharpRatio", "0"))
        })

    # Sort by Sharpe ratio (best risk-adjusted returns)
    results_sorted = sorted(results, key=lambda x: x["sharpe_ratio"], reverse=True)

    return {
        "etfs": results_sorted,
        "best_risk_adjusted": results_sorted[0] if results_sorted else None
    }

# Example usage
result = compare_risk_return_profile(["VTI.US", "VOO.US", "QQQ.US"], "demo")
print("\nRisk-Return Analysis:")
for etf in result["etfs"]:
    print(f"{etf['ticker']}: Return={etf['return_3y']:.2f}%, Volatility={etf['volatility_3y']:.2f}%, Sharpe={etf['sharpe_ratio']:.2f}")
```

---

## 11. Income Metrics

### 11.1 Dividend Yield

**Description**: Annual dividend income as percentage of ETF price.

**Fields Used**:
- `ETF_Data::Yield` (provided directly)
- `General::DividendYield` (from Technicals section, alternative)

**Python Example**:
```python
def analyze_income(ticker, api_token):
    """Analyze ETF income characteristics."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data"
    }

    response = requests.get(url, params=params).json()

    dividend_yield = float(response.get("Yield", "0"))
    dividend_frequency = response.get("Dividend_Paying_Frequency", "N/A")

    # Classify by yield
    if dividend_yield < 1:
        yield_category = "Low Yield (Growth Focus)"
    elif dividend_yield < 2:
        yield_category = "Below Average Yield"
    elif dividend_yield < 3:
        yield_category = "Average Yield"
    elif dividend_yield < 5:
        yield_category = "Above Average Yield"
    else:
        yield_category = "High Yield"

    # Calculate annual income on $10,000 investment
    annual_income = 10000 * (dividend_yield / 100)

    return {
        "dividend_yield_pct": dividend_yield,
        "dividend_frequency": dividend_frequency,
        "yield_category": yield_category,
        "annual_income_per_10k": annual_income
    }

# Example usage
result = analyze_income("VTI.US", "demo")
print(f"Dividend Yield: {result['dividend_yield_pct']:.2f}%")
print(f"Frequency: {result['dividend_frequency']}")
print(f"Annual income on $10,000: ${result['annual_income_per_10k']:.2f}")
```

**Interpretation**:
- **< 1%**: Growth-focused ETF
- **1-2%**: Market average for growth stocks
- **2-4%**: Moderate income ETF
- **4-6%**: High dividend ETF
- **> 6%**: Very high yield (verify sustainability)

---

### 11.2 Total Return (Price + Income)

**Description**: The Returns_* fields in Performance section already include dividends (total return).

**Python Example**:
```python
def decompose_total_return(ticker, api_token):
    """
    Estimate price return vs dividend contribution.

    Note: API provides total return. This estimates the breakdown.
    """
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json"
    }

    response = requests.get(url, params=params).json()

    # Get total return and yield
    total_return_3y = float(response["ETF_Data"]["Performance"].get("Returns_3Y", "0"))
    dividend_yield = float(response["ETF_Data"].get("Yield", "0"))

    # Estimate dividend contribution (simplified)
    # Assumes constant yield over 3 years
    estimated_dividend_contribution = dividend_yield * 3

    # Estimate price return
    estimated_price_return = total_return_3y * 3 - estimated_dividend_contribution
    estimated_annual_price_return = estimated_price_return / 3

    return {
        "total_return_3y_annualized": total_return_3y,
        "current_yield_pct": dividend_yield,
        "estimated_dividend_contribution_3y": estimated_dividend_contribution,
        "estimated_price_return_3y_annualized": estimated_annual_price_return
    }
```

---

## 12. Fixed Income Metrics

**Description**: For bond ETFs, analyze fixed income characteristics.

**Fields Used**:
- `ETF_Data::Fixed_Income::Average_Maturity`
- `ETF_Data::Fixed_Income::Average_Duration`
- `ETF_Data::Fixed_Income::Credit_Quality`
- `ETF_Data::Fixed_Income::Type`

### 12.1 Duration

**Description**: Sensitivity to interest rate changes. Higher duration = more interest rate risk.

**Formula**:
```
Price Change ≈ -Duration × Interest Rate Change

Example: Duration of 5 years
- If rates rise 1%, price falls ~5%
- If rates fall 1%, price rises ~5%
```

**Python Example**:
```python
def analyze_bond_etf(ticker, api_token):
    """Analyze fixed income ETF characteristics."""
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data::Fixed_Income"
    }

    response = requests.get(url, params=params).json()

    if not response or len(response) == 0:
        return {"error": "Not a bond ETF or no fixed income data"}

    duration = float(response.get("Average_Duration", "0"))
    maturity = float(response.get("Average_Maturity", "0"))
    credit_quality = response.get("Credit_Quality", "N/A")

    # Interest rate sensitivity
    if duration < 2:
        rate_sensitivity = "Very Low (Short-term bonds)"
    elif duration < 5:
        rate_sensitivity = "Low to Moderate (Intermediate bonds)"
    elif duration < 8:
        rate_sensitivity = "Moderate to High (Long-term bonds)"
    else:
        rate_sensitivity = "Very High (Long-duration bonds)"

    # Estimate price impact of 1% rate change
    price_impact_1pct = -duration

    return {
        "average_duration_years": duration,
        "average_maturity_years": maturity,
        "credit_quality": credit_quality,
        "rate_sensitivity": rate_sensitivity,
        "price_impact_1pct_rate_rise": price_impact_1pct,
        "price_impact_1pct_rate_fall": -price_impact_1pct
    }

# Example usage (for a bond ETF)
result = analyze_bond_etf("BND.US", "demo")
if "error" not in result:
    print(f"Duration: {result['average_duration_years']:.2f} years")
    print(f"Rate Sensitivity: {result['rate_sensitivity']}")
    print(f"If rates rise 1%: ~{result['price_impact_1pct_rate_rise']:.2f}% price change")
```

**Interpretation**:
- **Duration < 3**: Low interest rate risk (short-term bonds)
- **Duration 3-7**: Moderate interest rate risk (intermediate bonds)
- **Duration > 7**: High interest rate risk (long-term bonds)

---

### 12.2 Credit Quality

**Description**: Average credit rating of bond holdings.

**Typical Values**:
- "AAA" / "AA" - High quality
- "A" / "BBB" - Investment grade
- "BB" / "B" - High yield (junk bonds)
- "CCC" and below - Very high risk

---

## 13. Efficiency Metrics

### 13.1 Tracking Error

**Description**: Deviation between ETF returns and benchmark returns.

**Note**: EODHD API does not provide tracking error directly. Must be calculated using historical price data.

**Formula**:
```
Tracking Error = Standard Deviation(ETF Returns - Benchmark Returns)
```

**Python Example (Conceptual)**:
```python
# This requires end-of-day price data, not fundamentals data
def calculate_tracking_error_concept(etf_ticker, benchmark_ticker, api_token):
    """
    Conceptual example - requires historical price data.
    Use EODHD End-of-Day Historical Data API instead.
    """
    # Would fetch daily returns for ETF and benchmark
    # Calculate return differences
    # Calculate standard deviation of differences

    return {
        "note": "Use historical price API to calculate tracking error",
        "formula": "StdDev(ETF_Returns - Benchmark_Returns)"
    }
```

---

### 13.2 Tax Efficiency Score

**Description**: Estimate tax efficiency based on turnover and dividend yield.

**Formula**:
```
Tax Efficiency Score = 100 - (Turnover × 0.3) - (Dividend Yield × 0.5)

Higher score = more tax efficient
```

**Python Example**:
```python
def calculate_tax_efficiency(ticker, api_token):
    """
    Estimate tax efficiency based on turnover and yield.

    Lower turnover = fewer capital gains distributions
    Lower yield = less ordinary income
    """
    url = f"https://eodhd.com/api/fundamentals/{ticker}"
    params = {
        "api_token": api_token,
        "fmt": "json",
        "filter": "ETF_Data"
    }

    response = requests.get(url, params=params).json()

    turnover = float(response.get("AnnualHoldingsTurnover", "0")) * 100
    dividend_yield = float(response.get("Yield", "0"))

    # Tax efficiency score (0-100, higher = better)
    # Penalize high turnover (capital gains) and high yield (ordinary income)
    tax_score = 100 - (turnover * 0.3) - (dividend_yield * 0.5)
    tax_score = max(0, min(100, tax_score))  # Clamp between 0-100

    # Interpret
    if tax_score > 85:
        efficiency = "Highly Tax Efficient"
    elif tax_score > 70:
        efficiency = "Tax Efficient"
    elif tax_score > 50:
        efficiency = "Moderately Tax Efficient"
    else:
        efficiency = "Tax Inefficient"

    return {
        "tax_efficiency_score": tax_score,
        "efficiency_rating": efficiency,
        "turnover_pct": turnover,
        "dividend_yield_pct": dividend_yield,
        "recommendation": "Consider for taxable account" if tax_score > 70 else "Better for tax-advantaged account"
    }

# Example usage
result = calculate_tax_efficiency("VTI.US", "demo")
print(f"Tax Efficiency Score: {result['tax_efficiency_score']:.1f}/100")
print(f"Rating: {result['efficiency_rating']}")
print(f"Recommendation: {result['recommendation']}")
```

**Factors Affecting Tax Efficiency**:
- **Low Turnover**: Fewer capital gains distributions
- **Low Dividend Yield**: Less ordinary income
- **Index Funds**: Generally more tax-efficient than active funds
- **Growth Stocks**: Lower dividends than value stocks

---

## Summary Tables

### Quick Reference: ETF Analysis Checklist

| Category | Key Metrics | Ideal Values |
|----------|-------------|--------------|
| **Cost** | Net Expense Ratio | < 0.20% |
| | Annual Turnover | < 20% |
| **Diversification** | Holdings Count | > 100 |
| | Top 10 Weight | < 30% |
| | Sector HHI | < 1500 |
| **Performance** | 3Y/5Y Returns | > 10% |
| | Sharpe Ratio | > 1.0 |
| **Risk** | 3Y Volatility | 10-20% |
| **Income** | Dividend Yield | 1-3% (balanced) |
| **Tax Efficiency** | Tax Score | > 70 |

### Metric Categories by ETF Type

| ETF Type | Priority Metrics |
|----------|------------------|
| **Broad Market** | Expense ratio, holdings count, diversification |
| **Sector** | Sector concentration, relative performance, volatility |
| **International** | Geographic HHI, currency exposure, expense ratio |
| **Dividend** | Dividend yield, payout sustainability, tax efficiency |
| **Bond** | Duration, credit quality, yield to maturity |
| **Thematic** | Holdings concentration, expense ratio, tracking error |
| **Active** | Sharpe ratio, alpha, expense ratio vs category |

---

## Complete Analysis Example

```python
import requests
import json

class ETFAnalyzer:
    """Comprehensive ETF analysis using EODHD Fundamentals API."""

    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://eodhd.com/api/fundamentals"

    def get_data(self, ticker, filter_param=None):
        """Fetch fundamentals data with optional filter."""
        params = {
            "api_token": self.api_token,
            "fmt": "json"
        }
        if filter_param:
            params["filter"] = filter_param

        url = f"{self.base_url}/{ticker}"
        response = requests.get(url, params=params)
        return response.json()

    def comprehensive_analysis(self, ticker):
        """Perform complete ETF analysis."""

        # Fetch all data
        general = self.get_data(ticker, "General")
        etf_data = self.get_data(ticker, "ETF_Data")
        performance = etf_data.get("Performance", {})
        valuations = etf_data.get("Valuations_Growth", {})

        # 1. Basic Info
        basic_info = {
            "name": general.get("Name"),
            "category": general.get("Category"),
            "inception_date": etf_data.get("Inception_Date")
        }

        # 2. Cost Analysis
        expense_ratio = float(etf_data.get("NetExpenseRatio", "0")) * 100
        turnover = float(etf_data.get("AnnualHoldingsTurnover", "0")) * 100

        cost_analysis = {
            "expense_ratio_pct": expense_ratio,
            "turnover_pct": turnover,
            "cost_rating": "Low" if expense_ratio < 0.20 else "Moderate" if expense_ratio < 0.50 else "High"
        }

        # 3. Holdings Analysis
        holdings_count = etf_data.get("Holdings_Count", 0)
        top_10 = etf_data.get("Top_10_Holdings", {})
        top_10_weight = sum(h.get("Assets_%", 0) for h in top_10.values())

        holdings_analysis = {
            "holdings_count": holdings_count,
            "top_10_weight_pct": top_10_weight,
            "diversification": "High" if holdings_count > 500 else "Moderate" if holdings_count > 100 else "Low"
        }

        # 4. Performance Analysis
        returns_3y = float(performance.get("Returns_3Y", "0"))
        returns_5y = float(performance.get("Returns_5Y", "0"))
        volatility_3y = float(performance.get("3y_Volatility", "0"))
        sharpe = float(performance.get("3y_SharpRatio", "0"))

        performance_analysis = {
            "returns_3y_pct": returns_3y,
            "returns_5y_pct": returns_5y,
            "volatility_3y_pct": volatility_3y,
            "sharpe_ratio": sharpe,
            "risk_adjusted_rating": "Excellent" if sharpe > 1.5 else "Good" if sharpe > 1.0 else "Fair"
        }

        # 5. Valuation Analysis
        portfolio_pe = float(valuations.get("Valuations_Rates_Portfolio", {}).get("Price/Prospective Earnings", "0"))
        category_pe = float(valuations.get("Valuations_Rates_To_Category", {}).get("Price/Prospective Earnings", "0"))

        valuation_analysis = {
            "portfolio_pe": portfolio_pe,
            "category_pe": category_pe,
            "relative_valuation": "Cheap" if portfolio_pe < category_pe * 0.9 else "Expensive" if portfolio_pe > category_pe * 1.1 else "Fair"
        }

        # 6. Income Analysis
        dividend_yield = float(etf_data.get("Yield", "0"))

        income_analysis = {
            "dividend_yield_pct": dividend_yield,
            "annual_income_per_10k": dividend_yield * 100
        }

        # 7. Overall Rating
        scores = {
            "cost": 100 - (expense_ratio * 100),
            "diversification": min(100, holdings_count / 10),
            "performance": min(100, returns_5y * 5),
            "risk_adjusted": sharpe * 40,
            "income": min(100, dividend_yield * 25)
        }

        overall_score = sum(scores.values()) / len(scores)

        return {
            "basic_info": basic_info,
            "cost_analysis": cost_analysis,
            "holdings_analysis": holdings_analysis,
            "performance_analysis": performance_analysis,
            "valuation_analysis": valuation_analysis,
            "income_analysis": income_analysis,
            "component_scores": scores,
            "overall_score": overall_score,
            "overall_rating": "Excellent" if overall_score > 80 else "Good" if overall_score > 60 else "Average" if overall_score > 40 else "Below Average"
        }

# Usage Example
analyzer = ETFAnalyzer(api_token="demo")
result = analyzer.comprehensive_analysis("VTI.US")

print(json.dumps(result, indent=2))
```

---

## Best Practices

### 1. Data Validation
- Always check for null/empty values
- Convert strings to floats before calculations
- Handle missing data gracefully

### 2. Use Filters
- Reduce API payload size with specific filters
- Use nested filters (e.g., `ETF_Data::Performance`)
- Avoid fetching full data when only one section is needed

### 3. Comparison Analysis
- Compare ETF metrics to category averages
- Use relative metrics (vs category) for context
- Consider peer group comparisons

### 4. Multi-Factor Analysis
- Don't rely on single metric
- Combine cost, performance, risk, and diversification
- Weight factors based on investor goals

### 5. Time Period Selection
- Prefer 3Y/5Y/10Y data over 1Y for stability
- Consider full market cycle (bull + bear markets)
- YTD useful for recent performance only

---

## Additional Resources

### Related EODHD API Endpoints

For comprehensive ETF analysis, combine Fundamentals API with:

1. **End-of-Day Historical Data API** - Calculate tracking error, custom returns
2. **Live Stock Prices API** - Real-time NAV vs market price
3. **Calendar API** - Dividend payment dates
4. **Bulk API** - Screen multiple ETFs efficiently

### Further Reading

- Morningstar ETF Research
- ETF.com Education Center
- CFA Institute: ETF Analysis
- Index Fund Advisors: Portfolio Construction

---

**Document Version**: 1.0
**Last Updated**: 2024-11-27
**API Version**: EODHD Fundamentals API v1
