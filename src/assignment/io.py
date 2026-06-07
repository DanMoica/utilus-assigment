from pathlib import Path

import pandas as pd


def read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV file using consistent defaults for the assignment."""
    return pd.read_csv(path)
