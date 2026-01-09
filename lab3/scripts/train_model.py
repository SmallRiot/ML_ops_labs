from __future__ import annotations

import os
from argparse import ArgumentParser
from pathlib import Path

from mlops_lab3.cli import add_s3_args, add_tracking_args, s3_settings_from_args
from mlops_lab3.experiment import run_experiment

import yaml


def _load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> None:
    parser = ArgumentParser(description="Run a single MLflow experiment")
    parser.add_argument("--config", required=True, help="Path to experiment YAML config")
    add_s3_args(parser)
    add_tracking_args(parser)
    args = parser.parse_args()

    cfg = _load_config(Path(args.config))
    experiment_name = cfg["experiment_name"]
    dataset_key = cfg.get("dataset_key", os.getenv("S3_PROCESSED_KEY", ""))
    params = cfg.get("params", {})

    run_experiment(
        experiment_name=experiment_name,
        dataset_key=dataset_key,
        s3_settings=s3_settings_from_args(args),
        tracking_uri=args.tracking_uri,
        params=params,
    )


if __name__ == "__main__":
    main()
