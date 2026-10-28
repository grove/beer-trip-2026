---
title: Explore venues
---

# Find somewhere worth the journey

Prefer pins and a route filter? Open the **[interactive beer-trip map](map.md)**. It also provides **Google My Maps CSV downloads** for all 158 venues and each planned day.

Search the entire curated collection by venue, neighbourhood, speciality or description. Filter by location, priority and **cider evidence**, not an assumed current tap list. Each result leads to a sourced record with food and travel notes.

<div id="venue-finder" class="venue-finder" data-venues-url="../data/venues.json" data-opening-hours-url="../data/opening-hours.json" data-venue-base="../wiki/venues/">
  <div class="venue-finder__controls">
    <label>Search venues
      <input type="search" name="query" placeholder="Try tiled interiors, perry, Stockport…" autocomplete="off" aria-label="Search venues">
    </label>
    <label>Region
      <select name="region" aria-label="Filter by region"><option value="">All regions</option></select>
    </label>
    <label>Priority
      <select name="priority" aria-label="Filter by priority">
        <option value="">Any priority</option>
        <option value="essential">Essential</option>
        <option value="high">High</option>
        <option value="specialist">Specialist</option>
      </select>
    </label>
    <label>Day (published bar hours)
      <select name="day" aria-label="Choose a day to inspect published opening hours">
        <option value="">Choose any day</option>
        <option value="mon">Monday</option>
        <option value="tue">Tuesday</option>
        <option value="wed">Wednesday</option>
        <option value="thu">Thursday</option>
        <option value="fri">Friday</option>
        <option value="sat">Saturday</option>
        <option value="sun">Sunday</option>
      </select>
    </label>
    <label class="venue-finder__only-open"><input type="checkbox" name="onlyOpen" disabled> Only venues listing bar service that day</label>
    <label>Cider evidence
      <select name="cider" aria-label="Filter by cider evidence">
        <option value="">Any status</option>
        <option value="documented-real">Documented real cider</option>
        <option value="reported-cider-check-qualification">Reported, needs checking</option>
        <option value="unverified">Not established</option>
        <option value="none-reported">No real cider reported</option>
      </select>
    </label>
  </div>
  <div class="venue-finder__toolbar">
    <p class="venue-finder__status" role="status" aria-live="polite">Loading the venue directory…</p>
    <button class="venue-finder__reset" type="button">Clear filters</button>
  </div>
  <div class="venue-finder__results"></div>
  <button class="venue-finder__more" type="button" hidden>Show more places</button>
  <noscript>JavaScript is needed for filtering. You can still browse the <a href="../wiki/catalogue/">full alphabetical catalogue</a>.</noscript>
</div>

**New:** Select a weekday to see the **published ordinary bar schedule** for each venue. Tick **Only venues listing bar service that day** to filter, but **do not treat this as a live open-now guarantee**. Late closings marked “(+1 day)” are after midnight. Where independently documented, the venue cards also show kitchen hours; a missing kitchen schedule is not evidence of no food. See the [complete 9–13 November hours table](../wiki/opening-hours.md) and original sources on each venue profile.

For curated routes instead of a full search, start with the [shortlists](../wiki/shortlists.md) or [five-day plan](../wiki/five-day-plan.md). Real-cider evidence is a dated classification, not a promise about today's selection. See the [methodology](../wiki/methodology.md).
