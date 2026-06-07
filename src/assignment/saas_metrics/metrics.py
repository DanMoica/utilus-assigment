import pandas as pd


def calculate_monthly_mrr(subscriptions: pd.DataFrame) -> dict[str, float]:
    """Calculate Monthly Recurring Revenue by calendar month.

    A subscription contributes its full monthly price to every month where it is
    active for at least one day.

    Args:
        subscriptions: Validated subscription records.

    Returns:
        Mapping of month in YYYY-MM format to total MRR.
    """
    if subscriptions.empty:
        return {}

    first_month = subscriptions["start_date"].min().to_period("M").to_timestamp()
    last_candidates = subscriptions["end_date"].dropna()

    if last_candidates.empty:
        last_month = pd.Timestamp.today().normalize().to_period("M").to_timestamp()
    else:
        last_month = (
            max(subscriptions["start_date"].max(), last_candidates.max())
            .to_period("M")
            .to_timestamp()
        )

    months = pd.date_range(first_month, last_month, freq="MS")

    result: dict[str, float] = {}

    for month_start in months:
        month_end = month_start + pd.offsets.MonthEnd(0)

        active = subscriptions[
            (subscriptions["start_date"] <= month_end)
            & (subscriptions["end_date"].isna() | (subscriptions["end_date"] >= month_start))
        ]

        result[month_start.strftime("%Y-%m")] = round(float(active["monthly_price"].sum()), 2)

    return result


def calculate_monthly_churn(subscriptions: pd.DataFrame) -> dict[str, int]:
    """Calculate monthly churned customer counts.

    A subscription end is counted as churn unless the same customer starts a new
    subscription within 30 days after the end date.

    Args:
        subscriptions: Validated subscription records.

    Returns:
        Mapping of month in YYYY-MM format to churned customer count.
    """

    churn_counts: dict[str, int] = {}

    ended_subscriptions = subscriptions[subscriptions["end_date"].notna()].copy()

    for _, row in ended_subscriptions.iterrows():
        customer_id = row["customer_id"]
        end_date = row["end_date"]

        later_subscriptions = subscriptions[
            (subscriptions["customer_id"] == customer_id)
            & (subscriptions["start_date"] > end_date)
            & (subscriptions["start_date"] <= end_date + pd.Timedelta(days=30))
        ]

        if later_subscriptions.empty:
            month = end_date.strftime("%Y-%m")
            churn_counts[month] = churn_counts.get(month, 0) + 1

    return dict(sorted(churn_counts.items()))


def calculate_signup_cohort_retention(
    customers: pd.DataFrame,
    subscriptions: pd.DataFrame,
) -> dict[str, dict[str, float | int]]:
    """Calculate three-month retention by signup cohort.

    Args:
        customers: Validated customer records.
        subscriptions: Validated subscription records.

    Returns:
        Mapping of signup cohort month to cohort size, retained customers, and
        retention rate after three months.
    """
    result: dict[str, dict[str, float | int]] = {}

    customers = customers.copy()
    customers["cohort_month"] = customers["signup_date"].dt.strftime("%Y-%m")

    for cohort_month, cohort in customers.groupby("cohort_month"):
        cohort_size = len(cohort)
        active_after_3_months = 0

        for _, customer in cohort.iterrows():
            customer_id = customer["customer_id"]
            checkpoint = customer["signup_date"] + pd.DateOffset(months=3)

            customer_subscriptions = subscriptions[subscriptions["customer_id"] == customer_id]

            active = customer_subscriptions[
                (customer_subscriptions["start_date"] <= checkpoint)
                & (
                    customer_subscriptions["end_date"].isna()
                    | (customer_subscriptions["end_date"] >= checkpoint)
                )
            ]

            if not active.empty:
                active_after_3_months += 1

        result[cohort_month] = {
            "cohort_size": int(cohort_size),
            "active_after_3_months": int(active_after_3_months),
            "retention_rate_3m": round(active_after_3_months / cohort_size, 4),
        }

    return dict(sorted(result.items()))
