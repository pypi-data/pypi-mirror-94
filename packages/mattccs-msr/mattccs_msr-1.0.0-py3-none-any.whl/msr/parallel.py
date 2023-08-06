"""
Methods for parallel execution.
"""


import concurrent.futures

from msr import io


def multi_apply_concurrent(func, urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(func, url): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                yield (url, future.result())
            except Exception as exc:
                io.stderr(f"URL {repr(url)} threw error: {repr(exc)}", exc_info=True)
                yield (None, exc)
