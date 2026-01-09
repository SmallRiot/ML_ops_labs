from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import joblib
import mlflow

from .config import S3Settings
from .data import load_dataset
from .modeling import TrainResult, model_params_from_config, train_model
from .paths import ARTIFACTS_DIR, PROCESSED_DIR
from .s3_client import create_s3_client
from .s3_io import download_file, ensure_bucket, upload_file


@dataclass(frozen=True)
class ExperimentResult:
    run_id: str
    metrics: dict[str, float]
    model_path: Path


def _save_artifacts(
    experiment_name: str,
    run_id: str,
    result: TrainResult,
) -> Path:
    output_dir = ARTIFACTS_DIR / experiment_name / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "model.pkl"
    metrics_path = output_dir / "metrics.json"

    joblib.dump(result.model, model_path)
    metrics_path.write_text(json.dumps(result.metrics, indent=2), encoding="utf-8")

    return model_path


def run_experiment(
    *,
    experiment_name: str,
    dataset_key: str,
    s3_settings: S3Settings,
    tracking_uri: str,
    params: dict[str, float | int | str],
) -> ExperimentResult:
    client = create_s3_client(s3_settings)
    ensure_bucket(client, s3_settings.bucket)

    local_dataset = PROCESSED_DIR / Path(dataset_key).name
    download_file(client, s3_settings.bucket, dataset_key, local_dataset)

    data = load_dataset(local_dataset)
    train_params = model_params_from_config(params)
    train_result = train_model(data, **train_params)

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run() as run:
        mlflow.log_params(train_params)
        mlflow.log_metrics(train_result.metrics)

        model_path = _save_artifacts(experiment_name, run.info.run_id, train_result)
        mlflow.log_artifact(str(model_path))

        s3_prefix = f"models/{experiment_name}/{run.info.run_id}"
        upload_file(client, s3_settings.bucket, f"{s3_prefix}/model.pkl", model_path)
        upload_file(
            client,
            s3_settings.bucket,
            f"{s3_prefix}/metrics.json",
            model_path.with_name("metrics.json"),
        )

        return ExperimentResult(
            run_id=run.info.run_id,
            metrics=train_result.metrics,
            model_path=model_path,
        )
