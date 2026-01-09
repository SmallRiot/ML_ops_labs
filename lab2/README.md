# Lab 2 - S3 Pipeline (first person)

I keep this lab under `lab2/` and use Poetry as the dependency manager.

## Dataset

I use the Iris dataset (CSV). Source: https://archive.ics.uci.edu/ml/datasets/iris
I store the raw dataset in S3 without modifications.

## Setup (Unix)

```bash
cd /path/to/ML_ops_labs/lab2
poetry install
```

## Start local S3 (MinIO)

```bash
cd /path/to/ML_ops_labs/lab2
cp .env.example .env
docker compose up -d
```

## Upload raw dataset to S3

```bash
poetry run python scripts/upload_raw.py \
  --source data/raw/iris.csv \
  --bucket mlops-lab2 \
  --key raw/iris.csv
```

## Run the full pipeline (one button)

```bash
poetry run python scripts/run_pipeline.py \
  --bucket mlops-lab2 \
  --raw-key raw/iris.csv \
  --processed-key processed/iris_normalized.csv
```

## Run steps separately (modular)

```bash
poetry run python scripts/download_raw.py \
  --bucket mlops-lab2 \
  --key raw/iris.csv

poetry run python scripts/process_data.py \
  --input data/raw/iris.csv \
  --output data/processed/iris_normalized.csv

poetry run python scripts/upload_processed.py \
  --bucket mlops-lab2 \
  --key processed/iris_normalized.csv \
  --source data/processed/iris_normalized.csv
```

## Notes

- I pass S3 credentials and endpoint via CLI arguments or environment variables.
- Default environment values are in `.env.example`.
