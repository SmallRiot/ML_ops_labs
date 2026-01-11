# Lab 1 - MLOps

I use the cookiecutter-data-science template (v1) for this lab.

## Project layout

- `data/`: datasets (raw/interim/processed)
- `docs/`: documentation
- `models/`: trained models
- `notebooks/`: Jupyter notebooks
- `references/`: manuals and data dictionaries
- `reports/`: generated reports and figures
- `src/`: project code (including `src/mlops_lab1`)
- `scripts/`: demo scripts for lint/type checks

## Setup (Unix)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r lab1/requirements-dev.txt
```

## Install pre-commit hooks

```bash
cd /path/to/ML_ops_labs
pre-commit install
```

## Run checks locally

```bash
flake8 lab1/src lab1/scripts
mypy lab1/src lab1/scripts
```

## Run demo script

```bash
python lab1/scripts/demo_script.py
```

## Template reference

Project based on the cookiecutter-data-science template:
https://drivendata.github.io/cookiecutter-data-science/
