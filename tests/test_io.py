from pathlib import Path

from assignment.io import read_csv


def test_read_csv_loads_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("id,name\n1,Ada\n2,Grace\n", encoding="utf-8")

    frame = read_csv(csv_path)

    assert list(frame.columns) == ["id", "name"]
    assert len(frame) == 2
