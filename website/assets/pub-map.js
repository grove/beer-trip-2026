/* Beer Trip Companion: progressive map with full-fidelity address fallbacks.
 * Venue names, ranks, routes and classifications come from canonical JSON.
 * Postcodes.io supplies approximate postcode centroids, NOT verified pub entrances.
 * Do not use the public Nominatim service for bulk/browser geocoding.
 */
(() => {
  "use strict";

  const POSTCODE = /\b([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b/i;
  const CACHE_KEY = "beer-trip-postcode-centroids-v1";
  const CACHE_MS = 30 * 24 * 60 * 60 * 1000;
  const PAGE_SIZE = 24;
  const REGION_LABELS = {
    manchester: "Manchester & Salford",
    liverpool: "Liverpool & Wirral",
    surroundings: "Surrounding towns",
  };
  const CIDER_LABELS = {
    "documented-real": "Real cider documented (recheck stock)",
    "reported-cider-check-qualification": "Cider qualification unconfirmed",
    unverified: "Real cider not established",
    "none-reported": "No real cider reported",
  };
  const DAY_LABELS = { "2026-11-09": "Mon 9", "2026-11-10": "Tue 10",
    "2026-11-11": "Wed 11", "2026-11-12": "Thu 12", "2026-11-13": "Fri 13" };

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function normalise(value) {
    return String(value || "").toLocaleLowerCase("en").normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function postcode(address) {
    const found = String(address || "").match(POSTCODE);
    return found ? found[1].toUpperCase().replace(/\s+/g, "") : null;
  }

  function exactAddress(venue) {
    return venue.name + ", " + venue.address + ", United Kingdom";
  }

  function mapsSearch(venue) {
    return "https://www.google.com/maps/search/?api=1&query=" +
      encodeURIComponent(exactAddress(venue));
  }

  function walkingRoute(stops, byId) {
    const places = stops.map(s => byId.get(s.venue_id)).filter(Boolean);
    if (!places.length) return null;
    if (places.length === 1) return mapsSearch(places[0]);
    // Five places = three waypoints, supported in mobile browser Maps URLs.
    const start = "https://www.google.com/maps/dir/?api=1&travelmode=walking&origin=" +
      encodeURIComponent(exactAddress(places[0])) +
      "&destination=" + encodeURIComponent(exactAddress(places[places.length - 1]));
    const via = places.slice(1, -1).slice(0, 3);
    return via.length ? start + "&waypoints=" +
      via.map(v => encodeURIComponent(exactAddress(v))).join("%7C") : start;
  }

  function fetchJson(url) {
    return fetch(url).then(response => {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    });
  }

  function addStyle(url) {
    if (document.querySelector('link[href="' + url + '"]')) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = url;
    document.head.append(link);
  }

  function addScript(url) {
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = url;
      script.onload = resolve;
      script.onerror = () => reject(new Error("Map library unavailable: " + url));
      document.head.append(script);
    });
  }

  let leafletPromise = null;
  function ensureLeaflet() {
    if (leafletPromise) return leafletPromise;
    leafletPromise = (async () => {
      addStyle("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css");
      await addScript("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js");
      if (!window.L) throw new Error("Leaflet did not load");
      addStyle("https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css");
      addStyle("https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css");
      try {
        await addScript("https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js");
      } catch (error) {
        // Normal markers remain usable without the optional clustering plugin.
        console.warn(error);
      }
      return window.L;
    })();
    return leafletPromise;
  }

  function cachedPostcodes() {
    try {
      const cache = JSON.parse(sessionStorage.getItem(CACHE_KEY));
      if (cache && Number.isFinite(cache.at) && Date.now() - cache.at < CACHE_MS &&
          cache.values && typeof cache.values === "object") return cache.values;
    } catch (_) {
      // Storage can be disabled; the directory and map still work.
    }
    return {};
  }

  async function lookupPostcodes(venues) {
    const postcodes = [...new Set(venues.map(v => postcode(v.address)).filter(Boolean))];
    const values = cachedPostcodes();
    const missing = postcodes.filter(code => !values[code]);
    // The documented API accepts up to 100 UK postcodes in a single POST.
    // Never request one address per pin or call the public Nominatim endpoint.
    const chunks = [];
    for (let i = 0; i < missing.length; i += 100) chunks.push(missing.slice(i, i + 100));
    const lookups = chunks.map(async chunk => {
      const response = await fetch("https://api.postcodes.io/postcodes?filter=postcode,longitude,latitude", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ postcodes: chunk }),
      });
      if (!response.ok) throw new Error("Postcode service HTTP " + response.status);
      const data = await response.json();
      if (!Array.isArray(data.result)) throw new Error("Unexpected postcode result");
      for (const item of data.result) {
        const code = String(item.query || "").toUpperCase().replace(/\s+/g, "");
        const info = item.result;
        if (!chunk.includes(code) || !info) continue;
        const lat = info.latitude, lon = info.longitude;
        // Conservative bounding box for UK; reject missing/invalid data.
        if (Number.isFinite(lat) && Number.isFinite(lon) &&
            lat > 49 && lat < 61 && lon > -9 && lon < 3) {
          values[code] = [lat, lon];
        }
      }
    });
    const settled = await Promise.allSettled(lookups);
    const failed = settled.filter(item => item.status === "rejected");
    if (failed.length) console.warn("Some postcode lookups failed", failed.map(x => x.reason));
    try {
      sessionStorage.setItem(CACHE_KEY, JSON.stringify({ at: Date.now(), values: values }));
    } catch (_) {
      // Not essential.
    }
    return { values, failed: failed.length };
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
      top: root.querySelector('[name="top"]'),
    };
    const results = root.querySelector(".pub-map__results");
    const status = root.querySelector(".pub-map__status");
    const hint = root.querySelector(".pub-map__hint");
    const more = root.querySelector(".pub-map__more");
    const reset = root.querySelector(".pub-map__reset");
    const mapNode = root.querySelector(".pub-map__canvas");
    const routeLink = root.querySelector(".pub-map__route");
    const baseUrl = new URL(root.dataset.venueBase, window.location.href);
    let venues = [], routes = [], byId = new Map(), ranks = new Map();
    let openingHours = {};
    let map = null, markerLayer = null, L = null, coordinates = {}, postcodeError = false;
    let shown = PAGE_SIZE;
    let markers = new Map();

    function wikiUrl(v) {
      return new URL(encodeURIComponent(v.id) + "/", baseUrl).href;
    }

    function selectedRoute() {
      return routes.find(route => route.date === controls.day.value);
    }

    function filtered() {
      const query = normalise(controls.query.value.trim());
      const route = selectedRoute();
      const ids = route ? new Set(route.stops.map(stop => stop.venue_id)) : null;
      return venues.filter(venue => {
        if (ids && !ids.has(venue.id)) return false;
        if (controls.region.value && controls.region.value !== venue.region) return false;
        if (controls.priority.value && controls.priority.value !== venue.priority) return false;
        if (controls.cider.value && controls.cider.value !== venue.cider_status) return false;
        if (controls.top.checked && (ranks.get(venue.id) || 10000) > 20) return false;
        if (!query) return true;
        const searchText = [venue.name, venue.address, venue.area, venue.region,
          venue.why_visit, venue.beer, venue.cider_note, venue.food,
          ...(Array.isArray(venue.tags) ? venue.tags : [])].join(" ");
        return normalise(searchText).includes(query);
      });
    }

    function focusVenue(venue) {
      const marker = markers.get(venue.id);
      if (marker && map && markerLayer) {
        if (typeof markerLayer.zoomToShowLayer === "function") {
          markerLayer.zoomToShowLayer(marker, () => marker.openPopup());
        } else {
          map.setView(marker.getLatLng(), Math.max(map.getZoom(), 15));
          marker.openPopup();
        }
        mapNode.scrollIntoView({ behavior: "smooth", block: "nearest" });
      } else {
        hint.textContent = "No approximate pin for " + venue.name +
          ". Use its Google Maps link for a full-address search.";
      }
    }

    function publishedHoursLine(venue, day) {
      const entry = openingHours[venue.id];
      const formatter = window.BeerTripHours;
      if (!day || !formatter) return "Ordinary weekly hours on venue profile";
      const label = formatter.LABELS[formatter.DAYS.indexOf(day)];
      return "Published " + label + " bar hours: " + formatter.displayHours(entry, day);
    }

    function sourceLink(venue) {
      const entry = openingHours[venue.id];
      if (!entry?.source_url) return null;
      const link = element("a", "", "Hours source: " + window.BeerTripHours.sourceName(entry));
      link.href = entry.source_url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      return link;
    }

    function popup(venue, routeStop) {
      const div = element("div", "pub-map__popup");
      div.append(element("strong", "", venue.name));
      div.append(element("p", "", venue.address));
      div.append(element("p", "", venue.why_visit));
      if (routeStop) div.append(element("p", "", routeStop.note));
      const day = window.BeerTripHours?.dayKey(controls.day.value);
      div.append(element("p", "", publishedHoursLine(venue, day)));
      const hours = openingHours[venue.id];
      if (hours?.food_days && day) div.append(element("p", "",
        "Kitchen: " + window.BeerTripHours.displayHours(hours, day, true)));
      if (hours?.note) div.append(element("p", "", hours.note));
      const source = sourceLink(venue);
      if (source) div.append(source, element("span", "", " · "));
      const wiki = element("a", "", "Read sourced profile");
      wiki.href = wikiUrl(venue);
      const maps = element("a", "", "Find exact address in Google Maps");
      maps.href = mapsSearch(venue);
      maps.target = "_blank";
      maps.rel = "noopener noreferrer";
      const untappd = element("a", "", venue.untappd?.kind === "venue" ? "Untappd venue" : "Search Untappd");
      untappd.href = venue.untappd?.url || "https://untappd.com/search";
      untappd.target = "_blank";
      untappd.rel = "noopener noreferrer";
      div.append(wiki, element("span", "", " · "), maps, element("span", "", " · "), untappd);
      return div;
    }

    function makeCard(venue, routeStop) {
      const item = element("article", "pub-map__card");
      const heading = element("h3", "");
      const title = element("button", "pub-map__focus", venue.name);
      title.type = "button";
      title.addEventListener("click", () => focusVenue(venue));
      heading.append(title);
      const rank = element("span", "pub-map__rank", "#" + (ranks.get(venue.id) || "?"));
      heading.append(rank);
      item.append(heading);
      item.append(element("p", "pub-map__metadata",
        (REGION_LABELS[venue.region] || venue.region) + " · " + venue.area +
        (routeStop ? " · Stop " + routeStop.order + " (" + routeStop.role + ")" : "")));
      item.append(element("p", "pub-map__why", venue.why_visit));
      if (routeStop) item.append(element("p", "pub-map__note", routeStop.note));
      const day = window.BeerTripHours?.dayKey(controls.day.value);
      item.append(element("p", "pub-map__hours", publishedHoursLine(venue, day)));
      const hours = openingHours[venue.id];
      if (hours?.food_days && day) item.append(element("p", "pub-map__kitchen",
        "Kitchen: " + window.BeerTripHours.displayHours(hours, day, true)));
      if (hours?.status === "event-only" || hours?.note) {
        item.append(element("p", "pub-map__note", hours?.note || "Event-only opening; verify with producer."));
      }
      const source = sourceLink(venue);
      if (source) item.append(source);
      item.append(element("p", "pub-map__cider", CIDER_LABELS[venue.cider_status] || "Check cider evidence"));
      const buttons = element("div", "pub-map__cardlinks");
      const details = element("a", "", "Wiki profile");
      details.href = wikiUrl(venue);
      const destination = element("a", "", "Find address in Google Maps");
      destination.href = mapsSearch(venue);
      destination.target = "_blank";
      destination.rel = "noopener noreferrer";
      const untappd = element("a", "", venue.untappd?.kind === "venue" ? "Untappd venue" : "Search Untappd");
      untappd.href = venue.untappd?.url || "https://untappd.com/search";
      untappd.target = "_blank";
      untappd.rel = "noopener noreferrer";
      buttons.append(details, destination, untappd);
      item.append(buttons);
      if (!coordinates[postcode(venue.address)]) {
        item.append(element("span", "pub-map__unlocated", "Address search only — no approximate pin"));
      }
      return item;
    }

    function renderList(matches, route) {
      const routeStops = new Map(route ? route.stops.map((stop, index) =>
        [stop.venue_id, { order: index + 1, role: stop.role, note: stop.note }]) : []);
      const fragment = document.createDocumentFragment();
      matches.slice(0, shown).forEach(v => fragment.append(makeCard(v, routeStops.get(v.id))));
      results.replaceChildren(fragment);
      if (!matches.length) results.append(element("p", "pub-map__empty", "No matches. Remove a filter or choose another day."));
      more.hidden = shown >= matches.length;
      more.textContent = "Show " + Math.min(PAGE_SIZE, matches.length - shown) + " more venues";
    }

    function renderMap(matches, route) {
      if (!map || !markerLayer || !L) return 0;
      markers = new Map();
      markerLayer.clearLayers();
      const bounds = [];
      const routeStops = new Map(route ? route.stops.map((stop, index) =>
        [stop.venue_id, { order: index + 1, role: stop.role, note: stop.note }]) : []);
      for (const venue of matches) {
        const location = coordinates[postcode(venue.address)];
        if (!location) continue;
        const spot = L.marker(location, {
          title: venue.name + " (approximate postcode centre)",
          icon: L.divIcon({
            className: "pub-map__pin-wrap",
            html: '<span class="pub-map__pin pub-map__pin--' +
              (venue.priority === "essential" ? "essential" : "standard") +
              (venue.cider_status === "documented-real" ? " pub-map__pin--cider" : "") +
              '"></span>',
            iconSize: [22, 22],
            iconAnchor: [11, 11],
          }),
        });
        spot.bindPopup(popup(venue, routeStops.get(venue.id)), { maxWidth: 310 });
        markerLayer.addLayer(spot);
        markers.set(venue.id, spot);
        bounds.push(location);
      }
      if (bounds.length === 1) {
        map.setView(bounds[0], 15);
      } else if (bounds.length) {
        map.fitBounds(bounds, { padding: [24, 24], maxZoom: 13 });
      }
      return bounds.length;
    }

    function render() {
      const route = selectedRoute();
      let matches = filtered();
      // Trip days use the explicitly curated visiting order, not overall rank.
      if (route) {
        const order = new Map(route.stops.map((stop, index) => [stop.venue_id, index]));
        matches = matches.sort((a, b) => order.get(a.id) - order.get(b.id));
      }
      const mapped = renderMap(matches, route);
      renderList(matches, route);
      const n = map ? mapped : matches.filter(v => coordinates[postcode(v.address)]).length;
      status.textContent = matches.length + " of " + venues.length +
        " venues shown · " + n + " approximate postcode pins";
      if (postcodeError) {
        hint.textContent = "Some postcode lookups are unavailable. The address list and Google Maps links still work.";
      } else {
        hint.textContent = "Pins are postcode centres, not pub entrances. For navigation, use Google Maps' full-address search; verify opening and cider stock.";
      }
      if (route) {
        routeLink.hidden = false;
        routeLink.href = walkingRoute(route.stops, byId) || "#";
        routeLink.textContent = route.stops.length > 1 ?
          "Open proposed walking order in Google Maps" : "Open possible arrival stop in Google Maps";
      } else {
        routeLink.hidden = true;
      }
    }

    function attachEvents() {
      for (const [key, input] of Object.entries(controls)) {
        input.addEventListener(key === "query" ? "input" : "change", () => {
          shown = PAGE_SIZE;
          render();
        });
      }
      more.addEventListener("click", () => {
        shown += PAGE_SIZE;
        renderList(filtered(), selectedRoute());
      });
      reset.addEventListener("click", () => {
        for (const [key, input] of Object.entries(controls)) {
          if (key === "top") input.checked = false;
          else input.value = "";
        }
        shown = PAGE_SIZE;
        render();
      });
    }

    async function boot() {
      try {
        const [vdata, rdata, ranking, schedules] = await Promise.all([
          fetchJson(new URL(root.dataset.venuesUrl, window.location.href)),
          fetchJson(new URL(root.dataset.routesUrl, window.location.href)),
          fetchJson(new URL(root.dataset.rankingsUrl, window.location.href)),
          fetchJson(new URL(root.dataset.openingHoursUrl, window.location.href)).catch(error => {
            console.warn("Published hours unavailable; map remains usable", error);
            return { hours: {} };
          }),
        ]);
        if (!Array.isArray(vdata.venues) || !Array.isArray(rdata.routes) ||
            !Array.isArray(ranking.ranking_ids)) throw new Error("Malformed venue/route data");
        venues = vdata.venues;
        routes = rdata.routes;
        openingHours = schedules.hours || {};
        byId = new Map(venues.map(v => [v.id, v]));
        ranks = new Map(ranking.ranking_ids.map((id, index) => [id, index + 1]));
        venues.sort((a, b) => (ranks.get(a.id) || 10000) - (ranks.get(b.id) || 10000));
        for (const route of routes) {
          const option = element("option", "", route.title);
          option.value = route.date;
          controls.day.append(option);
        }
        attachEvents();
        render(); // Full text directory works immediately, before the map/CDN loads.

        const [positionResult, libraryResult] = await Promise.allSettled([
          lookupPostcodes(venues), ensureLeaflet(),
        ]);
        if (positionResult.status === "fulfilled") {
          coordinates = positionResult.value.values;
          postcodeError = positionResult.value.failed > 0;
        } else {
          postcodeError = true;
          console.warn(positionResult.reason);
        }
        if (libraryResult.status === "rejected") {
          mapNode.replaceChildren(element("p", "pub-map__error",
            "Interactive basemap unavailable. Use the full venue list and exact-address Google Maps links below."));
          console.warn(libraryResult.reason);
          render();
          return;
        }
        L = libraryResult.value;
        mapNode.replaceChildren(); // Remove the loading placeholder before Leaflet attaches its panes.
        map = L.map(mapNode, { scrollWheelZoom: false }).setView([53.44, -2.56], 9);
        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        }).addTo(map);
        markerLayer = typeof L.markerClusterGroup === "function" ?
          L.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 48 }) :
          L.layerGroup();
        markerLayer.addTo(map);
        render();
      } catch (error) {
        console.error("Beer trip map failed to initialise", error);
        status.textContent = "The live venue index is unavailable. Open the catalogue or a CSV export below.";
        mapNode.replaceChildren(element("p", "pub-map__error",
          "Map data could not be loaded. See the linked catalogue and My Maps exports."));
      }
    }

    boot();
  }

  function bootMaps() {
    document.querySelectorAll("#beer-map-app").forEach(initialise);
  }
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(bootMaps);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootMaps);
  } else {
    bootMaps();
  }
})();
