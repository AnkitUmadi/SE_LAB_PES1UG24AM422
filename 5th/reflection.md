# Lab 5: Reflection on Static Code Analysis

### 1. Which issues were the easiest to fix, and which were the most challenging? Why?
* **Easiest to fix:** Style and formatting issues flagged by **Flake8** and **Pylint**—such as removing the unused `import sys` (`F401`/`W0611`), adding two blank lines between functions (`E302`), wrapping lines over 79 characters (`E501`), and converting `%` string formatting into f-strings (`C0209`). These required purely mechanical syntax adjustments without altering program logic.
* **Most challenging to fix:** Refactoring the mutable default argument (`W0102`: `history=[]`), eliminating `global` statements (`W0603`), and fixing the logical bug with negative meter readings (`M-03: -50`). Removing `history=[]` required updating `main()` to pass the `history` list explicitly across calls so `len(history)` still tracked all 3 readings accurately.

### 2. Did the static analysis tools find all the bugs in `energy_system.py`, or did any issues require manual inspection?
No, the static analysis tools did **not** catch the domain-level logical bug where `record_reading("M-03", -50)` recorded `-50` kWh and `compute_bill()` calculated a negative electricity bill (`-192.50`). Pylint, Bandit, and Flake8 inspect syntax, structure, and known anti-patterns without executing the program or understanding business rules (such as electricity consumption being non-negative). Catching this required running the code and inspecting its output manually.

### 3. How did Pylint, Bandit, and Flake8 complement each other during the analysis?
Each tool targeted a distinct layer of software quality:
* **Bandit (Security):** Focused strictly on security vulnerabilities, flagging `eval(adjustment)` (`B307`, Medium severity, CWE-78) which could allow arbitrary code execution from user input.
* **Pylint (Code Quality & Bugs):** Acted as a deep code reviewer, catching functional bugs and bad practices like the mutable default argument `history=[]` (`W0102`), unclosed file handles (`R1732`), missing file encodings (`W1514`), bare `except:` blocks (`W0702`), and missing docstrings (`C0114`/`C0116`).
* **Flake8 (PEP 8 Style):** Enforced strict PEP 8 formatting rules such as line length limits (`E501`) and blank-line spacing (`E302`, `E305`) that keep code clean and readable across teams.

### 4. How does integrating static code analysis into a development workflow (e.g., CI/CD or pre-commit hooks) improve overall software quality and maintainability?
Integrating Pylint, Bandit, and Flake8 into pre-commit hooks or CI/CD pipelines catches security vulnerabilities (like `eval()`), resource leaks (unclosed files), and subtle Python bugs (like mutable default arguments) automatically before code is ever merged into production. It enforces consistent PEP 8 formatting across all developers, reduces time spent on trivial style comments during human code reviews, and prevents technical debt from accumulating over time.