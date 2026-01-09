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

CPU (wmic on Windows; `lscpu` is not available here):

```
MaxClockSpeed  Name                                  NumberOfCores  NumberOfLogicalProcessors
2500           12th Gen Intel(R) Core(TM) i5-12400F  6              12
```

GPU (`nvidia-smi`):

```
Fri Jan  9 18:49:02 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 576.02                 Driver Version: 576.02         CUDA Version: 12.9     |
|-----------------------------------------+------------------------+----------------------|
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 2060 ...  WDDM  |   00000000:01:00.0  On |                  N/A |
| 29%   38C    P8             19W /  175W |    1743MiB /   8192MiB |     32%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
```

Results (seconds):

| N | avg | q25 | q50 | q90 | q95 | q99 |
|---|-----|-----|-----|-----|-----|-----|
| 1 | 0.002263 | 0.001815 | 0.002040 | 0.003202 | 0.003342 | 0.003683 |
| 2 | 0.003126 | 0.002670 | 0.002972 | 0.004006 | 0.004207 | 0.004842 |
| 5 | 0.005485 | 0.004609 | 0.005333 | 0.007044 | 0.007658 | 0.009815 |
| 10 | 0.012609 | 0.009184 | 0.010947 | 0.018821 | 0.023511 | 0.031659 |
| 20 | 0.048928 | 0.025003 | 0.037451 | 0.095412 | 0.122798 | 0.168436 |
| 50 | 0.075826 | 0.066824 | 0.073950 | 0.092933 | 0.114153 | 0.127580 |

## Notes

- I keep all CLI parameters outside the code.
- The service expects a list of 4 numeric features in order:
  sepal_length, sepal_width, petal_length, petal_width.
