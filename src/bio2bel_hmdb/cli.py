# -*- coding: utf-8 -*-

import logging

import click

from .constants import DEFAULT_CACHE_CONNECTION
from .manager import Manager


@click.group()
@click.option('-c', '--connection', help='Defaults to {}'.format(DEFAULT_CACHE_CONNECTION))
@click.pass_context
def main(ctx, connection):
    """HMDB to BEL"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    ctx.obj = Manager(connection=connection)


@main.command()
@click.pass_obj
def populate(manager):
    """Populate the database"""
    manager.populate()


@main.command()
@click.pass_obj
def drop(manager):
    """Drop the database"""
    manager.drop_all()


@main.command()
@click.option('-v', '--debug', is_flag=True)
@click.option('-p', '--port')
@click.option('-h', '--host')
@click.pass_obj
def web(manager, debug, port, host):
    """Run the web app"""
    from .web import get_app
    app = get_app(connection=manager, url='/')
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
