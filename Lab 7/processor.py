"""Scholarship application processor hardened through Hypothesis fuzzing."""

CUTOFF_MARKS = {"merit": 75, "sports": 60, "arts": 65}
INCOME_LEVELS = {"low", "medium", "high"}


def _require_integer(value, field, minimum, maximum=None):
    """Require a true integer within the domain of a scholarship field."""
    if type(value) is not int:
        raise ValueError(f"{field} must be an integer")
    if value < minimum or (maximum is not None and value > maximum):
        if maximum is None:
            raise ValueError(f"{field} must be at least {minimum}")
        raise ValueError(f"{field} must be between {minimum} and {maximum}")


def _require_boolean(value, field):
    """Require an actual bool rather than a truthy/falsy substitute."""
    if type(value) is not bool:
        raise ValueError(f"{field} must be a boolean")


def award_amount(category, marks, income_level, is_renewal):
    """Calculate a scholarship award after validating application inputs."""
    if not isinstance(category, str) or category not in CUTOFF_MARKS:
        raise ValueError("unknown category")
    _require_integer(marks, "marks", 0, 100)
    if not isinstance(income_level, str) or income_level not in INCOME_LEVELS:
        raise ValueError("income_level must be low, medium, or high")
    _require_boolean(is_renewal, "is_renewal")

    cutoff = CUTOFF_MARKS[category]
    if is_renewal and category != "sports":
        cutoff -= 5
    above_cutoff = max(0, marks - cutoff)
    rate = 100 if income_level == "low" else 60
    if above_cutoff > 15:
        rate += 40
        if income_level == "low":
            rate += 20
    return above_cutoff * rate


def is_eligible(attendance, backlogs, is_special_quota):
    """Check scholarship eligibility after validating applicant data."""
    _require_integer(attendance, "attendance", 0, 100)
    _require_integer(backlogs, "backlogs", 0)
    _require_boolean(is_special_quota, "is_special_quota")

    if is_special_quota:
        return backlogs <= 2
    return attendance >= 75 and backlogs <= 1


def application_status(days_left, is_renewal, is_paper):
    """Return the application-window status after validating its inputs."""
    _require_integer(days_left, "days_left", 0)
    _require_boolean(is_renewal, "is_renewal")
    _require_boolean(is_paper, "is_paper")

    cutoff = 30 if is_renewal else 20
    if is_paper:
        cutoff += 10
    if days_left >= cutoff:
        return "open"
    if days_left >= cutoff - 15:
        return "closing"
    return "closed"


def main():
    """Show malformed examples and demonstrate defensive input rejection."""
    examples = (
        ("Marks 120 award", award_amount, ("merit", 120, "low", False)),
        ("Attendance 150 eligibility", is_eligible, (150, 0, False)),
        ("Negative days-left status", application_status, (-1, False, False)),
    )
    print("Scholarship application processor")
    for label, function, arguments in examples:
        try:
            print(f"{label}: {function(*arguments)}")
        except ValueError as error:
            print(f"{label}: rejected ({error})")


if __name__ == "__main__":
    main()
