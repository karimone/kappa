import click
from .info import info


@click.group()
def cli():
    pass


cli.add_command(info)  # noqa