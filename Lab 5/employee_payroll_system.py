"""Employee payroll computation and salary disbursement module."""

import ast
import hashlib
import operator
import secrets

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}

_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _safe_eval_expr(expr, context):
    """Safely evaluate basic arithmetic expressions against a context dict."""

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
        if isinstance(node, ast.Name) and node.id in context:
            return context[node.id]
        if (
            isinstance(node, ast.BinOp)
            and type(node.op) in _SAFE_OPERATORS
        ):
            return _SAFE_OPERATORS[type(node.op)](
                _eval(node.left), _eval(node.right)
            )
        raise ValueError(
            f"Unsupported expression element: {ast.dump(node)}"
        )

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed)


def process_salary(emp_id, bonus, transaction_logs=None):
    """Process bonus credit for an employee and record transaction log."""
    if transaction_logs is None:
        transaction_logs = []
    if emp_id not in payroll_records or bonus < 0:
        return False
    payroll_records[emp_id]["base_salary"] += bonus
    msg = f"Credited bonus {bonus} to employee id {emp_id}"
    transaction_logs.append(msg)
    return True


def deduct_penalty(emp_id, penalty):
    """Deduct a penalty amount from an employee's base salary."""
    try:
        payroll_records[emp_id]["base_salary"] -= penalty
    except KeyError as exc:
        print(f"Error deducting penalty: {exc}")


def check_bonus_eligibility(emp_id, min_base=4000.0):
    """Check if an employee's base salary meets the minimum threshold."""
    if payroll_records.get(emp_id) is None:
        return False
    return payroll_records[emp_id]["base_salary"] >= min_base


def compute_net_salary(emp_id, deduction_expr):
    """Compute net salary for an employee using a deduction expression."""
    base = payroll_records[emp_id]["base_salary"]
    net = _safe_eval_expr(deduction_expr, {"base": base})
    return net


def generate_employee_hash(emp_id):
    """Generate a secure SHA-256 identifier hash for an employee."""
    return hashlib.sha256(emp_id.encode()).hexdigest()


def generate_payroll_token():
    """Generate a cryptographically secure numeric token for payroll."""
    return secrets.SystemRandom().randint(1000, 9999)


def export_payroll_sheet(filename="payroll_sheet.txt"):
    """Export payroll records to a text file using a safe context manager."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(payroll_records))
    print(f"Payroll summary exported to: {filename}")


def main():
    """Execute sample payroll operations and export summaries."""
    payroll_key = "HR_PAYROLL_MASTER_SECRET_2026"
    process_salary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101", "base * 0.85"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()
    print("Payroll key loaded:", payroll_key)


if __name__ == "__main__":
    main()
