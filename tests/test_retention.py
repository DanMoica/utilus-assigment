import pandas as pd

from assignment.saas_metrics.metrics import calculate_signup_cohort_retention


def test_customer_active_exactly_three_months_after_signup_is_retained():
    customers = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "signup_date": pd.Timestamp("2024-01-15"),
                "country": "NL",
            }
        ]
    )

    subscriptions = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "start_date": pd.Timestamp("2024-01-15"),
                "end_date": pd.Timestamp("2024-04-15"),
                "plan": "basic",
                "monthly_price": 30.0,
            }
        ]
    )

    result = calculate_signup_cohort_retention(customers, subscriptions)

    assert result["2024-01"] == {
        "cohort_size": 1,
        "active_after_3_months": 1,
        "retention_rate_3m": 1.0,
    }


def test_customer_ended_before_three_month_checkpoint_is_not_retained():
    customers = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "signup_date": pd.Timestamp("2024-01-15"),
                "country": "NL",
            }
        ]
    )

    subscriptions = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "start_date": pd.Timestamp("2024-01-15"),
                "end_date": pd.Timestamp("2024-04-14"),
                "plan": "basic",
                "monthly_price": 30.0,
            }
        ]
    )

    result = calculate_signup_cohort_retention(customers, subscriptions)

    assert result["2024-01"] == {
        "cohort_size": 1,
        "active_after_3_months": 0,
        "retention_rate_3m": 0.0,
    }
