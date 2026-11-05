# Lab 5: Static Code Analysis — Employee Payroll System

This submission records analysis and cleanup of the payroll program with Pylint, Bandit and Flake8.

## Results

- Pylint final score: 10.00/10.
- Bandit final scan: no issues reported.
- Flake8 final scan: no violations reported.
- The unsafe `eval` call was replaced with a restricted AST arithmetic evaluator; weak hashing, shell execution, mutable defaults, and other documented issues were corrected.
- Removed a leftover hardcoded payroll key from the sample `main()` routine.

## Files

- `employee_payroll_system.py` — revised program.
- `issues.md` and `reflection.md` — findings, fixes and reflection.
- `*_report_before.txt` and `*_report_after.txt` — analyzer output before and after the fixes. The unsuffixed report files mirror the final runs.

Run the program with `python employee_payroll_system.py`. Install the analyzers with `python -m pip install pylint bandit flake8` before reproducing the reports.
