from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class S3Settings:
    endpoint_url: str | None
    region: str
    access_key: str
    secret_key: str
    bucket: str
