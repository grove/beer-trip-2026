"""Format the independently sourced, ordinary UK pub opening-hours dataset.

The source snapshot is NOT a live calendar. A missing entry is unknown, not closed.
Values beyond 24:00 represent closing after midnight on the following day.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
DAY_LABELS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
TIME = re.compile(r"^(?:[01]\d|2[0-6]):[0-5]\d$")


def load_hours(root=ROOT):
    return json.loads((root / "data/opening-hours.json").read_text(encoding="utf-8"))


def clock(value):
    """Display next-day closing times without hiding the day rollover."""
    hour, minute = map(int, value.split(":"))
    if hour >= 24:
        return f"{hour - 24:02d}:{minute:02d} (+1 day)"
    return value


def periods_text(periods):
    if not periods:
        return "Closed"
    return ", ".join(f"{clock(start)}–{clock(end)}" for start, end in periods)


def compact_hours(entry, day):
    """Short labels for week-at-a-glance tables and mobile lists."""
    if not entry:
        return "Not verified"
    if entry["status"] == "event-only":
        return "Event-only"
    return periods_text(entry["days"][day])


def section_lines(entry):
    """Insert in every generated venue page, even for missing evidence."""
    lines = ["## Published opening hours", ""]
    if entry is None:
        lines += [
            "**Not verified.** No dependable ordinary weekly opening schedule is held "
            "in this research snapshot. This does not mean the venue is closed.",
            "",
            "Check directly before travelling; a CAMRA listing or old itinerary "
            "does not guarantee that the doors will be open.",
            "",
        ]
        return lines

    source_name = "Operator" if entry["source_type"] == "official" else "CAMRA / local branch"
    if entry["status"] == "event-only":
        lines += [
            "**Event-only — no regular weekly bar schedule.** "
            + entry["note"],
            "",
            f"**Source:** [{source_name}]({entry['source_url']}) "
            f"(researched {entry['checked_on']}).",
            "",
            "A special opening is not an ordinary Monday–Sunday schedule. "
            "Confirm new events with the organiser.",
            "",
        ]
        return lines

    has_food = "food_days" in entry
    lines += [
        "**Ordinary published bar hours**, UK local time (Europe/London). "
        "These are **not confirmed November 2026 session hours**. "
        "Closing times after midnight are marked (+1 day).",
        "",
        "| Day | Bar |" + (" Food / kitchen |" if has_food else ""),
        "| --- | --- |" + (" --- |" if has_food else ""),
    ]
    for day, label in zip(DAYS, DAY_LABELS):
        bar = periods_text(entry["days"][day])
        if has_food:
            food = periods_text(entry["food_days"][day])
            lines.append(f"| {label} | {bar} | {food} |")
        else:
            lines.append(f"| {label} | {bar} |")
    lines += [
        "",
        f"**Hours source:** [{source_name}]({entry['source_url']}) "
        f"(checked {entry['checked_on']}). "
        + ("Kitchen times are independently listed above; "
           "confirm menu and last food orders. " if has_food else
           "Specific kitchen hours were not sufficiently established; "
           "see [food notes](#food). ")
        + "Ordinary opening, last orders and holiday/event hours may differ.",
        "",
    ]
    if entry.get("note"):
        lines += ["**Important qualification:** " + entry["note"], ""]
    return lines


def validate_hours(db, venues):
    """Return explicit provenance/shape errors; do not silently repair hours."""
    errors = []
    if db.get("schema_version") != 1 or db.get("timezone") != "Europe/London":
        errors.append("Opening-hours schema or timezone mismatch")
    if db.get("checked_on") != "2026-10-28":
        errors.append("Opening-hours research date must match this edition")
    records = db.get("hours", {})
    ids = {v["id"] for v in venues}
    if set(records) - ids:
        errors.append("Opening-hours records reference unknown venues: " +
                      ", ".join(sorted(set(records) - ids)))
    for venue_id, entry in records.items():
        status = entry.get("status")
        if status not in {"published", "event-only"}:
            errors.append(f"{venue_id}: invalid opening-hours status")
            continue
        if entry.get("source_type") not in {"camra", "official"}:
            errors.append(f"{venue_id}: missing source type")
        if not entry.get("source_url", "").startswith("https://"):
            errors.append(f"{venue_id}: missing HTTPS opening-hours source")
        if entry.get("checked_on") != db.get("checked_on"):
            errors.append(f"{venue_id}: inconsistent research date")
        if status == "event-only":
            if "days" in entry or "food_days" in entry or not entry.get("note"):
                errors.append(f"{venue_id}: event-only cannot imply regular hours")
            continue
        days = entry.get("days")
        if not isinstance(days, dict) or set(days) != set(DAYS):
            errors.append(f"{venue_id}: missing bar day(s)")
            continue
        if "food_days" in entry and (
                not isinstance(entry["food_days"], dict) or
                set(entry["food_days"]) != set(DAYS)):
            errors.append(f"{venue_id}: missing kitchen day(s)")
            continue
        for category in ("days", "food_days"):
            if category not in entry:
                continue
            for day, periods in entry[category].items():
                if not isinstance(periods, list):
                    errors.append(f"{venue_id}: non-list {category} {day}")
                    continue
                previous_end = -1
                for pair in periods:
                    if (not isinstance(pair, list) or len(pair) != 2 or
                            any(not isinstance(t, str) or not TIME.fullmatch(t)
                                for t in pair)):
                        errors.append(f"{venue_id}: invalid time interval {category} {day}")
                        continue
                    start, end = pair
                    a = int(start[:2]) * 60 + int(start[3:])
                    b = int(end[:2]) * 60 + int(end[3:])
                    if a >= b or a < previous_end or a >= 24 * 60:
                        errors.append(f"{venue_id}: unordered/invalid {category} {day}: {pair}")
                    previous_end = b
    return errors
