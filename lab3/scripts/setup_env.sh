#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

IMAGE_NAME=mlops-lab3-train

docker build -t "$IMAGE_NAME" .
docker compose up -d
