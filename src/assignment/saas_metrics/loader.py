import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

CUSTOMER_COLUMNS = {"customer_id", "signup_date", "country"}
SUBSCRIPTION_COLUMNS = {
    "customer_id",
    "start_date",
    "end_date",
    "plan",
    "monthly_price",
}
ALLOWED_PLANS = {"basic", "pro"}


def load_customers(path: Path) -> pd.DataFrame:
    """Load and validate customer records from a CSV file.

    Args:
        path: Path to the customers CSV file.

    Returns:
        Validated customer records with normalized values.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing or customer data is invalid.
    """
    df = _read_csv(path)
    _validate_required_columns(df, CUSTOMER_COLUMNS, "customers.csv")

    df = df.copy()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["country"] = df["country"].astype(str).str.strip()
    df["signup_date"] = _parse_required_date(df["signup_date"], "signup_date")

    duplicate_ids = df[df.duplicated("customer_id", keep=False)]["customer_id"].unique()
    if len(duplicate_ids) > 0:
        message = f"Duplicate customer_id values found in customers.csv: {sorted(duplicate_ids)}"
        logger.error(message)
        raise ValueError(message)

    if df["customer_id"].eq("").any():
        message = "customers.csv contains empty customer_id values"
        logger.error(message)
        raise ValueError(message)

    return df


def load_subscriptions(path: Path) -> pd.DataFrame:
    """Load and validate subscription records from a CSV file.

    Args:
        path: Path to the subscriptions CSV file.

    Returns:
        Validated subscription records with parsed dates and numeric prices.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing or subscription data is invalid.
    """
    df = _read_csv(path)
    _validate_required_columns(df, SUBSCRIPTION_COLUMNS, "subscriptions.csv")

    df = df.copy()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["plan"] = df["plan"].astype(str).str.strip()

    invalid_plans = df[~df["plan"].isin(ALLOWED_PLANS)]
    if not invalid_plans.empty:
        bad_rows = invalid_plans.index.tolist()
        bad_values = invalid_plans["plan"].tolist()
        message = (
            f"subscriptions.csv contains invalid plan values at rows {bad_rows}: "
            f"{bad_values}. Allowed plans: {sorted(ALLOWED_PLANS)}"
        )
        logger.error(message)
        raise ValueError(message)

    df["start_date"] = _parse_required_date(df["start_date"], "start_date")
    df["end_date"] = _parse_optional_date(df["end_date"], "end_date")

    prices = pd.to_numeric(df["monthly_price"], errors="coerce")
    invalid_prices = df[prices.isna()]

    if not invalid_prices.empty:
        bad_rows = invalid_prices.index.tolist()
        bad_values = invalid_prices["monthly_price"].tolist()
        message = (
            f"subscriptions.csv contains malformed monthly_price values "
            f"at rows {bad_rows}: {bad_values}"
        )
        logger.error(message)
        raise ValueError(message)

    df["monthly_price"] = prices.astype(float)

    invalid_ranges = df[df["end_date"].notna() & (df["end_date"] < df["start_date"])]
    if not invalid_ranges.empty:
        message = (
            f"subscriptions.csv contains rows where end_date is before start_date: "
            f"{invalid_ranges.index.tolist()}"
        )
        logger.error(message)
        raise ValueError(message)

    if df["customer_id"].eq("").any():
        message = "subscriptions.csv contains empty customer_id values"
        logger.error(message)
        raise ValueError(message)

    return df


def _read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV file from disk.

    Args:
        path: Path to the CSV file.

    Returns:
        DataFrame loaded from the CSV file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If pandas cannot read the CSV file.
    """
    if not path.exists():
        message = f"File not found: {path}"
        logger.error(message)
        raise FileNotFoundError(message)

    try:
        return pd.read_csv(path)
    except Exception as exc:
        message = f"Could not read CSV file {path}: {exc}"
        logger.error(message)
        raise ValueError(message) from exc


def _validate_required_columns(
    df: pd.DataFrame,
    required_columns: set[str],
    file_name: str,
) -> None:
    """Validate that a DataFrame contains required columns.

    Args:
        df: DataFrame to validate.
        required_columns: Column names that must be present.
        file_name: Human-readable file name for error messages.

    Returns:
        None.

    Raises:
        ValueError: If one or more required columns are missing.
    """
    missing = required_columns - set(df.columns)
    if missing:
        message = f"{file_name} is missing required columns: {sorted(missing)}"
        logger.error(message)
        raise ValueError(message)


def _parse_required_date(series: pd.Series, column_name: str) -> pd.Series:
    """Parse and normalize a required date column.

    Args:
        series: Series containing date values.
        column_name: Column name used in log and error messages.

    Returns:
        Series of normalized pandas timestamps.

    Raises:
        ValueError: If any value cannot be parsed as a date.
    """
    parsed = pd.to_datetime(series, errors="coerce", format="mixed")

    if parsed.isna().any():
        bad_rows = parsed[parsed.isna()].index.tolist()
        bad_values = series[parsed.isna()].tolist()
        message = (
            f"Malformed required date values in {column_name} at rows {bad_rows}: {bad_values}"
        )
        logger.error(message)
        raise ValueError(message)

    normalized = parsed.dt.normalize()
    raw_values = series.astype(str).str.strip()
    normalized_values = normalized.dt.strftime("%Y-%m-%d")
    reformatted = raw_values.ne(normalized_values)

    if reformatted.any():
        rows = reformatted[reformatted].index.tolist()
        logger.info(
            "Reformatted required date value(s) in %s at rows %s to YYYY-MM-DD",
            column_name,
            rows,
        )

    return normalized


def _parse_optional_date(series: pd.Series, column_name: str) -> pd.Series:
    """Parse and normalize an optional date column.

    Args:
        series: Series containing date values, blanks, or missing values.
        column_name: Column name used in log and error messages.

    Returns:
        Series of normalized pandas timestamps with missing values preserved.

    Raises:
        ValueError: If a non-empty value cannot be parsed as a date.
    """
    parsed = pd.to_datetime(series, errors="coerce")

    raw_has_value = series.notna() & series.astype(str).str.strip().ne("")
    malformed = raw_has_value & parsed.isna()

    if malformed.any():
        bad_rows = malformed[malformed].index.tolist()
        bad_values = series[malformed].tolist()
        message = f"Malformed date values in {column_name} at rows {bad_rows}: {bad_values}"
        logger.error(message)
        raise ValueError(message)

    return parsed.dt.normalize()
