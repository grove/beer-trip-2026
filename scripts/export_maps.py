#!/usr/bin/env python3
"""Build deterministic Google My Maps CSV layers from the canonical beer-trip data.

Google My Maps resolves the Location column from a pub name + street address.
No imprecise postcode-centroid coordinates are exported as exact venue locations.
"""

import argparse
import csv
import io
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DEST = Path("maps/google-my-maps")
SITE = "https://grove.github.io/beer-trip-2026/"
HEADERS = (
    "ID", "Name", "Location", "Address", "Area", "Region", "Rank",
    "Priority", "Real cider evidence", "Why visit", "Beer",
    "Cider and perry", "Food", "Visit date (UK)", "Stop order",
    "Visit role", "Visit note", "Wiki profile", "Google Maps",
)
CIDER = {
    "documented-real": "Real cider documented; check product and stock",
    "reported-cider-check-qualification": "Cider reported; real-cider qualification unresolved",
    "unverified": "Real cider not established",
    "none-reported": "No real cider reported by dated evidence",
}


def load():
    venues = json.loads((ROOT / "data/venues.json").read_text(encoding="utf-8"))["venues"]
    ranking = json.loads((ROOT / "data/rankings.json").read_text(encoding="utf-8"))["ranking_ids"]
    plan = json.loads((ROOT / "data/map-routes.json").read_text(encoding="utf-8"))
    by_id = {v["id"]: v for v in venues}
    if len(by_id) != len(venues) or len(ranking) != len(venues) or set(ranking) != set(by_id) or len(set(ranking)) != len(ranking):
        raise ValueError("Venue IDs and ranking must have a one-to-one correspondence")
    if plan["trip_dates"] != {"arrival": "2026-11-09", "departure": "2026-11-14"}:
        raise ValueError("Route dates must match the actual flights")
    if not plan["routes"] or len({r["id"] for r in plan["routes"]}) != len(plan["routes"]):
        raise ValueError("Duplicate or missing route identifiers")
    dates = set()
    used = set()
    for route in plan["routes"]:
        date = route["date"]
        if date in dates or not "2026-11-09" <= date <= "2026-11-13":
            raise ValueError("Routes must be unique within the feasible trip dates")
        dates.add(date)
        if not route["stops"]:
            raise ValueError("Route without stops: " + route["id"])
        seen = set()
        for stop in route["stops"]:
            key = stop["venue_id"]
            if key not in by_id or key in seen or key in used:
                raise ValueError("Unknown or repeated map stop: " + key)
            seen.add(key)
            used.add(key)
            if stop["role"] not in {"anchor", "lunch", "optional", "conditional"}:
                raise ValueError("Invalid route role: " + key)
    return by_id, ranking, plan


def compact(text, limit=250):
    """Single-line prose to keep My Maps popups usable; never guess new facts."""
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[:limit - 1].rsplit(" ", 1)[0].rstrip(" .,;") + "…"


def maps_url(venue):
    query = venue["name"] + ", " + venue["address"] + ", United Kingdom"
    return "https://www.google.com/maps/search/?api=1&query=" + quote(query, safe="")


def row(venue, rank, stop_info=None):
    date, order, role, note = stop_info if stop_info else ("", "", "", "")
    # Name + full address reduces ambiguous searches like "Marble Arch" (London).
    location = venue["name"] + ", " + venue["address"] + ", United Kingdom"
    return (
        venue["id"], venue["name"], location, venue["address"], venue["area"],
        venue["region"], rank, venue["priority"], CIDER[venue["cider_status"]],
        compact(venue["why_visit"]), compact(venue["beer"], 180),
        compact(venue["cider_note"], 180), compact(venue["food"], 180),
        date, order, role, compact(note, 180),
        SITE + "wiki/venues/" + venue["id"] + "/", maps_url(venue),
    )


def csv_text(rows):
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADERS)
    writer.writerows(rows)
    return buffer.getvalue()


def outputs():
    by_id, ranking, plan = load()
    order = {key: i + 1 for i, key in enumerate(ranking)}
    in_routes = {
        stop["venue_id"]: (route["date"], index, stop["role"], stop["note"])
        for route in plan["routes"]
        for index, stop in enumerate(route["stops"], 1)
    }
    files = {
        DEST / "all-venues.csv": csv_text(
            row(by_id[key], order[key], in_routes.get(key)) for key in ranking
        ),
        DEST / "top-20.csv": csv_text(
            row(by_id[key], order[key], in_routes.get(key)) for key in ranking[:20]
        ),
    }
    for route in plan["routes"]:
        files[DEST / (route["date"] + "-" + route["id"] + ".csv")] = csv_text(
            row(by_id[s["venue_id"]], order[s["venue_id"]],
                (route["date"], i, s["role"], s["note"]))
            for i, s in enumerate(route["stops"], 1)
        )
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on missing or stale exports")
    args = parser.parse_args()
    rendered = outputs()
    missing = []
    for relative, content in rendered.items():
        destination = ROOT / relative
        if not destination.exists() or destination.read_text(encoding="utf-8") != content:
            missing.append(str(relative))
            if not args.check:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(content, encoding="utf-8", newline="")
    if args.check and missing:
        raise SystemExit("Map exports need regenerating:\n" + "\n".join(missing))
    print(f"{'Checked' if args.check else 'Generated'} {len(rendered)} My Maps CSV layers; {len(missing)} {'stale' if args.check else 'written'}.")


if __name__ == "__main__":
    main()
