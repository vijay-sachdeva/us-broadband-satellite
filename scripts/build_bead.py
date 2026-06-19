#!/usr/bin/env python3
"""scripts/data_sources/bead_by_tech.csv -> data/bead.json

BEAD locations-won vs dollars-won by technology. Primary (NTIA BEAD).
"""
import csv, json, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts/data_sources/bead_by_tech.csv"


def main():
    rows, sources = [], set()
    with open(SRC, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
                "tech": r["tech"],
                "loc": float(r["locations_pct"]),
                "dol": float(r["dollars_pct"]),
            })
            if r.get("source"):
                sources.add(r["source"])
    out = {
        "lastUpdated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tier": "primary",
        "source": "; ".join(sorted(sources)),
        "rows": rows,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    with open(ROOT / "data/bead.json", "w", newline="\n") as f:
        json.dump(out, f, indent=2)
    print("wrote", len(rows), "bead rows")


if __name__ == "__main__":
    main()
