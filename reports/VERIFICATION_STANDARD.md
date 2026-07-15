# Codebase Verification Standard

This document outlines the strict verification discipline required for all contributions to CreditGuard AI. All claims of "done", "fixed", or "completed" must adhere to the rules in this standard.

---

## 1. The Core Standard: Evidence-Based Verification

Every modification, feature implementation, bug fix, or dependency update must be accompanied by **real, pasted verification evidence**. 

- **Narrative Descriptions are Insufficient:** Saying "the endpoint was tested and works" or "the database is now configured" is not acceptable.
- **Accepted Evidence Includes:**
  - Copy-pasted terminal command executions and their exact outputs.
  - HTTP request/response headers and status codes.
  - Database query results (SQL row prints).
  - Test suite runner output (e.g., `pytest` output logs).
  - Static analysis or security scanner reports (e.g., `black`, `flake8`, `bandit`).

---

## 2. Checklist of Verification Pitfalls

Historically, several verification gaps were identified and corrected in this repository. All future checks must run through this checklist:

### A. Status Codes Alone Do Not Prove Behavior
- *Example:* Checking that a path returns a `404` does not prove role-based access control (RBAC) works. It could simply mean the route doesn't exist.
- *Check:* To verify RBAC or rate limits, test both the authorized path (success state) and unauthorized path (verifying redirection `302` or access-denied `403` or rate-limited `429`), showing the exact redirected destination or response body.

### B. Unchanged Metrics Must Be Explained
- *Example:* Claiming a model metric has been corrected or updated while reporting the exact same placeholder metrics in reports.
- *Check:* Compare metrics before and after the change. If a metric is unchanged, explain why (e.g. mathematical convergence, dataset stability) rather than just repeating the prior number.

### C. Distinguish "Committed", "Pushed", and "Live"
- *Example:* Testing a local SQLite database and claiming that data persistence works in production.
- *Check:* 
  - **Committed:** Code is in local Git history.
  - **Pushed:** Code is in remote repository (CI pipeline is green).
  - **Live:** Code is deployed on production URL and has been verified with live HTTP requests under realistic deployment conditions.

### D. Local Bypasses are Not Production Proofs
- *Example:* Testing a rate limiter or security token locally under `TESTING=True` (where the check is bypassed/ignored) and claiming the security control is functional.
- *Check:* Ensure security and rate-limiting controls are tested with real request loops in a simulated or real production state where bypasses are disabled.

### E. README Claims Must Match Code
- *Example:* Claiming a feature exists in the project documentation (such as "PDF reports generated on server") when the actual implementation only triggers browser-based HTML prints.
- *Check:* Verify that every user-facing claim in `README.md` or manuals is directly supported by active code in the repository.

---

## 3. Standard Verification Commands

Before pushing any commit, developers must run the following checks and paste their success output:
1. **Pytest Run:** Run `pytest` and confirm 119/119 tests pass.
2. **Black Formatting:** Run `black --check 5_Project_Development_Phase` and confirm zero formatting warnings.
3. **Flake8 Linter:** Run `flake8` and confirm zero lint issues.
4. **Bandit Security:** Run `bandit -r src/ app/ -ll --skip B101,B105,B106` and confirm zero vulnerabilities.
