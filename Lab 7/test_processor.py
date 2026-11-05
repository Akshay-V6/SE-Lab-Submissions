"""Hypothesis property tests for the scholarship application processor."""

import pytest
from hypothesis import given, strategies as st

from processor import award_amount, application_status, is_eligible

CATEGORIES = ("merit", "sports", "arts")
INCOME_LEVELS = ("low", "medium", "high")


@given(
    category=st.sampled_from(CATEGORIES),
    marks=st.integers(min_value=0, max_value=100),
    income_level=st.sampled_from(INCOME_LEVELS),
    is_renewal=st.booleans(),
)
def test_award_amount_matches_rules_for_valid_inputs(
    category, marks, income_level, is_renewal
):
    cutoffs = {"merit": 75, "sports": 60, "arts": 65}
    cutoff = cutoffs[category]
    if is_renewal and category != "sports":
        cutoff -= 5
    above_cutoff = max(0, marks - cutoff)
    if income_level == "low":
        rate = 100
    else:
        rate = 60
    if above_cutoff > 15:
        rate += 40
        if income_level == "low":
            rate += 20
    assert award_amount(category, marks, income_level, is_renewal) == (
        above_cutoff * rate
    )


@given(marks=st.integers(min_value=101, max_value=10_000))
def test_award_amount_rejects_marks_above_100(marks):
    with pytest.raises(ValueError):
        award_amount("merit", marks, "low", False)


@given(
    attendance=st.integers(min_value=0, max_value=100),
    backlogs=st.integers(min_value=0, max_value=20),
    is_special_quota=st.booleans(),
)
def test_eligibility_matches_rules_for_valid_inputs(
    attendance, backlogs, is_special_quota
):
    expected = backlogs <= 2 if is_special_quota else (
        attendance >= 75 and backlogs <= 1
    )
    assert is_eligible(attendance, backlogs, is_special_quota) is expected


@given(attendance=st.integers(min_value=101, max_value=10_000))
def test_eligibility_rejects_attendance_above_100(attendance):
    with pytest.raises(ValueError):
        is_eligible(attendance, 0, False)


@given(
    days_left=st.integers(min_value=0, max_value=365),
    is_renewal=st.booleans(),
    is_paper=st.booleans(),
)
def test_application_status_matches_rules_for_valid_inputs(
    days_left, is_renewal, is_paper
):
    cutoff = 30 if is_renewal else 20
    if is_paper:
        cutoff += 10
    expected = "open" if days_left >= cutoff else (
        "closing" if days_left >= cutoff - 15 else "closed"
    )
    assert application_status(days_left, is_renewal, is_paper) == expected


@given(days_left=st.integers(max_value=-1))
def test_application_status_rejects_negative_days_left(days_left):
    with pytest.raises(ValueError):
        application_status(days_left, False, False)

INVALID_SCALARS = st.one_of(
    st.floats(allow_nan=True, allow_infinity=True),
    st.text(),
    st.none(),
    st.booleans(),
)


@given(marks=INVALID_SCALARS)
def test_award_amount_rejects_non_integer_marks(marks):
    with pytest.raises(ValueError):
        award_amount("merit", marks, "low", False)


@given(income_level=st.text().filter(lambda value: value not in INCOME_LEVELS))
def test_award_amount_rejects_unknown_income_level(income_level):
    with pytest.raises(ValueError):
        award_amount("merit", 90, income_level, False)


@given(is_renewal=st.one_of(st.integers(), st.text(), st.none()))
def test_award_amount_rejects_non_boolean_renewal(is_renewal):
    with pytest.raises(ValueError):
        award_amount("merit", 90, "low", is_renewal)


@given(attendance=INVALID_SCALARS)
def test_eligibility_rejects_non_integer_attendance(attendance):
    with pytest.raises(ValueError):
        is_eligible(attendance, 0, False)


@given(backlogs=st.one_of(st.integers(max_value=-1), st.floats(), st.text(), st.none(), st.booleans()))
def test_eligibility_rejects_invalid_backlog_counts(backlogs):
    with pytest.raises(ValueError):
        is_eligible(90, backlogs, False)


@given(is_special_quota=st.one_of(st.integers(), st.text(), st.none()))
def test_eligibility_rejects_non_boolean_quota(is_special_quota):
    with pytest.raises(ValueError):
        is_eligible(90, 0, is_special_quota)


@given(days_left=INVALID_SCALARS)
def test_application_status_rejects_non_integer_days(days_left):
    with pytest.raises(ValueError):
        application_status(days_left, False, False)


@given(is_renewal=st.one_of(st.integers(), st.text(), st.none()))
def test_application_status_rejects_non_boolean_renewal(is_renewal):
    with pytest.raises(ValueError):
        application_status(30, is_renewal, False)


@given(is_paper=st.one_of(st.integers(), st.text(), st.none()))
def test_application_status_rejects_non_boolean_paper_flag(is_paper):
    with pytest.raises(ValueError):
        application_status(30, False, is_paper)

@given(category=st.one_of(st.integers(), st.none(), st.lists(st.text(), max_size=3)))
def test_award_amount_rejects_non_string_category(category):
    with pytest.raises(ValueError):
        award_amount(category, 90, "low", False)


@given(marks=st.integers(max_value=-1))
def test_award_amount_rejects_negative_marks(marks):
    with pytest.raises(ValueError):
        award_amount("merit", marks, "low", False)


@given(attendance=st.integers(max_value=-1))
def test_eligibility_rejects_negative_attendance(attendance):
    with pytest.raises(ValueError):
        is_eligible(attendance, 0, False)
