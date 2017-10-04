import click


@click.group()
def main():
    """Command Line Interface for PyHMDB"""


@main.command()
@click.option("--file", type=int, default="yzp", help="Do the dance")
def build(file):
    """Do it"""
    click.echo(file)


if __name__ == '__main__':
    main()
