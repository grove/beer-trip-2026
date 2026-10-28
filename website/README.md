# The website

This directory contains **presentation only**. The canonical content remains in `data/` and `wiki/`; never hand-edit generated venue pages to fix the website.

The site uses [Zensical](https://zensical.org/) for a responsive, searchable static site. `scripts/prepare_site.py` builds a disposable `.site/docs/` staging tree, copying the wiki and data **without rewriting their links or source files**. It adds a landing page, searchable venue explorer, **Leaflet map** with day-aware filters, styling and an automatically generated navigation structure from `data/venues.json`. It also stages the checked-in **Google My Maps CSV files** from `maps/google-my-maps/`. All original Markdown is available; the repository-root README appears at `/overview/`, while wiki Home links go to the website landing page. Agent instructions, JSON data and `llms.txt` are also included.

## Local preview

Use Python 3.11 or newer:

```bash
python -m pip install -r requirements-site.txt
python scripts/build_wiki.py --check
python scripts/build_rankings.py --check
python scripts/export_maps.py --check
python scripts/validate_wiki.py
python scripts/prepare_site.py
zensical serve --config-file .site/mkdocs.yml
```

For a production-equivalent check, use:

```bash
zensical build --config-file .site/mkdocs.yml --strict
python scripts/check_site.py
python -m unittest discover -s tests -p 'test_*.py'
```

The **interactive map** is at `/map/`. It reads the same `data/venues.json`, `data/rankings.json` and `data/map-routes.json` as the rest of the site. Leaflet and its optional marker clustering assets load from version-pinned CDN URLs only on the map page; OpenStreetMap tiles render only on demand with attribution. A browser fetch to [Postcodes.io](https://postcodes.io/docs/postcode/bulk/) obtains **approximate postcode-centre coordinates** in batches of up to 100, cached in session storage. **No precision-geocoding or user-position tracking is performed**. Full street-address Google Maps links and all-venue text listings remain available if scripts or location lookup fail. Two entries without postcodes stay list/search only. External services must not be mistaken for live trading, beer stock or route timing.

The `.site/` directory is disposable and ignored by Git. If you change a source Markdown or JSON file while previewing, stop the server, rerun `prepare_site.py` and restart it. Run `python scripts/build_wiki.py` after editing canonical venue data before the check and site build.

## Publication

The GitHub Actions workflow `.github/workflows/site.yml` builds and validates each relevant pull request **without publishing it**. A push to `main` after merge (or a manual workflow run) builds the same site and deploys the artifact to GitHub Pages. The repository owner must select **Settings → Pages → Build and deployment → Source: GitHub Actions** once, and have Pages enabled for the repository/account. Default site URL: `https://grove.github.io/beer-trip-2026/`; change `site_url` in `website/mkdocs.yml` if a custom domain is configured.

**Visibility:** Publishing a GitHub Pages site from a private repository can still make its website publicly accessible, depending on GitHub's Pages settings and plan. Confirm the intended audience before enabling Pages; the built artifact includes the repo's public-facing research content and `data/*.json`.

## Growth and navigation

- New venue in `data/venues.json` → run `python scripts/build_wiki.py` → the new page is automatically included in search, the A–Z/region navigation and the JSON-backed venue finder.
- New `wiki/*.md` editorial article → the build discovers it and adds it to **More articles**. New pages under `wiki/areas/` appear in **Area directories**. To feature an article prominently, add its path to `FEATURED` in `scripts/prepare_site.py`.
- Rebuild the Google My Maps layers with `python scripts/export_maps.py` after any material address, ranking or route change. See the [My Maps guide](../maps/google-my-maps/README.md); GitHub cannot automatically publish/import the map into a Google account.
- Existing internal links and provenance remain unchanged. The site indexes the Markdown pages, while the venue finder reads the same canonical JSON; no duplicated venue catalogue needs maintaining.
- Navigation is subdivided by region and alphabet group and uses pruning so larger collections do not make every page's sidebar unwieldy. The search index is generated at build time and requires no hosted search service.

Data that mentions future openings, cider or event stock remains dated research, not live availability.
