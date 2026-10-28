# Structured data and LLM use

[Home](../README.md) · [Methodology](../wiki/methodology.md) · [LLM index](../llms.txt)

## Files

| File | Role |
| --- | --- |
| [rankings.json](rankings.json) | Ordered unique venue IDs, trip dates, editorial methodology; generates `wiki/rankings.md` with `scripts/build_rankings.py`. |
| [venues.json](venues.json) | Canonical venue records. Object containing `schema_version`, `research_date`, `travel_month`, `scope` and a `venues` array. |
| [sources.json](sources.json) | Generated, deduplicated venue sources with stable URL-derived IDs and a list of venue claims supported. |
| [events.json](events.json) | Event dates, sources, `usable_local_dates` for flight-feasible sessions and `trip_status` indicating before/after/overlap. Times in prose are UK local. |
| [map-routes.json](map-routes.json) | Named *optional/conditional* stop sequences for Mon 9–Fri 13 November. No Saturday venue day. Drives the website's day filter and downloadable My Maps CSV layers. |

## Venue record

| Field | Meaning |
| --- | --- |
| `id` | Stable lowercase kebab-case identifier and Markdown filename. Preserve it through ordinary name/operator changes. |
| `name`, `region`, `area`, `venue_type`, `address` | Identity and practical location; `region` is `manchester`, `liverpool` or `surroundings`. A region is a directory grouping rather than an administrative boundary. |
| `cluster` | Broader editorial grouping for a readable area directory. It is not a claim that every venue is walkable from every other venue in that group. |
| `priority` | `essential`, `high` or `specialist`; interpreted in the [methodology](../wiki/methodology.md). |
| `why_visit` | Specific editorial reason the venue fits this trip. |
| `beer` | Documented beer programme and limitations; never a live tap list. |
| `cider_status`, `cider_note` | Separate cider evidence classification and explanation. See below. |
| `food` | Evidence about meals, snacks, pop-ups or the absence of established information. |
| `visit_notes`, `transport` | Opening/booking/status qualifications and useful geographical travel context. No guaranteed journey time. |
| `tags` | Descriptive discovery labels, not a substitute for reading the evidence fields. |
| `source_checked` | Date the sources were researched, not a telephone or in-person confirmation. |
| `evidence_level` | `primary-and-specialist`, `primary` or `specialist`; provenance, not a quality score. |
| `sources` | Objects with `url`, `title`, `kind` and `supports`. Kinds: `official`, `camra`, `heritage`, `other`. |

### Cider states

- `documented-real`: a source explicitly documents real cider or sufficiently specific producer/product evidence supports it. Reconfirm actual availability.
- `reported-cider-check-qualification`: cider is advertised/reported, but its real-cider qualification is unresolved, mixed, stale or contradicted. Read the note.
- `unverified`: no adequate evidence for the real-cider offering. This does not establish absence.
- `none-reported`: the cited record reports no real cider or supports an explicit negative; it is still a dated observation.

## Read and filter

```python
import json
from pathlib import Path

database = json.loads(Path("data/venues.json").read_text())
cider_candidates = [
    venue for venue in database["venues"]
    if venue["cider_status"] == "documented-real"
]
for venue in cider_candidates:
    print(venue["name"], venue["area"], venue["cider_note"])
```

An LLM should start with [llms.txt](../llms.txt), preserve every uncertainty when answering, and open the cited sources again for live recommendations. If dates are unknown, propose modular clusters rather than inventing a timetable. Use venue IDs to join records to Markdown pages. Event status and venue status are independent: a listed festival does not mean normal taproom service will be available that day.

## Rebuild and verify

From the repository root, with Python 3.9 or newer and no third-party packages:

```bash
python3 scripts/build_wiki.py
python3 scripts/build_rankings.py
python3 scripts/export_maps.py
python3 scripts/build_wiki.py --check
python3 scripts/build_rankings.py --check
python3 scripts/export_maps.py --check
python3 scripts/validate_wiki.py
```

The generators emit the ranked guide and venue pages, three area directories, alphabetical catalogue, source register and `llms.txt`. The validator checks required data and enum values, unique IDs, evidence URL structure, event date bounds, local file links, source-use coverage and generated-page agreement. It does not network-check websites or certify the truth of a recommendation. Static planning essays should be reviewed whenever a linked venue or event changes.

## Maps and geocoding

The [My Maps guide](../maps/google-my-maps/README.md) explains the seven reproducible CSV exports. They use **full addresses** in the Location column and deliberately do not pretend postcode centroids are exact premises coordinates. The [interactive map](https://grove.github.io/beer-trip-2026/map/) reads the same venue IDs, ranking and routes in the browser; postcode centroids are requested from Postcodes.io in up to 100-postcode batches and are visibly labelled approximate. Venues without usable postcodes remain searchable via their full address. Neither route-order data nor CSV export implies guaranteed opening, live beer, booking or directions times. Changes to a canonical venue's address or ID require reviewing the mapped identity and regenerated CSVs.
