from __future__ import annotations

import os
from argparse import ArgumentParser
from pathlib import Path

from mlops_lab2.cli import add_s3_args, s3_settings_from_args
from mlops_lab2.paths import RAW_DIR
from mlops_lab2.s3_client import create_s3_client
from mlops_lab2.s3_io import download_file, ensure_bucket


def main() -> None:
    parser = ArgumentParser(description="Download raw dataset from S3")
    add_s3_args(parser)
    parser.add_argument(
        "--key",
        default=os.getenv("S3_RAW_KEY", "raw/iris.csv"),
        help="S3 object key for raw dataset",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Local output path (defaults to data/raw/<basename>)",
    )
    args = parser.parse_args()

    s3_settings = s3_settings_from_args(args)
    client = create_s3_client(
        access_key=s3_settings["access_key"],
        secret_key=s3_settings["secret_key"],
        region=s3_settings["region"],
        endpoint_url=s3_settings["endpoint_url"],
    )
    ensure_bucket(client, s3_settings["bucket"])

    output_path = Path(args.output) if args.output else RAW_DIR / Path(args.key).name
    download_file(client, s3_settings["bucket"], args.key, output_path)


if __name__ == "__main__":
    main()
