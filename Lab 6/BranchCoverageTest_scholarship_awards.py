import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# ============================================================================
# Tests for award_amount
# ============================================================================

def test_award_unknown_category():
    """Branch: category not in CUTOFF_MARKS -> True (raise ValueError)"""
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("music", 80, "low", False)


def test_award_negative_marks():
    """Branch: marks < 0 -> True (raise ValueError)"""
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


def test_award_marks_below_cutoff():
    """Branch: above <= 0 -> True (marks < cutoff, returns 0)"""
    assert award_amount("merit", 70, "low", False) == 0


def test_award_marks_exact_cutoff():
    """Branch: above <= 0 -> True boundary (marks == cutoff, returns 0)"""
    assert award_amount("merit", 75, "low", False) == 0


def test_award_renewal_sports_category():
    """
    Branch: is_renewal is True, but category == 'sports'.
    Ensures category != 'sports' evaluates to False and cutoff is not reduced.
    cutoff = 60. marks = 70 => above = 10 (<= 15).
    rate = 60 (income != low). Total = 10 * 60 = 600.
    """
    assert award_amount("sports", 70, "high", True) == 600


def test_award_renewal_arts_category():
    """
    Branch: is_renewal is True and category == 'arts'.
    Cutoff reduced from 65 to 60.
    marks = 70 => above = 10 (<= 15).
    rate = 100 (income == low). Total = 10 * 100 = 1000.
    """
    assert award_amount("arts", 70, "low", True) == 1000


def test_award_no_renewal_low_income_above_boundary():
    """
    Branch: above <= 15 boundary (above == 15).
    merit cutoff = 75. marks = 90 => above = 15.
    above > 15 is False. rate = 100. Total = 15 * 100 = 1500.
    """
    assert award_amount("merit", 90, "low", False) == 1500


def test_award_above_15_low_income():
    """
    Branch: above > 15 (True) AND income_level == 'low' (True).
    merit cutoff = 75 - 5 = 70 (renewal). marks = 90 => above = 20.
    rate = 100 + 40 + 20 = 160. Total = 20 * 160 = 3200.
    """
    assert award_amount("merit", 90, "low", True) == 3200


def test_award_above_15_non_low_income():
    """
    Branch: above > 15 (True) AND income_level == 'low' (False).
    merit cutoff = 75. marks = 95 => above = 20.
    rate = 60 + 40 = 100. Total = 20 * 100 = 2000.
    """
    assert award_amount("merit", 95, "medium", False) == 2000


# ============================================================================
# Tests for is_eligible
# ============================================================================

def test_is_eligible_special_quota_true():
    """Branch: is_special_quota -> True, backlogs <= 2 (True)"""
    assert is_eligible(attendance=50, backlogs=2, is_special_quota=True) is True


def test_is_eligible_special_quota_false_backlogs():
    """Branch: is_special_quota -> True, backlogs <= 2 (False)"""
    assert is_eligible(attendance=95, backlogs=3, is_special_quota=True) is False


def test_is_eligible_regular_low_attendance():
    """Branch: is_special_quota -> False, attendance < 75 (True)"""
    assert is_eligible(attendance=74, backlogs=0, is_special_quota=False) is False


def test_is_eligible_regular_boundary_attendance_pass():
    """Branch: is_special_quota -> False, attendance >= 75 (boundary 75), backlogs <= 1 (True)"""
    assert is_eligible(attendance=75, backlogs=1, is_special_quota=False) is True


def test_is_eligible_regular_high_backlogs_fail():
    """Branch: is_special_quota -> False, attendance >= 75, backlogs <= 1 (False)"""
    assert is_eligible(attendance=85, backlogs=2, is_special_quota=False) is False


# ============================================================================
# Tests for application_status
# ============================================================================

def test_application_status_renewal_paper_open():
    """
    Branches: is_renewal=True (cutoff=30), is_paper=True (cutoff=40).
    days_left >= cutoff (40 >= 40) -> 'open'.
    """
    assert application_status(days_left=40, is_renewal=True, is_paper=True) == "open"


def test_application_status_renewal_no_paper_closing():
    """
    Branches: is_renewal=True (cutoff=30), is_paper=False (cutoff=30).
    days_left < 30 but >= 15 (days_left=20) -> 'closing'.
    """
    assert application_status(days_left=20, is_renewal=True, is_paper=False) == "closing"


def test_application_status_renewal_no_paper_closed():
    """
    Branches: is_renewal=True (cutoff=30), is_paper=False (cutoff=30).
    days_left < 15 (days_left=10) -> 'closed'.
    """
    assert application_status(days_left=10, is_renewal=True, is_paper=False) == "closed"


def test_application_status_non_renewal_paper_closing_boundary():
    """
    Branches: is_renewal=False (cutoff=20), is_paper=True (cutoff=30).
    days_left == 15 (cutoff - 15 boundary) -> 'closing'.
    """
    assert application_status(days_left=15, is_renewal=False, is_paper=True) == "closing"


def test_application_status_non_renewal_no_paper_open():
    """
    Branches: is_renewal=False (cutoff=20), is_paper=False (cutoff=20).
    days_left = 25 >= 20 -> 'open'.
    """
    assert application_status(days_left=25, is_renewal=False, is_paper=False) == "open"


def test_application_status_non_renewal_no_paper_closed():
    """
    Branches: is_renewal=False (cutoff=20), is_paper=False (cutoff=20).
    days_left = 4 (< 5) -> 'closed'.
    """
    assert application_status(days_left=4, is_renewal=False, is_paper=False) == "closed"
