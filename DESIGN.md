# Design

The code is split into a few small parts:

- `main.py` handles the CLI, logging, and writing the JSON output.
- `loader.py` loads and validates the CSV files.
- `metrics.py` contains the MRR, churn, and cohort logic.
- `report.py` combines the metrics into one JSON report.

For MRR, I count a subscription as active in a month if it overlaps with that calendar month. If it is active for any part of the month, the full `monthly_price` is counted.

For churn, I count a churn event when a subscription ends and the customer does not start a new subscription within 30 days. A re-subscription exactly 30 days later is not counted as churn.

For cohorts, I group customers by signup month and check if they have any active subscription exactly 3 months after their signup date.

To add another metric, I would add a new function in `metrics.py`, test it, and include it in `report.py`.

Assumptions:

- `end_date` is inclusive.
- Empty `end_date` means active.
- Valid plans are `basic` and `pro`.
- Unknown subscription customers are logged and excluded.
- Invalid dates, prices, plans, missing columns, and duplicate customers fail validation.
- The solution favors clarity over performance.