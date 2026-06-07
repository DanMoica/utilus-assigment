import pandas as pd

from assignment.saas_metrics.metrics import (
    calculate_monthly_churn,
    calculate_monthly_mrr,
    calculate_signup_cohort_retention,
)


def build_report(customers: pd.DataFrame, subscriptions: pd.DataFrame) -> dict:
    """Build the complete SaaS metrics report.

    Args:
        customers: Validated customer records.
        subscriptions: Validated subscription records.

    Returns:
        Dictionary containing monthly MRR, monthly churn, and signup cohort
        retention metrics.
    """
    return {
        "monthly_mrr": calculate_monthly_mrr(subscriptions),
        "monthly_churned_customers": calculate_monthly_churn(subscriptions),
        "signup_cohorts_3_month_retention": calculate_signup_cohort_retention(
            customers,
            subscriptions,
        ),
    }
