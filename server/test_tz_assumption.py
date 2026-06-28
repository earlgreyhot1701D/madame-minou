"""
Test: R3.6 — Noon-UTC default timezone assumption and tz_assumption recording.

Verifies:
  1. tz_assumption is "noon UTC" for date_only and estimated tiers
  2. tz_assumption is None for full tier (exact time given)
  3. tz_assumption is None for mystery tier (no date at all)
  4. Reproducibility: same date always produces the same chart positions
     regardless of when the test is run (noon UTC is deterministic)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from server.chart_engine import compute_chart


def test_tz_assumption_full_tier():
    """Full tier (birth_time + location provided) → tz_assumption is None."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
    )
    assert facts["chart_tier"] == "full"
    assert facts["tz_assumption"] is None, (
        f"Full tier should have tz_assumption=None, got {facts['tz_assumption']!r}"
    )


def test_tz_assumption_date_only_tier():
    """Date-only tier (no time, no location) → tz_assumption is 'noon UTC'."""
    facts = compute_chart(
        cat_name="Mochi",
        birth_date=date(2019, 3, 21),
    )
    assert facts["chart_tier"] == "date_only"
    assert facts["tz_assumption"] == "noon UTC", (
        f"Date-only tier should have tz_assumption='noon UTC', got {facts['tz_assumption']!r}"
    )


def test_tz_assumption_estimated_tier():
    """Estimated tier (guessed date, is_estimated=True) → tz_assumption is 'noon UTC'."""
    facts = compute_chart(
        cat_name="Shadow",
        birth_date=date(2021, 10, 1),
        is_estimated=True,
    )
    assert facts["chart_tier"] == "estimated"
    assert facts["tz_assumption"] == "noon UTC", (
        f"Estimated tier should have tz_assumption='noon UTC', got {facts['tz_assumption']!r}"
    )


def test_tz_assumption_mystery_tier():
    """Mystery tier (no date at all) → tz_assumption is None (not applicable)."""
    facts = compute_chart(
        cat_name="Ghost",
        birth_date=None,
    )
    assert facts["chart_tier"] == "mystery"
    assert facts["tz_assumption"] is None, (
        f"Mystery tier should have tz_assumption=None, got {facts['tz_assumption']!r}"
    )


def test_reproducibility_same_date_same_result():
    """R3.6 reproducibility: calling compute_chart with the same date always
    yields the same sun and moon signs — noon UTC is deterministic."""
    fixed_date = date(2018, 7, 4)

    result_1 = compute_chart(cat_name="TestCat", birth_date=fixed_date)
    result_2 = compute_chart(cat_name="TestCat", birth_date=fixed_date)

    # Sun sign must be identical across calls
    assert result_1["sun"] == result_2["sun"], (
        f"Sun sign mismatch: {result_1['sun']} vs {result_2['sun']}"
    )
    # Moon sign must be identical across calls
    assert result_1["moon"] == result_2["moon"], (
        f"Moon sign mismatch: {result_1['moon']} vs {result_2['moon']}"
    )
    # Moon cusp flag must be identical
    assert result_1["moon_cusp"] == result_2["moon_cusp"], (
        f"Moon cusp mismatch: {result_1['moon_cusp']} vs {result_2['moon_cusp']}"
    )
    # tz_assumption must be "noon UTC" both times
    assert result_1["tz_assumption"] == "noon UTC"
    assert result_2["tz_assumption"] == "noon UTC"


def test_reproducibility_known_date():
    """Verify a known date always gives the same expected sign (regression-guard).
    July 4 2018 at noon UTC → Sun in Cancer (longitude ~102°, Cancer = 90-120°)."""
    facts = compute_chart(cat_name="Firecracker", birth_date=date(2018, 7, 4))
    assert facts["sun"] == "Cancer", (
        f"July 4 should be Cancer, got {facts['sun']}"
    )
    assert facts["tz_assumption"] == "noon UTC"


def test_date_only_with_time_but_no_location():
    """If birth_time is given but location is missing, tier is date_only.
    tz_assumption should be None because an exact time IS provided."""
    facts = compute_chart(
        cat_name="TimeNoPlace",
        birth_date=date(2020, 1, 15),
        birth_time="14:00",
        birth_location=None,
    )
    # With time but no location → date_only tier (no rising possible)
    assert facts["chart_tier"] == "date_only"
    # But the time was exact, so tz_assumption should be None
    assert facts["tz_assumption"] is None, (
        f"When birth_time is provided, tz_assumption should be None, got {facts['tz_assumption']!r}"
    )


# ---------- Run ----------

if __name__ == "__main__":
    tests = [
        test_tz_assumption_full_tier,
        test_tz_assumption_date_only_tier,
        test_tz_assumption_estimated_tier,
        test_tz_assumption_mystery_tier,
        test_reproducibility_same_date_same_result,
        test_reproducibility_known_date,
        test_date_only_with_time_but_no_location,
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
