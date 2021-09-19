from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List, Tuple


def run_concurrently(*tasks) -> Tuple[List, int]:
    start_time = datetime.now()

    if tasks:
        with ThreadPoolExecutor() as executor:
            running_tasks = [executor.submit(task) for task in tasks]
            results = [task.result() for task in running_tasks]

    else:
        results = []

    time_taken = datetime.now() - start_time
    time_in_milli_sec = int(time_taken.microseconds / 1000)

    return results, time_in_milli_sec
