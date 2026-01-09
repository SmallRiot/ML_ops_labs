# Lab 4 - Model Serving (first person)

I keep this lab under `lab4/` and use Poetry as the dependency manager.

## Model

I ship the trained model file with the repository at `lab4/models/model.pkl`.

## Setup (Unix)

```bash
cd /path/to/ML_ops_labs/lab4
poetry install
```

## Train (optional, if I want to rebuild the model)

```bash
poetry run python scripts/train_model.py --output models/model.pkl
```

## Run service (local)

```bash
poetry run uvicorn mlops_lab4.app:app --host 0.0.0.0 --port 8000
```

## Run service (Docker)

```bash
cd /path/to/ML_ops_labs/lab4
docker build -t mlops-lab4-serve .
docker run --rm -p 8000:8000 mlops-lab4-serve
```

## Predict example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

## Load test

```bash
poetry run python scripts/load_test.py \
  --url http://localhost:8000/predict \
  --total-requests 500 \
  --concurrency-list 1,2,5,10,20,50
```

## Load test results

I ran the load test on my machine and recorded the results below.

Hardware info:

```bash
lscpu
nvidia-smi
```

Results (seconds):

| N | avg | q25 | q50 | q90 | q95 | q99 |
|---|-----|-----|-----|-----|-----|-----|
| 1 |     |     |     |     |     |     |
| 2 |     |     |     |     |     |     |
| 5 |     |     |     |     |     |     |
| 10 |    |     |     |     |     |     |
| 20 |    |     |     |     |     |     |
| 50 |    |     |     |     |     |     |

## Notes

- I keep all CLI parameters outside the code.
- The service expects a list of 4 numeric features in order:
  sepal_length, sepal_width, petal_length, petal_width.
