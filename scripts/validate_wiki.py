#!/usr/bin/env python3
"""Check the wiki's data, evidence references and repository-local links."""

import datetime
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from build_wiki import CIDER, PRIORITY, REGIONS, render
from build_rankings import render_rankings

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    db = json.loads((ROOT / "data/venues.json").read_text())
    required = {"id", "name", "region", "area", "priority", "venue_type", "address", "why_visit", "beer", "cider_status", "cider_note", "food", "visit_notes", "transport", "tags", "source_checked", "evidence_level", "sources"}
    ids = set()
    total_source_uses = 0
    for venue in db["venues"]:
        identifier = venue.get("id", "<missing>")
        missing = required - venue.keys()
        if missing:
            errors.append(f"{identifier}: missing fields {sorted(missing)}")
            continue
        if identifier in ids or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            errors.append(f"Duplicate or invalid venue ID: {identifier}")
        ids.add(identifier)
        for field in required - {"sources", "tags"}:
            if not isinstance(venue[field], str) or not venue[field].strip():
                errors.append(f"{identifier}: empty/non-string {field}")
        for field, allowed in (("region", REGIONS), ("priority", PRIORITY), ("cider_status", CIDER), ("evidence_level", {"primary-and-specialist", "primary", "specialist"})):
            if venue[field] not in allowed:
                errors.append(f"{identifier}: invalid {field}")
        try:
            datetime.date.fromisoformat(venue["source_checked"])
        except ValueError:
            errors.append(f"{identifier}: invalid source date")
        if not venue["tags"] or len(venue["tags"]) != len(set(venue["tags"])):
            errors.append(f"{identifier}: missing or duplicate tags")
        if not venue["sources"]:
            errors.append(f"{identifier}: no sources")
        seen_urls = set()
        for source in venue["sources"]:
            total_source_uses += 1
            if not {"url", "title", "kind", "supports"} <= source.keys():
                errors.append(f"{identifier}: incomplete source")
                continue
            parsed = urlparse(source["url"])
            if parsed.scheme not in {"https", "http"} or not parsed.netloc:
                errors.append(f"{identifier}: invalid source URL {source['url']}")
            if source["url"] in seen_urls:
                errors.append(f"{identifier}: duplicate source URL")
            seen_urls.add(source["url"])
            if source["kind"] not in {"official", "camra", "heritage", "other"} or not source["supports"].strip():
                errors.append(f"{identifier}: invalid source kind/support")
    events = json.loads((ROOT / "data/events.json").read_text())
    event_ids = set()
    for event in events["events"]:
        if event["id"] in event_ids:
            errors.append(f"Duplicate event ID: {event['id']}")
        event_ids.add(event["id"])
        start, end = (datetime.date.fromisoformat(event[key]) for key in ("start_date", "end_date"))
        if start > end or start.strftime("%Y-%m") != "2026-11" or end.strftime("%Y-%m") != "2026-11":
            errors.append(f"{event['id']}: invalid November dates")
        if not event["sources"]:
            errors.append(f"{event['id']}: no sources")
    ranked = json.loads((ROOT / "data/rankings.json").read_text())
    ranked_ids = ranked.get("ranking_ids", [])
    if len(ranked_ids) != len(ids) or len(set(ranked_ids)) != len(ids) or set(ranked_ids) != ids:
        errors.append("Ranking must include every canonical venue exactly once")
    if ranked.get("trip_dates", {}).get("arrival") != "2026-11-09" or ranked.get("trip_dates", {}).get("departure") != "2026-11-14":
        errors.append("Ranking travel dates do not match supplied flights")
    ranking_path = ROOT / "wiki/rankings.md"
    if not ranking_path.exists() or ranking_path.read_text() != render_rankings():
        errors.append("Ranked guide differs from canonical ranking data")
    for event in events["events"]:
        status = event.get("trip_status")
        dates = event.get("usable_local_dates")
        if status not in {"before-arrival", "after-departure", "overlaps-but-requires-replan", "overlaps-and-fits-liverpool"} or not isinstance(dates, list):
            errors.append(f"{event['id']}: missing trip suitability classification")
            continue
        for date in dates:
            try:
                day = datetime.date.fromisoformat(date)
                if not datetime.date(2026, 11, 9) <= day <= datetime.date(2026, 11, 13) or not datetime.date.fromisoformat(event["start_date"]) <= day <= datetime.date.fromisoformat(event["end_date"]):
                    errors.append(f"{event['id']}: unusable event date {date}")
            except ValueError:
                errors.append(f"{event['id']}: invalid usable date {date}")
        if status in {"before-arrival", "after-departure"} and dates:
            errors.append(f"{event['id']}: out-of-window event cannot have usable dates")
    links_checked = 0
    for path in list(ROOT.rglob("*.md")) + [ROOT / "llms.txt"]:
        content = path.read_text()
        if re.search(r"(?:turn\d+(?:search|view)||TODO|PLACEHOLDER)", content):
            errors.append(f"{path.relative_to(ROOT)}: unresolved placeholder or chat citation")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", content):
            if urlparse(target).scheme or target.startswith("#"):
                continue
            relative = unquote(target.split("#", 1)[0])
            if relative:
                links_checked += 1
                destination = (path.parent / relative).resolve()
                if not destination.is_relative_to(ROOT) or not destination.exists():
                    errors.append(f"{path.relative_to(ROOT)}: broken local link {target}")
    sources = json.loads((ROOT / "data/sources.json").read_text())
    if sum(len(s["uses"]) for s in sources["sources"]) != total_source_uses:
        errors.append("Source-register use count does not match canonical venues")
    for relative, expected in render().items():
        path = ROOT / relative
        if not path.exists() or path.read_text() != expected:
            errors.append(f"Generated content differs: {relative}")
    actual_pages = {p.stem for p in (ROOT / "wiki/venues").glob("*.md")}
    if actual_pages != ids:
        errors.append("Venue page IDs do not exactly match canonical data")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: {len(ids)} venues, {len(sources['sources'])} distinct venue sources, {total_source_uses} evidence links, {len(event_ids)} events, {links_checked} local links; generated pages match canonical data.")
    print("Scope: internal consistency only; remote availability, stock and opening hours require live checks.")


if __name__ == "__main__":
    main()
