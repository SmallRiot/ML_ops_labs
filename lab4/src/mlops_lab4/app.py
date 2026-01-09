from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .paths import MODEL_PATH
from .predictor import PredictResponse, load_model, predict

app = FastAPI(title="mlops-lab4")


class PredictRequest(BaseModel):
    features: list[float]


@app.on_event("startup")
def _load_model() -> None:
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model not found at {MODEL_PATH}")
    app.state.model = load_model(MODEL_PATH)


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(payload: PredictRequest) -> PredictResponse:
    try:
        return predict(app.state.model, payload.features)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
