/* Progressive enhancement: the directory works from the canonical venue JSON. */
(() => {
  "use strict";

  const PAGE_SIZE = 24;
  const REGION_NAMES = {
    manchester: "Manchester & Salford",
    liverpool: "Liverpool & Wirral",
    surroundings: "Surrounding towns",
  };
  const PRIORITY_NAMES = { essential: "Essential", high: "High", specialist: "Specialist" };
  const CIDER_NAMES = {
    "documented-real": "Real cider documented",
    "reported-cider-check-qualification": "Cider evidence needs checking",
    unverified: "Cider not established",
    "none-reported": "No real cider reported",
  };
  const priorityOrder = { essential: 0, high: 1, specialist: 2 };
  const normalise = value => String(value || "").toLocaleLowerCase("en").normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "");

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function makeCard(venue, baseUrl, published, day) {
    const card = element("a", "venue-card");
    card.href = new URL(encodeURIComponent(venue.id) + "/", baseUrl).href;
    const top = element("div", "venue-card__head");
    top.append(element("h3", "venue-card__name", venue.name));
    top.append(element("span", "venue-card__priority", PRIORITY_NAMES[venue.priority] || venue.priority));
    card.append(top);
    card.append(element("p", "venue-card__area", `${REGION_NAMES[venue.region] || venue.region} · ${venue.area}`));
    const why = venue.why_visit || "Read the venue's evidence and practical notes.";
    card.append(element("p", "venue-card__why", why.length > 195 ? why.slice(0, 192).trimEnd() + "…" : why));
    card.append(element("span", "venue-card__cider", CIDER_NAMES[venue.cider_status] || "Check cider evidence"));
    const formatter = window.BeerTripHours;
    if (day && formatter) {
      const label = formatter.LABELS[formatter.DAYS.indexOf(day)];
      card.append(element("p", "venue-card__hours",
        "Published " + label + " bar hours: " + formatter.displayHours(published, day)));
      if (published?.food_days) card.append(element("p", "venue-card__kitchen",
        "Kitchen: " + formatter.displayHours(published, day, true)));
    } else {
      card.append(element("p", "venue-card__hours",
        "Weekly bar hours and original source on venue profile."));
    }
    return card;
  }

  function initialise(root) {
    if (root.dataset.initialised) return;
    root.dataset.initialised = "true";

    const controls = {
      query: root.querySelector('[name="query"]'),
      region: root.querySelector('[name="region"]'),
      priority: root.querySelector('[name="priority"]'),
      cider: root.querySelector('[name="cider"]'),
      day: root.querySelector('[name="day"]'),
      onlyOpen: root.querySelector('[name="onlyOpen"]'),
    };
    const results = root.querySelector(".venue-finder__results");
    const status = root.querySelector(".venue-finder__status");
    const more = root.querySelector(".venue-finder__more");
    const reset = root.querySelector(".venue-finder__reset");
    let venues = [];
    let openingHours = {};
    let visible = PAGE_SIZE;
    const baseUrl = new URL(root.dataset.venueBase, window.location.href);

    function filtered() {
      const query = normalise(controls.query.value.trim());
      return venues.filter(venue => {
        if (controls.region.value && venue.region !== controls.region.value) return false;
        if (controls.priority.value && venue.priority !== controls.priority.value) return false;
        if (controls.cider.value && venue.cider_status !== controls.cider.value) return false;
        if (controls.onlyOpen.checked && controls.day.value &&
            !window.BeerTripHours?.isPublishedOpen(openingHours[venue.id], controls.day.value)) return false;
        if (!query) return true;
        const searchable = [venue.name, venue.area, venue.region, venue.venue_type,
          venue.why_visit, venue.beer, venue.cider_note, venue.food,
          ...(Array.isArray(venue.tags) ? venue.tags : [])].join(" ");
        return normalise(searchable).includes(query);
      });
    }

    function render() {
      const matches = filtered();
      const fragment = document.createDocumentFragment();
      matches.slice(0, visible).forEach(venue =>
        fragment.append(makeCard(venue, baseUrl, openingHours[venue.id], controls.day.value)));
      results.replaceChildren(fragment);
      status.textContent = `${matches.length.toLocaleString("en")} ${matches.length === 1 ? "venue" : "venues"} found`;
      controls.onlyOpen.disabled = !controls.day.value;
      if (matches.length === 0) {
        results.append(element("p", "venue-finder__empty", "No matches yet. Try fewer filters or a broader search."));
      }
      more.hidden = visible >= matches.length;
      more.textContent = `Show more places (${Math.min(PAGE_SIZE, matches.length - visible)} next)`;
    }

    Object.values(controls).forEach(control => {
      control.addEventListener(control === controls.query ? "input" : "change", () => {
        visible = PAGE_SIZE;
        render();
      });
    });
    more.addEventListener("click", () => {
      visible += PAGE_SIZE;
      render();
    });
    reset.addEventListener("click", () => {
      for (const control of Object.values(controls)) {
        if (control.type === "checkbox") control.checked = false;
        else control.value = "";
      }
      visible = PAGE_SIZE;
      controls.query.focus();
      render();
    });

    const getJson = url => fetch(new URL(url, window.location.href))
      .then(response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      });
    Promise.all([
      getJson(root.dataset.venuesUrl),
      getJson(root.dataset.openingHoursUrl).catch(error => {
        console.warn("Opening-hours feed not available; listing remains usable", error);
        return { hours: {} };
      }),
    ]).then(([data, schedule]) => {
      if (!Array.isArray(data.venues)) throw new Error("Invalid venue database");
      openingHours = schedule.hours || {};
      venues = data.venues.slice().sort((a, b) =>
        (priorityOrder[a.priority] ?? 9) - (priorityOrder[b.priority] ?? 9) ||
        a.name.localeCompare(b.name, "en"));
      [...new Set(venues.map(v => v.region))].sort().forEach(region => {
        const option = element("option", "", REGION_NAMES[region] || region);
        option.value = region;
        controls.region.append(option);
      });
      render();
    }).catch(error => {
      status.textContent = "The directory could not be loaded. Use the alphabetical catalogue instead.";
      const link = element("a", "", "Open the complete catalogue");
      link.href = new URL("../wiki/catalogue/", window.location.href).href;
      results.replaceChildren(link);
      more.hidden = true;
      console.error("Venue directory loading error:", error);
    });
  }

  function boot() {
    document.querySelectorAll("#venue-finder").forEach(initialise);
  }
  // Handles both ordinary document loads and Zensical's optional instant navigation.
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(boot);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
