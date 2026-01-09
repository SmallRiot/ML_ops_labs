from __future__ import annotations

from pathlib import Path

from botocore.exceptions import ClientError


def ensure_bucket(client, bucket: str) -> None:
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")
        if error_code not in {"404", "NoSuchBucket"}:
            raise
        client.create_bucket(Bucket=bucket)


def download_file(client, bucket: str, key: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    client.download_file(bucket, key, str(destination))
    return destination


def upload_file(client, bucket: str, key: str, source: Path) -> None:
    source.parent.mkdir(parents=True, exist_ok=True)
    client.upload_file(str(source), bucket, key)
