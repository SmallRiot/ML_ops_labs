"""Core business logic for lab1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Summary:
    count: int
    total: float
    mean: float


def summarize_numbers(values: Iterable[float]) -> Summary:
    numbers = list(values)
    if not numbers:
        raise ValueError("values must contain at least one number")

    total = float(sum(numbers))
    count = len(numbers)
    mean = total / count
    return Summary(count=count, total=total, mean=mean)
