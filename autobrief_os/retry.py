from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def with_retry(
    fn: Callable[[], T],
    attempts: int = 3,
    base_delay_seconds: float = 0.2,
    retriable: tuple[type[Exception], ...] = (Exception,),
) -> T:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except retriable as exc:
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(base_delay_seconds * attempt)
    assert last_error is not None
    raise last_error
