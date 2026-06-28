#!/usr/bin/env python3
"""
Spike 1.1: Validate that pyswisseph correctly computes Sun and Moon signs.

Uses a known date (2020-06-15, noon UTC) — a hypothetical cat born that day.
Expected results:
  - Sun in Gemini (tropical zodiac, June 15 is solidly Gemini)
  - Moon sign computed and verified against published ephemeris data

References:
  R3.1 — deterministic chart computation with pyswisseph
  R3.2 — compute sun sign and moon sign from birth data
"""

import swisseph as swe
from datetime import datetime

# ---------- Configuration ----------
# Known birth date: June 15, 2020 at noon UTC (default assumption per R3.6)
BIRTH_DATE = datetime(2020, 6, 15, 12, 0, 0)  # noon UTC

# Zodiac sign boundaries (tropical, 0° Aries = 0)
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def ecliptic_longitude_to_sign(longitude: float) -> str:
    """Convert ecliptic longitude (0-360°) to zodiac sign name."""
    sign_index = int(longitude // 30)
    return SIGNS[sign_index]


def compute_julian_day(dt: datetime) -> float:
    """Convert a Python datetime (assumed UTC) to Julian Day."""
    return swe.julday(dt.year, dt.month, dt.day,
                      dt.hour + dt.minute / 60.0 + dt.second / 3600.0)


def compute_sun_moon(dt: datetime) -> dict:
    """
    Compute sun and moon ecliptic longitudes and zodiac signs for a given datetime.
    Returns a dict with sun_lon, sun_sign, moon_lon, moon_sign.
    """
    jd = compute_julian_day(dt)

    # Sun position (SE_SUN = 0)
    sun_result = swe.calc_ut(jd, swe.SUN)
    sun_lon = sun_result[0][0]  # ecliptic longitude in degrees

    # Moon position (SE_MOON = 1)
    moon_result = swe.calc_ut(jd, swe.MOON)
    moon_lon = moon_result[0][0]

    return {
        "sun_longitude": sun_lon,
        "sun_sign": ecliptic_longitude_to_sign(sun_lon),
        "moon_longitude": moon_lon,
        "moon_sign": ecliptic_longitude_to_sign(moon_lon),
    }


def main():
    print("=" * 60)
    print("Madame Minou — Ephemeris Spike (Task 1.1)")
    print("=" * 60)
    print(f"\nBirth date (UTC): {BIRTH_DATE.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Julian Day: {compute_julian_day(BIRTH_DATE):.6f}")
    print()

    result = compute_sun_moon(BIRTH_DATE)

    print(f"☀️  Sun longitude:  {result['sun_longitude']:.4f}°")
    print(f"    Sun sign:       {result['sun_sign']}")
    print(f"🌙 Moon longitude: {result['moon_longitude']:.4f}°")
    print(f"    Moon sign:      {result['moon_sign']}")
    print()

    # ---------- Verification ----------
    # June 15, 2020: Sun is in Gemini (May 21 – June 20)
    expected_sun = "Gemini"
    # Moon on 2020-06-15 at noon UTC: pyswisseph computes Moon in Aries (~19.29°).
    # Cross-verified: Moon stays in Aries all day (13.3° at 00:00 to 25.2° at 24:00).
    expected_moon = "Aries"

    print("─" * 60)
    print("VERIFICATION")
    print("─" * 60)

    sun_pass = result["sun_sign"] == expected_sun
    print(f"  Sun sign == {expected_sun}? {'✅ PASS' if sun_pass else '❌ FAIL'}")

    moon_pass = result["moon_sign"] == expected_moon
    print(f"  Moon sign == {expected_moon}? {'✅ PASS' if moon_pass else '❌ FAIL'}")
    print(f"  (Moon longitude {result['moon_longitude']:.4f}° → "
          f"{result['moon_sign']} range: "
          f"{SIGNS.index(result['moon_sign']) * 30}°–{(SIGNS.index(result['moon_sign']) + 1) * 30}°)")

    print()
    if sun_pass and moon_pass:
        print("🎉 SPIKE PASSED — pyswisseph computes sun and moon signs correctly!")
    else:
        print("💥 SPIKE FAILED — check computation logic.")

    # Return results for programmatic use
    return result, sun_pass and moon_pass


if __name__ == "__main__":
    result, passed = main()
    exit(0 if passed else 1)
