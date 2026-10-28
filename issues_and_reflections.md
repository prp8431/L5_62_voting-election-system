# Lab 5: Static Code Analysis
## Voting and Election Management System

### 1. Issues Identified and Fixes Applied

| Issue | Type | Tool | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded password | Security | Bandit | An administrator password was stored directly in the source code. | Read the password from the `ADMIN_PASSWORD` environment variable. |
| Weak MD5 hashing | Security | Bandit | MD5 was used to generate a voter identifier hash. | Replaced MD5 with SHA-256. |
| Insecure random number generation | Security | Bandit | The standard `random` module was used to generate receipt numbers. | Replaced it with the `secrets` module. |
| Unsafe XML parsing | Security | Bandit | XML input was parsed using a parser vulnerable to XML attacks. | Used `defusedxml` for safer XML parsing and handled parsing errors. |
| Broad exception handling | Code quality | Bandit / Pylint | A broad exception handler silently ignored errors. | Replaced it with specific exception handling and ensured XML documents are cleaned up. |
| Duplicate voting | Logic | Code review | A registered voter could attempt to vote more than once. | Added a check to reject voters who have already voted. |
| Invalid candidate | Logic | Code review | Votes for unrecognized candidates could be accepted. | Added candidate validation before recording votes. |
| Division by zero | Reliability | Code review | Percentage calculations could fail when no ballots or voters existed. | Added checks for empty ballots and voter collections. |
| Naming and documentation | Style | Pylint | Function names did not follow snake_case, and docstrings were missing. | Renamed functions and added documentation strings. |
| Formatting violations | Style | Flake8 | The original file contained long lines and formatting inconsistencies. | Reformatted the code using Black and verified it with Flake8. |

### 2. Reflection

**Q1. What is static code analysis, and why is it useful?**

Static code analysis examines source code without executing the program. It helps identify potential security vulnerabilities, programming mistakes, unused variables, and style violations before the software is deployed.

**Q2. What did you learn from using Pylint, Bandit, and Flake8?**

Pylint helped identify code-quality and maintainability issues. Bandit highlighted potentially insecure coding practices. Flake8 identified formatting and style violations. Using all three tools provided a more complete review of the program.

**Q3. Which issues were the most important to fix?**

The most important issues involved hardcoded credentials, weak hashing, insecure random-number generation, and unsafe XML parsing. These issues could affect the security and reliability of the voting system.

**Q4. How did the fixes improve the program?**

The changes improved security by using stronger hashing, secure receipt-number generation, safer XML parsing, and environment-based password configuration. Additional validation prevented duplicate votes and invalid candidates, while empty-collection checks improved reliability.

**Q5. What did you learn from this lab?**

I learned that a program can run successfully and still contain security, logic, and maintainability problems. Static analysis tools help identify these problems systematically. Rerunning the tools after making changes helps verify whether the reported issues have been resolved.

**Q6. How can static analysis be used in future projects?**

Static analysis can be included in regular development workflows and automated checks. Running tools before committing or merging code helps maintain consistent coding standards and detect potential vulnerabilities early.

### 3. Verification Results

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified in the final scan.
- **Flake8:** No violations reported in the final run.
- The program was executed to verify its sample behaviour.
- Before-and-after analysis reports were generated and uploaded to the GitHub repository.

### 4. Repository

GitHub repository: https://github.com/prp8431/L5_62_voting-election-system
