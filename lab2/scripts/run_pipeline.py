from __future__ import annotations

import os
from argparse import ArgumentParser

from mlops_lab2.cli import add_s3_args, s3_settings_from_args
from mlops_lab2.pipeline import run_pipeline


def main() -> None:
    parser = ArgumentParser(description="Run end-to-end S3 pipeline")
    add_s3_args(parser)
    parser.add_argument(
        "--raw-key",
        default=os.getenv("S3_RAW_KEY", "raw/iris.csv"),
        help="S3 object key for raw dataset",
    )
    parser.add_argument(
        "--processed-key",
        default=os.getenv("S3_PROCESSED_KEY", "processed/iris_normalized.csv"),
        help="S3 object key for processed dataset",
    )
    args = parser.parse_args()

    s3_settings = s3_settings_from_args(args)
    run_pipeline(
        endpoint_url=s3_settings["endpoint_url"],
        region=s3_settings["region"],
        access_key=s3_settings["access_key"],
        secret_key=s3_settings["secret_key"],
        bucket=s3_settings["bucket"],
        raw_key=args.raw_key,
        processed_key=args.processed_key,
    )


if __name__ == "__main__":
    main()
