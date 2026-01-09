from __future__ import annotations

import os
from argparse import ArgumentParser
from pathlib import Path

from mlops_lab2.cli import add_s3_args, s3_settings_from_args
from mlops_lab2.s3_client import create_s3_client
from mlops_lab2.s3_io import ensure_bucket, upload_file


def main() -> None:
    parser = ArgumentParser(description="Upload processed dataset to S3")
    add_s3_args(parser)
    parser.add_argument(
        "--key",
        default=os.getenv("S3_PROCESSED_KEY", "processed/iris_normalized.csv"),
        help="S3 object key for processed dataset",
    )
    parser.add_argument("--source", required=True, help="Local path to processed CSV")
    args = parser.parse_args()

    s3_settings = s3_settings_from_args(args)
    client = create_s3_client(
        access_key=s3_settings["access_key"],
        secret_key=s3_settings["secret_key"],
        region=s3_settings["region"],
        endpoint_url=s3_settings["endpoint_url"],
    )
    ensure_bucket(client, s3_settings["bucket"])

    upload_file(client, s3_settings["bucket"], args.key, Path(args.source))


if __name__ == "__main__":
    main()
