#!/usr/bin/env python
import logging

import click

from diadump import VERSION
from diadump.dumper import dump_many, dump_one, configure_logging


@click.group()
@click.version_option(version='.'.join(map(str, VERSION)))
@click.option('--verbose', help='Show more messages while processing', is_flag=True)
def entry_point(verbose):
    """diadump command line utilities."""
    configure_logging(logging.DEBUG if verbose else None)


@entry_point.command()
@click.argument('url')
@click.argument('target', type=click.Path(file_okay=False, writable=True))
@click.option('--max', help='Maximum number of titles to dump', type=click.INT)
def many(url, target, max):
    """Given a listing URL dumps several filmstrips into a target directory.

    :param url: Start URL.
    :param target: Directory to dump into.
    """
    dump_many(url, target, max_titles=max)


@entry_point.command()
@click.argument('url')
@click.argument('target', type=click.Path(exists=True, file_okay=False, writable=True))
def one(url, target):
    """Given a listing URL dumps the given filmstrip into a target directory.

    :param url: Filmstrip URL.
    :param target: Directory to dump into.
    """
    dump_one(url, target)


def main():
    entry_point(obj={})


if __name__ == '__main__':
    main()

