"""
Test: R3.1, R3.7 — Degradation tier tests for the chart engine.

Verifies each tier (full / date_only / estimated / mystery) produces
correct positions using known astronomical fixtures, returns the
correct contract shape, and is deterministic (same inputs → same output).

Fixtures are pre-verified against pyswisseph:
  - 2020-06-15 08:30 UTC at Paris (48.8566, 2.3522): Sun=Gemini, Moon=Aries, Rising=Leo
  - 2019-03-21 noon UTC (vernal equinox): Sun=Aries, Moon=Libra (cusp day)
  - 2020-06-15 noon UTC: Sun=Gemini, Moon=Aries, moon_cusp=False
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from server.chart_engine import compute_chart


# ---------- Contract shape constants ----------

REQUIRED_KEYS = {
    "cat_name", "chart_tier", "sun", "moon", "moon_cusp",
    "rising", "notable_transit", "tz_assumption", "behavior",
}


# ============================================================
# 1. FULL TIER TESTS
# ============================================================

def test_full_tier_known_fixture_paris():
    """R3.7: Full tier for cat born 2020-06-15 at 08:30 in Paris.
    Known positions: Sun=Gemini, Moon=Aries, Rising=Leo."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
    )
    assert facts["chart_tier"] == "full"
    assert facts["sun"] == "Gemini"
    assert facts["moon"] == "Aries"
    assert facts["rising"] == "Leo"
    assert facts["notable_transit"] is not None, (
        "Full tier with valid natal positions should compute a transit"
    )


def test_full_tier_contract_shape():
    """R3.7: Full tier facts object has all required keys."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
    )
    assert set(facts.keys()) == REQUIRED_KEYS, (
        f"Key mismatch. Missing: {REQUIRED_KEYS - set(facts.keys())}, "
        f"Extra: {set(facts.keys()) - REQUIRED_KEYS}"
    )


def test_full_tier_behavior_passthrough():
    """R3.7: Behavior field passes through correctly in full tier."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
        behavior="loves boxes",
    )
    assert facts["behavior"] == "loves boxes"


def test_full_tier_no_behavior():
    """R3.7: Without behavior, the field is None."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
    )
    assert facts["behavior"] is None


def test_full_tier_moon_cusp_always_false():
    """R3.2: Full tier always has moon_cusp=False (exact time resolves ambiguity)."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
    )
    assert facts["moon_cusp"] is False


def test_full_tier_tz_assumption_none():
    """R3.6: Full tier with exact time has tz_assumption=None."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
    )
    assert facts["tz_assumption"] is None


# ============================================================
# 2. DATE_ONLY TIER TESTS
# ============================================================

def test_date_only_equinox_fixture():
    """R3.3: Date-only for 2019-03-21 (vernal equinox at noon UTC).
    Known: Sun=Aries, Moon=Libra (cusp day), Rising=None."""
    facts = compute_chart(cat_name="Equinox", birth_date=date(2019, 3, 21))
    assert facts["chart_tier"] == "date_only"
    assert facts["sun"] == "Aries"
    assert facts["moon"] == "Libra"
    assert facts["moon_cusp"] is True
    assert facts["rising"] is None


def test_date_only_gemini_fixture():
    """R3.3: Date-only for 2020-06-15.
    Known: Sun=Gemini, Moon=Aries, moon_cusp=False, Rising=None."""
    facts = compute_chart(cat_name="Mochi", birth_date=date(2020, 6, 15))
    assert facts["chart_tier"] == "date_only"
    assert facts["sun"] == "Gemini"
    assert facts["moon"] == "Aries"
    assert facts["moon_cusp"] is False
    assert facts["rising"] is None


def test_date_only_tz_assumption():
    """R3.6: Date-only tier records tz_assumption='noon UTC'."""
    facts = compute_chart(cat_name="Mochi", birth_date=date(2020, 6, 15))
    assert facts["tz_assumption"] == "noon UTC"


def test_date_only_notable_transit_computed():
    """R3.7: Date-only tier still computes notable_transit (using today's transits)."""
    facts = compute_chart(cat_name="Mochi", birth_date=date(2020, 6, 15))
    # Transit depends on today's date, so just verify it's a string or None
    assert facts["notable_transit"] is None or isinstance(facts["notable_transit"], str)


# ============================================================
# 3. ESTIMATED TIER TESTS
# ============================================================

def test_estimated_tier_classification():
    """R3.5: is_estimated=True with a birth_date → chart_tier='estimated'."""
    facts = compute_chart(
        cat_name="Shadow",
        birth_date=date(2020, 6, 15),
        is_estimated=True,
    )
    assert facts["chart_tier"] == "estimated"


def test_estimated_tier_positions_match_date_only():
    """R3.5: Estimated tier computes the same positions as date_only for same date.
    The only difference is the chart_tier label."""
    date_only = compute_chart(cat_name="A", birth_date=date(2020, 6, 15))
    estimated = compute_chart(cat_name="A", birth_date=date(2020, 6, 15), is_estimated=True)

    assert date_only["sun"] == estimated["sun"]
    assert date_only["moon"] == estimated["moon"]
    assert date_only["moon_cusp"] == estimated["moon_cusp"]
    assert date_only["rising"] == estimated["rising"]
    assert date_only["notable_transit"] == estimated["notable_transit"]
    assert date_only["tz_assumption"] == estimated["tz_assumption"]


def test_estimated_tier_rising_none():
    """R3.3: Estimated tier never computes rising (no time/location)."""
    facts = compute_chart(
        cat_name="Shadow",
        birth_date=date(2020, 6, 15),
        is_estimated=True,
    )
    assert facts["rising"] is None


def test_estimated_tier_known_positions():
    """R3.5: Estimated tier for 2020-06-15 still yields Sun=Gemini, Moon=Aries."""
    facts = compute_chart(
        cat_name="Shadow",
        birth_date=date(2020, 6, 15),
        is_estimated=True,
    )
    assert facts["sun"] == "Gemini"
    assert facts["moon"] == "Aries"
    assert facts["moon_cusp"] is False


# ============================================================
# 4. MYSTERY TIER TESTS
# ============================================================

def test_mystery_tier_no_date():
    """R3.5: No birth_date → mystery tier with all positions None."""
    facts = compute_chart(cat_name="Ghost", birth_date=None)
    assert facts["chart_tier"] == "mystery"
    assert facts["sun"] is None
    assert facts["moon"] is None
    assert facts["rising"] is None
    assert facts["moon_cusp"] is False
    assert facts["notable_transit"] is None


def test_mystery_tier_cat_name_passes_through():
    """R3.7: Mystery tier still includes cat_name in facts."""
    facts = compute_chart(cat_name="Phantom", birth_date=None)
    assert facts["cat_name"] == "Phantom"


def test_mystery_tier_tz_assumption_none():
    """R3.6: Mystery tier has tz_assumption=None (no date, no assumption needed)."""
    facts = compute_chart(cat_name="Ghost", birth_date=None)
    assert facts["tz_assumption"] is None


# ============================================================
# 5. CONTRACT SHAPE TESTS (all tiers)
# ============================================================

def test_contract_shape_full_tier():
    """R3.7: Full tier produces exactly the required keys, no more, no less."""
    facts = compute_chart(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
    )
    assert set(facts.keys()) == REQUIRED_KEYS


def test_contract_shape_date_only_tier():
    """R3.7: Date-only tier produces exactly the required keys."""
    facts = compute_chart(cat_name="Mochi", birth_date=date(2020, 6, 15))
    assert set(facts.keys()) == REQUIRED_KEYS


def test_contract_shape_estimated_tier():
    """R3.7: Estimated tier produces exactly the required keys."""
    facts = compute_chart(
        cat_name="Shadow",
        birth_date=date(2020, 6, 15),
        is_estimated=True,
    )
    assert set(facts.keys()) == REQUIRED_KEYS


def test_contract_shape_mystery_tier():
    """R3.7: Mystery tier produces exactly the required keys."""
    facts = compute_chart(cat_name="Ghost", birth_date=None)
    assert set(facts.keys()) == REQUIRED_KEYS


# ============================================================
# 6. DETERMINISM TESTS (R3.1)
# ============================================================

def test_determinism_full_tier():
    """R3.1: Same full-tier inputs called twice → identical outputs."""
    kwargs = dict(
        cat_name="Biscuit",
        birth_date=date(2020, 6, 15),
        birth_time="08:30",
        birth_location=(48.8566, 2.3522),
        behavior="loves boxes",
    )
    result_1 = compute_chart(**kwargs)
    result_2 = compute_chart(**kwargs)
    assert result_1 == result_2, (
        f"Full tier not deterministic.\nCall 1: {result_1}\nCall 2: {result_2}"
    )


def test_determinism_date_only_tier():
    """R3.1: Same date-only inputs called twice → identical outputs."""
    kwargs = dict(cat_name="Mochi", birth_date=date(2020, 6, 15))
    result_1 = compute_chart(**kwargs)
    result_2 = compute_chart(**kwargs)
    assert result_1 == result_2, (
        f"Date-only tier not deterministic.\nCall 1: {result_1}\nCall 2: {result_2}"
    )


def test_determinism_estimated_tier():
    """R3.1: Same estimated inputs called twice → identical outputs."""
    kwargs = dict(cat_name="Shadow", birth_date=date(2020, 6, 15), is_estimated=True)
    result_1 = compute_chart(**kwargs)
    result_2 = compute_chart(**kwargs)
    assert result_1 == result_2, (
        f"Estimated tier not deterministic.\nCall 1: {result_1}\nCall 2: {result_2}"
    )


def test_determinism_mystery_tier():
    """R3.1: Same mystery inputs called twice → identical outputs."""
    kwargs = dict(cat_name="Ghost", birth_date=None)
    result_1 = compute_chart(**kwargs)
    result_2 = compute_chart(**kwargs)
    assert result_1 == result_2, (
        f"Mystery tier not deterministic.\nCall 1: {result_1}\nCall 2: {result_2}"
    )


# ---------- Run ----------

if __name__ == "__main__":
    tests = [
        # Full tier
        test_full_tier_known_fixture_paris,
        test_full_tier_contract_shape,
        test_full_tier_behavior_passthrough,
        test_full_tier_no_behavior,
        test_full_tier_moon_cusp_always_false,
        test_full_tier_tz_assumption_none,
        # Date only
        test_date_only_equinox_fixture,
        test_date_only_gemini_fixture,
        test_date_only_tz_assumption,
        test_date_only_notable_transit_computed,
        # Estimated
        test_estimated_tier_classification,
        test_estimated_tier_positions_match_date_only,
        test_estimated_tier_rising_none,
        test_estimated_tier_known_positions,
        # Mystery
        test_mystery_tier_no_date,
        test_mystery_tier_cat_name_passes_through,
        test_mystery_tier_tz_assumption_none,
        # Contract shape
        test_contract_shape_full_tier,
        test_contract_shape_date_only_tier,
        test_contract_shape_estimated_tier,
        test_contract_shape_mystery_tier,
        # Determinism
        test_determinism_full_tier,
        test_determinism_date_only_tier,
        test_determinism_estimated_tier,
        test_determinism_mystery_tier,
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
