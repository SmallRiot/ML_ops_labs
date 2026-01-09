from __future__ import annotations

import boto3


def create_s3_client(
    *,
    access_key: str,
    secret_key: str,
    region: str,
    endpoint_url: str | None,
):
    return boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
        endpoint_url=endpoint_url,
    )
