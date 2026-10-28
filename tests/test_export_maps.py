"""Regression tests for deterministic, flight-aware Google My Maps exports."""

import csv
import io
import json
import unittest
from pathlib import Path
from sys import path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT / "scripts"))
from export_maps import DEST, HEADERS, load, outputs  # noqa: E402


def parse(csv_data):
    return list(csv.DictReader(io.StringIO(csv_data)))


class MapExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.by_id, cls.ranking, cls.plan = load()
        cls.files = outputs()

    def test_all_venues_represented_in_rank_order(self):
        rows = parse(self.files[DEST / "all-venues.csv"])
        self.assertEqual(len(rows), len(self.by_id))
        self.assertEqual([row["ID"] for row in rows], self.ranking)
        self.assertEqual([int(row["Rank"]) for row in rows], list(range(1, len(rows) + 1)))
        for row in rows:
            self.assertEqual(row["Address"], self.by_id[row["ID"]]["address"])
            self.assertIn(row["Name"], row["Location"])
            self.assertIn("United Kingdom", row["Location"])
            self.assertTrue(row["Wiki profile"].endswith("/" + row["ID"] + "/"))
            self.assertIn("api=1", row["Google Maps"])
            self.assertEqual(row["Untappd"], self.by_id[row["ID"]]["untappd"]["url"])

    def test_top_twenty_and_cider_disclaimer(self):
        rows = parse(self.files[DEST / "top-20.csv"])
        self.assertEqual([row["ID"] for row in rows], self.ranking[:20])
        self.assertIn("check product and stock", rows[0]["Real cider evidence"])
        self.assertEqual(len(HEADERS), len(rows[0]))
        self.assertIn("Monday bar", rows[0])
        self.assertIn("Hours source", rows[0])
        self.assertIn("Closed", [row["Tuesday bar"] for row in rows])
        self.assertTrue(all(row["Hours source"].startswith("https://") for row in rows))
        self.assertNotIn("Latitude", HEADERS)
        self.assertNotIn("Longitude", HEADERS)

    def test_days_match_manifest_not_every_optional_venue(self):
        self.assertEqual(len(self.plan["routes"]), 5)
        for route in self.plan["routes"]:
            filename = DEST / (route["date"] + "-" + route["id"] + ".csv")
            rows = parse(self.files[filename])
            self.assertEqual([r["ID"] for r in rows], [s["venue_id"] for s in route["stops"]])
            self.assertEqual([int(r["Stop order"]) for r in rows], list(range(1, len(rows) + 1)))
            self.assertTrue(all(r["Visit date (UK)"] == route["date"] for r in rows))
        self.assertFalse(any("2026-11-14" in str(filename) for filename in self.files))

    def test_exports_match_checked_in_text(self):
        for relative, expected in self.files.items():
            with self.subTest(path=str(relative)):
                self.assertEqual((ROOT / relative).read_text(encoding="utf-8"), expected)

    def test_source_route_references_are_unique_and_known(self):
        self.assertEqual(len(self.by_id), len(self.ranking))
        self.assertEqual(set(self.by_id), set(self.ranking))
        self.assertEqual(len({route["date"] for route in self.plan["routes"]}), 5)


if __name__ == "__main__":
    unittest.main()
