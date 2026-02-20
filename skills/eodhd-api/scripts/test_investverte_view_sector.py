#!/usr/bin/env python3
"""Tests for the Investverte ESG View Sector API endpoint.

Validates response shape and data integrity against the documented spec.
Requires EODHD_API_TOKEN environment variable with Investverte marketplace access.

Usage:
  export EODHD_API_TOKEN="your_token_here"
  python test_investverte_view_sector.py
"""

from __future__ import annotations

import json
import os
import re
import unittest
import urllib.parse
import urllib.request

BASE_URL = "https://eodhd.com/api/mp/investverte"
YEAR_PERIOD_RE = re.compile(r"^\d{4}-(FY|Q[1-4])$")


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


class TestViewSectorResponseShape(unittest.TestCase):
    """Tests for GET /sector/{symbol} top-level response structure."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/sector/Airlines")

    def test_response_is_dict(self):
        self.assertIsInstance(self.data, dict)

    def test_has_find_field(self):
        self.assertIn("find", self.data)

    def test_find_is_true(self):
        self.assertTrue(self.data["find"])

    def test_has_industry_field(self):
        self.assertIn("industry", self.data)
        self.assertIsInstance(self.data["industry"], dict)

    def test_has_years_field(self):
        self.assertIn("years", self.data)
        self.assertIsInstance(self.data["years"], list)

    def test_only_expected_top_level_keys(self):
        self.assertEqual(set(self.data.keys()), {"find", "industry", "years"})


class TestViewSectorYearsArray(unittest.TestCase):
    """Tests for the years array structure."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/sector/Airlines")
        cls.years = cls.data["years"]

    def test_years_not_empty(self):
        self.assertGreater(len(self.years), 0)

    def test_years_are_strings(self):
        for y in self.years:
            self.assertIsInstance(y, str)

    def test_years_match_format(self):
        for y in self.years:
            self.assertRegex(y, YEAR_PERIOD_RE, f"Unexpected year format: {y}")

    def test_years_has_fy_entries(self):
        fy_entries = [y for y in self.years if y.endswith("-FY")]
        self.assertGreater(len(fy_entries), 0, "Expected at least one FY entry")

    def test_years_has_quarterly_entries(self):
        q_entries = [y for y in self.years if "-Q" in y]
        self.assertGreater(len(q_entries), 0, "Expected at least one quarterly entry")

    def test_years_groups_of_five(self):
        """Each year should have 5 entries: FY, Q1, Q2, Q3, Q4."""
        self.assertEqual(len(self.years) % 5, 0, "Years array length should be a multiple of 5")

    def test_years_start_reasonably(self):
        """First year should be between 2010 and 2020."""
        first_year = int(self.years[0].split("-")[0])
        self.assertGreaterEqual(first_year, 2010)
        self.assertLessEqual(first_year, 2020)


class TestViewSectorIndustryData(unittest.TestCase):
    """Tests for the industry data arrays."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/sector/Airlines")
        cls.industry = cls.data["industry"]
        cls.years = cls.data["years"]

    def test_industry_contains_queried_sector(self):
        self.assertIn("Airlines", self.industry)

    def test_industry_has_parent_group(self):
        """Should have at least two keys: the sector and a parent industry."""
        self.assertGreaterEqual(len(self.industry), 2, "Expected sector + parent industry")

    def test_sector_array_length_matches_years(self):
        for name, scores in self.industry.items():
            self.assertEqual(
                len(scores),
                len(self.years),
                f"'{name}' array length {len(scores)} != years length {len(self.years)}",
            )

    def test_sector_values_are_number_or_null(self):
        for name, scores in self.industry.items():
            for i, val in enumerate(scores):
                self.assertTrue(
                    val is None or isinstance(val, (int, float)),
                    f"'{name}' index {i}: expected number or null, got {type(val).__name__}",
                )

    def test_scores_in_reasonable_range(self):
        for name, scores in self.industry.items():
            for val in scores:
                if val is not None:
                    self.assertGreater(val, 0, f"'{name}' score should be positive")
                    self.assertLess(val, 100, f"'{name}' score should be below 100")

    def test_at_least_some_non_null_values(self):
        for name, scores in self.industry.items():
            non_null = [v for v in scores if v is not None]
            self.assertGreater(
                len(non_null), 0,
                f"'{name}' has all null values — expected at least one score",
            )


class TestViewSectorDifferentSector(unittest.TestCase):
    """Tests for GET /sector/{symbol} with a different sector (Banking)."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/sector/Banking")

    def test_find_is_true(self):
        self.assertTrue(self.data["find"])

    def test_industry_has_entries(self):
        """Industry object should contain at least one sub-industry."""
        self.assertGreater(len(self.data["industry"]), 0)

    def test_has_years(self):
        self.assertGreater(len(self.data["years"]), 0)

    def test_arrays_aligned(self):
        for name, scores in self.data["industry"].items():
            self.assertEqual(len(scores), len(self.data["years"]))


class TestViewSectorURLEncodedName(unittest.TestCase):
    """Tests for sector names with special characters."""

    @classmethod
    def setUpClass(cls):
        # "Aerospace & Defense" needs URL encoding
        cls.data = api_get("/sector/" + urllib.parse.quote("Aerospace & Defense"))

    def test_find_is_true(self):
        self.assertTrue(self.data["find"])

    def test_industry_has_entries(self):
        """Industry object should contain sub-industries for the queried sector."""
        self.assertGreater(len(self.data["industry"]), 0)

    def test_has_years(self):
        self.assertGreater(len(self.data["years"]), 0)


class TestViewSectorErrorHandling(unittest.TestCase):
    """Tests for error responses."""

    def test_invalid_sector_returns_error(self):
        """Invalid sector should return an HTTP error."""
        try:
            data = api_get("/sector/ZZZZZ_INVALID_SECTOR_99999")
            # If no HTTP error, check for find=false
            self.assertIsInstance(data, dict)
            if "find" in data:
                self.assertFalse(data["find"])
        except urllib.error.HTTPError as exc:
            # API may return 404, 400, or 500 for invalid sectors
            self.assertIn(exc.code, (400, 404, 500))

    def test_invalid_token_returns_401(self):
        """Invalid API token should return 401 or 403."""
        query = {"api_token": "invalid_token_12345"}
        url = BASE_URL + "/sector/Airlines?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=15)
        self.assertIn(ctx.exception.code, (401, 403))


if __name__ == "__main__":
    unittest.main(verbosity=2)
