# Assumptions

This file should be updated as the problem statement and CSV inputs become clear.

Current assumptions:

1. The solution will be implemented as a small Python package under `src/assignment`.
2. CSV processing will use `pandas` for readability and reliability.
3. The command-line interface will use `click`.
4. Tests will focus on transformation logic and edge cases rather than only end-to-end behavior.
5. Input CSV files are not committed unless they are explicitly allowed by the assignment.

Open questions:

1. What are the names and schemas of the two CSV files?
2. What exact output is expected: printed summary, generated CSV, JSON, database update, or another format?
3. Are malformed rows expected, and how should they be handled?
