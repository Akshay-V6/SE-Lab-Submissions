# Static Code Analysis Issues Report

**Target Program:** `employee_payroll_system.py`  
**Analyzers Used:** Pylint, Bandit, Flake8  

---

## Documented Issues Table

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **Shell Process Execution (`B605`)** | Security (High) | 58 | `os.system("echo ...")` spawns a subshell with string concatenation, exposing the system to potential command injection. | Replace `os.system` with standard, safe Python `print()` formatting and eliminate unnecessary shell subprocessing. |
| **Weak Cryptographic Hash (`B324`)** | Security (High) | 47 | `hashlib.md5(...)` uses the deprecated and collision-vulnerable MD5 hashing algorithm for employee identification. | Replace MD5 with collision-resistant SHA-256 (`hashlib.sha256()`). |
| **Unsafe Dynamic Code Evaluation (`B307` / `W0123`)** | Security (Medium) / Quality | 42 | `eval(deduction_expr)` dynamically executes arbitrary Python code strings, creating a severe arbitrary code execution vulnerability. | Eliminate `eval()` and replace it with a safe Abstract Syntax Tree (`ast`) evaluator (`_safe_eval_expr`) restricted to numbers, arithmetic binary operators, and valid context keys. |
| **Insecure Pseudo-Random Number Generation (`B311`)** | Security (Low) | 51 | `random.randint(...)` uses a deterministic PRNG unsuitable for security-sensitive tokens or session credentials. | Use Python's cryptographically secure pseudo-random number generator `secrets.SystemRandom().randint(...)`. |
| **Silent Exception Suppression (`B110` / `E722` / `W0702`)** | Security (Low) / Style / Quality | 26–27 | Bare `except:` clause paired with `pass` silently catches all exceptions (including syntax and interrupt signals) without logging. | Catch specific exception types (`KeyError`) and print or log descriptive error messages instead of silently passing. |
| **Dangerous Mutable Default Argument (`W0102`)** | Bug / Quality | 15 | `transaction_logs=[]` creates a mutable list shared across all invocations of the function across the module lifecycle. | Set default argument to `None` and initialize a fresh list `[]` inside the function body when `transaction_logs is None`. |
| **Non-PEP 8 Function Naming (`C0103`)** | Style / Quality | 15 | `processSalary` uses camelCase naming, violating the PEP 8 snake_case convention for function identifiers. | Rename the function to `process_salary` conforming to snake_case. |
| **Singleton Equality Comparison (`E711` / `C0121`)** | Style / Quality | 32 | Comparison `payroll_records.get(emp_id) == None` uses equality instead of identity checking. | Replace `== None` with identity check `is None`. |
| **Unused Module Import (`F401` / `W0611`)** | Style / Quality | 6 | `import math` imports a standard library module that is never referenced in the program. | Remove the redundant `import math` statement. |
| **Unused Local Variables (`F841` / `W0612`)** | Style / Quality | 31, 41 | Variables `statutory_buffer` and `base` were assigned but never utilized. | Remove `statutory_buffer` and properly pass `base` into the arithmetic context dictionary. |
| **Unmanaged File I/O (`R1732` / `W1514`)** | Quality / Resource Safety | 55–57 | `open(filename, "w")` without a context manager risks resource leaks on errors, and lacks explicit character encoding. | Use a `with open(filename, "w", encoding="utf-8") as f:` context manager. |
| **Missing Function Docstrings (`C0116`)** | Quality / Documentation | Multiple | Functions lacked docstrings explaining their parameters, behavior, and return values. | Add descriptive PEP 257 docstrings to all functions. |
| **PEP 8 Line Length Violations (`E501`)** | Style | 19, 27 | Long lines exceeded the 79-character PEP 8 limit. | Reformat and split statements across multiple lines cleanly. |
