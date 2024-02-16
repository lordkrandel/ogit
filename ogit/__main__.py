#!/usr/bin/env python

"""Console script for ogit."""

import click
from .ogit import cli
from pathlib import Path
from .project import Projects
from types import SimpleNamespace
from . import settings

def get_paths():
    config = Path(click.get_app_dir(settings.APPNAME, roaming=True, force_posix=False))
    starting = Path.cwd().absolute()
    projects = config / 'projects.json'
    return SimpleNamespace(config=config, starting=starting, projects=projects)

if __name__ == '__main__':
    settings.paths = get_paths()
    settings.projects = Projects.load_json(settings.paths.projects)
    cli()
