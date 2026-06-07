# Assumptions

## General Assumptions

1. The solution will be implemented as a small Python package under `src/assignment`.
2. CSV processing will use `pandas` for readability and reliability.
3. The program is intended to be run from the project root with:

   ```powershell
   python main.py customers.csv subscriptions.csv output.json
   ```

4. The input files are CSV files with headers.
5. `customers.csv` contains one row per customer.
6. `subscriptions.csv` contains one row per subscription period or plan period.
7. `customer_id` is the primary identifier for a customer.
8. Each row in `customers.csv` should represent one unique customer.
9. Dates are ISO formatted as `YYYY-MM-DD`.
10. Empty `end_date` means the subscription is active.
11. `end_date` is treated as inclusive.
12. A subscription contributes its full `monthly_price` to any month in which it is active for at least one day.
13. Multiple subscription periods for the same customer in the same month are counted independently if each period is active for at least one day in that month.
14. A customer can churn and later re-subscribe.
15. A re-subscription within 30 days after `end_date` means the previous subscription is not counted as churn.
16. A re-subscription exactly on the 30-day boundary is considered within the 30-day grace period.
17. For 3-month retention, the customer is retained if they have any subscription active exactly 3 calendar months after their individual `signup_date`.
18. Valid subscription plans are `basic` and `pro`.
19. Misspelled or unknown plan names are treated as invalid input and are not auto-corrected by the program.
20. `monthly_price` must be numeric.
21. Invalid dates, malformed prices, missing required columns, duplicate customers, empty customer IDs, and invalid plans fail validation.
22. Clean input files may include manual corrections, but normal program execution expects valid input and raises errors for invalid data.
23. Empty or missing country values may be normalized to `UNKNOWN` in cleaned data.
24. Unknown subscription customers are currently included in subscription-based metrics such as MRR and churn, but they cannot contribute to signup cohort retention unless they also exist in `customers.csv`.
25. The MRR reporting period starts with the first subscription month and ends with the latest month represented by subscription start or end dates.
26. Open-ended subscriptions are treated as active through the report period.
27. The output file is JSON with top-level keys `monthly_mrr`, `monthly_churned_customers`, and `signup_cohorts_3_month_retention`.
