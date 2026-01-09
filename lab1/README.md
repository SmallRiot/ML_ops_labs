# Lab 1 - MLOps

Minimal Python project scaffold for DS/MLOps labs (branch edit).

## Project layout

- `lab1/src/mlops_lab1`: package code
- `lab1/scripts`: demo script for lint/type checks

## Setup (Unix)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r lab1/requirements-dev.txt
```

## Install pre-commit hooks

```bash
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
