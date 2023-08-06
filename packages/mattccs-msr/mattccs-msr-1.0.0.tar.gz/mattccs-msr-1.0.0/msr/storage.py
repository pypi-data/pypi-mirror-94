"""
Methods for interacting with persistent storage.
"""


import pathlib

from msr import config


def ensure_storage():
    try:
        pathlib.Path(config.CONFIG_HOME).mkdir(parents=True, exist_ok=True)
        pathlib.Path(config.STORAGE_PATH).touch()
    except PermissionError:
        raise


def write_url(url):
    with open(config.STORAGE_PATH, 'a') as outfile:
        outfile.write(f'{url}\n')


def read_urls():
    with open(config.STORAGE_PATH, 'r') as infile:
        urls = infile.readlines()

    return [u.strip() for u in urls]
