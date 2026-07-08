# Contributing Guide

We welcome contributions to CreditGuard AI. Please review the following workflows:

---

## 1. Coding Standards
- **PEP 8**: All Python modules must follow PEP8 guidelines. Run Black style formatter and Flake8 linter on modifications.
- **Type Hints**: Type annotations are required on all public methods.
- **Exceptions**: Throw custom errors from `src/utils/exceptions.py`.

---

## 2. Git Workflow
1. Fork the repository and create a new feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Commit your modifications with descriptive logs:
   ```bash
   git commit -m "feat: description of change"
   ```
3. Run unit tests before pushing:
   ```bash
   pytest tests/ -v
   ```
4. Push and submit a Pull Request (PR) for review.

---

## 👥 Contributors

- **Shaik Mahammad Shariff** ([skmdshariff143-ai](https://github.com/skmdshariff143-ai)) — Lead Developer & Maintainer
