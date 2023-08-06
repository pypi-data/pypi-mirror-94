"""
Entry point for msr.
"""

__author__ = 'Matthew Cotton <matthewcotton.cs@gmail.com>'


import argparse

from msr import commands


DESCRIPTION = 'MSR performs various measurements on remote web pages'


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    subparsers = parser.add_subparsers(
        help='Sub-commands', dest='command', required=True)

    p_version = subparsers.add_parser('version')

    p_register = subparsers.add_parser('register')
    p_register.add_argument('url')

    p_measure = subparsers.add_parser('measure')

    p_race = subparsers.add_parser('race')

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == 'version':
        commands.version()
    elif args.command == 'register':
        commands.register(args.url)
    elif args.command == 'measure':
        commands.measure()
    elif args.command == 'race':
        commands.race()
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[-] User cancelled.')
