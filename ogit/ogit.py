import click
from .git import Git
from . import settings

@click.group()
def cli():
    pass

@cli.command()
def status():
    Git.status(settings.paths.starting, extended=True)
