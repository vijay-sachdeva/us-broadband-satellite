# US Broadband — satellite connectivity explorer

A single-page, public-data dashboard making one argument: **where fiber stops being worth it, satellite is the floor.** Satellite isn't competing with fiber — it's the floor under the rural tail fiber can't afford to reach.

**Live:** https://vijay-sachdeva.github.io/us-broadband-satellite/

## Stack

Vanilla `index.html` + Chart.js + D3 + topojson via CDN. **No build step.** Python feed scripts write `data/*.json`; the front-end `fetch()`es them on load and falls back to built-in seeds if a feed is missing. GitHub Pages from `main`.

```
index.html                         the dashboard (charts A–F + caveats)
data/*.json                        generated feeds (committed)
scripts/fetch_broadband_adoption.py  ACS B28002 -> broadband.json (seed fallback w/o key)
scripts/build_bead.py                seed CSV   -> bead.json
scripts/build_satellite.py           seed CSVs  -> satellite.json
scripts/data_sources/*.csv           release-cadence seed data
.github/workflows/refresh-data.yml   daily regen + commit
```

## Charts

| # | Chart | Source | Tier |
|---|-------|--------|------|
| A | Cost-per-location crossover (hero SVG) | modeled on BEAD per-loc costs | Modeled |
| B | Broadband gap map (state choropleth) | ACS B28002 | Primary |
| C | Won the locations, lost the dollars | NTIA BEAD | Primary |
| D | Starlink subscriber growth | SpaceX / analyst | Analyst |
| E | Performance vs the 100/20 bar | Ookla | Analyst |
| F | Who serves the shrinking tail | modeled | Modeled |

Every figure carries a tier badge (Primary / Analyst / Modeled) + source link.

## Refresh

```bash
cd scripts
python build_bead.py
python build_satellite.py
CENSUS_API_KEY=xxxx python fetch_broadband_adoption.py   # without a key, writes a seed snapshot
```

`broadband.json` uses live ACS data when `CENSUS_API_KEY` (a free [Census key](https://api.census.gov/data/key_signup.html)) is set — locally or as a repo secret. Without it, the script writes a complete embedded seed snapshot so the map always renders.

## Notes

- Public data only; the licensed FCC fabric (per-location lat/long) is out of scope — state/county summaries only.
- Not investment advice. No tickers, no buy/sell language.
