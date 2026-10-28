#!/usr/bin/env python3
"""Stage the existing LLM wiki for the website without changing source files.

The generated nav is based on canonical venue records and discovered Markdown,
so future additions do not require maintaining a second table of contents.
"""

import datetime
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGIONS = {
    "manchester": "Manchester & Salford",
    "liverpool": "Liverpool & Wirral",
    "surroundings": "Surrounding towns",
}
FEATURED = {
    "Plan the trip": [
        ("Trip overview", "overview.md"),
        ("Interactive venue map", "map.md"),
        ("Curated shortlists", "wiki/shortlists.md"),
        ("Five-day itinerary", "wiki/five-day-plan.md"),
        ("Choosing an excursion", "wiki/excursions.md"),
        ("November events", "wiki/november-events.md"),
        ("Getting around", "wiki/logistics.md"),
    ],
    "The beer guide": [
        ("Real cider & perry", "wiki/real-cider.md"),
        ("Beer & pub culture", "wiki/beer-and-pub-culture.md"),
        ("What to drink: cask & cider", "wiki/what-to-drink.md"),
        ("Manchester pub stories", "wiki/stories-manchester.md"),
        ("Stockport & excursion stories", "wiki/stories-stockport-and-excursions.md"),
        ("Liverpool pub stories", "wiki/stories-liverpool.md"),
    ],
    "Research & sources": [
        ("How we research", "wiki/methodology.md"),
        ("Closures & changes", "wiki/changes-and-exclusions.md"),
        ("Venue source register", "wiki/sources.md"),
        ("Research log", "wiki/log.md"),
        ("Wiki index", "wiki/index.md"),
        ("Structured data guide", "data/README.md"),
        ("Maintainer instructions", "AGENTS.md"),
    ],
}
BUCKETS = ("A–F", "G–L", "M–R", "S–Z", "Other")


def alphabetical_bucket(name):
    """Group names ignoring a leading article, while keeping display names intact."""
    significant = re.sub(r"^(the|a|an)\s+", "", name.strip(), flags=re.I)
    initial = significant[:1].upper()
    for low, high, label in (("A", "F", "A–F"), ("G", "L", "G–L"),
                              ("M", "R", "M–R"), ("S", "Z", "S–Z")):
        if low <= initial <= high:
            return label
    return "Other"


def navigation(docs, venues):
    """Build a nav that includes every Markdown page, even future editorial pages."""
    included = set()

    def item(label, path):
        if not (docs / path).is_file():
            raise ValueError(f"Missing navigation target: {path}")
        if path in included:
            raise ValueError(f"Duplicate navigation target: {path}")
        included.add(path)
        return {label: path}

    nav = [item("Home", "README.md")]
    nav.append({"Plan the trip": [item(label, path) for label, path in FEATURED["Plan the trip"]]})

    explore = [item("Find a venue", "explore.md")]
    area_paths = sorted((docs / "wiki/areas").glob("*.md"))
    area_paths.sort(key=lambda p: (list(REGIONS).index(p.stem) if p.stem in REGIONS else len(REGIONS), p.stem))
    explore.append({"Area directories": [item(REGIONS.get(p.stem, p.stem.replace("-", " ").title()),
                                               p.relative_to(docs).as_posix()) for p in area_paths]})
    explore.append(item("Complete venue catalogue", "wiki/catalogue.md"))

    by_region = defaultdict(list)
    ids = set()
    for venue in venues:
        identifier = venue["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            raise ValueError(f"Invalid venue ID: {identifier}")
        if identifier in ids:
            raise ValueError(f"Duplicate venue ID: {identifier}")
        ids.add(identifier)
        by_region[venue["region"]].append(venue)

    groups = []
    region_order = list(REGIONS) + sorted(set(by_region) - set(REGIONS))
    for region in region_order:
        selected = by_region.get(region, [])
        if not selected:
            continue
        buckets = defaultdict(list)
        for venue in sorted(selected, key=lambda v: v["name"].casefold()):
            buckets[alphabetical_bucket(venue["name"])].append(
                item(venue["name"], f"wiki/venues/{venue['id']}.md")
            )
        groups.append({f"{REGIONS.get(region, region.title())} ({len(selected)})": [
            {letter: buckets[letter]} for letter in BUCKETS if buckets[letter]
        ]})
    explore.append({"Browse venues by region & name": groups})
    nav.append({"Explore places": explore})

    for section in ("The beer guide", "Research & sources"):
        nav.append({section: [item(label, path) for label, path in FEATURED[section]]})

    remaining = sorted(p.relative_to(docs).as_posix() for p in docs.rglob("*.md")
                       if p.relative_to(docs).as_posix() not in included)
    if remaining:
        nav.append({"More articles": [item(p.rsplit("/", 1)[-1][:-3].replace("-", " ").title(), p)
                                      for p in remaining]})
    return nav


def site_template(root, name):
    """Resolve website-only links in staging, leaving the source wiki untouched."""
    text = (root / "website" / name).read_text(encoding="utf-8")
    return (text.replace("](../wiki/", "](wiki/")
                .replace("](../maps/", "](maps/")
                .replace("](../README.md)", "](overview.md)"))


def prepare(root=ROOT):
    stage = root / ".site"
    docs = stage / "docs"
    if stage.exists():
        shutil.rmtree(stage)
    docs.mkdir(parents=True)
    shutil.copytree(root / "wiki", docs / "wiki")
    shutil.copytree(root / "data", docs / "data")
    if (root / "maps").is_dir():
        shutil.copytree(root / "maps", docs / "maps")
    shutil.copytree(root / "website/assets", docs / "assets")
    for path in ("AGENTS.md", "LICENSE", "llms.txt"):
        shutil.copy2(root / path, docs / path)
    shutil.copy2(root / "README.md", docs / "overview.md")
    (docs / "explore.md").write_text(site_template(root, "explore.md"), encoding="utf-8")
    (docs / "map.md").write_text(site_template(root, "map.md"), encoding="utf-8")

    venues_db = json.loads((root / "data/venues.json").read_text(encoding="utf-8"))
    source_db = json.loads((root / "data/sources.json").read_text(encoding="utf-8"))
    research_date = datetime.date.fromisoformat(venues_db["research_date"])
    substitutions = {
        "{{VENUE_COUNT}}": str(len(venues_db["venues"])),
        "{{SOURCE_COUNT}}": str(len(source_db["sources"])),
        "{{RESEARCH_DATE}}": f"{research_date.day} {research_date:%B %Y}",
    }
    landing = site_template(root, "index.md")
    for token, value in substitutions.items():
        landing = landing.replace(token, value)
    (docs / "README.md").write_text(landing, encoding="utf-8")

    nav = navigation(docs, venues_db["venues"])
    config = (root / "website/mkdocs.yml").read_text(encoding="utf-8").rstrip()
    # JSON is valid YAML flow syntax. No additional dependency for generating config.
    (stage / "mkdocs.yml").write_text(
        config + "\n\nnav: " + json.dumps(nav, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Staged {len(venues_db['venues'])} venues and "
          f"{len(list(docs.rglob('*.md')))} Markdown pages; generated navigation in .site/mkdocs.yml")
    return stage


if __name__ == "__main__":
    prepare()
