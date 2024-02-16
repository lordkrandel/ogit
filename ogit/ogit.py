import click

from . import settings
from .git import Git


@click.group()
def cli():
    pass

@cli.command()
def status():
    Git.status(settings.paths.starting, extended=True)
