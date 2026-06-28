"""
Test: R3.4 — Moon-cusp detection for ambiguous moon sign days.
Test: R3.2, R3.3 — Rising sign computed only when time + location present.

Verifies:
  1. Moon cusp is True when the Moon changes zodiac sign during the day.
  2. Moon cusp is False when the Moon stays in one sign all day.
  3. The Pisces→Aries (360°→0°) boundary wrap is handled correctly.
  4. Full tier (birth time known) always reports moon_cusp=False (time is exact).
  5. Rising sign is not None only in the full tier.
  6. Rising sign is None for date_only, estimated, and mystery tiers.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from server.chart_engine import compute_chart, _detect_moon_cusp


# ---------- Moon cusp detection (R3.4) ----------

def test_moon_cusp_detected_on_sign_change_day():
    """R3.4: On a day when the Moon changes sign, moon_cusp should be True.
    2024-06-28: Moon goes from Pisces (354.77°) to Aries (8.91°) during the day."""
    sign, is_cusp = _detect_moon_cusp(date(2024, 6, 28))
    assert is_cusp is True, (
        f"Expected cusp=True on 2024-06-28 (Moon crosses Pisces→Aries), got {is_cusp}"
    )
    assert sign == "Aries", (
        f"Expected noon sign='Aries', got '{sign}'"
    )


def test_moon_cusp_false_on_stable_day():
    """R3.4: On a day when the Moon stays in one sign, moon_cusp should be False.
    2024-06-10: Moon stays in Leo all day."""
    sign, is_cusp = _detect_moon_cusp(date(2024, 6, 10))
    assert is_cusp is False, (
        f"Expected cusp=False on 2024-06-10 (Moon stays in Leo), got {is_cusp}"
    )
    assert sign == "Leo", (
        f"Expected noon sign='Leo', got '{sign}'"
    )


def test_moon_cusp_another_sign_change():
    """R3.4: Additional cusp detection on a different sign transition.
    2024-06-01: Moon changes sign (Pisces→Aries boundary area) during the day."""
    sign, is_cusp = _detect_moon_cusp(date(2024, 6, 1))
    assert is_cusp is True, (
        f"Expected cusp=True on 2024-06-01, got {is_cusp}"
    )


def test_moon_cusp_another_stable_day():
    """R3.4: Additional stable day check.
    2024-06-02: Moon stays in Aries all day."""
    sign, is_cusp = _detect_moon_cusp(date(2024, 6, 2))
    assert is_cusp is False, (
        f"Expected cusp=False on 2024-06-02, got {is_cusp}"
    )
    assert sign == "Aries", (
        f"Expected noon sign='Aries', got '{sign}'"
    )


def test_moon_cusp_pisces_aries_boundary():
    """R3.4 edge case: Moon wrapping from Pisces (near 360°) → Aries (near 0°).
    2024-06-28: start=354.77° (Pisces), end=8.91° (Aries). The 360°/0° wrap
    must not confuse the sign comparison."""
    sign, is_cusp = _detect_moon_cusp(date(2024, 6, 28))
    assert is_cusp is True, (
        f"Pisces→Aries wrap on 2024-06-28 should be detected as cusp"
    )


# ---------- Moon cusp via compute_chart (integration) ----------

def test_compute_chart_date_only_cusp_day():
    """R3.4 via compute_chart: date_only tier on a cusp day reports moon_cusp=True."""
    facts = compute_chart(cat_name="Luna", birth_date=date(2024, 6, 28))
    assert facts["chart_tier"] == "date_only"
    assert facts["moon_cusp"] is True, (
        f"Expected moon_cusp=True for date_only on cusp day, got {facts['moon_cusp']}"
    )
    assert facts["moon"] == "Aries"


def test_compute_chart_date_only_stable_day():
    """R3.4 via compute_chart: date_only tier on a stable day reports moon_cusp=False."""
    facts = compute_chart(cat_name="Luna", birth_date=date(2024, 6, 10))
    assert facts["chart_tier"] == "date_only"
    assert facts["moon_cusp"] is False, (
        f"Expected moon_cusp=False for date_only on stable day, got {facts['moon_cusp']}"
    )
    assert facts["moon"] == "Leo"


def test_compute_chart_full_tier_ignores_cusp():
    """R3.2: Full tier with exact birth time always sets moon_cusp=False
    (time resolves any ambiguity), even on a day the Moon changes sign."""
    facts = compute_chart(
        cat_name="Luna",
        birth_date=date(2024, 6, 28),  # cusp day
        birth_time="14:00",
        birth_location=(40.7128, -74.0060),  # NYC
    )
    assert facts["chart_tier"] == "full"
    assert facts["moon_cusp"] is False, (
        f"Full tier should always have moon_cusp=False, got {facts['moon_cusp']}"
    )


# ---------- Rising sign = None when time/location absent (R3.2, R3.3) ----------

def test_rising_computed_for_full_tier():
    """R3.2: Full tier (date + time + location) computes a rising sign."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),  # Paris
    )
    assert facts["chart_tier"] == "full"
    assert facts["rising"] is not None, (
        f"Full tier should compute rising sign, got None"
    )
    assert facts["rising"] == "Leo", (
        f"Expected rising='Leo' for Biscuit on 2020-06-15 08:30 Paris, got '{facts['rising']}'"
    )


def test_rising_null_for_date_only_tier():
    """R3.3: Date-only tier (no time, no location) → rising is None."""
    facts = compute_chart(cat_name="Mochi", birth_date=date(2019, 3, 21))
    assert facts["chart_tier"] == "date_only"
    assert facts["rising"] is None, (
        f"Date-only tier should have rising=None, got {facts['rising']!r}"
    )


def test_rising_null_for_estimated_tier():
    """R3.3: Estimated tier (guessed date) → rising is None."""
    facts = compute_chart(
        cat_name="Shadow",
        birth_date=date(2021, 10, 1),
        is_estimated=True,
    )
    assert facts["chart_tier"] == "estimated"
    assert facts["rising"] is None, (
        f"Estimated tier should have rising=None, got {facts['rising']!r}"
    )


def test_rising_null_for_mystery_tier():
    """R3.3: Mystery tier (no date at all) → rising is None."""
    facts = compute_chart(cat_name="Ghost", birth_date=None)
    assert facts["chart_tier"] == "mystery"
    assert facts["rising"] is None, (
        f"Mystery tier should have rising=None, got {facts['rising']!r}"
    )


def test_rising_null_when_time_given_but_no_location():
    """R3.3: Rising requires BOTH time and location. Time alone is not enough."""
    facts = compute_chart(
        cat_name="TimeOnly",
        birth_date=date(2020, 1, 15),
        birth_time="14:00",
        birth_location=None,
    )
    assert facts["chart_tier"] == "date_only"
    assert facts["rising"] is None, (
        f"Rising requires location too; should be None, got {facts['rising']!r}"
    )


# ---------- Run ----------

if __name__ == "__main__":
    tests = [
        test_moon_cusp_detected_on_sign_change_day,
        test_moon_cusp_false_on_stable_day,
        test_moon_cusp_another_sign_change,
        test_moon_cusp_another_stable_day,
        test_moon_cusp_pisces_aries_boundary,
        test_compute_chart_date_only_cusp_day,
        test_compute_chart_date_only_stable_day,
        test_compute_chart_full_tier_ignores_cusp,
        test_rising_computed_for_full_tier,
        test_rising_null_for_date_only_tier,
        test_rising_null_for_estimated_tier,
        test_rising_null_for_mystery_tier,
        test_rising_null_when_time_given_but_no_location,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print(f"{'='*60}")

    if failed:
        sys.exit(1)
