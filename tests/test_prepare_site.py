"""Small regression tests for growing the venue wiki without hand-editing nav."""

import json
import tempfile
import unittest
from pathlib import Path
from sys import path

path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from prepare_site import FEATURED, alphabetical_bucket, navigation, prepare  # noqa: E402


class SitePreparationTests(unittest.TestCase):
    def test_alphabetical_groups_ignore_leading_articles(self):
        self.assertEqual(alphabetical_bucket("The Marble Arch"), "M–R")
        self.assertEqual(alphabetical_bucket("Ye Cracke"), "S–Z")
        self.assertEqual(alphabetical_bucket("A Baltic Fleet"), "A–F")

    def test_new_venues_and_editorial_pages_join_navigation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "wiki/venues").mkdir(parents=True)
            (root / "wiki/areas").mkdir(parents=True)
            (root / "data").mkdir()
            for entries in FEATURED.values():
                for _, filename in entries:
                    dest = root / filename
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text("# Example\n")
            for filename in ("README.md", "overview.md", "explore.md", "wiki/catalogue.md",
                             "wiki/areas/manchester.md", "wiki/venues/new-pub.md",
                             "wiki/new-topic.md"):
                dest = root / filename
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text("# Example\n")
            nav = navigation(root, [{"id": "new-pub", "name": "The New Pub", "region": "manchester"}])
            text = json.dumps(nav, ensure_ascii=False)
            self.assertIn("wiki/venues/new-pub.md", text)
            self.assertIn("wiki/new-topic.md", text)
            self.assertIn("More articles", text)
            self.assertIn("M–R", text)

    def test_staging_does_not_modify_canonical_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for directory in ("website/assets", "wiki/venues", "wiki/areas", "data",
                              "maps/google-my-maps"):
                (root / directory).mkdir(parents=True)
            for filename in ("README.md", "AGENTS.md", "LICENSE", "llms.txt",
                             "website/mkdocs.yml", "website/explore.md", "website/map.md",
                             "maps/google-my-maps/all-venues.csv", "website/assets/pub-map.js",
                             "website/assets/pub-map.css", "website/assets/site.css",
                             "website/assets/venue-finder.js", "wiki/venues/new-pub.md"):
                (root / filename).write_text("original content\n")
            (root / "website/index.md").write_text("{{VENUE_COUNT}} / {{SOURCE_COUNT}} / {{RESEARCH_DATE}}\n")
            (root / "data/venues.json").write_text(json.dumps({"research_date": "2026-10-28", "venues": []}))
            (root / "data/sources.json").write_text(json.dumps({"sources": []}))
            for entries in FEATURED.values():
                for _, filename in entries:
                    dest = root / filename
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text("# Example\n")
            (root / "wiki/catalogue.md").write_text("# Catalogue\n")
            original = (root / "wiki/venues/new-pub.md").read_bytes()
            prepare(root)
            self.assertEqual((root / "wiki/venues/new-pub.md").read_bytes(), original)
            self.assertEqual((root / ".site/docs/wiki/venues/new-pub.md").read_bytes(), original)
            self.assertIn("0 / 0 / 28 October 2026", (root / ".site/docs/README.md").read_text())
            self.assertEqual((root / ".site/docs/overview.md").read_text(), "original content\n")
            self.assertEqual((root / ".site/docs/map.md").read_text(), "original content\n")
            self.assertEqual((root / ".site/docs/maps/google-my-maps/all-venues.csv").read_text(),
                             "original content\n")


if __name__ == "__main__":
    unittest.main()
