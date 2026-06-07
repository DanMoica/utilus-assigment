# Utilus Interview Assignment

Working solution for the interview assignment.

## Project Layout

- `src/assignment/` - application code
- `tests/` - pytest tests
- `data/` - input CSV files and local sample data
- `ASSUMPTIONS.md` - assumptions made while building the solution
- `AI_USAGE.md` - notes and prompts for AI-assisted work

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run

```powershell
assignment --help
```

Once the CSV requirements are clear, add command examples here.

## Test And Lint

```powershell
pytest
ruff check .
ruff format .
```
