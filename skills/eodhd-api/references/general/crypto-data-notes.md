# Cryptocurrency (CC) Data Notes

This document covers common questions and data characteristics specific to EODHD's cryptocurrency data.

## Data Sources

EODHD gets cryptocurrency data directly from crypto exchanges and performs calculations (e.g., aggregation) on its side.

## Exchanges

Data is aggregated from the **top 15 crypto exchanges by volume**.

## Volume

For cryptocurrencies, the volume is the **aggregated volume from the top 15 crypto exchanges**. Volume (or other data) from a specific individual exchange is not available as a separate data set.

## Price Discrepancies with Other Sources

Cryptocurrency prices may differ from other data providers. This is because there are many crypto exchanges, and:

- You might get data from one exchange while another source uses a different exchange.
- Even when aggregating data from multiple exchanges (as EODHD does), the aggregation methodology may produce slightly different results.

This is expected behavior for crypto data.

## Market Capitalization

If the `MarketCapitalization` field is missing for a cryptocurrency, you can use the `MarketCapitalizationDiluted` field as an alternative.

---

**Last Updated**: February 2026
**Source**: EODHD Official Documentation
**Maintained By**: EODHD Skills Team
