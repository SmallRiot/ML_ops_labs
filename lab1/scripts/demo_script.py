"""Small script for lint/type-check validation."""

from __future__ import annotations

from mlops_lab1 import summarize_numbers


def main() -> None:
    data = [10.0, 20.5, 30.25]
    summary = summarize_numbers(data)
    print(f"count={summary.count} total={summary.total:.2f} mean={summary.mean:.2f}")


if __name__ == "__main__":
    main()
