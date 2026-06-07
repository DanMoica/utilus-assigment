# AI Usage

AI tools were used during this assignment to help set up the project, refine validation logic,
document assumptions, and review the generated metrics output. The code and documentation were
reviewed and adjusted during the conversation.

## Conversation Log

### Project setup

User prompt:

> I have an interview assignment. My start project is located here:
> `C:\Users\moica\PycharmProjects\utilus`. I will use PyCharm as IDE.
> Libraries I want are pandas, pytest, click, ruff. Suggest if others if I am missing something.
> Create a readable and good structure for the project:
> README.md, ASSUMPTIONS.md, AI_USAGE.md, pyproject.toml, src/assignment/, tests/, data/.
> Add info to pyproject.toml.

AI actions:

- Created the initial project layout.
- Added `README.md`, `ASSUMPTIONS.md`, `AI_USAGE.md`, `pyproject.toml`, `.gitignore`,
  `src/assignment/`, `tests/`, and `data/`.
- Added starter package files and a simple CSV reader.
- Installed dependencies into the existing `.venv`.
- Fixed Hatch build configuration by adding the explicit package path.
- Ran pytest, Ruff, and CLI smoke checks.

### Requirements file

User prompt:

> Add a requirement.txt with pandas and pytest for my python version.

AI actions:

- Checked the project virtualenv Python version: Python 3.13.5.
- Checked installed versions of pandas and pytest.
- Added `requirement.txt` with:
  - `pandas==3.0.3`
  - `pytest==9.0.3`

### Main entry point

User prompt:

> Add a main.py with logging and a reader so I can run
> `python main.py customers.csv subscriptions.csv output.json`

AI actions:

- Added `main.py` with logging, argument parsing, CSV loading, and JSON output.
- Added a reusable reader module initially.
- Added tests around the output behavior.
- Ran pytest, Ruff, and a command smoke test.

### Loader logging for date parsing

User prompt:

> In saas_metrics/loader.py add a logger and log in _parse_required_date function that there is
> a bad row and reformated correctly.

AI actions:

- Added a module-level logger to `loader.py`.
- Updated `_parse_required_date` to log when required dates are reformatted to `YYYY-MM-DD`.
- Restored malformed required-date validation and error handling.
- Added tests for reformatted date logging and bad-row logging.
- Fixed drift in `main.py` so it used the current SaaS loader/report structure.
- Ran pytest and Ruff.

### Error logging before raises

User prompt:

> In my loader.py where I raise an error, log an error with a good correct message.

AI actions:

- Added `logger.error(...)` before each raise path in `loader.py`.
- Ensured logged messages match raised exception messages.
- Updated malformed required-date logging from warning to error.
- Updated tests to check the improved log message.
- Ran pytest and Ruff.

### Assumptions documentation

User prompt:

> Add general assumptions to the assumption.md file.

AI actions:

- Expanded `ASSUMPTIONS.md` with general assumptions about:
  - input CSV shape,
  - required columns,
  - customer IDs,
  - dates,
  - subscription periods,
  - monthly prices,
  - JSON output,
  - validation behavior,
  - open questions.

### Metrics formatting

User prompt:

> Reformat the metrics.py file.

AI actions:

- Ran Ruff formatting on `src/assignment/saas_metrics/metrics.py`.
- Ran pytest and Ruff checks.

### MRR review

User prompt:

> Can you check if my metric.py calculates the correct Monthly Recurring Revenue for the given
> data clean?

AI actions:

- Reviewed `calculate_monthly_mrr`.
- Compared the current implementation against the provided subscription data.
- Explained that the implementation counts subscriptions active at any point in the month.
- Noted that this matches the documented assumption, but differs from classic month-end MRR.
- Identified that overlapping or multiple same-customer subscription rows in a month can be
  counted independently under the current logic.

### Clean CSV files

User prompt:

> Give me two clean files, according to my assumptions.md. Write in *_clean.csv.

AI actions:

- Created `data/customers_clean.csv`.
- Created `data/subscriptions_clean.csv`.
- Cleaned issues such as:
  - invalid dates,
  - duplicate customer row,
  - misspelled plan value,
  - non-numeric price,
  - invalid subscription range,
  - date whitespace,
  - missing country value,
  - subscriptions for customers not present in the cleaned customer file,
  - duplicate active subscription row.
- Validated both clean files with the loader.
- Fixed stale test and report formatting drift found during verification.
- Ran pytest and Ruff.

### Allowed plan validation

User prompt:

> I see that in subscription.csv there is a misspelled word baisc. Add a line to check for allowed
> plans in load_subscription and if there is an invalid plan, log and throw error.

AI actions:

- Added `ALLOWED_PLANS = {"basic", "pro"}`.
- Added plan validation in `load_subscriptions`.
- Logged and raised an error for invalid plan values, including bad row indexes and values.
- Added a test for the `baisc` typo.
- Ran pytest and Ruff.

### Google-style docstrings

User prompt:

> Add Google style docstring to all functions.

AI actions:

- Added Google-style docstrings to application functions in:
  - `main.py`,
  - `src/assignment/cli.py`,
  - `src/assignment/io.py`,
  - `src/assignment/saas_metrics/loader.py`,
  - `src/assignment/saas_metrics/metrics.py`,
  - `src/assignment/saas_metrics/report.py`.
- Added docstrings to test functions as well.
- Ran Ruff format, pytest, and Ruff check.

### Output review

User prompt:

> Can you check output.json. Does it make sense?

AI actions:

- Compared `output.json` against a freshly generated report from:
  - `data/customers_clean.csv`,
  - `data/subscriptions_clean.csv`.
- Confirmed that `output.json` matches the current metrics logic.
- Explained that the output is coherent under the assumption that a subscription contributes its
  full monthly price to any month in which it is active for at least one day.
- Recommended adding a clarification that multiple subscription periods for the same customer in
  one month are counted independently.

### Additional MRR assumption

User prompt:

> Add that note.

AI actions:

- Updated `ASSUMPTIONS.md` to state that multiple subscription periods for the same customer in
  the same month are counted independently if each is active for at least one day.

### Test formatting and docstrings

User prompt:

> Can you reformat my tests and add docstrings?

AI actions:

- Reviewed the test files.
- Confirmed test docstrings already existed.
- Cleaned up test formatting.
- Added a missing `Path` type annotation for `tmp_path`.
- Ran Ruff format on tests, pytest, and Ruff check.

### Design and assumptions review

User prompt:

> Can You check my design.md file and tell me if I am missing something there.
> Also if something is missing from the assumptions.md file.

AI actions:

- Reviewed `DESIGN.md`, `ASSUMPTIONS.md`, `metrics.py`, `loader.py`, `main.py`, and `report.py`.
- Noted that `DESIGN.md` said unknown subscription customers are logged and excluded, but the code
  does not currently implement that cross-file filtering.
- Suggested adding assumptions about:
  - valid plans,
  - invalid plan handling,
  - numeric prices,
  - invalid dates and clean-file corrections,
  - unknown country handling,
  - unknown subscription customer behavior,
  - MRR reporting period,
  - open-ended subscriptions,
  - output JSON shape.

### Additional assumptions

User prompt:

> Add the suggestion for assumption file.

AI actions:

- Updated `ASSUMPTIONS.md` with assumptions about:
  - valid plans,
  - misspelled or unknown plans,
  - numeric prices,
  - validation failures,
  - clean-file manual corrections,
  - unknown countries,
  - unknown subscription customers,
  - MRR reporting period,
  - open-ended subscriptions,
  - JSON output keys.

### AI usage documentation

User prompt:

> Write this entire conversation on the appropriate file.

AI actions:

- Replaced the placeholder `AI_USAGE.md` with this chronological AI usage log.

## Verification Commands Used

The following commands were used throughout the conversation to verify the project:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format .
.\.venv\Scripts\python.exe main.py data\customers_clean.csv data\subscriptions_clean.csv output.json
```
