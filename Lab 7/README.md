# Lab 7 — Fuzz Testing for Input Validation Bugs

## Target and adaptation

The handout refers to an assigned `processor.py`, but no Lab 7 application source was included with the handout or in the existing submission repository. This lab uses the three scholarship-processing functions from Lab 6 as the target and places a standalone copy in `processor.py` so the requested `test_processor.py` can run independently.

## Findings

The initial Hypothesis run found 12 failing properties (3 passed):

- `award_amount` accepted marks above the valid 0–100 range; the smallest counterexample was `101`.
- `is_eligible` accepted attendance above 100; the smallest counterexample was `101`.
- `application_status` accepted negative days remaining; the smallest counterexample was `-1`.
- The fuzz cases also exposed crashes or silent acceptance for floats, `None`, malformed category/income values, and non-boolean flags.

The implementation now validates integer ranges, allowed strings, and exact boolean inputs before processing. The scholarship formulas and valid input behavior remain unchanged. The final Hypothesis run passes all 18 properties and input-validation checks.

## Run it

From this folder:

```powershell
python -m pip install -r requirements.txt
python processor.py
python -m pytest -q test_processor.py
```

The initial failing output and final passing output are preserved in `evidence/`. `fuzz_testing_report.pdf` contains the before/after output captures and findings summary.

## Files

- `processor.py` — fixed scholarship processor.
- `test_processor.py` — Hypothesis-based properties across the three processing functions.
- `requirements.txt` — pytest and Hypothesis dependencies.
- `fuzz_testing_report.pdf` — report with run output captures and analysis.
- `evidence/` — raw before/after command output and capture images.
