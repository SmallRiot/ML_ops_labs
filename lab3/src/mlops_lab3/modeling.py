from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

import pandas as pd


@dataclass(frozen=True)
class TrainResult:
    model: LogisticRegression
    metrics: dict[str, float]


def train_model(
    data: pd.DataFrame,
    *,
    test_size: float,
    random_state: int,
    max_iter: int,
    solver: str,
    c_value: float,
) -> TrainResult:
    if "species" not in data.columns:
        raise ValueError("expected 'species' column for target")

    x = data.drop(columns=["species"])
    y = data["species"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state, stratify=y
    )

    model = LogisticRegression(max_iter=max_iter, solver=solver, C=c_value, multi_class="auto")
    model.fit(x_train, y_train)

    preds = model.predict(x_test)
    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "f1_macro": f1_score(y_test, preds, average="macro"),
    }
    return TrainResult(model=model, metrics=metrics)


def model_params_from_config(cfg: dict[str, Any]) -> dict[str, Any]:
    return {
        "test_size": float(cfg.get("test_size", 0.2)),
        "random_state": int(cfg.get("random_state", 42)),
        "max_iter": int(cfg.get("max_iter", 200)),
        "solver": str(cfg.get("solver", "lbfgs")),
        "c_value": float(cfg.get("c_value", 1.0)),
    }
