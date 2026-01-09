from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from .paths import MODEL_PATH


@dataclass(frozen=True)
class PredictResponse:
    predicted_class: str
    probabilities: dict[str, float]


def load_model(path=MODEL_PATH) -> LogisticRegression:
    return joblib.load(path)


def predict(model: LogisticRegression, features: Sequence[float]) -> PredictResponse:
    if len(features) != 4:
        raise ValueError("expected 4 features")

    data = np.array([features], dtype=float)
    proba = model.predict_proba(data)[0]
    classes = model.classes_
    probabilities = {str(label): float(score) for label, score in zip(classes, proba)}
    predicted = str(classes[int(np.argmax(proba))])
    return PredictResponse(predicted_class=predicted, probabilities=probabilities)
