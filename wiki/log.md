# Research and maintenance log

[Home](../README.md) · [Methodology](methodology.md) · [Source register](sources.md)

## 2026-10-28 — brewery and cider leads for each of 158 venues

Added a source-linked [all-venue beer and cider guide](drinks-by-venue.md) with the existing independent beer/cider evidence on each of the 158 records, supplementing that with **56 specific beer/producer research leads** and **11 additional cider/perry leads**. The named examples distinguish operator/CAMRA regulars, rotating suppliers, seasonal exceptions and recently spotted beers; the guide gives a shorter version for the travel-feasible 9–13 November route. Research uses dated CAMRA/branch listings, existing operator sources and a clearly identified changing public menu snapshot.

Retained the canonical venue status, cider evidence classifications and the independent opening-hours dataset. A named beer or cider producer is not a November stock guarantee, and the particular cider product still needs qualification against current CAMRA rules. No venues were contacted and no bookings or purchases were made.


## 2026-10-28 — published opening hours for all 158 venues

Researched ordinary published *bar* opening schedules for **157 venues**, from the linked CAMRA pub guide/local branch or official operator pages, and retained **’Udders Orchard as event-only** (published November 7–8 producer dates are before arrival). Recorded source URL, source type, date (28 October 2026), seven local weekdays, exceptional midnight crossover and separate kitchen hours where independently published in [data/opening-hours.json](../data/opening-hours.json). This is **not** live trading verification or guaranteed November 9–13 opening; an empty published weekday means source-listed closed for an ordinary week, while missing food times mean *unverified*, not no meals.

Regenerated **all 158 individual venue pages** with source-linked bar-hours tables, separate kitchen tables where documented, and qualifications; added the [9–13 November comparison](opening-hours.md) for quick route decisions. Updated the [venue finder](https://grove.github.io/beer-trip-2026/explore/) and the [interactive map](https://grove.github.io/beer-trip-2026/map/) with source-aware daily hours; the finder can filter by source-listed weekdays (never claiming "open now"). All seven [Google My Maps CSVs](../maps/google-my-maps/README.md) now include Monday–Sunday bar hours and an Hours source URL. Built a formatter/schema validator and tests to preserve date, timezone, closed/event-only distinction, overlapping periods, and after-midnight notation.

**Important checks:** Marble Arch's *official* Tuesday closure supersedes the CAMRA conflict; its Monday kitchen last-order timing is separate from bar opening. Track, Runaway and other taprooms have limited service, and campus, older guide and seasonal schedules may change. Roscoe Head's September sale announcement is not a closure notice. Users must recheck venue/bar and kitchen sessions directly before visiting. No venue contacted; no reservation or beer-stock claims.

## 2026-10-28 — geographical companion and shareable Google My Maps exports

Added a route-aware [interactive map](https://grove.github.io/beer-trip-2026/map/), plus [downloadable Google My Maps CSV layers](../maps/google-my-maps/README.md) for all 158 venues, the top 20 and each of the five flight-feasible Mon–Fri visit days. Added deterministic `scripts/export_maps.py` and `data/map-routes.json`, with rank/venue/route integrity checks. The route sequences are *options*, never compulsory stops or promises of opening. Saturday 14 is still airport-only. The native map exposes priority, region, cider status, text search and day filters, plus detailed wiki links and **full-address** Google Maps directions.

The native map has **no independently verified pub-entrance coordinates**: Postcodes.io provides approximate UK *postcode centroids* for up to 156 entries in two batches; two postcode-less addresses remain accessible through exact-address search links. Pins explicitly warn not to use them as navigation endpoints. Google My Maps imports the full venue-name-and-address query and users must inspect geocoding before sharing. The browser falls back to the complete venue list if a map, postcode or CDN request fails; no published shared Google map, personal GPS tracking, reservation or live stock check is claimed.

## 2026-10-28 — deeper pub stories and a drinker's field guide

Added four fully sourced editorial companions: [Manchester](stories-manchester.md) (Marble Arch's Shap granite, tiled drink list and folklore, Peveril road rescue and Cracker appearance, historic serving arrangements), [Stockport and excursions](stories-stockport-and-excursions.md) (Raffald family, Robinsons' 1899 Old Tom story and the **7 November 2026 cask launch at Arden Arms and Swan**, plus perry/cider cellar leads), [Liverpool](stories-liverpool.md) (Cain/Thomas architectural rivalry, Lion locomotive, Bridewell cells, Dickens-and-Hogarth interiors) and [What to drink](what-to-drink.md) (named dated beer candidates, tasting passport, style and condition cues, precise real-cider/perry qualification questions).

Added a **new September 2026 CAMRA report that Roscoe Head is up for sale** after the licensee decided to retire, with an explicit distinction between a **sale** and a closure. Linked the caveat from the itinerary, shortlists and changes register. These new articles supplement the canonical 158-venue dataset and **do not replace or regenerate venue records**. Primary sources include Historic England listing/walks, Robinsons and Marble breweries, and dated CAMRA records and awards. Original prose separates documented anecdotes from pub lore, current source assertions from November stock guesses, and optionals from the four-day itinerary. No bookings or on-site verification.

**Maintenance:** The site navigation, wiki index, README, existing beer/cider guides and homepage have crosslinks to the new articles. The generated canonical venue content and source register remain untouched. Validate internal links and site build; cited external pages remain independent and can change.

## 2026-10-28 — exact flights, 2026 awards, ranking and revised programme

The travellers supplied flight confirmations: **DY1348 Mon 9 November OSL 16:45 → MAN 17:50** and **SK4608 Sat 14 November MAN 12:25 → OSL 15:25** (local times). This is five nights, **four full days**. Replaced the initial generic itinerary and logistics with local-time dated hour blocks, airport buffers, Wednesday Stockport visit, Thursday/Friday Liverpool, and a recommended Manchester final night to protect Saturday’s flight. Added festival filter, now identifying only November 12–13 as usable session days; confirmed published late-night rail engineering 9–12 November.

**Expanded the curated catalogue from 144 to 158 venues**: 51 Manchester, 57 Liverpool/north coast/Wirral and 50 surrounding towns. Canonical data now links **269 distinct venue-source URLs with 277 evidence uses**; **77 venues** have documented real-cider evidence, including occasional supply. Fourteen researched new entries feature Fox & Pine, Our Gracie’s, The Coop, B33R@33, Bank Top Ale House, Broad Street Social, Fell Northern Quarter and other worthwhile local destinations, with award-year checks. Added **[rankings.md](rankings.md)** and the canonical [data/rankings.json](../data/rankings.json), with a reproducible generator and integrity check. The overall order is editorial, **not a firsthand pub-quality score**.

Corrected Marble Arch's Tuesday closure and Monday food cutoff in the route; warned about the temporary closure of Sir Ralph Abercromby. Events before arrival/after departure are explicitly excluded. All checks are of desk-research records **as of 28 October**, not venue confirmation, live inventory or booked tickets.

## 2026-10-28 — initial November trip wiki

Created a repository-native Markdown wiki for a five-day Manchester–Liverpool trip, prioritising cask/real ale, real cider/perry, memorable traditional pubs, spectacular interiors and useful food. Research covered the two city regions and selectively chosen surrounding towns in parallel, followed by cross-review of the recommendations and travel facts.

The initial snapshot contains **144 venues**: 49 Manchester-region, 51 Liverpool-region and 44 surrounding-area records. It links to **249 distinct venue-source URLs** through 252 evidence references. There are 69 documented-real-cider records, including explicitly occasional provision, and seven dated November event/opening records. The completed initial validation checked 2,038 local file links and found the generated pages consistent with their canonical records.

The canonical venue database produces individual pages, grouped area directories, an alphabetical catalogue, a deduplicated source register and `llms.txt`. Editorial pages provide theme shortlists, a five-day plan, excursion tradeoffs, cider guidance, November events, practical logistics and a record of closures/conflicts. The original repository licence is retained.

### Decisions preserved

- Every included venue has a specific reason to visit; craft or heritage-only exceptions state what earns them a place.
- Cider evidence is separate from cask evidence. Generic cider wording, box/handpump format and historical reputation do not prove qualifying current products.
- Positive cider evidence can still mean occasional supply. Individual notes take precedence over a simplified filter.
- Operator and specialist sources are identified separately. Date-specific events are not inferred from a previous year's calendar or a recurring weekday pattern.
- Closed or materially unsuitable former favourites are recorded separately, including Caledonia, Vale Inn, Sip Club, Railway Portwood, Treacle Tap and the current Bear & Billet situation.
- Recent reopening or relocation evidence is preserved for Crown Stockport, Britons Protection, Vines, Pen Factory, Ye Cracke, Beacon and Runaway.
- A final coverage review added St Helens, Newton-le-Willows, Warrington, Rivington and New Mills, plus recent Liverpool conversions and Manchester food/brewery options. Robinsons' discontinued tours and Torrside's unconfirmed November brewery-tap availability are preserved as qualifications rather than active tour recommendations.
- The default route is two Manchester days, Stockport and two Liverpool days. Other towns and festivals are alternatives, not extra compulsory days.
- Published early-November Merseyrail works and selected overnight Manchester changes are linked to official notices.

### Verification

The checked-in validation scripts verify data fields, ID uniqueness, source URL structure, source-register coverage, event dates, repository-local links and agreement between canonical data and generated pages. Research cross-review focused on closure traps, cider contradictions, room/beer distinctions and date-specific transport/event claims. These checks are not an onsite quality assessment or a live availability guarantee.

### Still dependent on the travellers' dates

The exact five days, arrival/departure stations or airports, hotel locations and meal preferences were not supplied. Once known, assign the route blocks to days, check the actual anchors, reserve any important meals and inspect festival/session availability. No contact with venues, reservations or ticket purchases was made during creation of this wiki.

For later updates, add a new dated section explaining what evidence changed and which recommendations, routes or caveats were affected. Keep the previous history rather than silently rewriting a past check date.
