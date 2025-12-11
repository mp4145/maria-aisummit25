import time
from contextlib import contextmanager
from typing import Dict


@contextmanager
def track_timings(bucket: Dict[str, float], key: str):
  start = time.perf_counter()
  try:
    yield
  finally:
    bucket[key] = (time.perf_counter() - start) * 1000.0
