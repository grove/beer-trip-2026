# Import the 2026 beer trip into Google My Maps

[Start the map explorer](https://grove.github.io/beer-trip-2026/map/) · [Trip itinerary](../../wiki/five-day-plan.md) · [All venue profiles](../../wiki/catalogue.md) · [Repo home](../../README.md)

These are **ready-to-import CSV layers generated from the 158 canonical venue records**, ranked data and date-aware travel plan. The files are not a published Google map, a GPS survey, or a live pub-stock feed. **No account login, map publication or sharing has been done for you.**

## Download the layers

| File | Rows | Suggested My Maps use |
| --- | ---: | --- |
| [all-venues.csv](all-venues.csv) | **158** | Main overview; style by Priority or Region. |
| [top-20.csv](top-20.csv) | **20** | The highest-ranked shortlist; may overlap the main layer. |
| [2026-11-09-mon-09.csv](2026-11-09-mon-09.csv) | **1** | Conditional Monday arrival stop; Marble Arch Tuesday closure matters. |
| [2026-11-10-tue-10.csv](2026-11-10-tue-10.csv) | **5** | Manchester heritage, lunch, cask and cider. |
| [2026-11-11-wed-11.csv](2026-11-11-wed-11.csv) | **4** | Stockport heritage and real cider/perry. |
| [2026-11-12-thu-12.csv](2026-11-12-thu-12.csv) | **3** | Liverpool's Dale Street and station-area pubs. |
| [2026-11-13-fri-13.csv](2026-11-13-fri-13.csv) | **3** | Liverpool Georgian Quarter/Ropewalks. |

Total if you import all seven: **seven layers**, below My Maps' current ten-layer maximum. Locations deliberately overlap between the overview, shortlist and day layers; switch the unwanted layers off to reduce duplicate markers. Saturday 14 November is **airport morning, not a pub day**.

## Import into your own Google account

1. On a desktop browser open [Google My Maps](https://www.google.com/maps/d/) and select **Create a new map**. Give it a title such as *Manchester & Liverpool Beer Trip · November 2026*.
2. Click **Import** in the first layer. Choose the downloaded **all-venues.csv**.
3. When asked which column identifies locations, choose **Location**. This is **name + full street address + United Kingdom**, deliberately more distinctive than a pub name alone. **Do not select Rank, ID or Stop order as a location**.
4. When asked for a title column, select **Name**. Use **Uniform style → Group places by → Priority** or **Region** to colour the main layer, if those options appear in your current My Maps UI.
5. In **Add layer**, import any other files you want. Give the layers readable labels; optionally choose different colours for the five dates.
6. **Inspect every imported pin**, especially duplicates and the two entries without postcodes: **Sadler's Cat** and **That Beer Place**. A successful file import is not proof that Google's geocoder chose the correct business or street.
7. Use the map's **Share** controls to choose who can view/edit it. For a website embed, use My Maps' embed option after you have decided to publish an appropriate map. You control the access settings; an export file itself is not a shared live map.

Google's official [My Maps import instructions](https://support.google.com/mymaps/answer/3024836) document CSV address/place columns and a **2,000-row import cap** (well above 158). [My Maps Help](https://support.google.com/mymaps/) describes styling, sharing and embedding. For navigation between places, prefer the [site's flight-aware map view](https://grove.github.io/beer-trip-2026/map/) or Google Maps directions links rather than assuming My Maps imported an optimised walking route.

## What is in each marker?

The exports include **Monday–Sunday bar opening-hour columns and an Hours source URL**, with “Closed” only where an ordinary published schedule says so and “Event-only” for producer sessions without a regular weekly timetable. Hours after midnight show “(+1 day)”. These are checked schedules, **not a promise of opening on the travel dates**. Full kitchen hours and exceptions are on the linked venue profiles. The exports also include stable **ID**, **Name**, geocoding **Location**, **Address**, **Area**, **Region**, editorial **Rank**, **Priority**, nuanced **Real cider evidence**, concise **Why visit**, **Beer**, **Cider and perry**, **Food**, any suggested UK **Visit date**, **Stop order/role/note**, a direct **Wiki profile**, and a separate **Google Maps** search URL. Each venue's profile has its sources, caveats and fuller story.

Only the **real-cider evidence state** is structured; it is **not** a promise of today's product, real-cider qualification or on-hand quantity. The 2026-10-28 research snapshot can become stale. Review the linked source pages before travelling.

The CSV **Location** is for Google My Maps to geocode the full address. It is intentionally **not** replaced by postcode-centroid latitude/longitude from the website map: an approximate point could route someone to the wrong doorway.

## Maintenance

The CSVs are **generated files**. Never fix them by hand. When the database, ranking or itinerary changes:

1. Update [canonical venues](../../data/venues.json), [rankings](../../data/rankings.json) or [map-routes.json](../../data/map-routes.json), preserving the documented uncertainty.
2. Run **python3 scripts/build_wiki.py** to refresh 158 venue pages, then **python3 scripts/export_maps.py** from the repository root, and check using **python3 scripts/export_maps.py --check**.
3. Run the usual wiki and website validation checks. Commit canonical changes **together** with the regenerated CSVs; the CI check detects stale export files.
4. Reimport the updated CSV in My Maps. **My Maps does not automatically sync with GitHub**; the website map, however, reads the repository data whenever it loads.

No API key, proprietary geocoding service, per-user location tracking, Google Maps JavaScript API or credential is needed for these exports. The accompanying website map uses a clearly labelled postcode-centroid *approximation* and provides Google Maps full-address links for the final navigational decision.
