#!/usr/bin/env python3
"""Tests for the Investverte ESG View Country API endpoint.

Validates response shape and data integrity against the documented spec.
Requires EODHD_API_TOKEN environment variable with Investverte marketplace access.

Usage:
  export EODHD_API_TOKEN="your_token_here"
  python test_investverte_view_country.py
"""

from __future__ import annotations

import json
import os
import sys
import unittest
import urllib.parse
import urllib.request

BASE_URL = "https://eodhd.com/api/mp/investverte"
VALID_FREQUENCIES = {"FY", "Q1", "Q2", "Q3", "Q4"}


def get_token() -> str:
    token = os.getenv("EODHD_API_TOKEN", "")
    if not token:
        raise unittest.SkipTest("EODHD_API_TOKEN not set – skipping live API tests")
    return token


def api_get(path: str, params: dict | None = None, timeout: int = 30) -> list | dict:
    """Make a GET request to the Investverte API and return parsed JSON."""
    query: dict[str, str] = {"api_token": get_token()}
    if params:
        query.update(params)
    url = BASE_URL + path + "?" + urllib.parse.urlencode(query)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


class TestViewCountryFullTimeSeries(unittest.TestCase):
    """Tests for GET /country/{symbol} without year/frequency filters."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/country/US")

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_response_not_empty(self):
        self.assertGreater(len(self.data), 0, "Expected at least one record for US")

    def test_multiple_records_returned(self):
        self.assertGreater(len(self.data), 5, "Full time series should have many records")

    def test_record_has_required_fields(self):
        required = {"symbol", "name", "mean", "median", "year", "frequency"}
        for record in self.data:
            self.assertTrue(
                required.issubset(record.keys()),
                f"Missing fields: {required - record.keys()}",
            )

    def test_symbol_is_us(self):
        for record in self.data:
            self.assertEqual(record["symbol"], "US")

    def test_name_is_string(self):
        for record in self.data:
            self.assertIsInstance(record["name"], str)
            self.assertGreater(len(record["name"]), 0)

    def test_mean_is_number(self):
        for record in self.data:
            self.assertIsInstance(record["mean"], (int, float))

    def test_median_is_number(self):
        for record in self.data:
            self.assertIsInstance(record["median"], (int, float))

    def test_year_is_integer(self):
        for record in self.data:
            self.assertIsInstance(record["year"], int)
            self.assertGreaterEqual(record["year"], 2010)
            self.assertLessEqual(record["year"], 2030)

    def test_frequency_is_valid(self):
        for record in self.data:
            self.assertIn(
                record["frequency"],
                VALID_FREQUENCIES,
                f"Unexpected frequency: {record['frequency']}",
            )

    def test_scores_in_reasonable_range(self):
        for record in self.data:
            self.assertGreater(record["mean"], 0, "Mean should be positive")
            self.assertLess(record["mean"], 100, "Mean should be below 100")
            self.assertGreater(record["median"], 0, "Median should be positive")
            self.assertLess(record["median"], 100, "Median should be below 100")

    def test_has_fy_and_quarterly(self):
        frequencies = {r["frequency"] for r in self.data}
        self.assertIn("FY", frequencies, "Expected FY records")
        self.assertTrue(
            frequencies.intersection({"Q1", "Q2", "Q3", "Q4"}),
            "Expected at least one quarterly record",
        )

    def test_has_multiple_years(self):
        years = {r["year"] for r in self.data}
        self.assertGreater(len(years), 1, "Expected data for multiple years")


class TestViewCountryFiltered(unittest.TestCase):
    """Tests for GET /country/{symbol} with year and frequency filters."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/country/US", {"year": "2021", "frequency": "FY"})

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_single_record_returned(self):
        self.assertEqual(len(self.data), 1, "Filtered query should return exactly one record")

    def test_record_matches_filters(self):
        record = self.data[0]
        self.assertEqual(record["year"], 2021)
        self.assertEqual(record["frequency"], "FY")
        self.assertEqual(record["symbol"], "US")

    def test_record_has_all_fields(self):
        required = {"symbol", "name", "mean", "median", "year", "frequency"}
        self.assertTrue(required.issubset(self.data[0].keys()))

    def test_scores_are_numeric(self):
        record = self.data[0]
        self.assertIsInstance(record["mean"], (int, float))
        self.assertIsInstance(record["median"], (int, float))


class TestViewCountryYearOnly(unittest.TestCase):
    """Tests for GET /country/{symbol} with only year filter."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/country/US", {"year": "2022"})

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_returns_all_frequencies_for_year(self):
        frequencies = {r["frequency"] for r in self.data}
        self.assertIn("FY", frequencies)

    def test_all_records_same_year(self):
        for record in self.data:
            self.assertEqual(record["year"], 2022)


class TestViewCountryDifferentCountry(unittest.TestCase):
    """Tests for GET /country/{symbol} with a non-US country."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/country/GB", {"year": "2022", "frequency": "FY"})

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_symbol_matches(self):
        if self.data:
            self.assertEqual(self.data[0]["symbol"], "GB")

    def test_has_scores(self):
        if self.data:
            self.assertIsInstance(self.data[0]["mean"], (int, float))
            self.assertIsInstance(self.data[0]["median"], (int, float))


class TestViewCountryErrorHandling(unittest.TestCase):
    """Tests for error responses."""

    def test_invalid_country_returns_404_or_empty(self):
        """Invalid country code should return 404 or an empty list."""
        try:
            data = api_get("/country/ZZZZZZ")
            # If no HTTP error, we might get an empty list
            self.assertIsInstance(data, list)
        except urllib.error.HTTPError as exc:
            self.assertIn(exc.code, (404, 400))

    def test_invalid_token_returns_401(self):
        """Invalid API token should return 401."""
        query = {"api_token": "invalid_token_12345"}
        url = BASE_URL + "/country/US?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=15)
        self.assertIn(ctx.exception.code, (401, 403))


if __name__ == "__main__":
    unittest.main(verbosity=2)
