# -*- coding: utf-8 -*-

import logging

import click

from .constants import DEFAULT_CACHE_CONNECTION
from .manager import Manager


@click.group()
def main():
    """HMDB to BEL"""
    logging.basicConfig(level=logging.INFO)


@main.command()
def populate(connection):
    """Populate the database"""
    m = Manager(connection=connection)
    m.populate()


@main.command()
@click.option('-c', '--connection', help='Defaults to {}'.format(DEFAULT_CACHE_CONNECTION))
def drop(connection):
    """Drop the database"""
    m = Manager(connection=connection)
    m.drop_all()


@main.command()
@click.option('-c', '--connection', help='Defaults to {}'.format(DEFAULT_CACHE_CONNECTION))
def web(connection):
    """Run the web app"""
    from .web import get_app
    app = get_app(connection=connection)
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
