#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

IMAGE_NAME=mlops-lab3-train

# Build training image
Dockerfile_path="Dockerfile"
if [ ! -f "$Dockerfile_path" ]; then
  echo "Dockerfile not found in lab3/" >&2
  exit 1
fi

docker build -t "$IMAGE_NAME" .

# Run experiments from config
CONFIG_PATH=${1:-configs/grid.yaml}

docker run --rm \
  --network host \
  --env-file .env \
  -v "$(pwd)/configs:/app/configs" \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/artifacts:/app/artifacts" \
  "$IMAGE_NAME" \
  python scripts/run_experiments.py --config "$CONFIG_PATH"
