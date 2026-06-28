"""
Madame Minou — Deterministic Chart Engine

Computes astrological chart facts using pyswisseph (Swiss Ephemeris).
Produces the structured facts object consumed by the AI layer.

Requirements fulfilled:
  R3.1 — Deterministic computation; AI never invents positions.
  R3.2 — Full chart (sun, moon, rising, transits) when all inputs present.
  R3.3 — Date-only: sun + moon (when unambiguous), no rising, "estimated chart."
  R3.5 — Mystery: year-only or nothing reliable → whatever is derivable.
  R3.7 — Output as structured facts object for the AI contract.
"""

import swisseph as swe
from datetime import datetime, date
from typing import Optional

# ---------- Constants ----------

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Outer planets used for transit computation
TRANSIT_PLANETS = [
    (swe.JUPITER, "Jupiter"),
    (swe.SATURN, "Saturn"),
    (swe.URANUS, "Uranus"),
    (swe.NEPTUNE, "Neptune"),
]

# Major aspects and their angular separations
ASPECTS = [
    (0, "conjunct"),
    (180, "opposite"),
    (90, "square"),
    (120, "trine"),
]

# Orb tolerance in degrees for aspect detection
ASPECT_ORB = 8.0


# ---------- Helper functions ----------

def ecliptic_longitude_to_sign(longitude: float) -> str:
    """Convert ecliptic longitude (0–360 degrees) to zodiac sign name."""
    sign_index = int(longitude // 30) % 12
    return SIGNS[sign_index]


def compute_julian_day(dt: datetime) -> float:
    """Convert a Python datetime (assumed UTC) to Julian Day number."""
    hour_fraction = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    return swe.julday(dt.year, dt.month, dt.day, hour_fraction)


def compute_planet_position(jd: float, planet: int) -> float:
    """Compute the ecliptic longitude of a planet at a given Julian Day.

    Args:
        jd: Julian Day number.
        planet: Swiss Ephemeris planet constant (e.g. swe.SUN, swe.MOON).

    Returns:
        Ecliptic longitude in degrees (0–360).
    """
    result = swe.calc_ut(jd, planet)
    return result[0][0]


def compute_rising_sign(jd: float, lat: float, lon: float) -> str:
    """Compute the Ascendant (rising sign) for a given time and location.

    Uses the Placidus house system. The Ascendant is the first element
    of the ascmc tuple returned by swe.houses().

    Args:
        jd: Julian Day number (requires birth time).
        lat: Geographic latitude in degrees.
        lon: Geographic longitude in degrees.

    Returns:
        The zodiac sign name of the Ascendant.
    """
    # swe.houses returns (cusps_tuple, ascmc_tuple)
    # ascmc[0] = Ascendant, ascmc[1] = MC, etc.
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    ascendant_longitude = ascmc[0]
    return ecliptic_longitude_to_sign(ascendant_longitude)


def _angle_diff(a: float, b: float) -> float:
    """Compute the smallest angular difference between two longitudes (0–180)."""
    diff = abs(a - b) % 360
    if diff > 180:
        diff = 360 - diff
    return diff


def compute_notable_transit(
    natal_sun_lon: float,
    natal_moon_lon: Optional[float],
    current_date: Optional[date] = None,
) -> Optional[str]:
    """Find the most notable current transit to natal sun or moon.

    Checks outer planets (Jupiter, Saturn, Uranus, Neptune) against natal
    sun and moon for major aspects (conjunction, opposition, square, trine).

    Args:
        natal_sun_lon: Ecliptic longitude of natal Sun.
        natal_moon_lon: Ecliptic longitude of natal Moon (or None).
        current_date: The date to compute current positions for.
                      Defaults to today (UTC).

    Returns:
        A human-readable transit string (e.g. "Saturn square natal Sun"),
        or None if no aspect is within orb.
    """
    if current_date is None:
        current_date = date.today()

    current_dt = datetime(current_date.year, current_date.month, current_date.day, 12, 0, 0)
    current_jd = compute_julian_day(current_dt)

    # Natal points to check: always Sun, Moon if available
    natal_points = [("Sun", natal_sun_lon)]
    if natal_moon_lon is not None:
        natal_points.append(("Moon", natal_moon_lon))

    # Find the tightest aspect
    best_transit = None
    best_orb = ASPECT_ORB  # only report aspects within our tolerance

    for planet_id, planet_name in TRANSIT_PLANETS:
        current_lon = compute_planet_position(current_jd, planet_id)

        for natal_name, natal_lon in natal_points:
            for aspect_angle, aspect_name in ASPECTS:
                orb = abs(_angle_diff(current_lon, natal_lon) - aspect_angle)
                if orb < best_orb:
                    best_orb = orb
                    best_transit = f"{planet_name} {aspect_name} natal {natal_name}"

    return best_transit


def _detect_moon_cusp(birth_date: date) -> tuple[str, bool]:
    """Compute the moon sign for a date and detect if it changes sign that day.

    When birth time is unknown, we check the Moon at midnight and end-of-day.
    If the Moon changes sign during the day, it's on the cusp.

    Args:
        birth_date: The birth date.

    Returns:
        Tuple of (moon_sign_at_noon, is_cusp).
        moon_sign_at_noon is the sign at noon UTC (our default).
        is_cusp is True if the Moon changes sign during the day.
    """
    # Check Moon at start and end of day
    dt_start = datetime(birth_date.year, birth_date.month, birth_date.day, 0, 0, 0)
    dt_end = datetime(birth_date.year, birth_date.month, birth_date.day, 23, 59, 59)
    dt_noon = datetime(birth_date.year, birth_date.month, birth_date.day, 12, 0, 0)

    jd_start = compute_julian_day(dt_start)
    jd_end = compute_julian_day(dt_end)
    jd_noon = compute_julian_day(dt_noon)

    moon_lon_start = compute_planet_position(jd_start, swe.MOON)
    moon_lon_end = compute_planet_position(jd_end, swe.MOON)
    moon_lon_noon = compute_planet_position(jd_noon, swe.MOON)

    sign_start = ecliptic_longitude_to_sign(moon_lon_start)
    sign_end = ecliptic_longitude_to_sign(moon_lon_end)
    sign_noon = ecliptic_longitude_to_sign(moon_lon_noon)

    is_cusp = sign_start != sign_end

    return sign_noon, is_cusp


# ---------- Main chart computation ----------

def compute_chart(
    cat_name: str,
    birth_date: Optional[date] = None,
    birth_time: Optional[str] = None,
    birth_location: Optional[tuple[float, float]] = None,
    behavior: Optional[str] = None,
    is_estimated: bool = False,
) -> dict:
    """Compute the astrological chart facts for a cat.

    Determines the degradation tier based on available inputs and computes
    all derivable positions. Returns the structured facts object consumed
    by the AI layer.

    Args:
        cat_name: The cat's name.
        birth_date: Birth date (or estimated date). None for mystery tier.
        birth_time: Birth time as "HH:MM" string (24h UTC). None if unknown.
        birth_location: Tuple of (latitude, longitude) in degrees. None if unknown.
        behavior: Optional behavior description for behavior reads.
        is_estimated: If True and birth_date is provided, marks as "estimated" tier
                      (e.g. gotcha day, guessed date).

    Returns:
        Structured facts dict matching the deterministic-to-AI contract.
    """
    # ---------- Determine tier ----------
    if birth_date is None:
        chart_tier = "mystery"
    elif birth_time is not None and birth_location is not None:
        chart_tier = "full"
    elif is_estimated:
        chart_tier = "estimated"
    else:
        chart_tier = "date_only"

    # ---------- Initialize facts ----------
    facts = {
        "cat_name": cat_name,
        "chart_tier": chart_tier,
        "sun": None,
        "moon": None,
        "moon_cusp": False,
        "rising": None,
        "notable_transit": None,
        "tz_assumption": None,
        "behavior": behavior,
    }

    # ---------- Mystery tier: minimal computation ----------
    if chart_tier == "mystery":
        # Nothing reliably derivable without a date.
        # tz_assumption not applicable.
        return facts

    # ---------- Build datetime for computation ----------
    if birth_time is not None:
        parts = birth_time.split(":")
        hour, minute = int(parts[0]), int(parts[1])
        dt = datetime(birth_date.year, birth_date.month, birth_date.day, hour, minute, 0)
        facts["tz_assumption"] = None  # exact time given
    else:
        # Default: noon UTC (R3.6)
        dt = datetime(birth_date.year, birth_date.month, birth_date.day, 12, 0, 0)
        facts["tz_assumption"] = "noon UTC"

    jd = compute_julian_day(dt)

    # ---------- Sun sign (always computable with a date) ----------
    sun_lon = compute_planet_position(jd, swe.SUN)
    facts["sun"] = ecliptic_longitude_to_sign(sun_lon)

    # ---------- Moon sign + cusp detection ----------
    if birth_time is not None:
        # Exact time: Moon is unambiguous
        moon_lon = compute_planet_position(jd, swe.MOON)
        facts["moon"] = ecliptic_longitude_to_sign(moon_lon)
        facts["moon_cusp"] = False
    else:
        # No birth time: check if Moon changes sign during the day
        moon_sign, is_cusp = _detect_moon_cusp(birth_date)
        facts["moon"] = moon_sign
        facts["moon_cusp"] = is_cusp

    # ---------- Rising sign (full tier only) ----------
    if chart_tier == "full" and birth_location is not None:
        lat, lon = birth_location
        facts["rising"] = compute_rising_sign(jd, lat, lon)

    # ---------- Notable transit ----------
    natal_moon_lon = None
    if not facts["moon_cusp"] and facts["moon"] is not None:
        # Use moon longitude for transit check only when unambiguous
        moon_dt = dt
        moon_jd = compute_julian_day(moon_dt)
        natal_moon_lon = compute_planet_position(moon_jd, swe.MOON)

    facts["notable_transit"] = compute_notable_transit(
        natal_sun_lon=sun_lon,
        natal_moon_lon=natal_moon_lon,
    )

    return facts


# ---------- Self-test ----------

if __name__ == "__main__":
    from datetime import date

    print("=" * 60)
    print("Madame Minou — Chart Engine Self-Test")
    print("=" * 60)

    # --- Tier: full ---
    print("\n--- FULL TIER ---")
    full_facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),  # Paris
        behavior=None,
    )
    for k, v in full_facts.items():
        print(f"  {k}: {v}")

    # --- Tier: date_only ---
    print("\n--- DATE_ONLY TIER ---")
    date_facts = compute_chart(
        cat_name="Mochi",
        birth_date=date(2019, 3, 21),
    )
    for k, v in date_facts.items():
        print(f"  {k}: {v}")

    # --- Tier: estimated ---
    print("\n--- ESTIMATED TIER ---")
    est_facts = compute_chart(
        cat_name="Shadow",
        birth_date=date(2021, 10, 1),
        is_estimated=True,
    )
    for k, v in est_facts.items():
        print(f"  {k}: {v}")

    # --- Tier: mystery ---
    print("\n--- MYSTERY TIER ---")
    mystery_facts = compute_chart(
        cat_name="Ghost",
        birth_date=None,
    )
    for k, v in mystery_facts.items():
        print(f"  {k}: {v}")

    # --- Behavior read example ---
    print("\n--- BEHAVIOR READ (full tier) ---")
    behavior_facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
        behavior="won't cuddle lately",
    )
    for k, v in behavior_facts.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 60)
    print("All tiers exercised successfully.")
    print("=" * 60)
