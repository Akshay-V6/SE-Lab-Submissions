CUTOFF_MARKS = {"merit": 75, "sports": 60, "arts": 65}


def award_amount(category, marks, income_level, is_renewal):
    if category not in CUTOFF_MARKS:
        raise ValueError("unknown category")
    if marks < 0:
        raise ValueError("invalid marks")
    cutoff = CUTOFF_MARKS[category]
    if is_renewal and category != "sports":
        cutoff -= 5
    above = marks - cutoff
    if above <= 0:
        return 0
    if income_level == "low":
        rate = 100
    else:
        rate = 60
    if above > 15:
        rate = rate + 40
        if income_level == "low":
            rate += 20
    return above * rate


def is_eligible(attendance, backlogs, is_special_quota):
    if is_special_quota:
        return backlogs <= 2
    if attendance < 75:
        return False
    return backlogs <= 1


def application_status(days_left, is_renewal, is_paper):
    if is_renewal:
        cutoff = 30
    else:
        cutoff = 20
    if is_paper:
        cutoff += 10
    if days_left >= cutoff:
        return "open"
    elif days_left >= cutoff - 15:
        return "closing"
    return "closed"
