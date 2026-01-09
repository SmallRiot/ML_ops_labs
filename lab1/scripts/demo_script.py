"""Small script for lint/type-check validation."""

from __future__ import annotations

from mlops_lab1 import format_summary, summarize_numbers


def main() -> None:
    data = [10.0, 20.5, 30.25]
    summary = summarize_numbers(data)
    print(format_summary(summary))


if __name__ == "__main__":
    main()
