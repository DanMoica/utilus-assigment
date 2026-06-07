import logging
from pathlib import Path

import pandas as pd
import pytest

from assignment.saas_metrics.loader import _parse_required_date, load_subscriptions


def test_parse_required_date_logs_reformatted_values(caplog: pytest.LogCaptureFixture) -> None:
    """Verify that required dates log when values are reformatted.

    Args:
        caplog: Pytest fixture for capturing log records.

    Returns:
        None.
    """
    dates = pd.Series(["01/02/2024"])

    with caplog.at_level(logging.INFO):
        parsed = _parse_required_date(dates, "signup_date")

    assert parsed.dt.strftime("%Y-%m-%d").tolist() == ["2024-01-02"]
    assert "Reformatted required date value(s) in signup_date at rows [0]" in caplog.text


def test_parse_required_date_logs_bad_rows(caplog: pytest.LogCaptureFixture) -> None:
    """Verify that malformed required dates are logged and rejected.

    Args:
        caplog: Pytest fixture for capturing log records.

    Returns:
        None.
    """
    dates = pd.Series(["not-a-date"])

    with caplog.at_level(logging.ERROR), pytest.raises(ValueError):
        _parse_required_date(dates, "signup_date")

    assert (
        "Malformed required date values in signup_date at rows [0]: ['not-a-date']" in caplog.text
    )


def test_load_subscriptions_rejects_invalid_plan(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Verify that misspelled subscription plans are logged and rejected.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture for capturing log records.

    Returns:
        None.
    """
    subscriptions_path = tmp_path / "subscriptions.csv"
    subscriptions_path.write_text(
        "customer_id,start_date,end_date,plan,monthly_price\nC001,2024-01-01,,baisc,30\n",
        encoding="utf-8",
    )

    with caplog.at_level(logging.ERROR), pytest.raises(ValueError):
        load_subscriptions(subscriptions_path)

    assert "subscriptions.csv contains invalid plan values at rows [0]: ['baisc']" in caplog.text
