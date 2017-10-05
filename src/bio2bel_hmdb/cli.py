import click

from bio2bel_hmdb.manager import Manager


@click.group()
def main():
    """Command Line Interface for PyHMDB"""

@main.command()
def build():
    """Build the local version of the full HMDB."""
    m = Manager()
    click.echo("create tables")
    m.make_tables()
    click.echo("populate tables")
    m.populate()

if __name__ == '__main__':
    main()
