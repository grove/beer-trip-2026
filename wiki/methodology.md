# Scope, evidence and how to read this wiki

[Home](../README.md) · [Wiki index](index.md) · [Cider guide](real-cider.md)

## The brief

Two experienced beer travellers fly Oslo → Manchester on **Monday 9 November 2026 (MAN arrival 17:50)**, and Manchester → Oslo **Saturday 14 November (MAN departure 12:25)**. There are **five nights but only four full pub days**, Tuesday 10–Friday 13, plus Monday evening. The priorities are excellent real ale, real cider and perry, memorable traditional pubs, spectacular interiors, and good food where it strengthens the visit. The catalogue is deliberately much larger than a five-day itinerary: it is a set of worthwhile choices, not a completion challenge.

The geographical centre of gravity is Manchester/Salford and Liverpool. Nearby towns and accessible excursions are included when their beer, cider or pub experience justifies travel. A few more distant specialist trips are clearly labelled. They compete for the same limited time; they are not all additions to the default plan.

**Research cutoff: 28 October 2026.** A source-check date records when the material was researched, not a visit, a telephone confirmation, or the date on which every fact on that website was updated. Current-looking official websites and CAMRA records can still lag a closure, change of operator or kitchen timetable. No entry guarantees that a particular beer or cider will be pouring in November.

## What earns an entry

A venue must offer at least one distinctive reason for these travellers to go: a serious cask programme, convincing cider depth, exceptional surviving pub fabric, a particularly rewarding traditional local, food and beer together, or a brewery experience that adds something beyond another generic taproom. Craft-focused exceptions are included for their specific beer experience and identified as such. A heritage pub without cask is explicitly marked; an attractive room is not evidence of excellent ale.

The recommendations and route choices are editorial judgments based on the cited descriptions. They are not first-hand tasting reports. Avoid treating adjectives in venue marketing as independent quality assessments.

### Overall ranking versus priority tags

The **[complete 1–158 ranking](rankings.md)** is an **editorial relevance order**, not a firsthand beer-condition inspection, star rating or claim of precise objective differences. It prioritises documented cask and qualifying cider/perry range, distinctive heritage or brewing experiences, supported 2026 awards, food and atmosphere. Exceptional surrounding-town destinations appear high even if they **cannot all fit** into four days. The [dated schedule](five-day-plan.md) separately applies opening day, train time, flight and food-window feasibility. [data/rankings.json](../data/rankings.json) is the canonical unique-ID order, rendered with `scripts/build_rankings.py`.

### Priority labels

| Label | Meaning |
| --- | --- |
| Essential | A strong anchor for its area or specialism. An essential excursion venue does not mean the excursion itself must fit into five days. |
| High | Clearly worthwhile; choose when the area, opening pattern and your interests align. |
| Specialist | Particularly valuable for a narrower purpose: interiors, wild fermentation, a brewery visit, a rural outing or a longer detour. This is not a quality score. |

The shortlists and five-day plan make the final cut across the whole region. There is intentionally no numerical rating pretending that Victorian tiling and a cider bottle list are directly comparable.

## Evidence hierarchy

1. **Official pub, brewery, producer or event pages:** useful for the operator's present address, advertised offering, kitchen, bookings and announced dates. Promotional claims remain the operator's claims.
2. **CAMRA Pub Guide and local CAMRA branches:** useful for cask and cider detail, changes of ownership, branch awards and local updates. A branch's specific recent warning can be more informative than an older database feature badge.
3. **CAMRA Pub Heritage and statutory heritage records:** strongest for surviving interiors, listed fabric and carefully researched history. These do not establish today's beer condition or opening hours.
4. **Other reporting:** used selectively to resolve a change or supplement a gap, with the limitation stated. Search results were used to discover sources and, where full-page retrieval was limited, to inspect indexed source text. A source link is not a claim that every linked page was retrievable in full.

Each venue record includes source URLs, source types and a short statement of what each source supports. The [source register](sources.md) connects evidence back to venue pages. Descriptions are original summaries rather than copied pub-guide entries. No paywalled Good Beer Guide database or substantial source text is reproduced.

### Evidence labels

| Data value | Meaning |
| --- | --- |
| `primary-and-specialist` | Official operator evidence and specialist evidence were both used. |
| `primary` | The recommendation is principally grounded in an operator/producer source. |
| `specialist` | CAMRA, heritage or other specialist evidence carries the entry; a current operator confirmation would strengthen it. |

These labels describe provenance, not a guarantee that the venue is open. Individual practical notes take precedence over the label.

## Uncertainty is part of the record

- Cider is classified separately from beer, using the [four explicit evidence states](real-cider.md). A traditional pub, a handpump, a bag in box or an award for beer does not prove real cider.
- Beer lists describe the documented programme, not a live inventory. Regular beers and handpump counts can change; a large number of pumps is not a promise of quality or variety on the day.
- Food notes distinguish an established kitchen from snacks, occasional pop-ups and an unverified offering. Kitchen service may end well before the pub closes.
- Opening patterns and source conflicts belong in the practical notes. The wiki avoids a comprehensive timetable because the exact five dates are unknown and such a timetable would age quickly.
- Historical awards are dated wherever mentioned. A past award is useful context, not evidence of the current year's award or a future pint.
- Map links search for a verified name/address. They are conveniences, not independently verified coordinates or walking directions.
- Closed and materially unsuitable former favourites belong in [changes and exclusions](changes-and-exclusions.md), rather than appearing as ordinary recommendations.

## How to update without losing provenance

The canonical venue records are in [data/venues.json](../data/venues.json). Edit those records, retaining stable venue IDs and source support notes, then run `python3 scripts/build_wiki.py` from the repository root. This regenerates the individual venue pages, area directories, catalogue, source register and LLM index. Planning essays and routes are maintained separately.

Before promoting a venue or removing a caution, consult a current official source and the latest specialist record. Record disagreements instead of silently choosing whichever is more convenient. Do not turn "no evidence found" into "does not serve". Do not invent opening hours, tap lists, admission prices, accessibility, reservations, travel times or future events.

Run `python3 scripts/validate_wiki.py` after updates. It checks data, IDs, source URLs, local links, source-register coverage and agreement between canonical records and generated pages. It does not prove that remote websites are current or that a pub will be open when you arrive.
