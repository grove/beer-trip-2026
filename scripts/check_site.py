#!/usr/bin/env python3
"""Smoke-check the published output, including every data-driven venue page."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
output = ROOT / ".site/public"
required = (
    "index.html", "explore/index.html", "README/index.html",
    "wiki/index/index.html", "wiki/catalogue/index.html",
    "data/venues.json", "data/sources.json", "llms.txt",
    "assets/site.css", "assets/venue-finder.js",
)
missing = [path for path in required if not (output / path).is_file()]
venues = json.loads((ROOT / "data/venues.json").read_text(encoding="utf-8"))["venues"]
missing += [f"wiki/venues/{venue['id']}/index.html" for venue in venues
            if not (output / "wiki/venues" / venue["id"] / "index.html").is_file()]
if missing:
    raise SystemExit("Missing site files:\n" + "\n".join(missing))
print(f"OK: site includes search UI, full data and all {len(venues)} venue pages")
