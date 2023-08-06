"""
Methods for parsing and validating data.
"""


import sys

from msr import io


def validate_url(url):
    import validators
    if not validators.url(url):
        io.stdout(f'Error: the URL {repr(url)} is invalid.')
        sys.exit(1)


def get_domain(url):
    import tldextract
    extracted = tldextract.extract(url)
    return f'{extracted.domain}.{extracted.suffix}'
