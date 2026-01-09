from __future__ import annotations

from argparse import ArgumentParser
from itertools import product
from pathlib import Path

import yaml

from mlops_lab3.cli import add_s3_args, add_tracking_args, s3_settings_from_args
from mlops_lab3.experiment import run_experiment


def _load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _grid_combinations(grid: dict[str, list]) -> list[dict[str, object]]:
    if not grid:
        return [{}]

    keys = list(grid.keys())
    values = [grid[key] for key in keys]
    combos = []
    for parts in product(*values):
        combos.append(dict(zip(keys, parts)))
    return combos


def main() -> None:
    parser = ArgumentParser(description="Run grid experiments with MLflow")
    parser.add_argument("--config", required=True, help="Path to grid YAML config")
    add_s3_args(parser)
    add_tracking_args(parser)
    args = parser.parse_args()

    cfg = _load_config(Path(args.config))
    experiment_name = cfg["experiment_name"]
    dataset_key = cfg["dataset_key"]
    base_params = cfg.get("base_params", {})
    grid = cfg.get("grid", {})

    for grid_params in _grid_combinations(grid):
        params = {**base_params, **grid_params}
        run_experiment(
            experiment_name=experiment_name,
            dataset_key=dataset_key,
            s3_settings=s3_settings_from_args(args),
            tracking_uri=args.tracking_uri,
            params=params,
        )


if __name__ == "__main__":
    main()
