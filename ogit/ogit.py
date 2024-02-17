#!/usr/bin/env python

"""Console script for ogit."""

from pathlib import Path
from types import SimpleNamespace

import click
import project
import settings


@click.group()
def cli():
    pass

@cli.command()
@click.pass_context
def init(ctx):
    ctx.forward(project.project_init)
    ctx.forward(project.projects_init)

@cli.command()
@click.pass_context
def status(ctx):
    ctx.forward(project.projects_status)


def main():

    def get_paths():
        config = Path(click.get_app_dir(settings.APPNAME, roaming=True, force_posix=False))
        starting = Path.cwd().absolute()
        projects = config / 'projects.json'
        return SimpleNamespace(config=config, starting=starting, projects=projects)

    settings.paths = get_paths()
    settings.projects = project.Projects.load_json(settings.paths.projects)
    settings.project = (settings.projects or {}).get(settings.paths.starting.name)

    cli.add_command(project.project)
    cli.add_command(project.projects)
    cli()

if __name__ == '__main__':
    main()
