from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from mlops_lab2.processing import normalize_csv


def main() -> None:
    parser = ArgumentParser(description="Normalize raw dataset and save processed file")
    parser.add_argument("--input", required=True, help="Path to raw CSV")
    parser.add_argument("--output", required=True, help="Path to processed CSV")
    args = parser.parse_args()

    normalize_csv(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()
