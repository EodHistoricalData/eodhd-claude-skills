#!/usr/bin/env python3
"""Tests for the Investverte ESG List Sectors API endpoint.

Validates response shape and data integrity against the documented spec.
Requires EODHD_API_TOKEN environment variable with Investverte marketplace access.

Usage:
  export EODHD_API_TOKEN="your_token_here"
  python test_investverte_list_sectors.py
"""

from __future__ import annotations

import json
import os
import unittest
import urllib.parse
import urllib.request

BASE_URL = "https://eodhd.com/api/mp/investverte"

# Well-known sectors that should always be present
EXPECTED_SECTORS = {
    "Technology",
    "Healthcare",
    "Energy",
    "Banking",
    "Utilities",
    "Real Estate",
    "Industrials",
}


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


class TestListSectorsResponse(unittest.TestCase):
    """Tests for GET /sectors basic response shape."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/sectors")

    def test_response_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_response_not_empty(self):
        self.assertGreater(len(self.data), 0, "Expected at least one sector")

    def test_has_many_sectors(self):
        self.assertGreater(len(self.data), 40, "Expected 40+ sectors")


class TestListSectorsFields(unittest.TestCase):
    """Tests for field structure of each sector object."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/sectors")

    def test_each_record_has_sector_field(self):
        for record in self.data:
            self.assertIn("sector", record, f"Missing 'sector' field in {record}")

    def test_sector_is_string(self):
        for record in self.data:
            self.assertIsInstance(record["sector"], str)

    def test_sector_is_not_empty(self):
        for record in self.data:
            self.assertGreater(len(record["sector"].strip()), 0, "Sector name should not be empty")

    def test_only_sector_field(self):
        """Each record should only contain the 'sector' field."""
        for record in self.data:
            self.assertEqual(
                set(record.keys()),
                {"sector"},
                f"Unexpected fields: {set(record.keys()) - {'sector'}}",
            )


class TestListSectorsContent(unittest.TestCase):
    """Tests for expected sector values."""

    @classmethod
    def setUpClass(cls):
        cls.data = api_get("/sectors")
        cls.sector_names = {r["sector"] for r in cls.data}

    def test_contains_expected_sectors(self):
        for sector in EXPECTED_SECTORS:
            self.assertIn(sector, self.sector_names, f"Expected sector '{sector}' not found")

    def test_contains_unknown_sector(self):
        self.assertIn("Unknown", self.sector_names, "Expected 'Unknown' sector")

    def test_no_duplicate_sectors(self):
        sector_list = [r["sector"] for r in self.data]
        self.assertEqual(
            len(sector_list),
            len(set(sector_list)),
            "Duplicate sectors found",
        )

    def test_sectors_are_alphabetically_reasonable(self):
        """First sector should start with 'A' and last with a late letter."""
        sector_list = [r["sector"] for r in self.data]
        self.assertTrue(sector_list[0][0] in "AB", f"First sector unexpected: {sector_list[0]}")


class TestListSectorsErrorHandling(unittest.TestCase):
    """Tests for error responses."""

    def test_invalid_token_returns_401(self):
        """Invalid API token should return 401 or 403."""
        query = {"api_token": "invalid_token_12345"}
        url = BASE_URL + "/sectors?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=15)
        self.assertIn(ctx.exception.code, (401, 403))


if __name__ == "__main__":
    unittest.main(verbosity=2)
