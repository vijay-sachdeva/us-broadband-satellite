#!/usr/bin/env python3
"""Curated long-haul / intercity backbone data -> data/longhaul.json

Curated from primary (company IR / SEC / press) + analyst sources, refreshed on
release (like the BEAD/Starlink seeds). Each block carries its own tier + source.

IMPORTANT measurement trap baked into the notes: fiber-miles (strand-miles) are
NOT route-miles. The owners chart uses network-wide ROUTE miles; Lumen/Zayo AI
build figures are quoted in their native unit and labelled.
"""
import json, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

OWNERS = [
    # route miles, network-wide (mixes long-haul + metro + access where noted)
    {"name": "AT&T", "miles": 800000, "focus": "carrier", "note": "mostly metro/access", "tier": "analyst"},
    {"name": "Verizon", "miles": 800000, "focus": "carrier", "note": "mostly metro/access", "tier": "analyst"},
    {"name": "Lumen", "miles": 340000, "focus": "longhaul", "note": ">100k mi 400G intercity; Level 3/CenturyLink legacy", "tier": "primary"},
    {"name": "Uniti + Windstream", "miles": 240000, "focus": "longhaul", "note": "merged Aug 2025", "tier": "primary"},
    {"name": "Zayo", "miles": 224000, "focus": "longhaul", "note": "post Crown Castle fiber close (2026)", "tier": "primary"},
    {"name": "Cogent", "miles": 93000, "focus": "longhaul", "note": "+18,905 intercity route mi from Sprint backbone (2023)", "tier": "primary"},
    {"name": "Microsoft (private)", "miles": 500000, "focus": "hyperscaler", "note": "owned+leased+subsea, mixed unit", "tier": "analyst"},
]

# The AI revival: dollars flooding back into the backbone
BOOKINGS = [
    {"t": "Aug 2024", "lumen": 5.0, "label": "Lumen PCF launch: $5B AI bookings (Microsoft anchor)"},
    {"t": "2025", "lumen": 8.5, "label": "$8.5B across Microsoft, Meta, AWS, Google"},
    {"t": "Q3 2025", "lumen": 10.0, "label": "~$10B PCF backlog"},
]
ZAYO_COMMITTED_B = 4.0  # ~$4B committed to AI long-haul

# Construction intensity by year — ILLUSTRATIVE relative index (0-100), shape only.
# Grounded in: dot-com boom 1996-2001 (~80-90M fiber-mi, ~$1T), 85-95% went dark;
# "a decade of nothing" 2002-2012; modest 2010s; AI revival 2023+.
ERA = [
    {"y": 1996, "v": 18}, {"y": 1998, "v": 65}, {"y": 2000, "v": 100}, {"y": 2001, "v": 82},
    {"y": 2002, "v": 22}, {"y": 2004, "v": 7}, {"y": 2008, "v": 5}, {"y": 2012, "v": 6},
    {"y": 2016, "v": 9}, {"y": 2020, "v": 13}, {"y": 2023, "v": 30}, {"y": 2025, "v": 58},
    {"y": 2027, "v": 80},
]

# Demand shift — Zayo Bandwidth Report (vendor primary), 2023->2024 YoY growth
BUYERS = [
    {"seg": "Metro dark fiber", "yoy": 268, "tier": "primary"},
    {"seg": "Software/tech wavelength capacity", "yoy": 450, "tier": "primary"},
    {"seg": "Long-haul dark fiber", "yoy": 52.6, "tier": "primary"},
]
CONCENTRATION = {
    "metro_dark_fiber_hyperscaler_carrier_pct": 91.2,
    "wavelength_over_1tb_hyperscaler_carrier_pct": 66.8,
    "tier": "primary",
    "source": "Zayo Bandwidth Report (2020-2024)",
}


def main():
    out = {
        "lastUpdated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tier": "analyst",
        "source": "Lumen/Zayo/Cogent/Crown Castle IR+SEC; Zayo Bandwidth Report; TeleGeography/SemiAnalysis",
        "ai_deals_total_b": 13,            # ~$12-14B announced AI long-haul (modeled aggregation)
        "dotcom_dark_pct": 90,             # 85-95% of dot-com fiber went dark (modeled)
        "longhaul_demand_cagr_pct": 35,    # ~35%/yr long-haul demand to 2030 (Zayo)
        "owners": OWNERS,
        "bookings": BOOKINGS,
        "zayo_committed_b": ZAYO_COMMITTED_B,
        "era": ERA,
        "buyers": BUYERS,
        "concentration": CONCENTRATION,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    with open(ROOT / "data/longhaul.json", "w", newline="\n") as f:
        json.dump(out, f, indent=2)
    print("wrote longhaul.json:", len(OWNERS), "owners,", len(ERA), "era points,", len(BUYERS), "buyer segs")


if __name__ == "__main__":
    main()
