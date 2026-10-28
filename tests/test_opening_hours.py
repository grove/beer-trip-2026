"""Regression coverage for attributed weekly opening hours and special events."""
import unittest
from pathlib import Path
from sys import path
import json

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT / "scripts"))

from opening_hours import load_hours, validate_hours, periods_text, section_lines, compact_hours


class PublishedOpeningHoursTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = load_hours()
        cls.venues = json.loads((ROOT / "data/venues.json").read_text(encoding="utf-8"))["venues"]
        cls.hours = cls.db["hours"]

    def test_every_current_venue_has_sourced_hours_or_event_only_exception(self):
        ids = {v["id"] for v in self.venues}
        self.assertEqual(ids, set(self.hours))
        self.assertEqual(len(ids), 158)
        self.assertEqual(sum(h["status"] == "published" for h in self.hours.values()), 157)
        self.assertEqual(sum(h["status"] == "event-only" for h in self.hours.values()), 1)
        self.assertEqual(validate_hours(self.db, self.venues), [])

    def test_marble_official_tuesday_closure_preserved(self):
        marble = self.hours["marble-arch"]
        self.assertEqual(marble["source_type"], "official")
        self.assertEqual(marble["days"]["tue"], [])
        self.assertIn("Tuesday CLOSED", marble["note"])
        self.assertEqual(compact_hours(marble, "tue"), "Closed")
        self.assertIn("Food / kitchen", "\n".join(section_lines(marble)))

    def test_event_only_is_not_a_regular_week(self):
        producer = self.hours["udders-orchard-cidery"]
        self.assertEqual(producer["status"], "event-only")
        self.assertNotIn("days", producer)
        self.assertEqual(compact_hours(producer, "wed"), "Event-only")
        self.assertIn("BEFORE the trip", producer["note"])

    def test_after_midnight_and_multi_session_display(self):
        self.assertEqual(periods_text([["12:00", "24:00"]]), "12:00–00:00 (+1 day)")
        self.assertEqual(periods_text([["15:30", "26:30"]]), "15:30–02:30 (+1 day)")
        self.assertEqual(
            periods_text([["12:00", "15:00"], ["17:00", "22:30"]]),
            "12:00–15:00, 17:00–22:30",
        )
        self.assertEqual(periods_text([]), "Closed")

    def test_validation_rejects_invalid_period_and_misleading_event_hours(self):
        venue = {"id": "test-venue"}
        broken = {
            "schema_version": 1, "checked_on": "2026-10-28",
            "timezone": "Europe/London",
            "hours": {"test-venue": {
                "status": "published", "source_type": "official",
                "source_url": "https://example.com/hours", "checked_on": "2026-10-28",
                "days": {key: [] for key in ("mon", "tue", "wed", "thu", "fri", "sat", "sun")},
            }},
        }
        broken["hours"]["test-venue"]["days"]["mon"] = [["22:00", "20:00"]]
        self.assertTrue(validate_hours(broken, [venue]))
        broken["hours"]["test-venue"] = {
            "status": "event-only", "source_type": "official",
            "source_url": "https://example.com/events", "checked_on": "2026-10-28",
            "days": {}, "note": "Open on certain dates only",
        }
        self.assertTrue(validate_hours(broken, [venue]))


if __name__ == "__main__":
    unittest.main()
