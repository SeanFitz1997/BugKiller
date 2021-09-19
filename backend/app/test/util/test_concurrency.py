from functools import partial
from time import sleep

import pytest

from bug_killer.util.concurrency import run_concurrently


def mock_io_func(sleep_sec: float) -> int:
    sleep(sleep_sec)
    return 21


@pytest.mark.parametrize(
    "tasks, expected_results, expected_complete_within",
    [
        ([partial(mock_io_func, 0.05) for _ in range(5)], [21 for _ in range(5)], 100),
        ([partial(mock_io_func, 0.05)], [21], 100),
    ],
)
def test_run_concurrently(tasks, expected_results, expected_complete_within):
    results, time_taken = run_concurrently(*tasks)

    assert results == expected_results
    assert time_taken < expected_complete_within
