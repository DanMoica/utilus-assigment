import pandas as pd

from assignment.saas_metrics.metrics import calculate_monthly_churn


def test_churn_counts_customer_without_resubscription():
    subscriptions = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "start_date": pd.Timestamp("2024-01-01"),
                "end_date": pd.Timestamp("2024-01-31"),
                "plan": "basic",
                "monthly_price": 30.0,
            }
        ]
    )

    assert calculate_monthly_churn(subscriptions) == {"2024-01": 1}


def test_no_churn_when_resubscription_is_within_30_days():
    subscriptions = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "start_date": pd.Timestamp("2024-01-01"),
                "end_date": pd.Timestamp("2024-01-31"),
                "plan": "basic",
                "monthly_price": 30.0,
            },
            {
                "customer_id": "C001",
                "start_date": pd.Timestamp("2024-03-01"),
                "end_date": pd.NaT,
                "plan": "pro",
                "monthly_price": 50.0,
            },
        ]
    )

    assert calculate_monthly_churn(subscriptions) == {}
