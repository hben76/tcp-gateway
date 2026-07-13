#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# ssh_benchmark.py
#

"""
TCP Gateway SSH benchmark.

Benchmark the SSH connectivity endpoint.

Examples:

Basic benchmark:

    python3 tests/ssh_benchmark.py \
        --url http://localhost:59876 \
        --name awx \
        --apikey awx-secret-key

High load:

    python3 tests/ssh_benchmark.py \
        --url http://localhost:59876 \
        --name awx \
        --apikey awx-secret-key \
        --requests 5000 \
        --workers 100

Different target:

    python3 tests/ssh_benchmark.py \
        --url http://localhost:59876 \
        --name awx \
        --apikey awx-secret-key \
        --target 192.168.1.4
"""

from __future__ import annotations

import argparse
import concurrent.futures
import statistics
import time
from functools import partial

import requests


CLIENT_NAME_HEADER = "X-Client-Name"
API_KEY_HEADER = "X-API-Key"

DEFAULT_API_PREFIX = "/v1"


class HelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    """Argument parser help formatter."""


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="TCP Gateway SSH benchmark.",
        formatter_class=HelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Gateway base URL.",
    )

    parser.add_argument(
        "--api-prefix",
        default=DEFAULT_API_PREFIX,
        help="API prefix.",
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Client name.",
    )

    parser.add_argument(
        "--apikey",
        required=True,
        help="API key.",
    )

    parser.add_argument(
        "--target",
        default="localhost",
        help="Target hostname.",
    )

    parser.add_argument(
        "--target-port",
        type=int,
        default=22,
        help="Target SSH port.",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="SSH timeout in seconds.",
    )

    parser.add_argument(
        "--requests",
        type=int,
        default=1000,
        help="Number of requests.",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=50,
        help="Concurrent workers.",
    )

    return parser.parse_args()


def worker(
    _: int,
    url: str,
    headers: dict[str, str],
    payload: dict[str, object],
    timeout: int,
) -> tuple[bool, float]:
    """
    Execute a single benchmark request.

    Returns:
        Tuple containing:
            - True if the request succeeded.
            - Elapsed time in milliseconds.
    """

    start = time.perf_counter()

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=max(timeout + 5, 10),
        )

        success = response.status_code == 200

    except requests.RequestException:
        success = False

    elapsed_ms = (time.perf_counter() - start) * 1000

    return success, elapsed_ms


def main() -> int:
    """Program entry point."""

    args = parse_arguments()

    endpoint = f"{args.url}{args.api_prefix}/ssh/check"

    headers = {
        CLIENT_NAME_HEADER: args.name,
        API_KEY_HEADER: args.apikey,
    }

    payload = {
        "host": args.target,
        "port": args.target_port,
        "timeout": args.timeout,
    }

    print("=" * 60)
    print("TCP Gateway SSH Benchmark")
    print("=" * 60)
    print(f"Gateway      : {args.url}")
    print(f"API Prefix   : {args.api_prefix}")
    print(f"Client       : {args.name}")
    print(f"Endpoint     : {args.api_prefix}/ssh/check")
    print(f"Target       : {args.target}:{args.target_port}")
    print(f"Requests     : {args.requests}")
    print(f"Workers      : {args.workers}")
    print()

    benchmark = partial(
        worker,
        url=endpoint,
        headers=headers,
        payload=payload,
        timeout=args.timeout,
    )

    successful = 0
    failed = 0
    latency: list[float] = []

    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.workers,
    ) as executor:
        for success, elapsed_ms in executor.map(
            benchmark,
            range(args.requests),
        ):
            latency.append(elapsed_ms)

            if success:
                successful += 1
            else:
                failed += 1

    duration = time.perf_counter() - start
    completed = successful + failed

    print("=" * 60)
    print("Benchmark Results")
    print("=" * 60)
    print(f"Completed     : {completed}")
    print(f"Successful    : {successful}")
    print(f"Failed        : {failed}")
    print(f"Duration      : {duration:.2f} s")
    print(f"Requests/sec  : {completed / duration:.2f}")

    if latency:
        print()
        print("Latency")
        print("-" * 60)
        print(f"Minimum       : {min(latency):.2f} ms")
        print(f"Average       : {statistics.mean(latency):.2f} ms")
        print(f"Median        : {statistics.median(latency):.2f} ms")
        print(f"Maximum       : {max(latency):.2f} ms")

    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
