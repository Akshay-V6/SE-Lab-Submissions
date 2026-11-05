import pytest
from scholarship_awards import award_amount, is_eligible, application_status

# ============================================================================
# Tests for award_amount
# ============================================================================

def test_unknown_category_raises_value_error():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("engineering", 85, "low", False)


def test_invalid_negative_marks_raises_value_error():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -5, "low", False)


def test_below_cutoff_marks():
    assert award_amount("merit", 70, "low", False) == 0


def test_exact_cutoff_marks():
    assert award_amount("merit", 75, "low", False) == 0


def test_award_sports_renewal():
    # sports cutoff stays 60 even if renewal is True
    assert award_amount("sports", 70, "high", True) == 600


def test_award_arts_renewal():
    # arts cutoff decreases from 65 to 60 with renewal
    assert award_amount("arts", 70, "low", True) == 1000


def test_award_low_income_above_boundary():
    # above = 15 (boundary for above > 15)
    assert award_amount("merit", 90, "low", False) == 1500


def test_award_low_income_high_score_with_renewal():
    # above = 20 (> 15), income == low -> rate = 160
    assert award_amount("merit", 90, "low", True) == 3200


def test_award_general_income_above_15():
    # above = 20 (> 15), income != low -> rate = 100
    assert award_amount("merit", 95, "medium", False) == 2000


# ============================================================================
# Tests for is_eligible
# ============================================================================

def test_is_eligible():
    assert is_eligible(90, 0, False) is True


def test_is_eligible_special_quota():
    assert is_eligible(50, 2, True) is True


def test_is_eligible_special_quota_fails():
    assert is_eligible(95, 3, True) is False


def test_is_eligible_low_attendance():
    assert is_eligible(74, 0, False) is False


def test_is_eligible_regular_quota_boundary_attendance():
    assert is_eligible(75, 1, False) is True


def test_is_eligible_regular_quota_too_many_backlogs():
    assert is_eligible(85, 2, False) is False


# ============================================================================
# Tests for application_status
# ============================================================================

def test_application_status_renewal_paper_open():
    assert application_status(40, is_renewal=True, is_paper=True) == "open"


def test_application_status_renewal_no_paper_closing():
    assert application_status(20, is_renewal=True, is_paper=False) == "closing"


def test_application_status_renewal_no_paper_closed():
    assert application_status(10, is_renewal=True, is_paper=False) == "closed"


def test_application_status_non_renewal_paper_closing():
    assert application_status(15, is_renewal=False, is_paper=True) == "closing"


def test_application_status_non_renewal_no_paper_open():
    assert application_status(25, is_renewal=False, is_paper=False) == "open"


def test_application_status_non_renewal_no_paper_closed():
    assert application_status(4, is_renewal=False, is_paper=False) == "closed"
