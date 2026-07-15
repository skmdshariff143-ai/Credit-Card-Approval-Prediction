# Contributing to CreditGuard AI

> [!IMPORTANT]
> All contributions, bug fixes, and feature additions to this repository must strictly adhere to the [Verification Standard](reports/VERIFICATION_STANDARD.md).
> Under no circumstances will a code change be accepted or merged without real, copy-pasted evidence of verification.

---

## Code Quality Requirements

Before submitting any code changes, you must run and verify the following quality checks:

1. **Test Suite:**
   - Execute `pytest` and ensure all 119 tests pass cleanly.
2. **Formatting:**
   - Run `black --check 5_Project_Development_Phase` to ensure PEP 8 formatting standards are met.
3. **Linting:**
   - Run `flake8` to scan for syntax errors, unresolved symbols, and styling violations.
4. **Security Analysis:**
   - Run `bandit -r src/ app/ -ll --skip B101,B105,B106` to scan for security issues and vulnerabilities.

---

## Pull Request Submission checklist

1. **No Placeholders:** Ensure no temporary credentials or connection strings are committed.
2. **Local Fallback:** Maintain support for local SQLite databases so offline development continues to function.
3. **Pasted Evidence:** In your commit descriptions or verification notes, paste the exact command logs and response payloads confirming that the fix operates correctly.
