import json
from pathlib import Path

from main import build_output


def test_build_output_summarizes_input_files(tmp_path: Path) -> None:
    """Verify that the main output builder returns the metrics report.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    customers_path = tmp_path / "customers.csv"
    subscriptions_path = tmp_path / "subscriptions.csv"

    customers_path.write_text(
        "customer_id,signup_date,country\n1,2024-01-02,RO\n",
        encoding="utf-8",
    )
    subscriptions_path.write_text(
        "customer_id,start_date,end_date,plan,monthly_price\n1,2024-01-02,,basic,30\n",
        encoding="utf-8",
    )

    output = build_output(customers_path, subscriptions_path)

    assert output["monthly_mrr"]["2024-01"] == 30.0
    assert all(value == 30.0 for value in output["monthly_mrr"].values())
    assert output["monthly_churned_customers"] == {}
    assert output["signup_cohorts_3_month_retention"] == {
        "2024-01": {
            "cohort_size": 1,
            "active_after_3_months": 1,
            "retention_rate_3m": 1.0,
        },
    }


def test_output_can_be_written_as_json(tmp_path: Path) -> None:
    """Verify that output dictionaries can be serialized as JSON.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    output_path = tmp_path / "output.json"
    output = {"ok": True}

    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    assert json.loads(output_path.read_text(encoding="utf-8")) == output
