from __future__ import annotations

import asyncio
import json
import statistics
import time
from argparse import ArgumentParser
from pathlib import Path

import httpx


def _parse_concurrency_list(value: str) -> list[int]:
    return [int(item.strip()) for item in value.split(",") if item.strip()]


def _load_payload(payload_json: str | None, payload_file: str | None) -> dict:
    if payload_json:
        return json.loads(payload_json)
    if payload_file:
        return json.loads(Path(payload_file).read_text(encoding="utf-8"))
    return {"features": [5.1, 3.5, 1.4, 0.2]}


def _quantile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    rank = int((q / 100.0) * len(sorted_values) + 0.999999)
    index = min(max(rank - 1, 0), len(sorted_values) - 1)
    return sorted_values[index]


def _summarize(times: list[float]) -> dict[str, float]:
    values = sorted(times)
    return {
        "avg": statistics.mean(values),
        "q25": _quantile(values, 25),
        "q50": _quantile(values, 50),
        "q90": _quantile(values, 90),
        "q95": _quantile(values, 95),
        "q99": _quantile(values, 99),
    }


async def _worker(
    client: httpx.AsyncClient,
    url: str,
    payload: dict,
    semaphore: asyncio.Semaphore,
    timings: list[float],
) -> None:
    async with semaphore:
        start = time.perf_counter()
        response = await client.post(url, json=payload)
        response.raise_for_status()
        timings.append(time.perf_counter() - start)


async def _run_load(
    url: str,
    total_requests: int,
    concurrency: int,
    payload: dict,
) -> list[float]:
    semaphore = asyncio.Semaphore(concurrency)
    timings: list[float] = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [
            _worker(client, url, payload, semaphore, timings)
            for _ in range(total_requests)
        ]
        await asyncio.gather(*tasks)
    return timings


def main() -> None:
    parser = ArgumentParser(description="Load test the /predict endpoint")
    parser.add_argument("--url", required=True, help="Predict endpoint URL")
    parser.add_argument("--total-requests", type=int, default=500)
    parser.add_argument("--concurrency-list", default="1,2,5,10,20,50")
    parser.add_argument("--payload-json", default=None)
    parser.add_argument("--payload-file", default=None)
    args = parser.parse_args()

    payload = _load_payload(args.payload_json, args.payload_file)
    concurrencies = _parse_concurrency_list(args.concurrency_list)

    print("N,avg,q25,q50,q90,q95,q99")
    for concurrency in concurrencies:
        timings = asyncio.run(_run_load(args.url, args.total_requests, concurrency, payload))
        stats = _summarize(timings)
        print(
            f"{concurrency},"
            f"{stats['avg']:.6f},"
            f"{stats['q25']:.6f},"
            f"{stats['q50']:.6f},"
            f"{stats['q90']:.6f},"
            f"{stats['q95']:.6f},"
            f"{stats['q99']:.6f}"
        )


if __name__ == "__main__":
    main()
