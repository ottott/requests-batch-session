import time

import requests

from requests import BatchSession

NUM_REQUESTS = 50
URL = "https://httpbin.org/delay/1"


def benchmark_sequential() -> float:
    session = requests.Session()

    start = time.perf_counter()

    for _ in range(NUM_REQUESTS):
        session.get(URL)

    return time.perf_counter() - start


def benchmark_batch() -> float:
    session = BatchSession()

    for _ in range(NUM_REQUESTS):
        session.queue_get(URL)

    start = time.perf_counter()

    session.execute()

    return time.perf_counter() - start


if __name__ == "__main__":
    sequential_time = benchmark_sequential()
    batch_time = benchmark_batch()

    print(f"Benchmark ({NUM_REQUESTS} requests)")
    print("-" * 30)
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Batch:      {batch_time:.2f}s")
    print(f"Speedup:    {sequential_time / batch_time:.2f}x")