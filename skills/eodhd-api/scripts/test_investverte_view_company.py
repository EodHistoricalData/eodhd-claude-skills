#!/usr/bin/env python3
"""Tests for the Investverte ESG View Company API endpoint.

Validates response shape and data integrity against the documented spec.
Requires EODHD_API_TOKEN environment variable with Investverte marketplace access.

Usage:
  export EODHD_API_TOKEN="your_token_here"
  python test_investverte_view_company.py
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
REQUIRED_FIELDS = {"e", "s", "g", "esg", "year", "frequency"}


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


class TestViewCompanyFullTimeSeries(unittest.TestCase):
    """Tests for GET /esg/{symbol} without year/frequency filters (AAPL)."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/esg/AAPL")

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_response_not_empty(self):
        self.assertGreater(len(self.data), 0, "Expected at least one record for AAPL")

    def test_multiple_records_returned(self):
        self.assertGreater(len(self.data), 5, "Full time series should have many records")

    def test_record_has_required_fields(self):
        for record in self.data:
            self.assertTrue(
                REQUIRED_FIELDS.issubset(record.keys()),
                f"Missing fields: {REQUIRED_FIELDS - record.keys()}",
            )

    def test_no_extra_symbol_or_name_fields(self):
        """Company endpoint returns e/s/g/esg/year/frequency, not symbol/name."""
        for record in self.data:
            self.assertNotIn("symbol", record)
            self.assertNotIn("name", record)

    def test_e_is_number(self):
        for record in self.data:
            self.assertIsInstance(record["e"], (int, float))

    def test_s_is_number(self):
        for record in self.data:
            self.assertIsInstance(record["s"], (int, float))

    def test_g_is_number(self):
        for record in self.data:
            self.assertIsInstance(record["g"], (int, float))

    def test_esg_is_number(self):
        for record in self.data:
            self.assertIsInstance(record["esg"], (int, float))

    def test_year_is_integer(self):
        for record in self.data:
            self.assertIsInstance(record["year"], int)
            self.assertGreaterEqual(record["year"], 2000)
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
            for field in ("e", "s", "g", "esg"):
                self.assertGreater(record[field], 0, f"{field} should be positive")
                self.assertLess(record[field], 100, f"{field} should be below 100")

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


class TestViewCompanyFiltered(unittest.TestCase):
    """Tests for GET /esg/{symbol} with year and frequency filters."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/esg/AAPL", {"year": "2021", "frequency": "FY"})

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_single_record_returned(self):
        self.assertEqual(len(self.data), 1, "Filtered query should return exactly one record")

    def test_record_matches_filters(self):
        record = self.data[0]
        self.assertEqual(record["year"], 2021)
        self.assertEqual(record["frequency"], "FY")

    def test_record_has_all_fields(self):
        self.assertTrue(REQUIRED_FIELDS.issubset(self.data[0].keys()))

    def test_all_scores_are_numeric(self):
        record = self.data[0]
        for field in ("e", "s", "g", "esg"):
            self.assertIsInstance(record[field], (int, float))

    def test_scores_in_plausible_range(self):
        """Verify AAPL 2021 FY scores are in a plausible ESG range."""
        record = self.data[0]
        for field in ("e", "s", "g", "esg"):
            self.assertGreater(record[field], 20, f"{field} unexpectedly low")
            self.assertLess(record[field], 100, f"{field} unexpectedly high")


class TestViewCompanyYearOnly(unittest.TestCase):
    """Tests for GET /esg/{symbol} with only year filter."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/esg/AAPL", {"year": "2021"})

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_returns_multiple_frequencies_for_year(self):
        frequencies = {r["frequency"] for r in self.data}
        self.assertIn("FY", frequencies)
        self.assertGreater(len(frequencies), 1)

    def test_all_records_same_year(self):
        for record in self.data:
            self.assertEqual(record["year"], 2021)


class TestViewCompanyNonUS(unittest.TestCase):
    """Tests for GET /esg/{symbol} with a non-US company (000039.SZ)."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/esg/000039.SZ")

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_response_not_empty(self):
        self.assertGreater(len(self.data), 0)

    def test_record_has_required_fields(self):
        for record in self.data:
            self.assertTrue(
                REQUIRED_FIELDS.issubset(record.keys()),
                f"Missing fields: {REQUIRED_FIELDS - record.keys()}",
            )

    def test_scores_are_numeric(self):
        for record in self.data:
            for field in ("e", "s", "g", "esg"):
                self.assertIsInstance(record[field], (int, float))

    def test_has_multiple_years(self):
        years = {r["year"] for r in self.data}
        self.assertGreater(len(years), 1, "Expected data for multiple years")


class TestViewCompanyPillarRelationships(unittest.TestCase):
    """Tests for logical relationships between E, S, G and ESG scores."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/esg/AAPL")

    def test_esg_is_within_pillar_bounds(self):
        """Composite ESG should be within a reasonable range of the pillars."""
        for record in self.data:
            pillars = [record["e"], record["s"], record["g"]]
            min_pillar = min(pillars)
            max_pillar = max(pillars)
            # ESG should be somewhere near the pillars, allow some tolerance
            self.assertGreaterEqual(
                record["esg"], min_pillar - 10,
                f"ESG {record['esg']} too far below min pillar {min_pillar}",
            )
            self.assertLessEqual(
                record["esg"], max_pillar + 10,
                f"ESG {record['esg']} too far above max pillar {max_pillar}",
            )


class TestViewCompanyErrorHandling(unittest.TestCase):
    """Tests for error responses."""

    def test_invalid_symbol_returns_404_or_empty(self):
        """Invalid symbol should return 404 or an empty list."""
        try:
            data = api_get("/esg/ZZZZZINVALID99999")
            self.assertIsInstance(data, list)
        except urllib.error.HTTPError as exc:
            self.assertIn(exc.code, (404, 400))

    def test_invalid_token_returns_401(self):
        """Invalid API token should return 401."""
        query = {"api_token": "invalid_token_12345"}
        url = BASE_URL + "/esg/AAPL?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=15)
        self.assertIn(ctx.exception.code, (401, 403))


if __name__ == "__main__":
    unittest.main(verbosity=2)
