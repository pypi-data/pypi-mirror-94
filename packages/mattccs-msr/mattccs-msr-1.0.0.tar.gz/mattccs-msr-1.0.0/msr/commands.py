"""
Implementations of the CLI commands.
"""

import collections

from msr import config
from msr import io
from msr import net
from msr import parallel
from msr import storage
from msr import parsing


def version():
    io.stdout(config.VERSION)


def register(url):
    storage.ensure_storage()
    parsing.validate_url(url)
    storage.write_url(url)


def measure():
    import tabulate

    urls = storage.read_urls()

    headers = ['Content (B)', 'URL']
    table = []
    for (url, result) in parallel.multi_apply_concurrent(net.size, urls):
        table.append((result, url))

    io.stdout(tabulate.tabulate(table, headers=headers))


def race():
    import tabulate

    urls = storage.read_urls()

    results = collections.defaultdict(list)
    for (url, result) in parallel.multi_apply_concurrent(net.latency, urls):
        results[parsing.get_domain(url)].append(result)

    headers = ['Avg. Response (s)', 'URL']
    table = []
    for (domain, times) in results.items():
        avg = sum(times) / len(times)
        table.append((f'{avg:.4f}', domain))

    io.stdout(tabulate.tabulate(table, headers=headers))
