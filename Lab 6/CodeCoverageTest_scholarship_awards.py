import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# --- Tests for award_amount ---
def test_unknown_category_raises_value_error():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("engineering", 85, "low", False)


def test_invalid_negative_marks_raises_value_error():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -5, "low", False)


def test_marks_below_or_equal_cutoff():
    assert award_amount("merit", 70, "low", False) == 0


def test_award_amount_low_income_high_score_with_renewal():
    # merit cutoff = 75; renewal reduces cutoff to 70
    # above = 95 - 70 = 25 (> 15)
    # rate = 100 + 40 + 20 = 160
    assert award_amount("merit", 95, "low", True) == 25 * 160


def test_award_amount_general_income_low_score_no_renewal():
    # sports cutoff = 60
    # above = 70 - 60 = 10 (<= 15)
    # rate = 60
    assert award_amount("sports", 70, "high", False) == 10 * 60


# --- Tests for is_eligible ---
def test_is_eligible_special_quota():
    assert is_eligible(attendance=50, backlogs=2, is_special_quota=True) is True


def test_is_eligible_low_attendance():
    assert is_eligible(attendance=60, backlogs=0, is_special_quota=False) is False


def test_is_eligible_regular_quota_eligible():
    assert is_eligible(attendance=80, backlogs=1, is_special_quota=False) is True


# --- Tests for application_status ---
def test_application_status_renewal_open():
    # cutoff = 30; days_left = 35 >= 30 -> open
    assert application_status(days_left=35, is_renewal=True, is_paper=False) == "open"


def test_application_status_paper_closing():
    # cutoff = 20 + 10 = 30; days_left = 20 (>= 30 - 15 = 15) -> closing
    assert application_status(days_left=20, is_renewal=False, is_paper=True) == "closing"


def test_application_status_closed():
    # cutoff = 20; days_left = 2 (< 5) -> closed
    assert application_status(days_left=2, is_renewal=False, is_paper=False) == "closed"
