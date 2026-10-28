# Manchester & Liverpool beer trip — November 2026

A source-backed LLM wiki for two experienced beer travellers spending five days in Manchester, Liverpool and their surroundings. The focus is **real ale, real cider and perry, spectacular interiors, traditional pubs and worthwhile food**. Every selected venue has a reason to visit, practical notes and traceable evidence.

**Research checked: 28 October 2026.** This is an extensive curated choice set, not a claim that every good pub has been discovered or that every venue will be open on your dates. The five-day plan selects a manageable route from the much larger catalogue.

## Coverage

| Area | Selected venues |
| --- | ---: |
| Manchester, Salford and nearby suburbs | 49 |
| Liverpool, north-coast towns and Wirral | 51 |
| Surrounding towns and selected farther excursions | 44 |
| **Total** | **144** |

The venue records cite **249 distinct source URLs**. **69 venues have documented real-cider evidence**, including explicitly occasional offers; this is not a promise of 69 daily cider selections. Seven advertised November festivals or producer openings have their own dated event records. Definitions, transport and exclusion evidence are cited separately on the planning pages.

## Start here

| What you want | Read |
| --- | --- |
| The strongest choices by interest | [Shortlists: cask, cider, interiors, food and breweries](wiki/shortlists.md) |
| A practical first itinerary | [Five-day plan, with alternatives and sensible cuts](wiki/five-day-plan.md) |
| Every researched venue | [Complete alphabetical catalogue](wiki/catalogue.md) |
| Manchester, Salford and nearby suburbs | [Manchester area directory](wiki/areas/manchester.md) |
| Liverpool, the north coast and Wirral | [Liverpool area directory](wiki/areas/liverpool.md) |
| Stockport, Chester and other worthwhile town trips | [Surrounding-area directory](wiki/areas/surroundings.md) · [Which excursion to choose](wiki/excursions.md) |
| Real cider, with the product qualifications preserved | [Cider and perry guide](wiki/real-cider.md) |
| What fits November 2026 specifically | [Festivals and sessions](wiki/november-events.md) · [Transport and logistics](wiki/logistics.md) |
| What changed or no longer deserves an old recommendation | [Changes, closures and conflicting evidence](wiki/changes-and-exclusions.md) |
| How to assess or maintain the research | [Methodology](wiki/methodology.md) · [Source register](wiki/sources.md) · [Research log](wiki/log.md) |

## The trip I would build first

Spend **two days in Manchester, one excursion day in Stockport, and two days in Liverpool**. In Manchester, start with [Marble Arch](wiki/venues/marble-arch.md), [Crown & Kettle](wiki/venues/crown-and-kettle.md), [Smithfield](wiki/venues/smithfield-market-tavern.md) and a traditional central-pub circuit. In Liverpool, build around [Roscoe Head](wiki/venues/roscoe-head.md), [Ship & Mitre](wiki/venues/ship-and-mitre.md), [Lion Tavern](wiki/venues/lion-tavern.md), [Philharmonic](wiki/venues/philharmonic-dining-rooms.md), [Peter Kavanagh’s](wiki/venues/peter-kavanaghs.md) and [The Vines](wiki/venues/vines.md).

Stockport earns its place through [Petersgate Tap](wiki/venues/petersgate-tap-stockport.md), [Arden Arms](wiki/venues/arden-arms-stockport.md), [Swan with Two Necks](wiki/venues/swan-with-two-necks-stockport.md) and [Magnet](wiki/venues/magnet-stockport.md). If cider drives the excursion choice, consider **Chester and [That Beer Place](wiki/venues/that-beer-place-chester.md)** instead. For a producer visit, investigate [Dunham Apple Barn](wiki/venues/dunham-apple-barn.md) on an actually open weekend day. These are editorial priorities, with the underlying evidence on each linked page.

The exact five dates are not yet supplied, so routes remain modular. [Published November festivals](wiki/november-events.md) may justify replacing a block. Early-November Merseyrail work and some overnight Manchester rail changes are already captured in [logistics](wiki/logistics.md).

## What a venue page contains

Each page has a verified useful address and map-search link, priority and area, a specific reason to go, documented beer provision, a separate real-cider evidence state, food notes, practical/transport context, sources and what they establish. Heritage exceptions without cask and specialist modern-beer additions are explicitly identified. Daily beer inventories, future opening promises and invented reservations are deliberately avoided.

**Essential** means a strong anchor for an area or specialism; **high** means clearly worthwhile when it fits; **specialist** identifies a narrower interest or a longer detour. The labels are not numeric quality scores. The cider field distinguishes documented real cider, reported cider requiring qualification, unverified provision and an explicit negative report. Even a positive record can describe occasional rather than daily supply.

## Use it with an LLM

Start with [llms.txt](llms.txt), then the [wiki index](wiki/index.md) and [canonical venue data](data/venues.json). Stable IDs connect structured records to individual Markdown pages; the [source register](data/sources.json) records provenance. The [data guide](data/README.md) explains the fields.

Useful follow-up requests include: "Build a three-stop Stockport afternoon around cider and lunch for our actual date"; "Compare Chester with the Wirral for cider, using only documented provision"; or "Update the opening conflicts for the venues in our five-day plan." An LLM should retain uncertainty, consult current linked sources for live facts and never turn this research snapshot into a guarantee.

## Maintain and validate

Edit `data/venues.json` and regenerate the reference pages with Python 3.9+; no third-party packages are required:

```bash
python3 scripts/build_wiki.py
python3 scripts/build_wiki.py --check
python3 scripts/validate_wiki.py
```

Validation checks data, evidence references, local links and generated-page consistency. It does not certify current opening or stock. See [AGENTS.md](AGENTS.md) for future research and update rules. The repository's existing [licence](LICENSE) is retained.
