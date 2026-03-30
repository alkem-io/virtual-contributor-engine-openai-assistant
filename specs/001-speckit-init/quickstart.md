# Quickstart: speckit-init

## Prerequisites
- Python 3.12+
- Poetry installed

## Setup
```bash
poetry install
```

## Run Linting
```bash
poetry run flake8
```

## Run Tests
```bash
poetry run pytest --cov --cov-report=term-missing
```

## CI
CI runs automatically on push/PR via `.github/workflows/ci.yml`.

## Speckit Workflow
1. `/speckit.specify "feature description"` — Create specification
2. `/speckit.plan` — Generate implementation plan
3. `/speckit.tasks` — Break into tasks
4. `/speckit.implement` — Execute tasks
