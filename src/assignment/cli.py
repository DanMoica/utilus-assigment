from pathlib import Path

import click

from assignment.io import read_csv


@click.group()
def main() -> None:
    """Command-line interface for the assignment solution."""


@main.command()
@click.argument("csv_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def inspect(csv_path: Path) -> None:
    """Print a small preview of a CSV file."""
    frame = read_csv(csv_path)
    click.echo(f"Rows: {len(frame)}")
    click.echo(f"Columns: {', '.join(frame.columns)}")
    click.echo(frame.head().to_string(index=False))


if __name__ == "__main__":
    main()
