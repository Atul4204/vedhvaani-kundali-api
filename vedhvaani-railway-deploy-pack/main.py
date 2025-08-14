# main.py
import os
import hashlib
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(title="VedhVaani Kundali API (placeholder)", version="1.0")

@app.get("/")
def root():
    return {"status": "VedhVaani Kundali API running"}

@app.get("/health")
def health():
    return {"ok": True}

# small deterministic pseudo-kundali generator (safe fallback)
PLANET_NAMES = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]
NAKSHATRA_NAMES = [
 "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
 "Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
 "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"
]

def seed_hash(*parts) -> str:
    s = "|".join(map(str, parts))
    return hashlib.sha256(s.encode()).hexdigest()

def hex_to_float(hhex: str, maxv: float = 360.0) -> float:
    # use first 8 hex chars to produce a consistent float
    chunk = hhex[:8]
    v = int(chunk, 16)
    return (v / 0xFFFFFFFF) * maxv

@app.get("/kundali/basic")
def kundali_basic(
    y: int,
    m: int,
    d: int,
    hour: float,
    lat: float,
    lon: float,
    tz: float = 5.5,
    lang: str = "hi",
    chart_style: str = "north"
):
    """
    Simple deterministic /safe endpoint so the app always starts.
    (Later you can replace internals with real pyswisseph engine.)
    """
    try:
        seed = seed_hash(y, m, d, hour, lat, lon)
        positions = {}
        # create deterministic positions for planets
        for i, name in enumerate(PLANET_NAMES):
            # rotate through the hash to get variety
            hh = seed[i*6:(i+1)*6] + seed[-6:]
            lonp = hex_to_float(hh, 360.0)
            positions[name] = {"lon": round(lonp, 4)}

        # simple ascendant approximation (NOT accurate): based on local hour + lon
        asc = (((hour % 24) / 24.0) * 360.0 + (lon % 360.0)) % 360.0
        rashi_index = int(asc // 30)

        moon_lon = positions["Moon"]["lon"]
        span = 360.0 / 27.0
        nak_index = int(moon_lon // span) % 27
        nak_name = NAKSHATRA_NAMES[nak_index]
        pada = int(((moon_lon % span) / span) * 4) + 1

        return {
            "ascendant": round(asc, 4),
            "rashi_lagna": rashi_index,
            "planets": positions,
            "moon_nakshatra": nak_name,
            "moon_pada": pada,
            "lang": lang,
            "chart_style": chart_style
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
