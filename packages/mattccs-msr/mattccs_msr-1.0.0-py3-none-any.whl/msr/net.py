"""
Methods for network requests.
"""


import time


def content(url):
    import requests
    return requests.get(url).content


def size(url):
    return len(content(url))


def latency(url):
    t0 = time.perf_counter()
    _ = size(url)
    t1 = time.perf_counter()
    return t1 - t0
