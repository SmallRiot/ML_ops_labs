from __future__ import annotations

import os
from argparse import ArgumentParser, Namespace

from .config import S3Settings


def add_s3_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--endpoint-url",
        default=os.getenv("S3_ENDPOINT_URL", "http://localhost:9000"),
        help="S3 endpoint URL",
    )
    parser.add_argument(
        "--region",
        default=os.getenv("S3_REGION", "us-east-1"),
        help="S3 region",
    )
    parser.add_argument(
        "--access-key",
        default=os.getenv("S3_ACCESS_KEY", "minioadmin"),
        help="S3 access key",
    )
    parser.add_argument(
        "--secret-key",
        default=os.getenv("S3_SECRET_KEY", "minioadmin"),
        help="S3 secret key",
    )
    parser.add_argument(
        "--bucket",
        default=os.getenv("S3_BUCKET", "mlops-lab2"),
        help="S3 bucket name",
    )


def s3_settings_from_args(args: Namespace) -> S3Settings:
    return S3Settings(
        endpoint_url=args.endpoint_url,
        region=args.region,
        access_key=args.access_key,
        secret_key=args.secret_key,
        bucket=args.bucket,
    )


def add_tracking_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--tracking-uri",
        default=os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"),
        help="MLflow tracking URI",
    )
