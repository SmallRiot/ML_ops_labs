# Lab 3 - ML Experiments (first person)

I keep this lab under `lab3/` and use Poetry as the dependency manager.

## Dataset

I use the preprocessed Iris dataset stored in S3 (output of lab2). The dataset is a CSV file.

## Setup (Unix)

```bash
cd /path/to/ML_ops_labs/lab3
poetry install
```

## Start local S3 + MLflow (containers)

```bash
cd /path/to/ML_ops_labs/lab3
cp .env.example .env
./scripts/setup_env.sh
```

## Upload processed dataset to S3 (one time)

```bash
poetry run python scripts/upload_processed.py \
  --source /path/to/ML_ops_labs/lab2/data/processed/iris_normalized.csv \
  --bucket mlops-lab2 \
  --key processed/iris_normalized.csv
```

## Run a single experiment

```bash
poetry run python scripts/train_model.py \
  --config configs/experiment.yaml
```

## Run grid experiments

```bash
poetry run python scripts/run_experiments.py \
  --config configs/grid.yaml
```

## Notes

- I pass all S3 and MLflow settings via CLI or `.env`.
- Each run logs params/metrics to MLflow and uploads the trained model to S3 under
  `models/<experiment_name>/`.
