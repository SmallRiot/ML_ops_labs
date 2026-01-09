from __future__ import annotations

import boto3

from .config import S3Settings


def create_s3_client(settings: S3Settings):
    return boto3.client(
        "s3",
        aws_access_key_id=settings.access_key,
        aws_secret_access_key=settings.secret_key,
        region_name=settings.region,
        endpoint_url=settings.endpoint_url,
    )
