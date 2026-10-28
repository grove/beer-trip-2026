---
title: Explore the beer map
---

# The beer-trip map

[Trip overview](../README.md) · [All 158 venue profiles](../wiki/catalogue.md) · [Actual 9–14 November itinerary](../wiki/five-day-plan.md) · [Google My Maps export instructions](../maps/google-my-maps/README.md)

See where the beer and cider stops are, filter the **158 curated venues**, and switch between the complete research catalogue and each *feasible* travel day. The pub profiles remain the authority on beer, cider qualification, food, opening caveats and sources.

**Important:** this website draws **approximate UK postcode-centre pins**, fetched from [Postcodes.io](https://postcodes.io/) when the map opens. **They are not individual building entrances.** Two venues in the catalogue have no reliable postcode and appear as address-search links instead. Open the **Google Maps** link on each card for a full street-address search and confirm the correct venue before travelling. The native map does *not* track your location or compute live transit times.

<div id="beer-map-app" class="pub-map"
  data-venues-url="../data/venues.json"
  data-routes-url="../data/map-routes.json"
  data-rankings-url="../data/rankings.json"
  data-venue-base="../wiki/venues/">
  <div class="pub-map__controls">
    <label>Search venues, drinks or neighbourhoods
      <input name="query" type="search" autocomplete="off" placeholder="Try perry, tiled, mild, Stockport…" aria-label="Search pub names and interests">
    </label>
    <label>Trip day
      <select name="day" aria-label="Choose a planned day">
        <option value="">All dates / all venues</option>
      </select>
    </label>
    <label>Region
      <select name="region" aria-label="Filter by region">
        <option value="">All regions</option>
        <option value="manchester">Manchester &amp; Salford</option>
        <option value="liverpool">Liverpool &amp; Wirral</option>
        <option value="surroundings">Surrounding towns</option>
      </select>
    </label>
    <label>Priority
      <select name="priority" aria-label="Filter by priority">
        <option value="">Any priority</option>
        <option value="essential">Essential</option>
        <option value="high">High</option>
        <option value="specialist">Specialist</option>
      </select>
    </label>
    <label>Real cider evidence
      <select name="cider" aria-label="Filter by real cider evidence">
        <option value="">Any cider status</option>
        <option value="documented-real">Real cider documented</option>
        <option value="reported-cider-check-qualification">Reported, check qualification</option>
        <option value="unverified">Unverified</option>
        <option value="none-reported">None reported</option>
      </select>
    </label>
    <label class="pub-map__top-label"><input name="top" type="checkbox">Top 20 only</label>
  </div>
  <div class="pub-map__toolbar">
    <p class="pub-map__status" role="status" aria-live="polite">Loading venue index…</p>
    <div class="pub-map__actions">
      <a class="pub-map__route" href="#" target="_blank" rel="noopener noreferrer" hidden>Open proposed walking order</a>
      <button type="button" class="pub-map__reset">Clear filters</button>
    </div>
  </div>
  <div class="pub-map__legend" aria-label="Map pin legend">
    <span><i class="pub-map__swatch pub-map__swatch--essential"></i>Essential</span>
    <span><i class="pub-map__swatch"></i>Other priorities</span>
    <span><i class="pub-map__swatch pub-map__swatch--cider"></i>Real-cider evidence</span>
  </div>
  <div class="pub-map__canvas" aria-label="Map of pubs in North West England">
    <p>Loading the interactive map…</p>
  </div>
  <p class="pub-map__hint">Pins approximate postcode centres, not exact pub entrances. Use full-address Google Maps links for travel.</p>
  <h2 class="pub-map__results-title">Venues matching your filters</h2>
  <div class="pub-map__results" aria-live="polite"></div>
  <button type="button" class="pub-map__more" hidden>Show more places</button>
  <noscript>
    <p>JavaScript is needed for map pins and filters. The full <a href="../wiki/catalogue/">venue catalogue</a> and importable Google My Maps CSVs below still work.</p>
  </noscript>
</div>

## Google My Maps: your shareable map

Unlike the website map, **Google My Maps imports the full street addresses**, resolves their location in Google Maps and lets you share the resulting map from your own Google account. The exported CSV includes a short reason to visit, 2026 ranking, beer and cider caveats, and direct wiki/profile links.

- **[Download all 158 venues (CSV)](../maps/google-my-maps/all-venues.csv)** — use this as the main geographical layer, styled by priority.
- **[Download the top 20 (CSV)](../maps/google-my-maps/top-20.csv)** — a quick low-clutter overview.
- **[Monday arrival](../maps/google-my-maps/2026-11-09-mon-09.csv)** · **[Tuesday Manchester](../maps/google-my-maps/2026-11-10-tue-10.csv)** · **[Wednesday Stockport](../maps/google-my-maps/2026-11-11-wed-11.csv)** · **[Thursday Liverpool](../maps/google-my-maps/2026-11-12-thu-12.csv)** · **[Friday Liverpool](../maps/google-my-maps/2026-11-13-fri-13.csv)** — small, ordered, flight-aware day layers; **no Saturday pub crawl**.

Read the **[step-by-step My Maps import and sharing guide](../maps/google-my-maps/README.md)**. Importing into a Google account and publishing/sharing the resulting map is a separate manual action; these downloadable files do **not** claim a public My Maps map has already been created.

### What the route filter means

Selecting Tuesday, Wednesday or another day shows the *planned stop order*, not an optimised walking route or guaranteed opening. The **Open proposed walking order** link sends the stops to Google Maps for walking directions using their full addresses. If you change the day or swap a pub, re-check the route and opening hours. The [dated itinerary](../wiki/five-day-plan.md) contains alternatives and essential flight/rail warnings that deliberately do not all appear as additional pins.

**Map data and privacy:** venue names/addresses, ranks and plan come from the repository. Postcode lookup uses two small batches from [Postcodes.io](https://postcodes.io/docs/postcode/bulk/) in a typical uncached session; results are cached in session storage for up to 30 days. Basemap tiles load from OpenStreetMap only for the map area you view, with required attribution. No precise user location is requested. If a mapping provider is unavailable, the venue list and individual Google Maps links remain usable. [OpenStreetMap copyright](https://www.openstreetmap.org/copyright).
