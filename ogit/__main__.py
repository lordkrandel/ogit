#!/usr/bin/env python

"""Console script for ogit."""

from pathlib import Path
from types import SimpleNamespace

import click

from . import settings
from .ogit import cli
from .project import Projects


def get_paths():
    config = Path(click.get_app_dir(settings.APPNAME, roaming=True, force_posix=False))
    starting = Path.cwd().absolute()
    projects = config / 'projects.json'
    return SimpleNamespace(config=config, starting=starting, projects=projects)

if __name__ == '__main__':
    settings.paths = get_paths()
    settings.projects = Projects.load_json(settings.paths.projects)
    cli()
