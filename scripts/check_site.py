#!/usr/bin/env python3
"""Smoke-check the published output, including every data-driven venue page."""

import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
output = ROOT / ".site/public"
required = (
    "index.html", "explore/index.html", "map/index.html", "overview/index.html",
    "wiki/index.html", "wiki/catalogue/index.html",
    "data/venues.json", "data/sources.json", "data/map-routes.json",
    "data/opening-hours.json", "wiki/opening-hours/index.html",
    "maps/google-my-maps/all-venues.csv", "maps/google-my-maps/top-20.csv",
    "maps/google-my-maps/2026-11-09-mon-09.csv",
    "maps/google-my-maps/2026-11-10-tue-10.csv",
    "maps/google-my-maps/2026-11-11-wed-11.csv",
    "maps/google-my-maps/2026-11-12-thu-12.csv",
    "maps/google-my-maps/2026-11-13-fri-13.csv", "llms.txt",
    "assets/site.css", "assets/venue-finder.js",
    "assets/pub-map.js", "assets/pub-map.css", "assets/venue-hours.js",
)
missing = [path for path in required if not (output / path).is_file()]
venues = json.loads((ROOT / "data/venues.json").read_text(encoding="utf-8"))["venues"]
missing += [f"wiki/venues/{venue['id']}/index.html" for venue in venues
            if not (output / "wiki/venues" / venue["id"] / "index.html").is_file()]
if missing:
    raise SystemExit("Missing site files:\n" + "\n".join(missing))

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.sources.append(dict(attrs).get("src", ""))

for page, consumer in (("map/index.html", "pub-map.js"),
                       ("explore/index.html", "venue-finder.js")):
    parser = Scripts()
    parser.feed((output / page).read_text(encoding="utf-8"))
    sources = [src.rsplit("/", 1)[-1] for src in parser.sources]
    if "venue-hours.js" not in sources or consumer not in sources or \
            sources.index("venue-hours.js") > sources.index(consumer):
        raise SystemExit(f"{page}: venue-hours.js must load before {consumer}")
print(f"OK: site includes search UI, full data and all {len(venues)} venue pages")
