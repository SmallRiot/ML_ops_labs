from __future__ import annotations

import csv
import statistics
from pathlib import Path
from typing import Iterable


def _is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def _detect_numeric_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []

    numeric_columns: list[str] = []
    for key in rows[0].keys():
        if all(_is_float(row[key]) for row in rows):
            numeric_columns.append(key)
    return numeric_columns


def _column_values(rows: Iterable[dict[str, str]], column: str) -> list[float]:
    return [float(row[column]) for row in rows]


def normalize_csv(input_path: Path, output_path: Path) -> Path:
    with input_path.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    if not rows:
        raise ValueError("input CSV is empty")

    numeric_columns = _detect_numeric_columns(rows)
    means = {
        col: statistics.mean(_column_values(rows, col)) for col in numeric_columns
    }
    stds = {
        col: statistics.pstdev(_column_values(rows, col)) for col in numeric_columns
    }

    for row in rows:
        for col in numeric_columns:
            value = float(row[col])
            std = stds[col]
            row[col] = "0.0" if std == 0 else f"{(value - means[col]) / std:.6f}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return output_path
