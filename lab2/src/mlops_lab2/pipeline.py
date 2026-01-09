from __future__ import annotations

from pathlib import Path

from .paths import PROCESSED_DIR, RAW_DIR
from .processing import normalize_csv
from .s3_client import create_s3_client
from .s3_io import download_file, ensure_bucket, upload_file


def run_pipeline(
    *,
    endpoint_url: str | None,
    region: str,
    access_key: str,
    secret_key: str,
    bucket: str,
    raw_key: str,
    processed_key: str,
) -> Path:
    client = create_s3_client(
        access_key=access_key,
        secret_key=secret_key,
        region=region,
        endpoint_url=endpoint_url,
    )
    ensure_bucket(client, bucket)

    raw_path = RAW_DIR / Path(raw_key).name
    download_file(client, bucket, raw_key, raw_path)

    processed_path = PROCESSED_DIR / Path(processed_key).name
    normalize_csv(raw_path, processed_path)

    upload_file(client, bucket, processed_key, processed_path)
    return processed_path
