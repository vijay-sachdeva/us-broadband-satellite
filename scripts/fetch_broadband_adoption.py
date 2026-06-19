#!/usr/bin/env python3
"""ACS B28002 broadband subscription by state + national trend -> data/broadband.json

B28002_001E = total households; B28002_004E = "Broadband of any type".
Works with or without a CENSUS_API_KEY (key only needed for high volume).
"""
import os, json, datetime, pathlib, urllib.parse, urllib.request

KEY = os.environ.get("CENSUS_API_KEY")
ROOT = pathlib.Path(__file__).resolve().parents[1]


# Embedded seed: ACS 5-yr B28002 "Broadband of any type" % of households by state,
# ~2023 vintage (representative snapshot). Used as a fallback when no CENSUS_API_KEY
# is available so the dashboard always has a complete map; CI regenerates live values.
SEED = {
    "01": ("Alabama", 84.6), "02": ("Alaska", 88.4), "04": ("Arizona", 88.5),
    "05": ("Arkansas", 82.5), "06": ("California", 90.6), "08": ("Colorado", 91.3),
    "09": ("Connecticut", 90.5), "10": ("Delaware", 90.0), "11": ("District of Columbia", 90.3),
    "12": ("Florida", 89.1), "13": ("Georgia", 87.5), "15": ("Hawaii", 90.2),
    "16": ("Idaho", 87.7), "17": ("Illinois", 88.6), "18": ("Indiana", 86.4),
    "19": ("Iowa", 86.5), "20": ("Kansas", 87.1), "21": ("Kentucky", 84.3),
    "22": ("Louisiana", 83.6), "23": ("Maine", 87.2), "24": ("Maryland", 91.4),
    "25": ("Massachusetts", 90.9), "26": ("Michigan", 87.2), "27": ("Minnesota", 89.6),
    "28": ("Mississippi", 80.9), "29": ("Missouri", 86.0), "30": ("Montana", 86.0),
    "31": ("Nebraska", 87.4), "32": ("Nevada", 89.6), "33": ("New Hampshire", 91.6),
    "34": ("New Jersey", 91.5), "35": ("New Mexico", 83.9), "36": ("New York", 89.3),
    "37": ("North Carolina", 87.0), "38": ("North Dakota", 86.9), "39": ("Ohio", 86.9),
    "40": ("Oklahoma", 84.4), "41": ("Oregon", 90.3), "42": ("Pennsylvania", 88.0),
    "44": ("Rhode Island", 89.3), "45": ("South Carolina", 86.0), "46": ("South Dakota", 86.0),
    "47": ("Tennessee", 85.8), "48": ("Texas", 88.1), "49": ("Utah", 92.5),
    "50": ("Vermont", 87.5), "51": ("Virginia", 90.0), "53": ("Washington", 92.0),
    "54": ("West Virginia", 81.9), "55": ("Wisconsin", 87.1), "56": ("Wyoming", 86.6),
}
SEED_TREND = [
    (2015, 77.0), (2016, 78.3), (2017, 80.1), (2018, 81.5), (2019, 82.7),
    (2020, 85.2), (2021, 87.0), (2022, 88.0), (2023, 88.6),
]


def acs(year, geo):
    base = f"https://api.census.gov/data/{year}/acs/acs5"
    q = {"get": "NAME,B28002_001E,B28002_004E", "for": geo}
    if KEY:
        q["key"] = KEY
    url = base + "?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def write_seed():
    states = {fips: {"name": n, "broadband_pct": p} for fips, (n, p) in SEED.items()}
    trend = [{"year": y, "broadband_pct": p} for y, p in SEED_TREND]
    out = {
        "lastUpdated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tier": "primary",
        "source": "ACS 5-yr B28002 (~2023 seed snapshot) - set CENSUS_API_KEY to refresh live",
        "seed": True,
        "states": states,
        "national_trend": trend,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    with open(ROOT / "data/broadband.json", "w", newline="\n") as f:
        json.dump(out, f, indent=2)
    print("wrote SEED broadband.json:", len(states), "states,", len(trend), "trend points")


def main():
    if not KEY:
        print("No CENSUS_API_KEY set - writing embedded seed.")
        return write_seed()
    year = 2023  # latest 5-yr vintage; bump as released
    rows = acs(year, "state:*")
    h = rows[0]
    i = {k: h.index(k) for k in h}
    states = {}
    for r in rows[1:]:
        tot = float(r[i["B28002_001E"]] or 0)
        bb = float(r[i["B28002_004E"]] or 0)
        if tot > 0:
            states[r[i["state"]]] = {
                "name": r[i["NAME"]],
                "broadband_pct": round(100 * bb / tot, 1),
            }
    # national trend 2015..year
    trend = []
    for y in range(2015, year + 1):
        try:
            n = acs(y, "us:1")
            j = {k: n[0].index(k) for k in n[0]}
            tot = float(n[1][j["B28002_001E"]])
            bb = float(n[1][j["B28002_004E"]])
            trend.append({"year": y, "broadband_pct": round(100 * bb / tot, 1)})
        except Exception as e:
            print("trend", y, e)
    out = {
        "lastUpdated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tier": "primary",
        "source": f"ACS 5-yr B28002 ({year})",
        "states": states,
        "national_trend": trend,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    with open(ROOT / "data/broadband.json", "w", newline="\n") as f:
        json.dump(out, f, indent=2)
    print("wrote", len(states), "states,", len(trend), "trend points")


if __name__ == "__main__":
    main()
