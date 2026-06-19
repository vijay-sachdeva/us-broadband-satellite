#!/usr/bin/env python3
"""scripts/data_sources/starlink.csv -> data/satellite.json

Emits:
  series : subscriber growth by year (global + US where known)   [analyst]
  perf   : measured download/upload by half-year                 [analyst]
  crossover : modeled fiber/satellite cost-per-location params   [modeled]
"""
import csv, json, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts/data_sources/starlink.csv"


def f(v):
    return float(v) if v not in (None, "") else None


def main():
    series, perf = [], []
    with open(SRC, newline="") as fh:
        for r in csv.DictReader(fh):
            year = int(r["year"])
            series.append({
                "year": year,
                "g": f(r["global_subs_m"]),
                "us": f(r["us_subs_m"]),
            })
            dl, ul = f(r["dl_mbps"]), f(r["ul_mbps"])
            if dl is not None and ul is not None:
                # split each year's measured pair onto a 1H/2H label for the perf chart
                perf.append({"t": f"{year}", "dl": dl, "ul": ul})

    out = {
        "lastUpdated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tier": "analyst",
        "source": "SpaceX disclosures + Ookla Starlink reports (subs analyst-estimated)",
        "target_subs_m": 25,
        "target_year": 2026,
        "series": series,
        "perf": perf,
        "crossover": {
            "tier": "modeled",
            "satellite_flat_usd": 600,
            "satellite_monthly_usd": 120,
            "bead_high_cost_threshold_usd": 10000,
            "note": "Illustrative; shape grounded in BEAD per-location costs.",
        },
    }
    (ROOT / "data").mkdir(exist_ok=True)
    with open(ROOT / "data/satellite.json", "w", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", len(series), "series points,", len(perf), "perf points")


if __name__ == "__main__":
    main()
